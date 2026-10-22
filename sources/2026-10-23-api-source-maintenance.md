# API source maintenance — 2026-10-23

Reviewed official documentation on 2026-10-22; applied as source/reference
maintenance on 2026-10-23. These are dated documentation findings, not tests of
model behavior or a migration of downstream applications.

## Claude API and SDK versions are separate compatibility conditions

The [October 21 announcement](https://platform.claude.com/docs/en/release-notes/overview)
introduces API version `2026-10-21` and SDK major releases that use it by default.
The [migration guide](https://platform.claude.com/docs/en/api/migration-2026-10-21)
distinguishes API-version-dependent changes from SDK/CLI changes:

- The new API version rejects `temperature`, `top_p`, and `top_k`, even at their
  default values. It also changes the accepted placement of document blocks and
  citations. This is not an instruction to rewrite requests that remain on the
  earlier API version without checking their actual conditions.
- New SDKs/CLI generally send API keys using `Authorization: Bearer` rather than
  `X-Api-Key`. A proxy that reads only the latter may need an update; the API accepts
  either header, and platform clients have documented exceptions.
- Establish the actual model, API version, SDK version, platform client, and proxy
  behavior before deciding which changes apply. No default model or reasoning
  effort change follows from this announcement.

The registry now tracks the migration guide explicitly. The current documentation
index did not expose that guide during review; the release notes linked to it.
Index discovery alone is not a complete update review.

## TypeSafe contracts now have separate pages

The old `/api` URL redirects to the [System One endpoint](https://docs.typesafe.ai/api/system-one).
Keep its existing source ID and use the canonical Markdown page. Track
[List models](https://docs.typesafe.ai/api/list-models) and
[Request rules and errors](https://docs.typesafe.ai/api/errors) separately so moved
limits, compression, error, and retry guidance remains covered.

An HTTP schema field is not proof that every model supports it. The endpoint
schema includes image assets/Box and says image assets require a vision-language
model, while the [model guide](https://docs.typesafe.ai/models) lists Jev 1.13/1.14
as text-input models at review time. Do not infer Jev image support or enable an
experimental header from the shared schema alone. Model aliases and the existing
typed-judgment review criteria are unchanged by this source maintenance.

## Scope and evidence limits

The registry grows from 36 to 39 sources; one existing endpoint URL and the Jev
reference link are updated. The collector, discovery logic, review behavior,
default models, and optional plugins are unchanged. The official TypeSafe skill
remains an upstream-maintained separate installation. Public documentation
collection and package/CI checks do not establish improved model quality,
downstream API compatibility, or installed-session activation.
