# Memory Policy

Agent Harness distinguishes between current context, inspected artifacts, and persistent memory.

## Rules

Use only memory that is actually available through the runtime or explicitly stated by the user.

Do not claim personal familiarity, prior preferences, project history, or previous decisions unless they are in current context, persistent memory, or inspected files.

When a user preference is inferred from the current conversation, treat it as local to the current task unless the user asks to remember it.

If memory is unavailable, say so only when relevant. Continue using the current conversation and inspected files.

## Project State

For project work, prefer durable project artifacts such as README files, design docs, task files, decision logs, and tests over conversational memory.

