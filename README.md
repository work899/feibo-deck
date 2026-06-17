# Agent Harness Kit

Agent Harness Kit is a portable governance layer for AI agents. It turns a large, monolithic system prompt into a maintainable set of prompts, policy cards, profiles, adapters, and regression checks that can be used across Codex, Claude Code, and IDE assistants.

The project started from a Claude-style system prompt as a design corpus. The goal is not to clone that assistant. The goal is to extract the durable engineering pattern: agents should inspect before assuming, use current sources when facts may have changed, create real files when durable output is requested, verify before claiming completion, and report evidence instead of performing confidence.

## What Problem It Solves

AI coding and research agents often fail in predictable ways. They answer from stale memory, summarize files they never opened, say tests passed when nothing ran, produce chat text when the user asked for a reusable file, or behave differently across tools because every host has a separate prompt.

Agent Harness addresses that by making agent behavior modular and portable. One harness can compile host-specific instructions for different tools while preserving the same operating discipline.

## What It Provides

- A compact core system prompt that defines the agent's mission, routing, tool use, file behavior, style, and completion standard.
- Policy cards for research, files, tools, memory, safety, style, and verification.
- Profiles that select policy cards for different modes such as general use, coding, and research.
- Host adapters for Codex, Claude Code, and IDE assistants.
- A target capability matrix that checks whether a profile can safely run on a host.
- Declarative done criteria that verify the kit is ready without asking an LLM to judge it.
- A no-dependency Python CLI for compiling, installing, and validating the harness.
- Lightweight eval files that catch regressions in routing, formatting, tool use, and completion claims.

## Requirements

Use Python 3.10 or newer. The CLI uses only the Python standard library.

No package installation is required.

## Quick Start

List available profiles and targets:

```powershell
python .\scripts\agent_harness.py list
```

Compile a coding profile for Codex:

```powershell
python .\scripts\agent_harness.py compile --profile coding --target codex
```

Compile a coding profile for Claude Code:

```powershell
python .\scripts\agent_harness.py compile --profile coding --target claude-code
```

Compile a coding profile for IDE assistants:

```powershell
python .\scripts\agent_harness.py compile --profile coding --target ide
```

Run the harness validation checks:

```powershell
python .\scripts\agent_harness.py eval
```

Check whether a profile is compatible with a target host:

```powershell
python .\scripts\agent_harness.py doctor --profile coding --target codex
```

Run the project-level completion checks:

```powershell
python .\scripts\agent_harness.py verify
```

Compiled prompts are written under the local build directory. Generated build outputs are intentionally ignored by git.

## Install Into A Project

Install for Codex:

```powershell
python .\scripts\agent_harness.py install --profile coding --target codex --project .
```

Install for Claude Code:

```powershell
python .\scripts\agent_harness.py install --profile coding --target claude-code --project .
```

Install for IDE assistants:

```powershell
python .\scripts\agent_harness.py install --profile coding --target ide --project .
```

The installer is conservative. If a target instruction file already exists, it writes a sibling Agent Harness file instead of overwriting the existing file.

## Concepts

The core prompt is the kernel. It should stay short and stable. It defines default behavior that should apply in any host.

Policy cards are behavior modules. They hold detailed guidance for domains such as research freshness, file creation, memory honesty, tool discipline, and completion verification.

Profiles choose which policy cards to load. A coding profile can prioritize repository inspection and test evidence. A research profile can prioritize source quality and freshness-sensitive claims.

Adapters translate the same harness into a host-specific instruction surface. The Codex adapter emphasizes repository instructions and verification. The Claude Code adapter targets project memory and command files. The IDE adapter targets project-level assistant rules.

Capabilities describe what each target host supports. Profiles declare requirements, and `doctor` fails early when a profile asks for behavior the target cannot provide.

Done criteria are deterministic checks for the kit itself. They verify files, compilation, eval structure, and forbidden-text regressions without relying on model judgment.

Evals are lightweight regression cases. They are not a full model evaluation framework yet; they validate that the harness files have the expected structure and document the behavior that future tests should enforce.

## Common Workflows

To create a new behavior rule, add or edit a policy card, include it in the relevant profile, then add an eval case that captures the failure mode the rule is meant to prevent.

To create a new agent mode, add a profile that selects an appropriate policy-card set. Then compile it for the target host and inspect the generated prompt.

To support a new host, add an adapter that describes how the host should consume the compiled prompt. Then register the adapter in the manifest.

To define target requirements, update the capability matrix and add `requires` entries to the relevant profile. Use `doctor` to catch mismatches before installing.

To tighten release readiness, add a deterministic check to the done criteria file and run `verify`.

To improve prompt quality, start from observed failures. Do not grow the core prompt just because a rule sounds useful. Prefer a focused policy card and a regression case.

## Repository Layout

```text
agents/
  agent-harness/
    SYSTEM.md
    SKILL.md
    capabilities.json
    done_criteria.json
    harness.json
    adapters/
    evals/
    notes/
    policies/
    profiles/
scripts/
  agent_harness.py
```

The original source prompt is kept as a design corpus. It should not be copied into compiled runtime prompts.

## Safety And Maintenance Notes

Agent Harness is a prompt and instruction compiler, not a sandbox. The host still controls available tools, permissions, network access, and memory. Host instructions remain higher priority than compiled harness text.

Keep generated outputs out of source control unless there is a reason to snapshot a compiled prompt for review. Source files, policy cards, profiles, adapters, and evals are the maintainable artifacts.

When changing behavior, run:

```powershell
python .\scripts\agent_harness.py eval
python .\scripts\agent_harness.py verify
python -m py_compile .\scripts\agent_harness.py
```

If you compile prompts during development, remove transient Python cache files before committing. The project gitignore already excludes common cache and build outputs.
