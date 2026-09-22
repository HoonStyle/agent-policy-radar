# Model Release Prompt/Instruction Guidance Check — 2026-09-22

## Question

When Claude Code or Codex/OpenAI releases new models or major model updates, do they also publish updated guidance for existing project instructions or prompt guidelines?

## Checked sources

### Anthropic / Claude Code

- Claude Code memory docs: https://code.claude.com/docs/en/memory.md
- Claude Code settings docs: https://code.claude.com/docs/en/settings.md
- Anthropic prompt engineering docs: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview

Relevant observed facts:

- Claude Code documents how `CLAUDE.md` and `AGENTS.md` are loaded and managed.
- Claude Code states that `CLAUDE.md`/`AGENTS.md` content is context/behavior guidance, not a hard enforcement layer.
- The memory docs explicitly recommend shorter, specific instructions for better adherence and warn that files over 200 lines consume context and may reduce adherence.
- Claude Code has migration/import support for other agents' instruction files and version-specific behavior such as direct `AGENTS.md` support.
- Claude Code settings docs state that Claude Code's system prompt is not published; standing instructions should use `CLAUDE.md` or `--append-system-prompt`.

Interpretation:

- Anthropic provides living docs for instruction files and prompt engineering, and Claude Code feature changes can update instruction-file guidance.
- This is not the same as a guaranteed, per-new-model checklist for rewriting existing `CLAUDE.md` files.

### OpenAI / Codex

- Codex CLI docs: https://developers.openai.com/codex/cli.md
- OpenAI prompt engineering docs: https://developers.openai.com/api/docs/guides/prompt-engineering.md
- GPT-5 prompting guide: https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide.md

Relevant observed facts:

- Codex CLI documents `AGENTS.md`, model/reasoning selection, permissions, scripts/CI, skills/plugins, and `/init` for creating instruction files.
- OpenAI's general prompt engineering docs say different model types may need different prompting and recommend tests/evals when changing or upgrading model versions.
- OpenAI has published model-specific prompting guides, e.g. the GPT-5 prompting guide.
- The GPT-5 guide explicitly says some prompt sections effective with earlier models needed tuning for GPT-5; overly strong thoroughness instructions could become counterproductive.
- The GPT-5 guide recommends reviewing contradictory or poorly constructed prompts because stronger instruction following can make prompt defects more visible.

Interpretation:

- OpenAI does publish model-specific prompting guidance for major models and maintains Codex/agent docs.
- The guidance is not an automatic migration of a repo's `AGENTS.md`; local owners still need to review standing instructions against the new model/harness behavior.

## Operational conclusion

Providers do publish guidance, but in two different layers:

1. **Harness/instruction-file docs**: how Claude Code or Codex loads and prioritizes `CLAUDE.md`/`AGENTS.md`, settings, permissions, model selection, etc.
2. **Model-specific prompting docs**: how a new model family behaves and what prompt patterns may need tuning.

There does not appear to be a reliable guarantee that every new model release ships with a complete local-instruction migration guide. Treat official guidance as an input to a local review, not as a replacement for checking existing project prompts.

## Suggested policy for this repo

When a major Claude/Codex model or harness version changes:

- Check official model-specific prompting guide/release notes if available.
- Check Claude Code/Codex CLI docs for instruction-file loading changes.
- Review local `CLAUDE.md`/`AGENTS.md` for obsolete workarounds, duplicated imports, excessive context, and model-specific oversteering.
- Record facts in `sources/` and local operational judgments in `findings/` before proposing changes to other repos.
