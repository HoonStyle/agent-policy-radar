# Coherent color systems

## Design the roles before choosing hex values

Inspect existing brand tokens and actual screens. Preserve their role names and compatible values when possible. Record a short palette rationale: neutral temperature, accent character, how much visual emphasis belongs to the primary action, and how status colors remain distinct. Do not assign a palette purely from an industry label.

Map canvas, surfaces, primary/secondary text, decorative lines, essential control boundaries, primary action/on-action text, focus, selection, and success/warning/error roles. For changed controls, cover default, hover, pressed, focused, selected, invalid, and disabled states as applicable. A token reused for unrelated meanings should be split only when the design requires it.

Review color area in the real screen: large backgrounds dominate perceived harmony, while a small saturated accent can carry the action. Do not enforce a universal 60/30/10 ratio. Coordinate hue, lightness, chroma, and surface relationships; a mathematically related set is not automatically attractive. A palette should not overwhelm text, imagery, or data.

Build each supported theme deliberately. Inverting colors or copying light-theme status fills into dark mode is not enough. Keep role meaning consistent across screens and themes. Never communicate status or selection through color alone.

## Check the pairs actually used

Use a project's existing color/contrast tooling first. The bundled Python 3.9+ helper is an optional zero-dependency fallback for **opaque sRGB `#RGB`/`#RRGGBB`** token sets. It is not a CSS parser, DTCG implementation, gamut mapper, or aesthetic evaluator. Resolve aliases and composite transparency against the actual background before supplying values; do not approximate unsupported colors silently.

Paths below are relative to this skill directory; resolve them to absolute paths when running from elsewhere.

```bash
python3 scripts/palette.py check assets/palettes/paper-olive.json
python3 scripts/palette.py css assets/palettes/paper-olive.json --theme light
python3 scripts/palette.py preview assets/palettes/paper-olive.json --output /tmp/paper-olive.html
python3 scripts/palette.py preview assets/palettes/paper-olive.json --lang en --output /tmp/paper-olive-en.html
```

`check` prints JSON and exits 0 for all declared required pairs passing, 1 for a contrast failure, 2 for invalid input. Disabled-label contrast is reported as advisory, not an AA failure. A pair is tested against the unrounded ratio. Text targets are 4.5:1 for ordinary text and 3:1 for qualifying large text; non-text 3:1 applies only where the adjacent-color criterion is relevant. The built-in focus checks are useful pair checks, not a complete focus-appearance audit.

`css` prints `--ui-*` variables; translate these into the project's existing token vocabulary rather than creating a competing global theme. `preview` writes one self-contained local HTML specimen, refusing overwrite unless `--force` is explicit. It contains theme selection, swatches, type, controls, selection, validation, and status examples. It performs no network requests and submits no data. Rendering a specimen does not replace reviewing the actual product.

`preview --lang ko|en` selects the initial language (default Korean). Both languages remain available in the specimen's language menu. Labels, accessible names, errors, results, and date/number samples switch while preserving entered values and selected state. The examples use ko-KR/en-US formatting with a fixed UTC sample date; choose the real product's locale separately.

The two example families, `paper-olive.json` and `mineral-violet.json`, demonstrate different neutral temperatures and emphasis. They are optional samples, **not presets to apply to every product**. Their light/dark counterparts preserve role semantics; selection and status remain labeled.

## Palette input contract (schema version 1)

```json
{
  "schemaVersion": 1,
  "name": "Project palette",
  "themes": {
    "light": {
      "tokens": { "canvas": "#FFFFFF" },
      "pairs": [
        { "name": "Hero heading", "foreground": "hero-text", "background": "hero-bg", "kind": "large-text" }
      ]
    }
  }
}
```

The snippet shows shape only; use an included complete palette as the starting file. Each theme needs the required semantic roles listed by the helper's `roles` command. Additional token names and theme IDs must be lowercase kebab-case. Optional `pairs` add checks, never replace the built-in checks. Each additional pair names existing tokens and a kind: `normal-text`, `large-text`, or `non-text`. Choose `large-text` only after verifying actual size/weight in the rendered product. Names and roles may not be duplicated. `name`, `schemaVersion`, and `themes` are the only root fields; each theme accepts `tokens` and optional `pairs`.

## Close the color task

Inspect the real screen in every affected theme, including primary action states, keyboard focus, selection, and errors. Examine screenshots at a broad composition level as well as reading-size detail. Report mathematical contrast separately from judgment about harmony, consistency, and emphasis.

References: [WCAG contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), [DTCG format](https://www.designtokens.org/tr/2025.10/format/) for projects already using exchange tokens.
