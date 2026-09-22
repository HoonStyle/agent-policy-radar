# Service References — 2026-09-22

This file records starting references for model/harness policy review. Summaries are intentionally short; read the current docs before making concrete policy changes.

## Anthropic / Claude

- Claude Code memory / `CLAUDE.md` management  
  https://code.claude.com/docs/en/memory
- Claude Code settings / standing instructions  
  https://code.claude.com/docs/en/settings
- Anthropic prompt engineering overview  
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- Claude prompting best practices / prompt improver  
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Testing and eval guidance  
  https://platform.claude.com/docs/en/test-and-evaluate/develop-tests

Initial note: Claude provides memory/settings/prompt guidance, but local `CLAUDE.md` hygiene remains project-specific.

## OpenAI / Codex

- OpenAI prompt engineering guide  
  https://developers.openai.com/api/docs/guides/prompt-engineering
- OpenAI evals  
  https://developers.openai.com/api/docs/guides/evals
- Codex CLI documentation, including `AGENTS.md`, config, MCP  
  https://learn.chatgpt.com/docs/codex/cli
- Codex config reference  
  https://github.com/openai/codex/blob/main/docs/config.md

Initial note: Codex documents agent configuration and eval options, but does not automatically clean up local project instructions.

## Google / Gemini

- Gemini / Vertex prompt design  
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/prompts/introduction-prompt-design
- Google prompt optimizer  
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/prompts/prompt-optimizer

Initial note: prompt optimization exists, but should not be treated as automatic approval to rewrite local policies.

## MCP / Tool Harness Layer

- MCP prompts specification  
  https://modelcontextprotocol.io/specification/2026-07-28/server/prompts
- MCP tools specification  
  https://modelcontextprotocol.io/specification/2026-07-28/server/tools

Initial note: MCP defines prompts/tools capabilities, while the local decision about how long or opinionated server instructions should be is operational policy.
