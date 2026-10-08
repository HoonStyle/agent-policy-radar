# Page craft and verification

## Structure and aesthetic character

Let purpose set the visual tone. A formal memo can be appealing through proportion, type, and whitespace; a proposal may benefit from appropriate imagery and clearer section openings. Preserve supplied templates and mature documents before introducing a new visual direction.

Define body, title, heading, caption, list, and table roles. Keep a readable measure and consistent paragraph spacing. Use actual heading levels rather than bold-only substitutes. Place the key information early and build a scan-friendly outline without arbitrary decorative subtitles.

Use a restrained color system that survives grayscale/printing when those uses matter. Background fills, rules, and accent headings must fit the template and host's rules. Do not assume an attractive screen palette is appropriate for paper.

## Styles, fields, and flowing layout

Retain the source's style definitions or map changes deliberately. In python-docx, built-in style names use English identifiers such as `Heading 1` even in Korean Word; custom styles retain their defined names. Do not rename a source style merely to translate the application's UI.

Attach headings to following content where needed. Use paragraph pagination controls rather than empty paragraphs. Keep-with-next, keep-lines-together, page-break-before, and widow/orphan control solve different problems; excessive use can push whole sections or tables away. Use section breaks only for a genuine change in page geometry or header/footer behavior.

For tables, use real cells, meaningful header rows, readable cell padding, and widths within the printable area. Avoid overly complex merging or nesting. Where tables span pages, check header repetition and row splitting in the actual renderer. Never shrink all table text to rescue one long value.

Preserve dynamic TOC, page-number, cross-reference, and caption fields when required. A cached displayed value is not proof that a field will update correctly. Structural changes may require field refresh in the target application; record whether that happened. Check both visible hyperlink text and target.

## English/Korean and accessibility

Confirm fonts for Latin and East Asian scripts, language/proofing metadata where supported, line-height, units, date conventions, and long labels. Do not force one language's layout by shrinking the other. When delivering two versions, compare completeness and hierarchy, not identical pagination.

Check heading order, clear link text, table headers, image descriptions, and color-independent meaning. A printed/rendered page cannot verify comments, all tracked-change state, field behavior, or screen-reader navigation; inspect the relevant document structure or application as well.

## Visual closure

Inspect every rendered page, including the final short page. Check orphaned headings, excessive gaps, crowded or split tables, clipped glyphs, image/caption separation, missing content, header/footer drift, and unexpected blank pages. Re-render after a layout-affecting change. Keep the source intact and identify the final revision unambiguously.

Sources: [Microsoft accessible Word documents](https://support.microsoft.com/en-us/accessibility/word/make-your-word-documents-accessible-to-people-with-disabilities), [Word line/page breaks](https://support.microsoft.com/en-us/word/line-and-page-breaks), [python-docx styles](https://python-docx.readthedocs.io/en/stable/user/styles-using.html).
