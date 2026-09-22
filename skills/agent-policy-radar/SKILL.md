---
name: agent-policy-radar
description: Review model/harness prompt guidance and local instruction hygiene. Use when the user asks to run policy radar, check Claude/Codex model changes against AGENTS.md/CLAUDE.md, scan global/project/skill/MCP instruction overlap, or generate approval-gated policy recommendations.
---

# Agent Policy Radar

Use this skill as a thin wrapper around the local `agent-policy-radar` CLI. The CLI produces source notes, findings, and recommendations only; it must not silently edit global instructions, project files, skills, or MCP configs.

## Repository

```bash
cd /Users/hoonstyle/dev/agent-policy-radar
```

Before changing this repository, read its `AGENTS.md`.

## User intents

Use the CLI when the user asks things like:

- “policy radar 돌려줘”
- “전역 지침이랑 스킬 지침 중복 검사해줘”
- “새 Claude/Codex 모델 기준으로 AGENTS.md 점검해줘”
- “MCP instructions랑 스킬 instructions 충돌 찾아줘”
- “공식 프롬프트 가이드 바뀐 거 확인해줘”

## Commands

Run the full pipeline:

```bash
cd /Users/hoonstyle/dev/agent-policy-radar
python3 scripts/policy_radar.py all
```

Run individual steps:

```bash
python3 scripts/policy_radar.py sources     # official docs change check
python3 scripts/policy_radar.py scan        # instruction inventory
python3 scripts/policy_radar.py overlap     # overlap/conflict analysis
python3 scripts/policy_radar.py recommend   # markdown recommendation drafts
```

## Outputs

Summarize these files after running:

- `reports/source_changes.json`
- `reports/instruction_inventory.json`
- `reports/overlap_analysis.md`
- `recommendations/*.md`

For Telegram-originated turns, keep the reply concise and list the most important generated paths.

## Approval gate

Always preserve this boundary:

1. Automatic work may fetch public official docs, scan local instruction files, and create reports/recommendations inside `agent-policy-radar`.
2. Do not edit any target global instruction, project `CLAUDE.md`/`AGENTS.md`, skill, or MCP config unless the user explicitly approves that specific target edit.
3. If a recommendation concerns another repository, make the edit only in that target repository after approval and after reading that repository's own `CLAUDE.md`/`AGENTS.md`.
4. If analysis detects conflict or ambiguity, report excerpts and ask for approval/choice; do not auto-resolve.

## Interpretation rules

- Separate official source facts from local operational interpretation.
- Treat model-specific prompting guides as review inputs, not automatic migration authority.
- Treat duplicated safety text as a responsibility-separation candidate, not automatic deletion.
- Prefer: global = common safety/operating principles; skill/MCP = domain-specific procedure; project = repo-local workflow.
