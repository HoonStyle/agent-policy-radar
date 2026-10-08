---
name: document-design
description: Design, refine, or critique Word/DOCX reports, proposals, memos, and manuals with semantic styles, coherent typography/color, stable pagination, and page-by-page review. Use for English or Korean documents; not slide decks or web UI.
---

# Document Design

Add document art direction and review to the host's Word/DOCX workflow. This skill does not implement a new document builder or renderer.

## 1. Identify the document and preservation rules

Read the source, reference/template, intended reader, requested action, language/locale, print versus screen use, page size/budget, and required output. Distinguish memo, proposal, report, form, manual, or resume; do not dress every document like a slide deck. Preserve factual content, chronology, links, fields, comments, tracked changes, and existing style hierarchy unless changing them is requested.

For resume conversions or other established document pipelines, reuse the project’s approved converter and formatting unless the user requests a replacement. Verify content, links, and rendered pages; do not create a new builder merely to change the styling.

Read the [shared design foundation](../design-director/references/shared-foundations.md) when defining or coordinating a visual system. Read [page craft and QA](references/page-craft.md) before layout work. Finish with the change boundary and document purpose; do not edit for a review-only request.

## 2. Establish a readable document system

Reuse the supplied template and approved brand. Set an appropriate type hierarchy, body measure, spacing rhythm, table style, caption treatment, and restrained accent use. Record decisions in [document-plan.md](assets/document-plan.md) only when substantial work needs continuity.

Lead with context and the reader's main conclusion/action. Use real heading styles and coherent sections. Color and imagery should help comprehension or express an appropriate visual character, not turn each paragraph into a card. Support both English and Korean layouts, inspecting actual glyphs, word wrapping, and translated text length.

Map shared brand roles into permitted document styles; do not import UI hover/state tokens or dark page backgrounds indiscriminately. Follow the host's document-specific style defaults when no template or explicit user direction overrides them.

## 3. Use the established authoring path

Discover and read the host's Documents/DOCX skill or existing project converter. Use its prescribed dependency loader, authoring libraries, field handling, and renderer. This skill does not authorize global package installation, replacement of a managed runtime, cloud upload, or publication.

Apply styles rather than formatting every paragraph independently. Keep data as native tables and headings as semantic text. Preserve numbering, hyperlinks, captions, references, and change-tracking state. Do not accept tracked changes or remove comments as a cosmetic cleanup.

Inspect pagination after content/formatting changes: heading attachment, widows/orphans, table breaks, caption/figure grouping, section orientation, and header/footer placement. Avoid blank paragraphs as layout spacers. Do not apply keep-with-next to all paragraphs, which can create large blank areas.

If an allowed authoring or rendering tool is missing, finish the style/content plan and report the exact limitation. Do not substitute HTML screenshots for DOCX page verification or describe an unrendered document as finished.

## 4. Render and verify every page

Use the host's DOCX renderer, inspect every final page image at reading size, and check semantic structure separately. For the Codex Documents workflow, follow its `render_docx.py` and render-inspect-repair gate. Verify page count, margins, text flow, fonts, tables, figures, links/fields, and metadata relevant to the task.

Fix concrete findings in a new output revision and repeat rendering after layout-sensitive edits. Confirm content and meaning survived; aesthetic polish cannot justify factual loss. Record actual rendered evidence and any native Word/Google Docs checks performed, without implying cross-application fidelity from one renderer.

Deliver the requested editable document with concise use-affecting limits. Keep temporary PNG/PDF QA outputs separate unless requested. For a review-only task, report page/section, observation, impact, and proposed correction.
