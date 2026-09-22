# Policy Radar Automation Development Plan — 2026-09-22

## Goal

Automate detection and review support for changes in model/harness guidance and overlaps among global instructions, project instructions, skills, and MCP/server instructions.

The system should produce evidence-backed notes and recommendations, not silently rewrite policies.

## Non-goals

- No automatic edits to other repositories.
- No destructive cleanup of skills, MCP configs, or instruction files.
- No large benchmark suite by default.
- No provider-specific hidden prompt assumptions beyond official docs and observed local behavior.

## Safety model

All automated checks stop at one of these outputs:

1. `sources/` note: official doc/release-note change summary.
2. `findings/` note: dated local interpretation or observed behavior.
3. `recommendations/` note: proposed change requiring user approval.

Actual edits to global instructions, project `CLAUDE.md`/`AGENTS.md`, skills, or MCP instructions require explicit approval and must be done in the target repo/context.

## Architecture

```text
agent-policy-radar/
  scripts/
    check_sources.py              # Fetch official docs, compare hash/etag/last-modified
    scan_instructions.py          # Inventory and statically inspect instruction files
    analyze_overlap.py            # Detect duplicate/conflicting policy themes
    generate_recommendations.py   # Emit markdown recommendation drafts
  data/
    source_registry.json          # URLs, labels, check cadence, last hashes
    instruction_targets.json      # Known global/project/skill/MCP instruction paths
    snapshots/                    # Optional raw or normalized text snapshots
  sources/
  findings/
  recommendations/
```

## Phase 1 — CLI MVP

### 1. Source registry and change detector

Create `data/source_registry.json` with official sources:

- Claude Code memory/settings docs
- Anthropic prompt engineering docs
- OpenAI prompt engineering docs
- Codex CLI docs
- major model prompting guides when known
- MCP spec docs if relevant

`check_sources.py` should:

- fetch URL with timeout and clear user agent
- prefer markdown docs where available
- record `etag`, `last-modified`, content hash, checked timestamp
- detect changes since last check
- create a short `sources/YYYY-MM-DD-*.md` draft for changed pages
- never treat a changed page as an instruction to modify local files automatically

### 2. Instruction inventory scanner

`scan_instructions.py` should collect:

- global Pi/user instructions
- current repo `AGENTS.md`
- registered project `CLAUDE.md`/`AGENTS.md` under `~/dev`
- installed skill `SKILL.md` files
- known MCP server instruction/config files, if configured

Initial static metrics:

- line count / byte count
- repeated headings
- imports or references to `AGENTS.md`, `CLAUDE.md`
- model-specific names
- strong modal words: `always`, `never`, `무조건`, `항상`, `절대`
- external-transfer / API-key / approval / destructive-change rules
- stale workaround patterns, e.g. “read AGENTS.md” in `CLAUDE.md` when native loading exists

### 3. Overlap/conflict classifier

`analyze_overlap.py` should classify duplicated policy fragments into categories:

- `global-safety`: approval, destructive changes, credentials, privacy
- `transport`: Telegram-specific behavior
- `tool-domain`: skill-specific API/procedure
- `project-local`: repo-specific build/test/workflow
- `model-harness`: Claude/Codex/Pi behavior assumptions
- `cost-external-api`: paid API or external transmission rules

Output should be JSON plus a markdown summary.

Rules:

- If global and skill say the same safety rule, recommend keeping global and shortening skill to reference global.
- If skill is more specific, keep skill-specific rule.
- If project-local rule appears globally, recommend moving it down.
- If conflict is detected, do not auto-resolve; create recommendation with both excerpts.

### 4. Recommendation generator

`generate_recommendations.py` should create files under `recommendations/`, grouped by target:

```text
recommendations/global-instructions.md
recommendations/skills-overlap.md
recommendations/mcp-instructions.md
recommendations/<repo>.md
```

Each recommendation entry should include:

- target file
- issue type
- evidence excerpts
- risk level: low/medium/high
- suggested edit shape
- approval required: yes
- auto-edit allowed: no by default

## Phase 2 — Pi Skill wrapper

Add a thin skill/playbook for this repo after CLI MVP stabilizes.

The skill should answer user requests like:

- “policy radar 돌려줘”
- “전역 지침이랑 스킬 중복 검사해줘”
- “새 Claude/Codex 모델 기준으로 지침 점검해줘”
- “MCP instructions랑 스킬 instructions 충돌 찾아줘”

Skill responsibilities:

- identify requested scope
- run the appropriate CLI command
- summarize generated files
- enforce approval gate
- remind that target repo edits require separate approval

The skill should not contain the scanning logic itself.

## Phase 3 — Optional scheduled check

Add a local cron/launchd wrapper only after Phase 1 is useful.

Suggested cadence:

- source docs: daily or weekly
- full local instruction scan: manual or weekly
- recommendation generation: only when changes or explicit request exist

Notification options:

- write a local report only
- optional Telegram notification: “source changed; review generated”

No automatic policy edits from scheduled jobs.

## Phase 4 — Optional MCP wrapper

Only add MCP after CLI and skill usage patterns are stable.

Candidate MCP tools:

- `policy_radar.check_sources`
- `policy_radar.scan_instruction_inventory`
- `policy_radar.analyze_overlap`
- `policy_radar.generate_recommendations`

MCP is useful if Claude Code, Codex, Pi, or another harness should call the same functionality as tools with JSON outputs.

## Default invocation model

- Normal use: explicit user request.
- Passive automation: source-change detection only.
- No broad auto-trigger during unrelated coding tasks.

Good triggers:

- “새 모델”, “프롬프트”, “AGENTS.md”, “CLAUDE.md”, “스킬 중복”, “MCP 지침”
- known source-change report exists

Bad triggers:

- every coding task
- every skill install
- any casual mention of “prompt”

## Implementation order

1. Create `data/source_registry.json`.
2. Implement `scripts/check_sources.py`.
3. Implement `data/instruction_targets.json` and `scripts/scan_instructions.py`.
4. Implement heuristic overlap analyzer.
5. Generate first recommendation report against global/project/skill instructions.
6. Review results manually and tune heuristics.
7. Add Pi skill wrapper if repeated use is confirmed.
8. Consider scheduled checks.
9. Consider MCP wrapper.

## Acceptance criteria for MVP

- A single command can check official source changes and update local source metadata.
- A single command can inventory known instruction files and emit a JSON report.
- Duplicate/conflict candidates are listed with exact file paths and excerpts.
- Recommendation markdown is generated without modifying target files.
- All outputs clearly distinguish official fact from local interpretation.
