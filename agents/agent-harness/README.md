# Feibo Deck

Feibo Deck is a portable governance layer for AI coding and knowledge-work agents. It turns lessons from the Claude Fable 5 source prompt into a maintainable kit: a compact system prompt, policy cards, profiles, host adapters, eval cases, and a small compiler/installer CLI.

It is not just a skill. The skill is one entry point. The harness itself can compile prompts for Codex, Claude Code, and IDE assistants.

## Reader

This documentation is for maintainers who need to modify Feibo Deck behavior, add a policy card, define a new profile, or install the compiled prompt into a coding assistant.

## Post-Read Action

After reading this directory, a maintainer should be able to compile a host-specific prompt, install it into a project, and add eval coverage for changed behavior.

## Structure

- `SYSTEM.md`: compact host-neutral runtime prompt.
- `harness.json`: manifest for profiles, adapters, and policy cards.
- `capabilities.json`: target capability matrix used by `doctor`.
- `done_criteria.json`: deterministic project-readiness checks used by `verify`.
- `profiles/`: policy selections for `core`, `coding`, and `research`.
- `adapters/`: host-specific wrappers for `core`, `codex`, `claude-code`, and `ide`.
- `policies/`: expandable behavior cards for research, files, tools, memory, style, safety, routing examples, preflight checks, context refresh, and verification.
- `evals/`: lightweight regression cases for routing, formatting, tool use, and completion.
- `SKILL.md`: Codex skill entry point for operating the harness.
- `notes/source-prompt-map.md`: traceability from source prompt sections to Feibo Deck modules.

## CLI

Run from the repository root:

```powershell
python .\scripts\agent_harness.py list
python .\scripts\agent_harness.py compile --profile coding --target codex
python .\scripts\agent_harness.py compile --profile coding --target claude-code
python .\scripts\agent_harness.py compile --profile research --target ide
python .\scripts\agent_harness.py eval
python .\scripts\agent_harness.py doctor --profile coding --target codex
python .\scripts\agent_harness.py verify
```

Compiled prompts are written to `.agent-harness/build/` by default.

## Installing Into Hosts

Codex:

```powershell
python .\scripts\agent_harness.py install --profile coding --target codex --project .
```

Claude Code:

```powershell
python .\scripts\agent_harness.py install --profile coding --target claude-code --project .
```

IDE assistants:

```powershell
python .\scripts\agent_harness.py install --profile coding --target ide --project .
```

The installer avoids overwriting existing instruction files. If a target file already exists, it writes a sibling file with `.agent-harness` in the name.

## Design Rule

Keep `SYSTEM.md` compact. Put detailed domain behavior in policy cards and load those cards through profiles. Do not copy long platform-specific prompts into runtime prompts.

## Maintenance Workflow

Change behavior by starting with the failure mode. Add or update an eval, adjust the smallest relevant prompt/policy/profile, compile the affected target, then run `python .\scripts\agent_harness.py eval` and `python .\scripts\agent_harness.py verify`.

If a profile starts depending on a host feature, add that feature to `capabilities.json` and list it in the profile's `requires` array. `doctor` should fail before install when the target does not satisfy the profile.

Small prompt lessons should usually become examples or preflight checks, not core prompt text. Use `routing-examples.md` for "request -> route" examples, `preflight-checks.md` for before-answer/before-complete checklists, and `context-refresh.md` for long-task continuation behavior.
