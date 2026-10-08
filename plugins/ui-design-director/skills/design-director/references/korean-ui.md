# Korean and mixed-language UI

For a bilingual product, also use [english-ui.md](english-ui.md) for language switching, locale formatting, and English-specific layout checks. Do not force Korean onto a product whose requested UI language is English.

- Inspect the actual loaded font and fallback for 한글, Latin, punctuation, and numerals. A Latin font choice alone does not define Korean typography. Prefer existing project fonts or local system fallbacks; adding a remote font changes network, licensing, and performance assumptions.
- Evaluate long labels such as `검토 요청 다시 보내기`, mixed text such as `출고 검수 API v2`, and numbers such as `1,240건 · 2026.10.08`. Keep units and dates understandable; use tabular numerals only where alignment helps comparison.
- Test Korean heading line breaks at narrow widths. `word-break: keep-all` can improve phrase rhythm but requires `overflow-wrap: anywhere` or targeted wrapping for long URLs/identifiers; do not apply nowrap globally.
- Let buttons grow or wrap appropriately, preserving touch targets and focus. Avoid fixed heights that clip enlarged text. Inspect 200% text/zoom where the host supports it and 320 CSS-pixel reflow where relevant.
- Use concise, consistent functional Korean. Preserve the product's established register. Explain errors with a recovery action, not technical stack traces or filler slogans. Color is not a substitute for `오류`, `완료`, or `선택됨` semantics.
- Check line-height, weight, and letter-spacing using rendered Korean text, not an English-only specimen. Do not shrink Korean labels simply to force an English-sized component.
