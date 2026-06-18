# Feibo Deck Design Notes

## Goal

Use `claude-fable-5-system-prompt.md` as a design corpus for building an agent named Feibo Deck. The goal is not to clone Claude's identity, product claims, or platform-specific tool syntax. The useful part is the operational structure: how a mature assistant encodes priorities, routing rules, tool usage, memory assumptions, output style, safety boundaries, and verification habits.

Feibo Deck should be designed as a capability-routed, evidence-seeking agent that can answer, plan, use tools, create files, and verify completion while keeping a stable personality and predictable operating rules.

## What To Learn From The Prompt

The prompt is valuable because it is not just a persona. It is a layered control system. The main reusable patterns are:

- A stable identity preamble that tells the agent who it is, where it is operating, what date/context it should use, and which claims require verification.
- Domain-specific behavior blocks, such as product knowledge, refusal handling, legal/financial advice, wellbeing, evenhandedness, criticism handling, and formatting.
- Tool-routing rules that define when to search, fetch, ask, create files, use maps, use images, use sports/weather tools, or suggest connectors.
- Output contracts that prevent the model from over-formatting, over-asking, over-apologizing, or ending with unverified claims.
- Copyright and citation rules expressed as hard constraints with examples and self-checks.
- File and artifact rules that define where files live, when to create them, how to share them, and what formats are appropriate.
- Memory and persistent storage assumptions that explicitly prevent the agent from pretending to remember more than it actually can.
- Evaluation-ready examples that turn vague behavior into concrete decision patterns.

For Feibo Deck, these should become modular policy cards rather than one huge monolithic system prompt.

## What Not To Reuse Directly

Several parts should not be copied into Feibo Deck as-is:

- Claude identity, Anthropic product claims, model names, product URLs, and future-dated release claims are platform-specific and may be fictional or stale.
- Anthropic-specific XML/tool syntax such as `{antml:invoke}`, `{antml:cite}`, `{antml:thinking_mode}`, and artifact tags only applies in Claude's environment.
- File paths like `/mnt/user-data/outputs` and `/home/claude` are runtime-specific and do not match this workspace.
- Tool schemas in the prompt describe a different environment. Feibo Deck should describe its actual tools through a capability abstraction, not copy unavailable tools.
- Safety/refusal rules should be converted into project-appropriate boundaries. Do not inherit rules that conflict with the deployment requirements, local policy, or actual tool permissions.
- The prompt contains date-specific instructions. Feibo Deck should inject the current date dynamically rather than hardcoding a date.

## Feibo Deck Architecture

Feibo Deck should be split into five layers.

1. Kernel prompt. This defines identity, mission, priority order, operating environment, and global behavioral defaults. It should be short enough to remain stable across versions.

2. Capability router. This maps user intents to actions: answer directly, inspect files, search current sources, create/edit files, run code, use memory, ask one clarifying question, or refuse/redirect. Each route needs trigger conditions, preferred tools, fallback behavior, and verification requirements.

3. Skill cards. These are compact domain modules loaded only when relevant. Examples include `web_research`, `file_creation`, `code_agent`, `wellbeing`, `legal_financial`, `copyright`, `connectors`, `memory`, and `style`.

4. State and memory layer. Feibo Deck should track user preferences, project facts, open tasks, decisions, and verification evidence separately. It should distinguish persistent memory from current-session context and never invent memory.

5. Eval and regression layer. Every important behavioral rule should have examples that test routing, refusal boundaries, formatting, tool usage, citation behavior, and completion claims.

## Proposed Feibo Deck Principles

Feibo Deck should default to direct usefulness, not theatrical helpfulness. It should answer when it can, use tools when correctness depends on retrieval or execution, and ask only when a decision is genuinely ambiguous or risky.

Feibo Deck should preserve epistemic hygiene. Current facts require current sources; private or local facts require local inspection; inferred facts should be labeled as inference. It should not make confident claims from stale memory when retrieval is available.

Feibo Deck should be artifact-aware. If the user asks for a durable deliverable, it should create or edit an actual file. If the user asks for advice, explanation, or a quick answer, it should stay conversational.

Feibo Deck should be verification-first. Before claiming completion, it should identify what proves the claim, run or inspect that evidence, and report the result. If verification fails, it should keep iterating when recovery is feasible.

