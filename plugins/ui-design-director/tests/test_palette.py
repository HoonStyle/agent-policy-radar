import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/design-director"
SCRIPT = SKILL / "scripts/palette.py"
spec = importlib.util.spec_from_file_location("palette", SCRIPT)
palette = importlib.util.module_from_spec(spec)
spec.loader.exec_module(palette)


class PaletteTests(unittest.TestCase):
    def setUp(self):
        self.example = SKILL / "assets/palettes/paper-olive.json"
        self.data = json.loads(self.example.read_text(encoding="utf-8"))

    def load(self, data):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "palette.json"
            path.write_text(json.dumps(data))
            return palette.load_palette(path)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True, encoding="utf-8",
                              env=dict(os.environ, PYTHONIOENCODING="utf-8"))

    def test_known_wcag_extremes_and_symmetry(self):
        self.assertEqual(palette.contrast("#000", "#FFF"), 21)
        self.assertEqual(palette.contrast("#123456", "#123456"), 1)
        self.assertEqual(palette.contrast("#123", "#ABC"), palette.contrast("#ABC", "#123"))
        self.assertAlmostEqual(palette.luminance("#FF0000"), 0.2126)

    def test_threshold_uses_unrounded_ratio(self):
        self.data["themes"]["light"]["tokens"]["muted"] = "#777777"
        report = palette.check_palette(self.load(self.data))
        row = next(r for r in report["results"] if r["theme"] == "light" and r["name"] == "muted / surface")
        self.assertAlmostEqual(row["ratio"], 4.478089453577214, places=10)
        self.assertFalse(row["passed"])

    def test_shipped_examples_all_themes(self):
        for path in (SKILL / "assets/palettes").glob("*.json"):
            with self.subTest(palette=path.name):
                data = palette.load_palette(path)
                report = palette.check_palette(data)
                self.assertEqual(report["failed"], 0)
                self.assertEqual({r["theme"] for r in report["results"]}, set(data["themes"]))

    def test_rejects_missing_role(self):
        del self.data["themes"]["light"]["tokens"]["focus"]
        with self.assertRaises(palette.PaletteError): self.load(self.data)

    def test_rejects_unsupported_or_injectable_colors(self):
        for value in ("#12345678", "rgba(0,0,0,.5)", "oklch(.5 .2 30)", "var(--brand)", "red;}</style>", None, 42):
            with self.subTest(value=value):
                self.data["themes"]["light"]["tokens"]["text"] = value
                with self.assertRaises(palette.PaletteError): self.load(self.data)

    def test_rejects_unsafe_theme_and_token_names(self):
        for field in ("theme", "token"):
            data = copy.deepcopy(self.data)
            target = data["themes"] if field == "theme" else data["themes"]["light"]["tokens"]
            target['x\"></style>'] = target.pop(next(iter(target)))
            with self.assertRaises(palette.PaletteError): self.load(data)

    def test_rejects_invalid_structure(self):
        for data in ([], {}, dict(self.data, schemaVersion=True), dict(self.data, themes={}), dict(self.data, surprise=1)):
            with self.subTest(data=str(data)[:60]):
                with self.assertRaises(palette.PaletteError): self.load(data)

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "palette.json"
            path.write_text('{"name":"one","name":"two"}')
            with self.assertRaises(palette.PaletteError): palette.load_palette(path)

    def test_extra_pairs_add_to_required_checks(self):
        theme = self.data["themes"]["light"]
        theme["tokens"].update({"hero-text": "#777", "hero-bg": "#FFF"})
        theme["pairs"] = [{"name": "Hero", "foreground": "hero-text", "background": "hero-bg", "kind": "large-text"}]
        report = palette.check_palette(self.load(self.data))
        self.assertEqual(report["checked"], 43)
        self.assertTrue(next(r for r in report["results"] if r["name"] == "Hero")["passed"])

    def test_bad_pair_reference_and_kind_rejected(self):
        for field, value in (("foreground", "missing"), ("kind", "text"), ("background", []), ("kind", [])):
            pair = {"name": "Extra", "foreground": "text", "background": "canvas", "kind": "normal-text"}
            pair[field] = value
            self.data["themes"]["light"]["pairs"] = [pair]
            with self.assertRaises(palette.PaletteError): self.load(self.data)

    def test_disabled_pair_is_advisory(self):
        self.data["themes"]["light"]["tokens"]["disabled-text"] = self.data["themes"]["light"]["tokens"]["disabled"]
        report = palette.check_palette(self.load(self.data))
        self.assertEqual(report["failed"], 0)
        self.assertEqual(report["advisory"][0]["ratio"], 1)

    def test_css_export_and_unknown_theme(self):
        data = self.load(self.data)
        css = palette.css_tokens(data, "dark")
        self.assertIn("--ui-canvas: #1D241C", css)
        self.assertNotIn("#F4F3EB", css)
        with self.assertRaises(palette.PaletteError): palette.css_tokens(data, "missing")

    def test_preview_escapes_metadata_without_template_recursion(self):
        self.data["name"] = '<script>alert(1)</script> @@CSS@@'
        output = palette.preview_html(self.load(self.data))
        self.assertNotIn('<script>alert(1)</script>', output)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt; @@CSS@@', output)
        self.assertIn("form-action 'none'", output)

    def test_preview_language_and_script_metadata_are_safe(self):
        self.data['name'] = '</script><script>alert(1)</script>'
        for lang in ('ko', 'en'):
            output = palette.preview_html(self.load(self.data), lang)
            self.assertIn(f'<html lang="{lang}"', output)
            self.assertNotIn('</script><script>alert(1)</script>', output)
            self.assertNotIn('@@I18N:', output)
        with self.assertRaises(palette.PaletteError): palette.preview_html(self.load(self.data), 'fr')

    def test_translations_cover_the_same_messages_and_placeholders(self):
        import re
        messages = json.loads((SKILL / 'scripts/locales.json').read_text(encoding="utf-8"))
        self.assertEqual(set(messages['ko']), set(messages['en']))
        for key in messages['ko']:
            self.assertEqual(set(re.findall(r'\{(\w+)\}', messages['ko'][key])),
                             set(re.findall(r'\{(\w+)\}', messages['en'][key])), key)

    def test_cli_english_entry_point(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'english.html'
            result = self.cli('preview', self.example, '--output', output, '--lang', 'en')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('<html lang="en"', output.read_text(encoding="utf-8"))
            self.assertIn('>Select item</button>', output.read_text(encoding="utf-8"))

    def test_cli_codes_success_failure_invalid(self):
        self.assertEqual(self.cli("check", self.example).returncode, 0)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.json"
            self.data["themes"]["light"]["tokens"]["text"] = "#FFFFFF"
            path.write_text(json.dumps(self.data))
            result = self.cli("check", path)
            self.assertEqual(result.returncode, 1)
            self.assertGreater(json.loads(result.stdout)["failed"], 0)
            path.write_text("{broken")
            result = self.cli("check", path)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stderr)["status"], "error")

    def test_preview_refuses_overwrite_and_input_clobber(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "preview.html"
            self.assertEqual(self.cli("preview", self.example, "--output", output).returncode, 0)
            original = output.read_bytes()
            self.assertEqual(self.cli("preview", self.example, "--output", output).returncode, 2)
            self.assertEqual(output.read_bytes(), original)
            self.assertEqual(self.cli("preview", self.example, "--output", output, "--force").returncode, 0)
            source = Path(temp) / "input.json"
            source.write_text(json.dumps(self.data))
            self.assertEqual(self.cli("preview", source, "--output", source, "--force").returncode, 2)
            self.assertEqual(json.loads(source.read_text(encoding="utf-8")), self.data)


if __name__ == "__main__":
    unittest.main()
