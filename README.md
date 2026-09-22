# Agent Policy Radar

Tracks model and harness changes, reviews standing agent instructions, and proposes project-specific prompt/policy updates.

## Purpose

AI services and coding-agent harnesses change quickly. This project exists to keep local agent policy current without mixing that work into product/tool repositories such as `tierwork` or `local-ai-connector`.

It is not a benchmark suite by default. It is an operational note and review layer for:

- model behavior trends: Claude, Codex/GPT, Gemini, Astra, etc.
- harness behavior trends: Claude Code, Codex CLI/App, Pi, Telegram bridge, MCP, skills/tools.
- standing instruction hygiene: `AGENTS.md`, `CLAUDE.md`, MCP server instructions, skills, project playbooks.
- project-specific recommendations: what to shorten, split, remove, or keep.

## Core Principle

Separate facts from interpretation.

- **Source notes** summarize official docs and observed service capabilities.
- **Findings** record dated operational observations.
- **Recommendations** propose project-specific changes.
- Actual edits to another repo require separate approval and should be recorded in that repo.

## Directory Layout

```text
agent-policy-radar/
  sources/           # official docs and service capability notes
  findings/          # dated observations about models + harnesses
  recommendations/   # project-specific policy cleanup proposals
  notes/             # raw discussion notes and decisions
```

## Initial Scope

- Do not assume each provider optimizes for this user's multi-harness setup.
- Providers improve general model/harness behavior, but local standing instructions can still become stale.
- Focus on lightweight policy review, not large automatic eval projects.
- Prefer “proposal → human approval → targeted repo change” over automatic policy rewrites.

## Pi Package

This repo is structured as a Pi package with `package.json` metadata:

- keyword: `pi-package`
- skill manifest: `pi.skills = ["skills"]`
- skill: `agent-policy-radar`

Install from GitHub:

```bash
pi install git:github.com/HoonStyle/agent-policy-radar@v0.1.2
```

For local development, run this from the checked-out repository root:

```bash
pi install .
```

## CLI MVP

Run from the repository root:

macOS/Linux:

```bash
python3 scripts/policy_radar.py all
```

Windows PowerShell:

```powershell
py -3 scripts\policy_radar.py all
```

Equivalent individual commands on macOS/Linux:

```bash
python3 scripts/check_sources.py --no-note
python3 scripts/scan_instructions.py
python3 scripts/analyze_overlap.py
python3 scripts/generate_recommendations.py
```

On Windows, use `py -3` and backslash paths, for example:

```powershell
py -3 scripts\check_sources.py --no-note
py -3 scripts\scan_instructions.py
py -3 scripts\analyze_overlap.py
py -3 scripts\generate_recommendations.py
```

Outputs:

- `reports/source_changes.json`: official-doc change check results
- `reports/instruction_inventory.json`: discovered instruction files and static metrics
- `reports/overlap_analysis.{json,md}`: duplicate/conflict candidates
- `recommendations/*.md`: approval-gated recommendation drafts

Guardrail: the CLI only detects and drafts recommendations. It must not edit global instructions, skills, MCP configs, or other repositories without explicit approval.

A Pi skill wrapper source is tracked at:

`skills/agent-policy-radar/SKILL.md`

It delegates to this CLI and preserves the same approval gate. The skill uses package-relative paths; it should not depend on `/Users/...` or other machine-specific locations.
