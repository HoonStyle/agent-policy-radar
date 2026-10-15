# TypeSafe / Jev: targeted review criteria

Use only for a requested Jev review or an affected integration. Consult the current
[official index](https://docs.typesafe.ai/llms.txt) and relevant pages, not every
cookbook. These are review criteria, not a replacement implementation skill or an
instruction to add Jev to a project. Use the [official skill](https://docs.typesafe.ai/agent-skill)
when building with Jev; keep its upstream maintenance separate from Radar.

## What to compare

- **Surface and version.** Establish the actual SDK/HTTP API, requested model and
  returned model ID. Jev does not load `AGENTS.md` or replace a coding agent's LLM.
  Read [models](https://docs.typesafe.ai/models) and the [API contract](https://docs.typesafe.ai/api).
  Moving aliases and pinned versions have different reproducibility properties;
  do not upgrade either automatically. Recheck relevant language, modality and
  per-request/per-question limits for the selected model. Do not infer capability
  from a page title or reuse another version's benchmark as current validation.
- **Inputs and question meaning.** Inspect the actual request construction.
  [State](https://docs.typesafe.ai/concepts/state) must contain the relevant evidence,
  entities and relationships. Put the full judgment in `instructions` and define
  appropriate outcomes in `criteria`: question IDs are response keys, not model
  input. Use the appropriate [primitive](https://docs.typesafe.ai/primitives).
  Separate independently useful judgments without discarding the relationship
  being evaluated; include no-match or insufficient-evidence outcomes when needed.
- **Uncertainty and composition.** Check the consumer against the current response
  schema. [Choice/Score confidence](https://docs.typesafe.ai/confidence) summarizes
  a distribution, not end-to-end correctness or authority to act. Noul returns a
  yes-probability without a separate confidence field. Do not silently equate
  insufficient evidence with false, or a Score with a yes-probability. Thresholds,
  fallback and action rules belong in reviewable application code and need relevant
  workload evidence, especially for non-English use; demo values are not defaults.
- **Dependencies and budgets.** Independent questions can share a request and state,
  but cannot read one another's answers. A dependent judgment needs the required
  evidence in a later request. Inspect actual context limits, retry behavior and
  end-to-end cost/latency when relevant; batching alone proves neither speed nor quality.
- **Evidence tasks.** Where applicable, distinguish relevance, support for each
  condition, contradictory evidence and missing evidence. Keep source identity and
  relationships available to the consumer. The [RAG cookbook](https://docs.typesafe.ai/cookbooks/classifying_rag_passages)
  is an example architecture, not proof that a target service satisfies its conditions.

## Decision and verification

Report keep / change / defer against the actual affected rule or integration.
Fix an established API-contract mismatch from official evidence; require observed
target behavior before adding compensating prompt restrictions or claiming a
quality improvement. Preserve existing authorization and external-data boundaries.
Public documentation checks need no inference key or model call. Reuse relevant
existing evaluation results; do not trigger paid or private-data experiments just
to complete this checklist. Installation, schema validity and collection success
are not model-quality measurements.
