---
name: agent-policy-radar
description: Review model/harness prompt guidance and local instruction hygiene. Use when the user asks to run policy radar, check Claude/Codex model changes against AGENTS.md/CLAUDE.md, scan global/project/skill/MCP instruction overlap, or generate approval-gated policy recommendations.
---

# Agent Policy Radar

Use the local `agent-policy-radar` CLI to collect evidence; the agent must interpret relevant changes against the actual instructions and review criteria. CLI reports alone are not a completed policy review. The CLI produces source notes, findings, and recommendations only; it must not silently edit global instructions, project files, skills, or MCP configs.

## Repository and path handling

This skill is packaged with the repository/plugin. Resolve paths relative to this `SKILL.md` file or the host-provided plugin root, not to a user-specific home directory.

- Claude Code plugin root: `${CLAUDE_PLUGIN_ROOT}` when available
- Skill directory in the package: `skills/agent-policy-radar/`
- Package/repository root: two directories above the skill directory (`../..`) when no host variable is available
- CLI entrypoint from the package root: `scripts/policy_radar.py`

Before changing this repository, read `AGENTS.md` from the package/repository root.

## User intents

Use the CLI when the user asks things like:

- “policy radar 돌려줘”
- “전역 지침이랑 스킬 지침 중복 검사해줘”
- “새 Claude/Codex 모델 기준으로 AGENTS.md 점검해줘”
- “MCP instructions랑 스킬 instructions 충돌 찾아줘”
- “공식 프롬프트 가이드 바뀐 거 확인해줘”

## Commands

Run the full pipeline from the package/repository root.

macOS/Linux:

```bash
python3 scripts/policy_radar.py all
```

Windows PowerShell:

```powershell
py -3 scripts\policy_radar.py all
```

Run individual steps with the same Python executable:

```bash
python3 scripts/policy_radar.py sources     # official docs change check
python3 scripts/policy_radar.py scan        # instruction inventory
python3 scripts/policy_radar.py overlap     # overlap/conflict analysis
python3 scripts/policy_radar.py recommend   # markdown recommendation drafts
```

```powershell
py -3 scripts\policy_radar.py sources
py -3 scripts\policy_radar.py scan
py -3 scripts\policy_radar.py overlap
py -3 scripts\policy_radar.py recommend
```

## Discover newly published guidance

For requests about new models or newly available guidance, run `python3 scripts/policy_radar.py discover` from the package root (`py -3` on Windows). Read the returned local report. It finds candidate links in official indexes, not verified recommendations. First-seen does not mean newly published. Review relevant candidate pages and their dates before proposing source-registry changes or prompt edits. Index failures must be reported, not interpreted as no changes. This command also runs first in `all`; there is no scheduler.

## Update review: from changes to decisions

For a general request to review updates, review relevant provider guidance against the affected instructions. Inspect this package's own review/editing criteria when the user requests it or an actual review reveals a missed change or unsupported verdict. A source-only request may stop at source findings; do not silently narrow a policy update review to collecting URLs.

Use the authorized task scope and existing target configuration to locate affected instructions. Read the relevant passages and establish the model, harness/API surface, loading scope, and version conditions. Do not scan unrelated projects or private memory. If a necessary target is inaccessible or its loading is unknown, name that gap and defer that target's verdict; do not conclude that its instructions need no changes.

For material changes, connect the official passage or observed failure to the actual target rule (or missing coverage), then decide keep, revise, remove, or defer. Record the reason and a minimal proposed replacement for change candidates. An existing rule that already covers the change is evidence for keeping it; a source-change count is not. Use a short finding rather than a mandatory ledger for small changes.

Distinguish the evidence needed for the decision:

- **Documented correctness:** An obsolete factual claim, changed loading condition, or API incompatibility can justify correcting the affected guidance from current official evidence and confirmed applicability. A model failure is not required to correct a fact.
- **Behavioral compensation:** New prompt restrictions, effort changes, or provider-specific workarounds require an observed problem in the relevant environment. Validate a proposed remedy on a small representative task when feasible; otherwise label its effect unverified, not improved.
- **Radar's own criteria:** If a real review missed an applicable change or produced an unsupported verdict, inspect the rule that led to it and propose a scoped correction to this skill. Do not merely append the new URL or add one rule per release. Apply repository-owned skill changes when the user requests them; this does not authorize changes to other targets.

Before completing the review, check the proposed decision against the actual evidence and preserve user intent and approval boundaries. For changed behavioral criteria, use representative cases, including a case that should remain unchanged; distinguish a desk review from a fresh model/workload test. Do not repeat costly experiments just to create an update.

Lead the report with a concrete decision and scope: policy/criteria update, source maintenance only, no change warranted, or incomplete review. State what was actually compared and validated. Recommend a release for the identified user benefit, not merely because documents changed. Collection success and CI do not prove better agent behavior.

## Harness-specific instruction checks

