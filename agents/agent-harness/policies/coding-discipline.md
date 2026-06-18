# Coding Discipline Policy

Feibo Deck applies these constraints when implementing, reviewing, or debugging code.

## Read Before Write

Read every file about to be modified. Understand its patterns, imports, naming, and structure before changing anything. Match the existing style rather than introducing a new one.

## Immutability

Prefer creating new objects over mutating existing ones. Return new state rather than modifying arguments in place. This applies to data transformations, state updates, and configuration changes. Mutation is acceptable only when the host language or framework requires it and the scope is local.

## Small, Focused Units

Keep functions single-purpose and under 50 lines. Keep files under 800 lines and focused on one concept. Extract when a file grows or a function serves two masters. Organize by feature or domain, not by type.

## Input Validation

Validate at system boundaries: user input, external API responses, file contents, environment variables. Trust internal code that has already been validated upstream. Do not scatter defensive checks through every layer.

## Error Handling

Handle errors at the boundary where recovery is possible. Provide context about what failed and why. Do not swallow errors silently. Do not add error handling for scenarios that cannot occur.

## Security Defaults

Before committing code:

- No hardcoded secrets (keys, tokens, passwords) — use environment variables
- Parameterized queries for all database access
- Sanitized output to prevent XSS
- Validated and bounded user inputs
- No sensitive data in error messages or logs

## Test-Driven Verification

For new features and bug fixes:

1. Extract test scenarios from requirements before writing tests
2. Each requirement maps to at least one test case
3. Cover the happy path, edge cases (boundaries, empty, max), error handling (invalid inputs, permission failures), and state transitions
4. Run tests and confirm they pass before declaring done

A single test file or a single happy-path test is not sufficient. Enumerate scenarios explicitly.

## Minimal Change

Implement what the task requires. Do not refactor adjacent code, add speculative features, introduce abstractions for hypothetical futures, or clean up unrelated style issues. A bug fix is a bug fix. A feature is a feature. Keep the diff reviewable.

## Reuse Before Invention

Search the existing codebase for utilities, patterns, and helpers before creating new ones. If a similar function exists, extend or reuse it. New dependencies require justification.
