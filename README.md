# Agent Policy Radar

Tracks model and harness changes, reviews standing agent instructions, and proposes project-specific prompt/policy updates.

## Purpose

AI services and coding-agent harnesses change quickly. This project exists to keep local agent policy current without mixing that work into product/tool repositories such as `tierwork` or `local-ai-connector`.

It is not a benchmark suite by default. It is an operational note and review layer for:

- model behavior trends: Claude, Codex/GPT, Gemini, Astra, etc.
- harness behavior trends: Claude Code, Codex CLI/App, Pi, Telegram bridge, MCP, skills/tools.
- standing instruction hygiene: `AGENTS.md`, `CLAUDE.md`, MCP server instructions, skills, project playbooks.
- project-specific recommendations: what to shorten, split, remove, or keep.

## Change History and Auditability

- [CHANGELOG.md](CHANGELOG.md): release changes, reasons, commit evidence, verification limits.
- [Audit trail proposal](recommendations/audit-trail.md): planned per-run records and approval/application evidence.
- Unified CLI executions now record start/end UTC times, duration, command arguments, runtime/version, implementation/config hashes, exit status and exceptions under `~/.agent-policy-radar/audit/`.
- Before/after report, source snapshot and recommendation contents are preserved as local hash-addressed blobs even when the normal output is overwritten. Unchanged artifacts are labeled, not claimed as newly generated.
- These records can contain private paths and excerpts. They are not uploaded automatically, are not tamper-proof, and have no automatic retention cleanup. POSIX permissions do not replace Windows ACLs.
- Direct execution of individual scripts bypasses the unified execution audit. Review/discovery bundles retain their separate records; approval/application linkage is still incomplete. A hard-killed run may have only `started.json`; this is not success.

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

## Claude / Codex / Pi Distribution

This repo is structured for multiple agent surfaces:

