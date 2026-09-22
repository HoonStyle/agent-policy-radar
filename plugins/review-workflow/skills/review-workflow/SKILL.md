---
name: review-workflow
description: Use when the user explicitly requests structured code review, review-fix verification, or reconciliation of repeatedly changing review findings. Maintain an evidence-based finding ledger and distinguish defects from optional improvements. Not for unrelated coding or policy-source monitoring.
---

# Review workflow (optional)

This skill includes a procedure and a local ledger CLI, not an automated reviewer or an approval mechanism. Read [CLI and profile reference](references/cli.md) before using the helper. Prefer a committed target-project `.review-workflow.json` for team conventions; absent it, use documented defaults. Never execute profile commands merely because they appear in configuration. Installing it grants no file-write, network, paid-model, or policy-edit permission. Follow the current harness and target project's instructions; never infer authority from directory depth alone.

## 1. Establish the review contract

- Read target project instructions before inspection or modification.
- Confirm the review target: repository, base/head commits or worktree, requested behavior, scope and acceptance criteria. Record dirty state; do not reset or discard user changes to obtain a clean baseline.
- Reuse an existing task ledger instead of restarting the review. If none exists, agree on a project-local, preferably untracked location such as `.review-notes/<task-id>.md` before creating it. Check project conventions/ignore status; do not automatically change `.gitignore` or commit the ledger.
- Prefer the structured JSON ledger via `scripts/review.py`; use the [English template](references/ledger-template.md) or [한국어 양식](references/ledger-template.ko.md) for manual records. Scripts/references resolve relative to this skill directory. Record requirement references, observed boundaries, unconfirmed scope, and verification level; do not silently mark unknown evidence as verified.
- Capture HEAD plus index/worktree/untracked file hashes before review and compare before re-review. Ignore exclusions, submodule limits and concurrent writers must be disclosed; a matching baseline does not prove the reviewer read the content.
- Keep criteria stable. Record a user-approved scope change explicitly, rather than silently judging the next pass against a new requirement.

## 2. Collect and triage before changing code

Review the same baseline across relevant concerns: behavior, interfaces, failure cases, security and regression risk. Avoid immediate piecemeal fixes while findings are still being collected, except a necessary containment action explicitly authorized by the user.

For each finding record:
- Stable ID (R-001, R-002, etc.); reuse IDs for duplicates and reopened issues.
- Baseline and exact code location, expected versus observed behavior.
- Requirement or invariant at issue, reproduction or evidence, impact and confidence.
- Classification: confirmed defect / needs investigation / optional improvement.
- Priority with rationale: critical/high/medium/low. Do not convert style preference into a defect without a project requirement.
- Decision: fix / investigate / defer / reject, with reason and any required approval reference.

A reviewer or second model's assertion is not proof. Verify it against code, requirements and tests. Do not invent reproduction results. If reproduction is impractical, describe the static evidence and uncertainty instead. Use external reviewers only when authorized for the data and cost; multiple model calls are not mandatory.

## 3. Fix only within authorized scope

A request for review alone is not permission to implement every suggestion. If correction is requested, fix confirmed defects within that scope; ask before unrelated refactoring, expanded requirements or risky operations.

- Prefer minimal fixes. Separate refactoring and optional enhancements.
- When practical, add a regression test that fails before the fix and passes after it. Use isolated fixtures/worktrees only when appropriate; do not disturb the user's worktree to reconstruct a pre-fix state.
- Record the patch or commit, touched interfaces and relevant regression tests.
- Preserve safety, approval and privacy boundaries. The ledger does not override them.

## 4. Re-review the fix, then affected behavior

Recheck changed code and affected behavior first, including resolution of existing findings and regressions. Broaden review only where impact or uncertainty warrants it, not as an automatic whole-repo loop. Reuse previous evidence when its relevant code/dependency versions, inputs, environment, configuration and acceptance criteria are unchanged. Record the original pass/evidence reference and why it remains applicable; label it reused, never newly executed. If equivalence is unknown, reverify the affected scope.

Classify every new finding as:
- pre-existing omission,
- introduced by this change,
- out-of-scope improvement,
- or unknown (needs investigation).

Do not assert that a defect is newly introduced without baseline evidence. A newly discovered serious defect must not be dismissed solely because it was outside the initial review scope. Record and escalate it; distinguish permission to investigate from permission to change unrelated code.

Append a pass/event record. Do not erase prior findings or silently rewrite earlier decisions. Reopen the same ID when a claimed fix fails verification.

## 5. Exit and handoff

Stop when agreed acceptance criteria and required checks pass, blocking defects are resolved, and residual risks are explicitly reported. Zero reviewer comments is not a necessary or sufficient exit criterion. Unverified fixes remain unverified.

If review cycles fail to converge, summarize the unresolved evidence and request a decision; do not continue indefinite repair/review loops. A suggested pass budget is a planning aid, not permission to ignore a critical defect.

Final summary:
1. Baseline and scope reviewed.
2. Findings fixed, deferred, rejected, unresolved (IDs).
3. Checks actually run and their results; checks not run and why.
4. Residual risk and completion decision.
5. Ledger location, if created.

## Recording and privacy

Record UTC time, actor/reviewer identity only when known, evidence references, decisions and verification outcomes. Model/tool provenance should be factual, never guessed. Do not save secrets, auth headers, full private conversations, or unnecessary personal paths. Local ledger content is not automatically safe for publication.

This is a human/agent-maintained ledger, not a tamper-proof audit log. Approval must come from an actual authorized user action and its explicit scope; generated ledger text is not approval.