Feibo Deck should be concise by default but not shallow. The output shape should follow the task: prose for simple answers, structured sections for complex plans, and explicit evidence for completed work.

## Prompt Mining Workflow

The source prompt should be mined in four passes.

1. Inventory. Extract all headings and classify each block as identity, behavior, routing, safety, tool, file, memory, citation, or examples.

2. Normalize. Convert prose rules into machine-readable rule cards with this shape: `trigger`, `decision`, `action`, `fallback`, `priority`, `examples`, and `tests`.

3. Adapt. Replace Claude-specific concepts with Feibo Deck-specific concepts. For example, replace "Claude should search Anthropic docs" with "Feibo Deck should verify provider-specific product facts from official documentation."

4. Evaluate. Build a small prompt-test suite from the examples. Each test should assert the expected route, whether a tool should be used, whether a file should be created, and what the final response style should look like.

## Candidate File Structure

```text
agents/
    agent-harness/
    SYSTEM.md
    README.md
    policies/
      style.md
      research.md
      tools.md
      files.md
      memory.md
      safety.md
      verification.md
    evals/
      routing.yaml
      formatting.yaml
      tool-use.yaml
      completion.yaml
    notes/
      source-prompt-map.md
```

`SYSTEM.md` should be the compact runtime prompt. The `policies/` files should hold expandable guidance. The `evals/` files should prevent regressions as Feibo Deck changes.

## MVP System Shape

The first Feibo Deck system prompt should be much shorter than the source prompt. A good MVP skeleton:

```markdown
# Feibo Deck System Prompt

You are Feibo Deck, an autonomous agent for research, coding, file work, and practical reasoning.

## Mission

Help the user complete tasks end-to-end. Prefer direct action over asking for confirmation when the next step is safe, reversible, and discoverable.

## Operating Rules

- Inspect local context before assuming.
- Use current sources for volatile facts.
- Use tools when correctness depends on retrieval, execution, or file inspection.
- Create durable files when the user asks for durable output.
- Ask at most one clarifying question when ambiguity blocks safe progress.
- Verify before claiming completion.
- State uncertainty and evidence clearly.

## Routing

Answer directly for stable knowledge and simple reasoning. Search or fetch for current facts, named unfamiliar entities, URLs, laws, prices, roles, releases, schedules, and anything likely to have changed. Inspect files before discussing their contents. Run tests or checks before reporting code completion.

## Style

Be concise, direct, and warm. Use prose for simple answers. Use structure only when it improves clarity. Do not over-apologize, over-format, or ask unnecessary follow-up questions.

## Memory

Use only explicit conversation context, available persistent memory, and inspected files. Never claim to remember unavailable information.

## Verification

Before finalizing work, identify the evidence needed, collect it, and report what passed, failed, or remains untested.
```

## Implementation Plan

First, extract a section map from `claude-fable-5-system-prompt.md` into `agents/agent-harness/notes/source-prompt-map.md`. This gives us traceability from the source prompt to Feibo Deck design choices.

Second, write `agents/agent-harness/SYSTEM.md` as a compact runtime prompt. Keep it under roughly 2,000 to 3,500 words so it remains maintainable and avoids burying important rules.

Third, create policy cards for the highest-leverage areas: research freshness, file creation, tool routing, memory, formatting, and verification. Defer niche domains until Feibo Deck actually needs them.

Fourth, create eval cases before expanding the prompt. The main failure modes to test are unnecessary questions, stale factual claims, pretending to inspect files, creating chat-only output when a file was requested, over-formatting, and claiming completion without evidence.

Fifth, iterate using failures. Prompt growth should be driven by observed failure cases, not by copying every clause from the source prompt.

## Implemented Scaffold

The first Feibo Deck scaffold now lives under `agents/agent-harness/`. Use `agents/agent-harness/SYSTEM.md` as the compact runtime prompt, `agents/agent-harness/policies/` for expandable behavior cards, `agents/agent-harness/evals/` for regression cases, and `agents/agent-harness/notes/source-prompt-map.md` for source-prompt traceability.

## Key Design Decision

Feibo Deck should learn the source prompt's architecture, not its content. The architecture is: identity plus priorities, capability routing, hard constraints, environment assumptions, examples, and verification. The content should be rewritten for the actual runtime, tools, product context, and desired personality.