- **Claude Code plugin**: `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
- **ChatGPT/Codex Agent Plugin**: root `plugin.json`
- **Codex local/repo marketplace**: `.agents/plugins/marketplace.json`
- **Pi package**: `package.json` with `pi-package` and `pi.skills = ["skills"]`
- **Shared skill**: `skills/agent-policy-radar/SKILL.md`

Claude Code marketplace install from this repo:

```bash
claude plugin marketplace add HoonStyle/agent-policy-radar@main
claude plugin install agent-policy-radar@agent-policy-radar
```

Codex marketplace install from this repo:

```bash
codex plugin marketplace add HoonStyle/agent-policy-radar --ref main
codex plugin add agent-policy-radar@agent-policy-radar
```

The Claude/Codex marketplaces track `main`, not a release tag. New releases must bump `package.json`, root `plugin.json`, `.claude-plugin/plugin.json`, and both version fields in `.claude-plugin/marketplace.json` together. A branch-tracking source permits discovery; it does not guarantee automatic installation.

To fetch and install newer versions without re-registering the marketplace:

```bash
claude plugin marketplace update agent-policy-radar
claude plugin update agent-policy-radar@agent-policy-radar
codex plugin marketplace upgrade agent-policy-radar
codex plugin add agent-policy-radar@agent-policy-radar
```

Existing tag-pinned users must first remove and re-add this marketplace using the commands above, then reinstall the plugin. Removing the marketplace can uninstall its plugins, including any optional plugins you installed. Prefer marketplace update/upgrade when tracking `main`.

Pi install from GitHub:

```bash
pi install git:github.com/HoonStyle/agent-policy-radar@v0.1.10
```

For local development, run this from the checked-out repository root:

```bash
pi install .
```

Public Claude/OpenAI directory submission still requires the provider review portals; this repository now contains the manifest and marketplace metadata needed for local/Git marketplace testing and submission preparation.

## Optional Review Workflow plugin

`review-workflow` is a separate optional plugin in this marketplace. Small fixes use lightweight notes by default: reason, change, and verification result. A final response or existing task note suffices; structured ledgers, IDs, baseline snapshots and independent reviews are not mandatory. Detailed recording is opt-in when requested, required by the project, or warranted by complexity/risk. It is not a dependency of Policy Radar and is not in the default root `skills/` directory. Installing/updating Policy Radar alone does not enable it. No global instruction edits, hooks, background jobs, or automatic code fixes are added.

Install only if wanted (after registering the marketplace above):

```bash
claude plugin marketplace update agent-policy-radar
claude plugin install review-workflow@agent-policy-radar
codex plugin marketplace upgrade agent-policy-radar
codex plugin add review-workflow@agent-policy-radar
```

In Claude invoke `/review-workflow:review-workflow`; in Codex explicitly request the Review Workflow skill after starting a new session. The procedure records a stable baseline and finding IDs, separates defects/investigation/improvements, checks minimal fixes and regressions, and defines an evidence-based stopping criterion. It asks for an appropriate project-local ledger location before writing; review-only requests do not authorize fixes.

The template is bundled under `plugins/review-workflow/skills/review-workflow/references/ledger-template.md`. It includes a Python 3.10+ ledger helper (`plugins/review-workflow/skills/review-workflow/scripts/review.py`): `init`, `finding`, `update`, `pass`, `validate`, and `compare`. The helper stores UTC history, hashes index/worktree/untracked content separately, classifies reviews from declared provenance/inputs, and rejects verified findings missing level-specific evidence. Commands in profiles are never executed.

Teams may commit a `.review-workflow.json` profile at their repository root; see `plugins/review-workflow/profile.example.json`. Missing profiles use defaults. Ledger location may follow project conventions or be explicitly outside the repo; nonignored local ledgers themselves change the baseline. Korean and English manual templates are available. This is not an authenticated approval engine or a guarantee of reviewer accuracy. Its version is independent of Policy Radar.

## Discover new official guidance

```bash
python3 scripts/policy_radar.py discover
```

Fetches four official `llms.txt` indexes (Claude Code, Anthropic platform, OpenAI developers, ChatGPT Learn) and extracts prompting/model/migration/instruction/release/changelog links. Only HTTPS links and redirects to explicitly allowed official hosts are accepted. Requests have timeouts and size limits, without retries or recursive crawling.

Reports are preserved per run in `~/.agent-policy-radar/discovery/`. First-seen URLs are not necessarily new publications. Candidates require original-page review; discovery does not fetch their bodies, change the source registry, or edit instructions. Failures are recorded and return a nonzero status. `discover` can run separately and is now the first step of `all`. In `all`, failed discovery/source checks are reported while independent local analysis continues; the final exit status remains nonzero (partial result). A failed local stage stops its dependent stages. Failures are never interpreted as no changes. No scheduler is installed.

## Prompt cleanup review

```bash
python3 scripts/policy_radar.py review "path/to/CLAUDE.md"
python3 scripts/policy_radar.py review "path/to/CLAUDE.md" --proposal "path/to/draft.md"
```

Use `py -3` on Windows. Outputs are unique private-local review directories under `~/.agent-policy-radar/reviews/` (override with `--output-dir`), outside the plugin cache. Each contains a proposed text, unified diff, original/proposed/patch hashes, and pending-review status. Originals are never edited; no apply command exists. Bundles contain potentially private excerpts: do not publish them automatically. POSIX permission bits are best-effort and do not substitute for Windows ACLs.

Without a supplied proposal, cleanup is limited to adjacent identical plain bullets outside code fences, retaining safety-keyword matches. Broader shortening, moves, and semantic conflicts require agent/human review through the skill workflow and `--proposal`; the CLI does not claim to solve them automatically.

## Analysis limits and current results

This is an instruction-review assistant, not a validated latest-model optimization engine. Duplicate lines and keyword signals do not establish conflicts or justify deletion. Official guidance and observed behavior still require human/agent comparison before any optimization recommendation.

`all` runs discovery, source checks, inventory, overlap analysis and draft generation in that order. Source reports distinguish first-seen, changed, unchanged and failed. Generated drafts live in `recommendations/runs/<id>/`; `recommendations/current.json` identifies the current run even with zero candidates. Older root-level drafts are historical and must not be used as current results.

**MCP configuration analysis is currently excluded**; restoring it requires a separate scope decision. MCP-scoped files and non-Markdown configuration/cache files are excluded before reading their contents. For MCP instructions, explicitly select a sanitized Markdown instruction document instead. Markdown is not automatically secret-free; inspect before sharing. Previously generated reports may already contain private values: this fix does not retroactively sanitize local archives or Git history.

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
