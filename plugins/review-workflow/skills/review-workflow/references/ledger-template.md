# Review ledger — <task ID>

Status: pending review
Created (UTC): <time>
Repository: <identifier; avoid unnecessary personal paths>
Baseline: <base/head commit or worktree snapshot description>
Dirty state: <index/worktree/untracked file state and SHA-256 list; ignored exclusions>
Profile: <project .review-workflow.json hash, or defaults>
Scope: <requested behavior and boundaries>
Acceptance criteria: <agreed checks>
Authority: <review-only or explicitly authorized correction scope>
Storage: <agreed local location; publication not implied>

## Findings

### R-001 — <title>

- First seen: <pass ID, UTC>
- Location and baseline: <file:line, revision>
- Requirement reference: <spec section or NFR ID>
- Expected / observed: <requirement and evidence>
- Observed boundary: <entry/processing/return/serialization/external observation>
- Unconfirmed scope: <explicit limits or none>
- Classification: <confirmed defect / needs investigation / optional improvement>
- Priority / impact / confidence: <with rationale>
- Origin: <pre-existing omission / introduced by change / out-of-scope improvement / unknown>
- Reproduction or static evidence: <reference; do not invent results>
- Decision and reason: <fix / investigate / defer / reject>
- Approval reference: <actual user authorization and scope, or none>
- Fix reference: <commit/diff, or none>
- Verification level: <unverified / source / execution / simulator / device>
- Verification: <source location+reasoning OR command+result+environment; simulator/device additionally require device/configuration IDs>
- Outcome: <pass / fail / not-run>
- Current status: <open / investigating / fixed-unverified / verified / deferred / rejected / reopened>

## Pass/event history (append; do not erase prior decisions)

| UTC | Pass/event ID | Actor | Baseline | Finding IDs | Action and reason | Evidence/result |
| --- | --- | --- | --- | --- | --- | --- |
| <time> | P-001 | <known actor> | <revision> | R-001 | Initial triage | <reference> |

## Check comparison

| Check | Command | Baseline | Current | Result | Evidence |
| --- | --- | --- | --- | --- | --- |

## Reviewer provenance (per pass)

- Initial reviewer / current reviewer / agent / model if known / execution reference:
- Complete supplied input inventory (source / requirements / initial-judgment / briefing / other, each with reference):
- Derived classification: self / independent / comparative / unknown. Based only on recorded inputs, not guaranteed independence.

## Completion decision

- Acceptance criteria: <pass/fail/not checked per item>
- Blocking defects: <IDs or none; include unresolved serious findings>
- Deferred improvements and residual risks: <IDs and explanation>
- Checks not run: <what and why>
- Outcome: <complete / blocked / further investigation>
- Decision authority: <actual decision source; never generated approval>
