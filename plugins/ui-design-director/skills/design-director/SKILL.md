---
name: design-director
description: Design or refine product-specific UIs, coordinate color palettes, and critique rendered screens when layouts feel generic or visually incoherent. Use for UI art direction, English/Korean typography, color systems, localization, or visual polish; not unrelated backend work or a full redesign for a small copy fix.
---

# Design Director

Deliver a screen whose structure fits its task and whose typography, composition, color, imagery, and interaction belong together. Judge visual appeal, product specificity, and usability separately; removing familiar AI patterns is not proof of beauty.

For coordinated UI/PPT/Word work, consult the [shared foundation](references/shared-foundations.md). Route slide decks to [presentation-design](../presentation-design/SKILL.md) and flowing documents to [document-design](../document-design/SKILL.md); screen rules do not replace their artifact workflows.

## 1. Match the requested scope

Read existing screens, tokens, components, content, and project conventions before proposing a direction. Reuse an existing brief or decisions. Infer known context; ask only for a missing constraint that changes the result.

Choose the smallest applicable route:

| Request | Route and completion evidence |
| --- | --- |
| Understand the product / prepare a design brief | Capture audience, primary task, real content, constraints, and preserved behavior. Finish with the brief; do not edit the app. |
| New screen / substantial redesign / generic layout | Read [art-direction.md](references/art-direction.md). Compare meaningfully different structures when helpful, select from existing intent or explain an assumption, then implement. |
| Match the palette / inconsistent colors | Read [color-system.md](references/color-system.md). Map semantic roles and interaction states, check contrast, then inspect actual screen color balance. Do not rebuild the layout without reason. |
| Critique / review only | Read [screen-review.md](references/screen-review.md). Deliver findings grounded in inspected evidence; do not fix without scope to do so. |
| Polish / fix an agreed issue | Preserve unaffected branding and behavior, make the scoped change, then use [screen-review.md](references/screen-review.md) for the affected screen and flow. |

End this step knowing what may change, what must stay, and the main user action. A small edit does not require a new brief, moodboard, or multiple concepts.

## 2. Establish a visual decision, not a template

For substantial work, write a compact direction beside existing project design notes: task-led structure, visual focal point, type hierarchy, color roles and relative emphasis, image treatment if relevant, and interaction character. Use [brief-and-review.md](assets/brief-and-review.md) only when an artifact helps continuity; fill or remove its fields.

Compare structures, not recolorings. A record comparison may need a table; focused editing may need a split view; a reading experience may need editorial rhythm. These are task hypotheses, not industry-to-style rules. Preserve a good existing composition when the problem is local.

Make aesthetic choices visible in a representative screen using actual or clearly labeled sample content. If references are useful, record their source and the specific principle being borrowed; do not copy whole layouts or assume assets are licensed. Available Impeccable/frontend-design skills can supply broader craft guidance; load only what the task needs, without installing them as a side effect.

Do not default every product to navy, nested cards, metric tiles, pills, or the same alternative editorial style. No color, font, shape, gradient, or level of ornament is universally forbidden. Explain fit rather than inventing an “AI design score.”

## 3. Implement a coherent system

Reuse the project's tokens and accessible components. Keep typography, spacing, borders, icon weight, imagery, and motion aligned with the direction. If changing color, use the color-system reference even when color is only part of the task. Preserve meaningful status distinctions and support themes already in scope; do not add dark mode merely to complete a checklist.

Determine the UI language from the product and request, not from the conversation language. For English screens, read [english-ui.md](references/english-ui.md); for Korean screens, read [korean-ui.md](references/korean-ui.md); for a bilingual product, use both. Treat both as first-class design targets, not an English layout with Korean text squeezed in or a Korean layout mechanically translated. Use real long labels, numbers, dates, and errors. Preserve values, selection, and focus when switching language. Do not add a language switcher to an otherwise single-language product unless requested.

Do not invent customer counts, testimonials, product facts, or decorative slogans to fill space.

Use existing browser, screenshot, test, and image tools when available. This package supplies no browser, image service, live connection, or credentials. Keep edits in the authorized project. Honor the host and user’s hot-reload rules, including watcher-triggering edits. If explicit reload confirmation is required, explain the target and impact and prepare an isolated copy while confirmation is pending.

## 4. Render, critique, and recheck

Inspect rendered wide and narrow screens in each affected UI language and exercise the primary action and affected states. Source code alone cannot establish visual quality. If a browser is unavailable, mark visual/behavioral review unverified and still finish useful source-level work.

Separate three conclusions: **visual appeal**, **product specificity**, **usability/accessibility**. State location, observation, user effect, proposed change, and evidence for each actionable finding. Fix within the authorized scope, then rerun only relevant checks. Stop when blocking issues are resolved or explicitly documented; avoid speculative redesign loops.

Report what changed, where to see it, what actually ran, and what remains unverified. Palette checks cover declared color pairs only; a successful report does not certify beauty or WCAG conformance. Installation, publication, and live reload are distinct from building this package.
