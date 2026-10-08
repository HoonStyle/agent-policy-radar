# Shared design foundation for UI, slides, and documents

Use this reference when a task spans media or needs the same brand across them. A supplied template, established project styles, and explicit user instructions take precedence over new defaults. Keep this package together: presentation-design and document-design reference these shared files.

## Capture only decisions the next artifact needs

Reuse the existing brand brief. Otherwise record audience, intended action, factual source, language/locale, delivery medium, brand assets, constraints, and editable-format requirements. Separate approved facts from sample data and design judgments. Maintain one shared set of decisions rather than three conflicting style documents.

Specify roles rather than a fixed aesthetic: dominant type hierarchy, neutral family, accent meaning, status meaning, image/diagram character, and density. Assess visual appeal, identity, and comprehension independently. Do not make all outputs look like a dashboard or all look like a cream editorial page.

## Adapt shared intent to the medium

| Shared role | UI | PowerPoint | Word |
| --- | --- | --- | --- |
| Background/text | Canvas and surfaces | Slide backgrounds and foregrounds | Usually paper and running text; preserve required black heading/body conventions |
| Accent | Action and focus | A message, series, or focal element | Restrained emphasis, permitted table fill or link color |
| Status | State plus label/icon | Labeled category or evidence annotation | Labeled finding, note, or table entry |
| Typography | Fluid viewport hierarchy | Readable at presentation distance | Comfortable continuous reading and pagination |
| Structure | Navigation and task state | Narrative order and slide purpose | Heading hierarchy and document flow |
| Validation | Viewports and interactions | Each slide plus deck sequence | Each rendered page plus semantic structure |

Reuse color meaning, not every UI token. A Word memo does not need hover colors; a slide has no responsive button states. Retain document/slide templates and medium-specific accessibility rules. Do not copy a dark UI surface onto all printed pages just to match the brand.

For a coordinated palette, start from the source brand or a selected family in [color-system.md](color-system.md), then inspect its actual use in each medium. Validate the colors actually used, not arbitrary proxy tokens. The optional opaque-sRGB checker accepts additional declared pairs but cannot inspect a PowerPoint theme, Word style, gradient, or exported PDF.

## Preserve usable, editable artifacts

Prefer actual theme/style definitions and native text/table/chart elements when editability matters. A screenshot of a table is not an editable table. Generated illustrations must not masquerade as real evidence. Retain source data, units, links, caveats, and authorship.

For bilingual work, use [english-ui.md](english-ui.md) and [korean-ui.md](korean-ui.md) for language/typography principles, adapting their screen-specific checks to slide/page layout. Agree separate language versions versus side-by-side bilingual text from the task context. Do not duplicate every paragraph in both languages by default. Set proofing/language metadata where the chosen tool supports it, and verify glyphs and line breaks in every delivered language.

## Verification boundary

Record the toolchain actually used, supported file type, content preservation, and latest rendered evidence. Schema checks and package parsing cannot establish layout quality. A browser mockup cannot verify a DOCX page or PPTX slide. If an allowed authoring/rendering tool is absent, complete design guidance and clearly mark artifact creation/rendering unverified; do not fabricate a finished file or silently swap runtimes against host rules.