For findings that depend on Claude Code instruction loading, distinguish files found on disk from files loaded into the session. Check only the relevant loading conditions in the current [memory reference](https://code.claude.com/docs/en/memory), using `/context` or available session evidence rather than inventory alone. Read/Write/Edit may trigger on-demand loading; missing Read history alone does not prove non-loading. Check session-specific auto-memory behavior only for auto-memory findings. A file not loaded in the current session is not evidence of duplicate loading there; assess its actual usage before proposing removal. Do not transfer Claude-specific conditions to other harnesses.

For Claude Code prompt audits, suggest the built-in `/doctor prompt-audit <path>` where available, or reuse an existing relevant result before duplicating work. Consult the current memory reference for availability and prerequisites rather than fixing version details here. Any execution remains subject to the authorized target scope and existing data/cost permissions; otherwise continue with local inspection. Verify findings as candidates, not automatic edit approval. An additional audit or model call is not required.

## Prompt cleanup (explicit request)

For cleanup requests, do not stop at an overlap count. Read the explicitly selected instruction files locally. Identify which harness actually loads each file; if authority or loading is unknown, ask rather than infer priority from directory depth.

Classify each proposed change as keep, shorten, move, delete, or conflict-review. Preserve safety/approval rules and domain constraints. Repeated rules across independent skills may be necessary for portability. Do not send private instructions to external helper APIs without separate permission.

Write a proposed replacement to a private local draft file, without changing the original. Explain the evidence and reason for each change. Then generate the review bundle:

```bash
python3 scripts/policy_radar.py review "<original-file>" --proposal "<draft-file>"
```

On Windows use `py -3` instead of `python3`. Without `--proposal`, the CLI only drafts adjacent identical bullet cleanup; it is not semantic analysis. Inspect `changes.diff` and the safety-removal flags before presenting the proposal. The bundle records hashes, not user approval. Application is outside this CLI and requires explicit approval of the exact target and diff; recheck the original hash before applying. For moves, review both source and destination together.

## Outputs

For ordinary result reports too, inspect the surrounding source sentences and actual loading/application scope of automated candidates relevant to the user's request. Classify them as keep, change candidate, or judgment deferred, with a brief reason. Sentence duplication alone does not justify a change recommendation. If context or scope cannot be confirmed, defer judgment rather than imply a verified issue. Do not expand review to unrelated files or the entire conversation history.

When reporting provider guidance, identify the applicable model, harness or direct API surface and distinguish official advice from locally observed behavior. Do not present Astra-based observations as measured Sol/Luna behavior. Read rolling guides for their current scope; registry labels are dated hints, not permanent proof.

Summarize these files after running:

- `reports/source_changes.json`
- `reports/instruction_inventory.json`
- `reports/overlap_analysis.md`
- `recommendations/current.json` and only the current run files it names; root-level drafts are historical

For Telegram-originated turns, keep the reply concise and list the most important generated paths.

## Approval gate

Always preserve this boundary:

1. Automatic work may fetch public official docs, scan local instruction files, and create reports/recommendations inside `agent-policy-radar`.
2. Do not edit any target global instruction, project `CLAUDE.md`/`AGENTS.md`, skill, or MCP config unless the user explicitly approves that specific target edit.
3. If a recommendation concerns another repository, make the edit only in that target repository after approval and after reading that repository's own `CLAUDE.md`/`AGENTS.md`.
4. If analysis detects a relevant conflict or ambiguity, report the excerpts and uncertainty regardless of whether it blocks work. Ask for approval/choice only where the unresolved decision blocks the next action; do not auto-resolve it. Continue unrelated work already authorized.

Complete requested investigation, analysis and reviewable drafts before waiting for approval of their application. Do not stop at offering a plan when the user already requested that work. If an instruction requires stopping, identify the file and relevant passage, explain its application, and distinguish the explicit restriction from your interpretation. A progress update or announced next step is not completion: report the requested deliverable, performed checks and remaining blockers. This does not expand authorization for risky actions or modify existing approval boundaries.

## Interpretation rules

- Prefer each provider's native harness defaults and documented behavior. Propose additional prompt/configuration compensation only for a confirmed problem in the actual environment, and keep it minimal and scoped. Do not transplant another provider's workaround or add speculative rules based solely on model trends. Preserve explicit user/project requirements and applicable safety boundaries.

- Preserve the user's personal preferences and intent (including language, tone, workflow, and risk tolerance within applicable safety boundaries). Brevity, duplication, or a provider's generic recommendation alone is not a reason to rewrite them.
- For personal instructions, propose only the minimum change tied to an evidenced conflict or observed unwanted behavior. Explain that connection and what intent remains preserved. If evidence or intended meaning is unclear, ask rather than recommend changing the preference. Broader style cleanup requires an explicit user request.

- Separate official source facts from local operational interpretation.
- Treat model-specific prompting guides as review inputs, not automatic migration authority.
- Treat duplicated safety text as a responsibility-separation candidate, not automatic deletion.
- Treat global/skill/project responsibility separation as a hypothesis to review, not a relocation instruction. Require actual loading-scope evidence before changing safety text.
- Automated results are review candidates, not latest-model optimization findings. Use the evidence requirements above: official corrections and behavioral optimizations are different decisions. Disclose missing applicability or validation evidence.
