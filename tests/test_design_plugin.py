"""Exercise the optional design plugin from the marketplace's normal test entrypoint."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/ui-design-director'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DesignPluginTests(unittest.TestCase):
    def test_catalog_resolves_to_self_contained_package(self):
        for relative in ('.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json'):
            data = json.loads((ROOT / relative).read_text(encoding='utf-8'))
            entries = [p for p in data['plugins'] if p['name'] == 'ui-design-director']
            self.assertEqual(len(entries), 1)
            source = entries[0]['source']
            source = source if isinstance(source, str) else source['path']
            self.assertEqual((ROOT / source).resolve(), PLUGIN.resolve())
        package = load_module('design_package_check', PLUGIN / 'scripts/package.py')
        manifest = package.validate(package.package_files())
        self.assertEqual(manifest['name'], 'ui-design-director')
        self.assertTrue((PLUGIN / 'LICENSE').is_file())

    def test_optional_skills_do_not_leak_into_base_plugin(self):
        for skill in ('design-director', 'presentation-design', 'document-design'):
            self.assertTrue((PLUGIN / 'skills' / skill / 'SKILL.md').is_file())
            self.assertFalse((ROOT / 'skills' / skill).exists())
        for relative in ('plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
            manifest = json.loads((PLUGIN / relative).read_text(encoding='utf-8'))
            for field in ('hooks', 'mcpServers', 'dependencies', 'settings'):
                self.assertNotIn(field, manifest)


def load_tests(loader, tests, pattern):
    palette_tests = load_module('design_palette_tests', PLUGIN / 'tests/test_palette.py')
    tests.addTests(loader.loadTestsFromModule(palette_tests))
    return tests
