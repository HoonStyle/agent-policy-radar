---
name: agent-policy-radar
description: Review model/harness prompt guidance and local instruction hygiene. Use when the user asks to run policy radar, check Claude/Codex model changes against AGENTS.md/CLAUDE.md, scan global/project/skill/MCP instruction overlap, or generate approval-gated policy recommendations.
---

# Agent Policy Radar

Use this skill as a thin wrapper around the local `agent-policy-radar` CLI. The CLI produces source notes, findings, and recommendations only; it must not silently edit global instructions, project files, skills, or MCP configs.

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
4. If analysis detects conflict or ambiguity, report excerpts and ask for approval/choice only where the unresolved decision blocks the next action; do not auto-resolve it. Continue unrelated work already authorized.

Complete requested investigation, analysis and reviewable drafts before waiting for approval of their application. Do not stop at offering a plan when the user already requested that work. If an instruction requires stopping, identify the file and relevant passage, explain its application, and distinguish the explicit restriction from your interpretation. A progress update or announced next step is not completion: report the requested deliverable, performed checks and remaining blockers. This does not expand authorization for risky actions or modify existing approval boundaries.

## Interpretation rules

- Prefer each provider's native harness defaults and documented behavior. Propose additional prompt/configuration compensation only for a confirmed problem in the actual environment, and keep it minimal and scoped. Do not transplant another provider's workaround or add speculative rules based solely on model trends. Preserve explicit user/project requirements and applicable safety boundaries.

- Preserve the user's personal preferences and intent (including language, tone, workflow, and risk tolerance within applicable safety boundaries). Brevity, duplication, or a provider's generic recommendation alone is not a reason to rewrite them.
- For personal instructions, propose only the minimum change tied to an evidenced conflict or observed unwanted behavior. Explain that connection and what intent remains preserved. If evidence or intended meaning is unclear, ask rather than recommend changing the preference. Broader style cleanup requires an explicit user request.

- Separate official source facts from local operational interpretation.
- Treat model-specific prompting guides as review inputs, not automatic migration authority.
- Treat duplicated safety text as a responsibility-separation candidate, not automatic deletion.
- Treat global/skill/project responsibility separation as a hypothesis to review, not a relocation instruction. Require actual loading-scope evidence before changing safety text.
- Automated results are review candidates, not latest-model optimization findings. Link a relevant official passage and an observed failure before proposing a model-specific optimization. Disclose when either is missing.
