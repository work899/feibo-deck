# Codex Adapter

Use this compiled prompt from a Codex project instruction surface such as `AGENTS.md`, or from a Codex skill that loads the compiled prompt before acting.

## Codex Integration Contract

- Inspect repository files before editing or explaining project-specific behavior.
- Use `apply_patch` for manual file edits when available.
- Preserve unrelated user changes.
- Run relevant tests or checks before claiming completion.
- Keep final reports concise and include verification evidence.
- Treat `AGENTS.md` and nested project instructions as higher-priority local operating contracts.

## Recommended Install Targets

- `AGENTS.md` for project-level Codex behavior.
- `.codex/skills/agent-harness/SKILL.md` when used as an invocable Codex skill.
- `.agent-harness/build/codex.md` as the generated artifact for review before installation.

## Usage Pattern

Compile the prompt for Codex, review it, then install or paste the generated content into the project-level Codex instruction surface.

