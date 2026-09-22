# Recommendation: local-ai-connector

## Status

Initial recommendation recorded after the 2026-09-22 correction.

## Recommendation

Keep `local-ai-connector` as an execution/connection tool. Do not make it the general model/harness trend tracker.

## Policy

- Profile-specific routing is required.
- spouse Windows:
  - Keep `Office` / `Paper` distinction.
  - Use `begin_task` / `complete_task` only when measurement is useful.
  - Codex is primary; Claude is a limited reviewer when called.
- owner Mac:
  - Do not inject Office/Paper routing.
  - Use connector for occasional cross-model review and handoff.
  - Do not copy spouse Paper/Office Claude skills into owner Mac by default.

## Rationale

The connector should expose tools and minimal instructions. Broader policy drift, model trend interpretation, and harness behavior review belong in `agent-policy-radar`.

## Applied Separately

A local-ai-connector change was made on 2026-09-22:

- `routingInstructions(host, profile)` split by profile.
- Mac owner installed copy updated.
- Mac connector-provided office/paper Claude skills removed.
- `CHANGELOG.md` added in `local-ai-connector`.

Future edits should still be approved and made in the target repository, not from this project automatically.
