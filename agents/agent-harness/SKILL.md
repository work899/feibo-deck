---
name: agent-harness
description: Build, audit, compile, and install Feibo Deck profiles for Codex, Claude Code, and IDE assistants. Use when the user asks to create an agent harness, compile prompts, add policy cards, run harness evals, or connect an agent profile to coding assistants.
---

# Feibo Deck Skill

Feibo Deck is broader than a skill. This skill is an entry point for operating the harness from Codex.

## Use Cases

- Compile `SYSTEM.md` plus selected policy cards into a host-specific prompt.
- Install compiled prompts into Codex, Claude Code, or IDE instruction surfaces.
- Audit an existing prompt against Feibo Deck policies.
- Add or revise policy cards.
- Run lightweight harness eval validation.

## Workflow

1. Inspect `agents/agent-harness/harness.json`.
2. Choose a profile: `core`, `coding`, or `research`.
3. Choose a target: `core`, `codex`, `claude-code`, or `ide`.
4. Compile with `python scripts/agent_harness.py compile --profile <profile> --target <target>`.
5. Review the generated prompt under `.agent-harness/build/`.
6. Install only when the user asked to write host integration files.
7. Run `python scripts/agent_harness.py eval` after changing harness files.

## Commands

```powershell
python .\scripts\agent_harness.py list
python .\scripts\agent_harness.py compile --profile coding --target codex
python .\scripts\agent_harness.py install --profile coding --target codex --project .
python .\scripts\agent_harness.py eval
```

## Guardrails

Do not paste the original Claude Fable 5 source prompt into runtime prompts. Retain mechanisms, not platform-specific identity, product claims, paths, dates, or tool syntax.

Do not overwrite project instruction files without checking whether they already exist. When an install target exists, the CLI writes a sibling `.agent-harness.md` file instead of replacing it.

