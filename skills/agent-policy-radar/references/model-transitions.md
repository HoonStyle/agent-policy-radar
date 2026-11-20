# Model-transition review reference

Verified: 2026-11-20. These are dated review inputs, not permanent defaults or evidence of improved local behavior. Recheck the linked rolling documentation before applying a finding. Apply a check only to an authorized target that uses the relevant model and interface.

## GPT-6.2 Astra and Sol

The official API changelog dates the release to 2026-11-17. The current latest-model guide covers both Astra and Sol; its prompting examples are no longer described as Astra-only observations.

For direct API adapters, inspect:

- Tool calling: use Responses; Chat Completions support does not imply tool support.
- Effort: the migration guide starts new integrations at medium and maps none/minimal to low. Do not change a tuned workload's effort solely because this reference exists.
- Stable instructions: GPT-6.2 places top-level `instructions` after `input`. For reusable cached guidance, the official guide uses a developer message at the beginning of `input`; top-level `instructions` are for the current request.
- Prefix preservation: edits to prior messages, certain model switches, and end-user or organization changes can remove reasoning items. Inspect actual message construction, model routing, and account boundaries before claiming compatibility. This does not mean every model switch loses the whole conversation.
- Parameter support: inspect the current model and migration references, including unsupported sampling/logprob parameters and service tiers, rather than inheriting older model defaults.

For prompting reviews, compare the requested outcome with the existing completion rule before adding another rule. GPT-6.2's guide discusses premature handoffs, but an agent ignoring an existing rule does not prove the rule is absent. Keep user preferences and explicit approval boundaries. Treat recommended wording as a remedy to test only when the relevant environment exhibits the problem.

Sources:
- https://developers.openai.com/api/docs/changelog.md
- https://developers.openai.com/api/docs/guides/latest-model.md
- https://developers.openai.com/api/docs/models/gpt-6.2-astra.md
- https://developers.openai.com/api/docs/models/gpt-6.2-sol.md

## Claude Fable 5.2 and Mythos 5.2

The official platform release notes date the release to 2026-11-09. Mythos access is restricted to verified organizations; public documentation is not proof that an account can use it.

For direct Messages API adapters, inspect:

- Prefix checks: changing `system`, `tools`, or earlier messages and returning affected thinking blocks can produce a 400 error. Retrying the identical request does not repair that mismatch. Do not prescribe `drop_block` as a blanket default; the official guide treats it as a temporary measure with possible reasoning/token costs.
- History ownership: distinguish code that constructs `messages` itself from Claude Code, claude.ai, Managed Agents, or Agent SDK managing history. Do not automatically prescribe direct-API migrations to managed harness users.
- Model routing: Fable/Mythos 5.2 can read other models' thinking on supported platforms, but models outside this pair cannot read their thinking. A successful response after a downgrade is not proof that reasoning survived.
- Account routing: their thinking blocks are tied to the producing account or a linked account. Do not describe a cross-account request succeeding as preservation of every thinking block.
- Computer use and advisors: verify the declared computer tool version and executor/advisor pairing against current platform-specific compatibility tables.
- Data handling: confirm required retention and actual access eligibility before suggesting a model switch. Do not assume an existing ZDR arrangement covers these models.

For behavioral reviews, the guide discusses early stopping at low/medium effort, subagent cost, accumulated caution, and unrequested changes encouraged by code-ownership wording. Inspect the actual instruction and an observed failure before proposing compensation. Do not delete safety gates or a user's intentional multi-model workflow from these observations alone. Do not add code-ownership language where the user wants minimal changes. Higher effort is not a substitute for authorization or measured validation.

Sources:
- https://platform.claude.com/docs/en/release-notes/overview.md
- https://platform.claude.com/docs/en/models/fable-5-2/migration-guide.md
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2.md

## Representative review cases

These are desk-review acceptance cases, not fresh model benchmarks.

| Input | Expected decision |
| --- | --- |
| A GPT-6.2 adapter uses Chat Completions tool calls | Revise the adapter against Responses guidance; do not add a global instruction to force tools. |
| A Fable 5.2 adapter changes its system prompt and replays old signed thinking | Review prefix handling; do not classify a blind retry as a fix. |
| A managed Claude Code user has no custom message adapter | Do not prescribe direct Messages API changes solely from the release notes. |
| A user's intentional delegation rule has no observed excess calls | Keep or defer; do not remove it on the strength of the provider's delegation warning alone. |
| A completion rule exists but the agent stopped at a source list | Report failure to follow the rule; do not claim missing coverage or append a duplicate global rule. |
| Source checkout is older than the selected installed package | Preserve the newer baseline; verify the active package after any authorized local update. |
