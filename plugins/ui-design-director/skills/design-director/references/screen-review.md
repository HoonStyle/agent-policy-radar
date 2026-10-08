# Evidence-based screen review

## Establish the evidence boundary

Record the target URL/file, viewport, theme, state, and browser or tool actually used. Identify whether each conclusion comes from source inspection, a rendered screenshot, or an exercised interaction. Never present a mock image as proof of working UI.

For affected English/Korean surfaces, record the language and formatting locale. Check long labels, document language, accessible names, validation text, numbers/dates, and state preservation on language switch where supported. A passing Korean screen does not verify the English one.

## Inspect three independent dimensions

| Dimension | Questions | Useful evidence |
| --- | --- | --- |
| Visual appeal | Are type hierarchy, composition, color, imagery, material, and detail coherent and attractive for this intent? | Actual rendered screen, focal-point and rhythm observations, specific locations |
| Product specificity | Does the layout express this task and content? Is the structure justified beyond a familiar template? | Primary task, real data, alternative structure trade-offs |
| Usability/accessibility | Can someone complete and recover from the task with the supported inputs and viewports? | Exercised task, keyboard sequence, states, semantic inspection, relevant automated checks |

Do not collapse these into a synthetic score. Subjective preferences should be labeled as judgments and connected to observable details.

## Check affected surfaces

For a new screen, inspect a wide and narrow viewport, long/empty data, loading/error/recovery, selection, and relevant themes. For a local correction, target the affected states rather than imposing the full list.

Verify keyboard reachability, focus visibility and restoration, labels, form errors, semantics, and overflow. Use existing Playwright/axe tests if present. Automatic checks do not cover every accessibility requirement. State which input methods and flows were actually exercised.

For color, examine relative area, neutral temperature, competing accents, consistent semantic roles, and status text/icons. Confirm actual adjacent colors for focus and controls; a decorative separator is not automatically a 3:1 requirement. A palette-only report does not inspect geometry, overlays, transparency, gradients, images, or the final CSS cascade.

## Findings and closure

Use `severity · location/state · observation · user impact · proposed fix · evidence`. Separate blockers (task cannot complete, unreadable important content) from improvements (rhythm, balance, finish) and preferences. Do not label every stylistic preference a defect.

After authorized fixes, repeat the failing or affected checks and capture current evidence. Keep a short list of remaining limits. Stop once the scoped result is supported; do not demand human approval for every reversible aesthetic adjustment.
