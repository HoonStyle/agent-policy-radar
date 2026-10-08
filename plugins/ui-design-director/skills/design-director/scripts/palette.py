#!/usr/bin/env python3
"""Check declared opaque sRGB pairs, export CSS, or render a local specimen.

Python >=3.9; standard library only. No installation, network, or live app edits.
WCAG formula: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

ROLES = tuple("canvas surface surface-alt text muted line control-border accent "
              "accent-hover accent-active on-accent focus selection selection-text "
              "success success-bg warning warning-bg danger danger-bg disabled disabled-text".split())
THRESHOLDS = {"normal-text": 4.5, "large-text": 3.0, "non-text": 3.0}
SLUG = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
HEX = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\Z")


class PaletteError(ValueError):
    pass


def strict_object(items):
    result = {}
    for key, value in items:
        if key in result:
            raise PaletteError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def exact_fields(value, required, optional, where):
    if not isinstance(value, dict):
        raise PaletteError(where + " must be an object")
    missing = set(required) - value.keys()
    extra = value.keys() - set(required) - set(optional)
    if missing or extra:
        raise PaletteError(f"{where}: missing={sorted(missing)}, unknown={sorted(extra)}")


def nonempty(value, where):
    if not isinstance(value, str) or not value.strip():
        raise PaletteError(where + " must be a nonempty string")


def normalize_hex(value):
    if not isinstance(value, str) or not HEX.fullmatch(value):
        raise PaletteError(f"Unsupported color {value!r}; use opaque #RGB or #RRGGBB")
    return ("#" + "".join(c * 2 for c in value[1:]) if len(value) == 4 else value).upper()


def load_palette(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=strict_object)
    exact_fields(data, ("schemaVersion", "name", "themes"), (), "palette")
    if type(data["schemaVersion"]) is not int or data["schemaVersion"] != 1:
        raise PaletteError("schemaVersion must be integer 1")
    nonempty(data["name"], "name")
    if not isinstance(data["themes"], dict) or not data["themes"]:
        raise PaletteError("themes must be a nonempty object")
    for theme_id, theme in data["themes"].items():
        if not SLUG.fullmatch(theme_id):
            raise PaletteError("Invalid theme ID: " + theme_id)
        exact_fields(theme, ("tokens",), ("pairs",), theme_id)
        tokens = theme["tokens"]
        if not isinstance(tokens, dict):
            raise PaletteError(theme_id + ".tokens must be an object")
        missing = set(ROLES) - tokens.keys()
        if missing:
            raise PaletteError(theme_id + " missing roles: " + ", ".join(sorted(missing)))
        for role, value in tokens.items():
            if not SLUG.fullmatch(role):
                raise PaletteError("Invalid token name: " + role)
            tokens[role] = normalize_hex(value)
        pairs = theme.get("pairs", [])
        if not isinstance(pairs, list):
            raise PaletteError(theme_id + ".pairs must be an array")
        seen = {p["name"] for p in default_pairs()}
        for pair in pairs:
            exact_fields(pair, ("name", "foreground", "background", "kind"), (), "pair")
            nonempty(pair["name"], "pair.name")
            if pair["name"] in seen:
                raise PaletteError("Duplicate pair name: " + pair["name"])
            seen.add(pair["name"])
            for field in ("foreground", "background"):
                if not isinstance(pair[field], str) or pair[field] not in tokens:
                    raise PaletteError("Unknown pair token: " + str(pair[field]))
            if not isinstance(pair["kind"], str) or pair["kind"] not in THRESHOLDS:
                raise PaletteError("Unknown pair kind: " + str(pair["kind"]))
    return data


def luminance(color):
    color = normalize_hex(color)
    channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return sum(c * weight for c, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(foreground, background):
    low, high = sorted((luminance(foreground), luminance(background)))
    return (high + 0.05) / (low + 0.05)


def default_pairs():
    result = []

    def add(fg, bg, kind="normal-text"):
        result.append({"name": f"{fg} / {bg}", "foreground": fg, "background": bg, "kind": kind})

    for bg in ("canvas", "surface", "surface-alt"):
        for fg in ("text", "muted"):
            add(fg, bg)
        add("focus", bg, "non-text")
    for bg in ("accent", "accent-hover", "accent-active"):
        add("on-accent", bg)
    add("selection-text", "selection")
    for status in ("success", "warning", "danger"):
        add(status, status + "-bg")
    add("danger", "surface")
    for bg in ("canvas", "surface"):
        add("control-border", bg, "non-text")
        add("accent", bg)
    return result


def check_palette(data):
    results = []
    advisory = []
    for theme_id, theme in data["themes"].items():
        tokens = theme["tokens"]
        for pair in default_pairs() + theme.get("pairs", []):
            ratio = contrast(tokens[pair["foreground"]], tokens[pair["background"]])
            minimum = THRESHOLDS[pair["kind"]]
            results.append(dict(pair, theme=theme_id, ratio=ratio, minimum=minimum, passed=ratio >= minimum))
        advisory.append({"theme": theme_id, "pair": "disabled-text / disabled",
                         "ratio": contrast(tokens["disabled-text"], tokens["disabled"]),
                         "note": "Inactive control: informational, not an AA pass/fail."})
    failed = sum(not row["passed"] for row in results)
    return {"name": data["name"], "status": "fail" if failed else "pass",
            "checked": len(results), "passed": len(results) - failed, "failed": failed,
            "results": results, "advisory": advisory,
            "scope": "Declared opaque sRGB pairs only; not visual harmony or full WCAG conformance."}


def css_tokens(data, selected=None):
    if selected is not None and selected not in data["themes"]:
        raise PaletteError("Unknown theme: " + selected)
    blocks = []
    for index, (theme_id, theme) in enumerate(data["themes"].items()):
        if selected is not None and theme_id != selected:
            continue
        selector = ":root" if selected else (":root, " if index == 0 else "") + f'[data-theme="{theme_id}"]'
        lines = [f"  --ui-{role}: {value};" for role, value in theme["tokens"].items()]
        if theme_id in ("light", "dark"):
            lines.append("  color-scheme: " + theme_id + ";")
        blocks.append(selector + " {\n" + "\n".join(lines) + "\n}")
    return "\n\n".join(blocks) + "\n"


def preview_html(data, lang="ko"):
    esc = html.escape
    locales = json.loads(Path(__file__).with_name("locales.json").read_text(encoding="utf-8"))
    if lang not in locales:
        raise PaletteError("Unsupported preview language: " + str(lang))
    messages = locales[lang]
    report = check_palette(data)
    params = {"passed": report["passed"], "checked": report["checked"], "count": "1,240",
              "date": "2026. 10. 8." if lang == "ko" else "Oct 8, 2026", "value": ""}

    def tr(key):
        return esc(messages[key].format(**params))

    def theme_label(key):
        return tr("themeLight" if key == "light" else "themeDark") if key in ("light", "dark") else esc(key)

    options = "".join(f'<option value="{key}" data-theme-name="{key}">{theme_label(key)}</option>' for key in data["themes"])
    language_options = "".join(f'<option value="{key}" lang="{key}"{chr(32) + "selected" if key == lang else ""}>{label}</option>'
                               for key, label in (("ko", "한국어"), ("en", "English")))
    sections = []
    for index, (theme_id, theme) in enumerate(data["themes"].items()):
        chips = "".join(f'<li><span class="chip" style="background:var(--ui-{role})"></span>'
                        f'<span>{esc(role)}<code>{value}</code></span></li>'
                        for role, value in theme["tokens"].items())
        rows = ""
        for row in report["results"]:
            if row["theme"] != theme_id:
                continue
            key = "pass" if row["passed"] else "fail"
            rows += (f'<tr><th scope="row">{esc(row["name"])}</th><td>{row["ratio"]:.3f}:1</td>'
                     f'<td>{row["minimum"]}:1</td><td data-i18n="{key}">{tr(key)}</td></tr>')
        hidden = " hidden" if index else ""
        sections.append(f'<div data-palette="{theme_id}"{hidden}><ul class="swatches">{chips}</ul>'
                        f'<details><summary><span data-i18n="contrastSummary">{tr("contrastSummary")}</span> · '
                        f'<span data-theme-name="{theme_id}">{theme_label(theme_id)}</span></summary><div class="table-wrap">'
                        f'<table><thead><tr><th scope="col" data-i18n="pairHeading">{tr("pairHeading")}</th>'
                        f'<th scope="col" data-i18n="ratioHeading">{tr("ratioHeading")}</th>'
                        f'<th scope="col" data-i18n="targetHeading">{tr("targetHeading")}</th>'
                        f'<th scope="col" data-i18n="resultHeading">{tr("resultHeading")}</th></tr></thead><tbody>{rows}</tbody></table>'
                        '</div></details></div>')
    template = Path(__file__).with_name("specimen.html").read_text(encoding="utf-8")
    settings = {"paletteName": data["name"], "passed": report["passed"], "checked": report["checked"],
                "sampleCount": 1240, "sampleDate": "2026-10-08T00:00:00Z"}
    script_json = lambda value: json.dumps(value, ensure_ascii=True).replace("<", "\\u003c")
    replacements = {"@@TITLE@@": esc(data["name"]), "@@CSS@@": css_tokens(data),
                    "@@OPTIONS@@": options, "@@PALETTES@@": "".join(sections),
                    "@@THEME@@": next(iter(data["themes"])), "@@LANG@@": lang,
                    "@@LANGOPTIONS@@": language_options, "@@LOCALES@@": script_json(locales),
                    "@@SETTINGS@@": script_json(settings)}
    replacements.update({"@@I18N:" + key + "@@": tr(key) for key in messages})
    # Single substitution prevents user text from becoming a template instruction.
    return re.sub(r"@@(?:[A-Z]+|I18N:[a-zA-Z]+)@@", lambda match: replacements[match.group()], template)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("roles", help="Print required semantic token names")
    sub.add_parser("check", help="Check pairs; JSON on stdout").add_argument("palette")
    css = sub.add_parser("css", help="Print CSS custom properties")
    css.add_argument("palette")
    css.add_argument("--theme")
    preview = sub.add_parser("preview", help="Write a standalone local HTML specimen")
    preview.add_argument("palette")
    preview.add_argument("--output", required=True)
    preview.add_argument("--lang", choices=("ko", "en"), default="ko", help="Initial UI language; both remain switchable")
    preview.add_argument("--force", action="store_true", help="Overwrite the named output")
    args = parser.parse_args(argv)
    try:
        if args.command == "roles":
            print(json.dumps(ROLES, indent=2))
            return 0
        data = load_palette(args.palette)
        if args.command == "check":
            report = check_palette(data)
            print(json.dumps(report, indent=2, ensure_ascii=False))
            return 1 if report["failed"] else 0
        if args.command == "css":
            print(css_tokens(data, args.theme), end="")
        else:
            content = preview_html(data, args.lang)
            output = Path(args.output)
            if output.resolve() == Path(args.palette).resolve():
                raise PaletteError("Preview output must not overwrite the palette input")
            with output.open("w" if args.force else "x", encoding="utf-8") as stream:
                stream.write(content)
            print(str(output.resolve()))
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
