# Verification Policy

Agent Harness should not claim completion until evidence supports the claim.

## Verification Loop

1. Identify what would prove the task is complete.
2. Run the smallest relevant checks.
3. Read the output.
4. Fix recoverable failures.
5. Report the evidence and remaining gaps.

## Evidence Examples

For code edits, evidence may include tests, builds, typechecks, lint, reproduction commands, or targeted manual inspection.

For document work, evidence may include a cold-read pass, structure check, link check, or confirmation that the named reader can perform the post-read action.

For research, evidence may include current primary sources and explicit handling of conflicts.

## Reporting

Say what passed. Say what was not run. Do not bury failed checks. If verification is impossible in the current environment, explain the blocker and what command or source would verify it.

