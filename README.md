# Agent Policy Radar

**English** | [한국어](README.ko.md)

**Optional skills for instruction audits, development reviews, research, and UI/document design workflows.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-D97757)
![Codex](https://img.shields.io/badge/Codex-plugin-111111)

Install only the plugins you need. Agent Policy Radar favors the host's native behavior and targeted changes for observed problems. It does not automatically rewrite your instructions or impose a long review process on every task.

[Quick start](#quick-start) · [Plugins](#plugins) · [Usage](#usage) · [Privacy and limitations](#privacy-and-limitations) · [Releases](https://github.com/HoonStyle/agent-policy-radar/releases) · [Changelog](CHANGELOG.md)

## Plugins

| Plugin | Purpose | Version |
| --- | --- | --- |
| **`agent-policy-radar`** | Track official guidance and review local instruction inventories, overlap candidates, and proposed edits. | 0.1.19 |
| **`review-workflow`** | Organize review findings, fixes, and verification without an endless review loop. | 0.2.1 |
| **`paper-research`** | Assist with literature review, research planning, analysis, and writing; includes optional nursing research references. | 0.1.1 |
| **`ui-design-director`** | Design and review English/Korean UI, PowerPoint, and Word with shared color and typography. | 0.2.0 |

These plugins are independent. Installing or updating the base plugin does not install the others. If you only need research assistance, install `paper-research` alone.

> This is an instruction-review aid, not a guarantee of better model performance or an automatic duplicate-removal tool.

## Quick start

### Requirements

- Claude Code or Codex CLI, already installed and authenticated, plus Git.
- **Python 3.10+** for the Policy Radar CLI and optional Review Workflow recording tools. CI uses Python 3.11.
- Paper Research's skill documents do not require Python. Search, document access, and statistical execution depend on your host and available tools.

This is a self-hosted GitHub marketplace, not a listing in an official public plugin directory. Run the following commands in a terminal.

### Claude Code

Register the marketplace, then run only the installation commands you need:

```sh
claude plugin marketplace add HoonStyle/agent-policy-radar@main

claude plugin install agent-policy-radar@agent-policy-radar
claude plugin install review-workflow@agent-policy-radar
claude plugin install paper-research@agent-policy-radar
claude plugin install ui-design-director@agent-policy-radar
```

### Codex

```sh
codex plugin marketplace add HoonStyle/agent-policy-radar --ref main

codex plugin add agent-policy-radar@agent-policy-radar
codex plugin add review-workflow@agent-policy-radar
codex plugin add paper-research@agent-policy-radar
codex plugin add ui-design-director@agent-policy-radar
```

Start a **new session** after installation. Check the installed plugins with `claude plugin list` or `codex plugin list`.

### Pi

The root Policy Radar skill is also available as a version-pinned Pi package:

```sh
pi install git:github.com/HoonStyle/agent-policy-radar@v0.1.19
```

This does not automatically register the optional plugins as Pi skills and does not imply npm publication or gallery listing.

### Desktop, mobile, and remote sessions

The documented installation checks cover Claude Code and Codex CLI on macOS and Windows. Installing on one computer does not install plugins in other devices, cloud sessions, or the general Claude/ChatGPT apps. Remote use must target the environment where the plugin is installed. Check separate cloud environments for installation and file-access support.

## Usage

### Agent Policy Radar: instruction audits

In Claude Code, use `/agent-policy-radar:agent-policy-radar`. In Codex, explicitly ask for the installed Agent Policy Radar skill.

> Review my global and project instructions. Preserve personal preferences and report only supported conflicts or unnecessary overlap candidates.

> Check whether official model guidance has changed and explain which changes matter for my current instructions.

The workflow discovers candidate documentation links, checks registered sources, inventories configured instruction paths, and produces proposed edits and diffs. It distinguishes initial collection, changes, unchanged sources, and failures. It does not apply edits to the original files.

Overlap candidates are not confirmed defects. Semantic conflicts and model-performance improvements require further review; length or repetition alone is not sufficient reason to change an instruction. Unrelated files and complete conversation histories are outside the requested audit scope.

### Review Workflow: development reviews

Claude Code: `/review-workflow:review-workflow`. In Codex, request the installed Review Workflow skill.

> Review this change. Separate defects from optional improvements, and recheck the fixes and affected behavior rather than reopening the entire review.

- Small changes need only the reason, change, and verification result.
- Complex work can use a ledger for finding IDs, evidence, decisions, fixes, and checks.
- Previously verified evidence can be reused when versions and conditions still match; reuse must be disclosed.
- Completion follows agreed criteria and required checks, not an arbitrary target of zero findings.

The optional [recording CLI](plugins/review-workflow/skills/review-workflow/references/cli.md) provides `init`, `finding`, `update`, `pass`, `validate`, and `compare`. It checks references and evidence fields, not the truth of the evidence or user approval. Team settings can live in `.review-workflow.json`; configured commands are not automatically executed. See the [example profile](plugins/review-workflow/profile.example.json).

### Paper Research: research and writing

Claude Code: `/paper-research:paper-research`. In Codex, request the installed Paper Research skill.

> Summarize this paper's claims, methods, and limitations with source locations. Distinguish inaccessible sections from sections you actually read.

> Compare these papers for a related-work paragraph. Do not present results from different experimental conditions as a controlled comparison.

Choose only the stages needed:

| Stage | Assistance |
| --- | --- |
| Literature discovery | Search scope, paper identity and version, contribution and method comparisons |
| Critical reading | Claim–evidence mapping, assumptions, experiments, alternative explanations |
| Research planning | Questions, hypotheses, evaluation plans, reproducibility and resource limits |
| Data preparation | Provenance, permissions, variables, missing data, exclusion criteria |
| Statistical analysis | Methods, assumptions, and uncertainty appropriate to the study design |
| Writing and editing | Meaning-preserving edits and consistency among citations, tables, figures, and claims |

Optional [nursing research references](plugins/paper-research/skills/paper-research/references/nursing.md) cover instrument development, interventions, qualitative and mixed methods, systematic/scoping reviews, meta-analysis, data protection, and SPSS/AMOS/R workflows.

The skill must not invent citations, DOIs, statistics, or experimental results. It distinguishes author claims, observed results, and interpretation. Editing preserves meaning, numbers, conditions, and citation alignment. A request for review does not authorize changes, and simple editing does not require the entire research workflow.

It is **not** an SPSS/AMOS/R execution engine, automatic data-collection service, or IRB decision tool. Without the required tools and permissions, outputs remain plans or drafts. It does not replace clinical, statistical, or ethics expertise. External transmission of participant data or private manuscripts requires appropriate permission and institutional-policy checks.

### Design Director: UI, PowerPoint, and Word

Install `ui-design-director` to get three skills: `design-director` for UI, `presentation-design` for slide decks, and `document-design` for flowing documents. English and Korean share design foundations but keep medium-specific layout and review workflows.

> Use `design-director` to coordinate this UI’s palette while preserving its layout and behavior.

> Use `presentation-design` to improve this deck’s story and composition, preserving its template and editable charts.

> Use `document-design` to refine this report’s headings, tables, and page flow without changing its content or links.

The optional offline palette helper needs Python 3.9+. This package supplies no browser, Office engine, renderer, hooks, or background service. It uses the host’s existing authoring and rendering tools. Package/UI checks are recorded; actual PPTX/DOCX creation, rendering, and installed-host activation remain unverified. See the [plugin guide](plugins/ui-design-director/README.md) and [verification scope](plugins/ui-design-director/VERIFICATION.md).

## Updates

The Claude/Codex marketplace commands above track `main`. Discovering updates does not guarantee automatic installation or cross-device synchronization. Update only the plugins you use:

```sh
# Claude Code
claude plugin marketplace update agent-policy-radar
claude plugin update agent-policy-radar@agent-policy-radar
claude plugin update review-workflow@agent-policy-radar
claude plugin update paper-research@agent-policy-radar
claude plugin update ui-design-director@agent-policy-radar

# Codex
codex plugin marketplace upgrade agent-policy-radar
codex plugin add agent-policy-radar@agent-policy-radar
codex plugin add review-workflow@agent-policy-radar
codex plugin add paper-research@agent-policy-radar
codex plugin add ui-design-director@agent-policy-radar
```

Codex `add` also installs missing plugins. Start a new session and check the plugin list afterward. Moving from a pinned marketplace tag to `main` may require re-registration; removing a marketplace can also remove its plugins, so inspect installed plugins first.

`main` may contain unreleased work. Use a verified release tag for reproducible installation, and change pinned versions explicitly when updating.

## Policy Radar CLI

Run these commands from the repository or installed package root, not from the project being audited:

```sh
git clone https://github.com/HoonStyle/agent-policy-radar.git
cd agent-policy-radar
python3 scripts/policy_radar.py all
```

On Windows, use `py -3 scripts\policy_radar.py all`, or `python` if that is your installed interpreter.

| Command | Purpose |
| --- | --- |
| `discover` | Discover candidate links from four official `llms.txt` indexes |
| `sources` | Check documents registered in `data/source_registry.json` |
| `scan` | Inventory instructions at configured paths in `data/instruction_targets.json` |
| `overlap` | Analyze overlap candidates in the existing inventory |
| `recommend` | Generate review drafts from existing analysis |
| `all` | Run discovery, source checks, inventory, overlap analysis, and recommendations |
| `review <file>` | Generate a proposed cleanup and diff for one file |

```sh
python3 scripts/policy_radar.py review "path/to/CLAUDE.md"
python3 scripts/policy_radar.py review "path/to/CLAUDE.md" --proposal "path/to/draft.md"
```

Without `--proposal`, automatic cleanup is limited to adjacent identical bullets outside code blocks and preserves safety-keyword content. Semantic edits require an agent- or human-authored proposal. There is no command to apply the proposal to the original file.

If external discovery/source checks fail, `all` continues independent local analysis and exits with code 1 to report partial failure. Failed local stages stop dependent stages.

## Privacy and limitations

- Scans cover configured paths, not every file or custom location on the computer. Edit targets in a maintained checkout; changes inside an installation cache can be lost during updates. General external configuration-file support is not available.
- MCP configuration analysis is currently excluded.
- Discovery finds links; it does not verify their contents or automatically register them. First discovery does not imply recent publication.
- Source changes are relative to saved snapshots. Registered sources can still fail to load, including HTTP 403 responses.
- Checks run explicitly. There is no background scheduling, new-model alert service, or automatic optimization.
- API guidance and harness behavior are distinct. Findings for one model are not automatically validated for another.

### Output locations

| Location | Contents |
| --- | --- |
| Package `reports/` | Latest source checks, inventory, and overlap analysis |
| Package `recommendations/current.json` | Current recommendation run and file list, including zero-candidate runs |
| Package `recommendations/runs/<id>/` | Per-run review drafts |
| `~/.agent-policy-radar/discovery/` | Discovered documentation links |
| `~/.agent-policy-radar/reviews/` | Proposed edits, diffs, and source/proposal/patch hashes |
| `~/.agent-policy-radar/audit/` | Unified CLI start/end records, environment and configuration/code hashes, before/after results |

On Windows, `~` means the user home. Review Workflow ledgers use a separately chosen path.

Reports and source snapshots can be overwritten by subsequent runs. Package-cache outputs may not survive updates. The unified CLI preserves selected before/after records in the user home; running individual scripts bypasses this unified audit. Old root-level `recommendations/*.md` files are not necessarily current—check `current.json`.

**Records may contain private instructions, paths, and document excerpts.** Review them before sharing; do not automatically upload them to issues, Git, or external models. Markdown is not inherently free of secrets. There is no retroactive history cleanup, automatic retention cleanup, tamper-proof audit, or complete approval-to-application audit chain. POSIX permission settings alone do not establish Windows access controls.

See [PRIVACY.md](PRIVACY.md) and [TERMS.md](TERMS.md).

## Validation and evidence

For the pre-existing plugins, recorded checks include macOS/Windows CLI plugin installation and activation, a complete Windows Policy Radar run, fixture regressions, simulated research requests, and selected-page citation/numerical checks for two JMLR papers.

These checks do not establish better model performance, exhaustive literature searches, correctness across research fields, clinical/statistical validity, IRB suitability, actual SPSS/AMOS execution, or automatic app/mobile/cloud synchronization. Installation checks and research-quality evidence are different. See [findings/](findings/) for results and limitations.

### Guidance tracking

As of **2026-10-06**, the registry tracks official guidance for GPT-6.1 Sol, Opus 5.5, and Sonnet 5.5, while distinguishing GPT-6 Sol and 6.1 Sol API conditions and retaining older guidance as historical context. Releases do not automatically change personal instructions or reasoning effort. Registry cadence is metadata, not a scheduler.

See the dated [model guidance](sources/2026-10-01-model-guidance.md), [October 6 update](sources/2026-10-06-guidance-update.md), and [Claude model differences](sources/2026-09-29-opus-sonnet55-guidance.md). These records are date-specific, not a live compatibility guarantee.

## Feedback and development

[Open an issue](https://github.com/HoonStyle/agent-policy-radar/issues) with the plugin/host versions, request scope, expected outcome, observed difference, and a minimal example. Use synthetic or de-identified excerpts instead of private manuscripts, participant data, credentials, or complete conversations.

Feedback is not automatic authorization to edit instructions. Fix verified problems with limited changes and focused checks; keep personal preferences in user/project settings rather than adding universal rules.

```sh
python3 -m unittest discover -s tests -v
```

GitHub Actions runs Python 3.11 tests and packaging checks on macOS and Windows (`PYTHONUTF8=0/1`) for pushes, pull requests, and manual runs. CI excludes live checks requiring external sites, paid models, or sign-in. Logs are retained for 14 days.

Releases require manifest and changelog updates plus a `v<version>` tag. GitHub Actions creates the Release after CI passes for that tag. Version decisions, tag creation, and user-machine updates are not automatic; the workflow is not a separate permission policy preventing all manual bypasses.

## Repository layout

```text
.claude-plugin/              Claude Code marketplace and base plugin manifests
.agents/plugins/            Codex marketplace manifest
plugin.json                 Portable base plugin manifest
skills/agent-policy-radar/   Base audit skill
plugins/review-workflow/     Optional review skill and recording CLI
plugins/paper-research/      Optional research skill and references
plugins/ui-design-director/  Optional UI, PowerPoint, and Word design skills
scripts/                    Policy Radar CLI
tests/                      Regression tests
sources/                    Official guidance records
findings/                   Observations, verification, and limitations
recommendations/            Proposals and per-run drafts
notes/                      Decision records
```

## License

Project code and original documentation use the [MIT License](LICENSE). Referenced papers, official documentation, and third-party materials retain their respective rights; this license does not replace them.
