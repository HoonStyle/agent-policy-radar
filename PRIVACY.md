# Privacy Policy

Agent Policy Radar is a local skill/plugin and CLI. It does not run a hosted service operated by this repository.

## Data processed

When you run the CLI, it may read local instruction files such as `AGENTS.md`, `CLAUDE.md`, skill `SKILL.md` files, and MCP-related configuration paths that you configured or that match the default registry.

It may fetch public documentation URLs listed in `data/source_registry.json` to detect official guidance changes.

## Data storage

Reports are written locally inside the checkout under `reports/`, `sources/`, `findings/`, and `recommendations/`.

## Data sharing

This project does not automatically upload local instruction files, reports, secrets, or repository content to a service owned by this project. If your agent harness, plugin marketplace, or Git remote syncs generated files, that behavior is controlled by that external product or by your own commands.

## Secrets

Do not place credentials, API keys, or private tokens in instruction files or generated reports. The scanner does not automatically redact secrets. Reports can contain source excerpts and local paths; inspect them before sharing or committing them.

## Contact

Repository: https://github.com/HoonStyle/agent-policy-radar
