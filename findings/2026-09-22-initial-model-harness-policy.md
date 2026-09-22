# Initial Model + Harness Policy Finding — 2026-09-22

## Finding

Modern models and coding-agent harnesses often handle simple routing, tool choice, and task decomposition better than older setups. Long standing instructions that were once useful can become counterproductive by consuming context or encouraging unnecessary tool calls.

## Scope

This is an operational judgment for the user's current multi-harness environment, not a universal benchmark result.

Relevant environment:

- Claude Code
- Codex CLI/App
- Pi
- Telegram bridge
- MCP servers
- custom skills
- multiple repositories with `AGENTS.md` / `CLAUDE.md`
- separate owner Mac and spouse Windows workflows

## Implications

- Keep MCP server instructions short and profile-specific.
- Do not encode model-call ratios as standing behavior unless there is current evidence they improve outcomes.
- Prefer optional external review for explicit requests or high-impact final checks.
- Avoid classifying unrelated work just to produce metrics.
- Separate environment-specific instructions, e.g. owner Mac vs spouse Windows.

## Example Trigger

`local-ai-connector` mistakenly had spouse Office/Paper routing applied to owner Mac. The correction was to split routing by profile:

- spouse: Office/Paper distinction remains.
- owner Mac: no Paper/Office classification; occasional cross-model review only.

## Confidence

Medium. Based on recent operational experience and current public documentation patterns. Should be revisited when major model or harness versions change.
