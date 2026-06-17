# Claude Code Adapter

Use this compiled prompt from Claude Code project memory or command surfaces. The adapter is intentionally conservative: it does not assume a specific Claude Code version or unavailable tool syntax.

## Claude Code Integration Contract

- Put durable project-level behavior in `CLAUDE.md` when the project uses Claude Code memory.
- Put repeatable workflows in `.claude/commands/` when slash-command style invocation is desired.
- Keep tool names and exact invocation syntax host-provided; do not embed unavailable tool schemas in the compiled prompt.
- Use the harness as a behavior contract around repository inspection, edits, verification, and final reporting.

## Recommended Install Targets

- `CLAUDE.md` for project-level Claude Code memory.
- `.claude/commands/agent-harness.md` as an invocation command that points to the compiled harness.
- `.agent-harness/build/claude-code.md` as the generated artifact for review before installation.

## Usage Pattern

Compile the prompt for Claude Code, review it, then install it into the project memory or command file according to the team's Claude Code conventions.

