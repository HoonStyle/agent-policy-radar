# English and bilingual UI

## Design English as a first-class surface

- Use the product's established English variant and terminology. Do not infer the audience's region from an English request; dates, currency, units, and time zones are separate choices. Preserve an explicit region, and label any sample-locale assumption.
- Check Latin x-height, weight, punctuation, numerals, and reading measure in the actual font. Match hierarchy across languages without requiring identical line breaks or tracking. Avoid applying Korean-specific negative tracking or `word-break: keep-all` to English globally.
- Use sentence case for ordinary labels unless the brand uses another convention. Prefer a specific verb/object such as `Request review` over vague labels or noun-heavy literal translations. Maintain consistent terminology across navigation, buttons, and errors.
- Test realistic longer text such as `Resend review request` and `Assign a reviewer before submitting`. Let labels wrap or controls grow rather than reducing type until they fit. Preserve recognizable words, adequate line-height, and usable control targets. Use targeted wrapping for URLs and long unbroken identifiers.
- Review heading rhythm and paragraph measure at wide and narrow widths. Hyphenation is language-dependent; if used, set the correct document language and inspect actual breaks rather than assuming browser support.

## When the product supports both English and Korean

- Use the project's existing localization setup. For a small standalone specimen, a shared message dictionary and native locale formatters are sufficient; do not introduce a framework for a few labels.
- Set the document `lang`, localize accessible names, placeholders, validation/recovery messages, empty states, counts, dates, and dynamically updated content—not just navigation. Language menu options should remain recognizable in their own language.
- Keep semantic color roles and interaction behavior identical across languages. Adjust typography, measure, and spacing only where the rendered language requires it.
- On a language switch, preserve input values, current selection, chosen theme, validation state, and focus. Update the displayed messages to the new language without reloading or submitting data. Do not translate user-entered text or identifiers.
- Format numbers/dates with the chosen locale and explicit time-zone semantics. Avoid ambiguous numeric dates for international audiences; currency must come from product data, not from language selection. Avoid composing translated sentences from fragments when word order or plural forms differ.
- Exercise keyboard controls and error recovery in both languages. Check narrow screens and enlarged text with realistic long English labels and mixed Korean/English content. Compare the two screens for equivalent hierarchy and function, not pixel-identical layouts.

The bundled specimen uses `ko-KR` and `en-US` for demonstration and one fixed UTC sample date. These are sample formatting choices, not mandatory locales for the user's products.
