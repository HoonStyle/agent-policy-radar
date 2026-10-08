# Sources and provenance

Checked 2026-10-08. This is an original implementation informed by the sources below; it does not vendor third-party skill bodies, binaries, fonts, images, or browser engines.

## Existing solutions preflight

- [Impeccable](https://github.com/pbakaus/impeccable): closest workflow comparator. Broad art direction and critique already exist; this package stays a small product-context/Korean-UI/color/evidence layer. No claim of outperformance; no installer or hooks run.
- [Anthropic frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design): intentional visual direction as a reference, not a copied skill.
- [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill): optional search/reference source, not a mandatory dependency or copied palette database.
- [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines): interaction-quality reference, not a visual-style preset.

## Packaging

- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins): portable root manifest, skill directory, optional Codex compatibility manifest.
- [Claude plugin manifest](https://code.claude.com/docs/en/plugins-reference): Claude manifest and root skill discovery; validated with the installed CLI.
- [OpenClaw bundles](https://docs.openclaw.ai/plugins/bundles): portable Agent Plugins bundles map skill roots to normal skills. Implementation also checked the installed distribution's `docs/plugins/bundles.md`.
- [Agent Skills](https://agentskills.io/specification/): skill frontmatter and progressive disclosure.

## Color and review

- [WCAG contrast minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html): opaque sRGB relative luminance, contrast ratio, ordinary/large text thresholds. Calculation uses the 0.04045 sRGB breakpoint and unrounded pass/fail comparisons.
- [WCAG non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html): adjacent-color requirements for meaningful controls and graphics; the helper's pair checks do not assess full applicability or geometry.
- [ARIA APG](https://www.w3.org/WAI/ARIA/apg/patterns/): interaction and keyboard review reference.
- [DTCG format](https://www.designtokens.org/tr/2025.10/format/): optional interchange standard for existing token pipelines. The helper's schema is explicitly a small project-specific format, not DTCG.

The two example palette families and HTML specimen are original task artifacts. Existing local Playwright and Chrome were used only for verification and are not included in the archive. Further platform activation and comparative agent trials are separate from this build.

## Version 0.2.0 document extension

The [PPT/Word research report](docs/document-design-research.md) adds ten official/public primary sources and five official GitHub repository metadata observations. The new presentation-design/document-design workflows are original guidance, not copied host skill bodies. They defer authoring/rendering to the host's existing tools and their runtime requirements. No third-party document engine or renderer was vendored or installed. English/Korean specimen messages are maintained in a shared local dictionary and use native browser locale formatters.
