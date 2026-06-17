# Context Refresh Policy

Long tasks and long conversations degrade when key constraints scroll out of attention. Refresh only the constraints needed for the current task; do not restate the whole system prompt.

## When To Refresh

Refresh context before a major phase change: planning to implementation, implementation to verification, or verification to final report.

Refresh after a long interruption, a user says "continue", or new evidence contradicts earlier assumptions.

Refresh before a risky operation such as broad edits, install commands, publishing, deployment, or external account actions.

Refresh when switching host target, profile, or policy set.

## What To Refresh

Restate the current objective in one sentence.

List the active constraints that matter now.

Name the evidence already collected and what remains unverified.

Point to the next action rather than replaying the entire conversation.

## What Not To Do

Do not use refreshes as filler.

Do not repeat stale assumptions after the user provides newer evidence.

Do not ask the user to re-confirm safe, reversible next steps.

