# IDE Adapter

Use this compiled prompt with IDE assistants that support project instructions, prompt files, rules, or copilot-style guidance.

## IDE Integration Contract

- Keep instructions focused on local project behavior, not host-specific tool syntax.
- Tell the IDE agent to inspect files before making project claims.
- Require verification evidence before completion claims.
- Prefer small, reversible edits.
- Do not overwrite unrelated user work.

## Recommended Install Targets

- `.github/copilot-instructions.md` for GitHub Copilot-style project instructions.
- `.cursor/rules/agent-harness.mdc` for Cursor-style project rules.
- `.windsurfrules` for Windsurf-style project rules.
- `.vscode/agent-harness.prompt.md` as a generic prompt artifact for IDEs that support prompt files.
- `.agent-harness/build/ide.md` as the generated artifact for review before installation.

## Usage Pattern

Compile the prompt for IDE usage, review it, then install to the instruction file supported by the user's editor.

