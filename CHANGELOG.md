# Changelog

## 0.3.0 — 2026-06-18

### Added
- `policies/anti-patterns.md` — 9 explicit failure modes to avoid (empty acknowledgements, over-formatting, over-apologizing, unnecessary questions, tool theater, engagement maximization, confidence without evidence, inventing capabilities) plus rule-creation meta-principle
- `policies/coding-discipline.md` — immutability, TDD, security defaults, minimal change, reuse-before-invention
- `evals/anti-patterns.json` — 5 regression cases protecting anti-pattern rules
- `evals/research-depth.json` — 5 regression cases protecting research-depth rules
- `README.zh-CN.md` — Chinese README
- `CHANGELOG.md` — version history
- Research-depth rules: research planning for 5+ tool calls, calibrated skepticism by topic, conflict resolution by additional search, partial-recognition trap, substantive-response obligation
- Epistemic precision rules in style policy (observed/inferred/assumed distinction)
- Pre-output self-check gate in style policy
- Evidence-narrative interleaving rule in style policy
- Unconditional read-before-write rule in preflight-checks policy
- Prose-first formatting guidance strengthened in style policy
- "Inventory before invent" principle in tools policy
- Single-question constraint reinforced in routing-examples policy
- Governance meta-principle in SYSTEM.md: rules must point to observed failures

### Changed
- `README.md` rewritten with architecture diagram, design origin, and core principles
- `harness.json` updated to register anti-patterns and coding-discipline policies (v0.3.0)
- `profiles/coding.json` now includes anti-patterns and coding-discipline cards
- `profiles/research.json` now includes anti-patterns card
- `policies/research.md` expanded with research planning, calibrated skepticism, conflict resolution, partial-recognition, substantive-response
- Eval coverage: 23 → 33 cases, 100% enforced_by

## 0.2.0 — 2026-06-18

### Added
- `policies/anti-patterns.md` — 9 explicit failure modes to avoid (empty acknowledgements, over-formatting, over-apologizing, unnecessary questions, tool theater, engagement maximization, confidence without evidence, inventing capabilities) plus rule-creation meta-principle
- `policies/coding-discipline.md` — immutability, TDD, security defaults, minimal change, reuse-before-invention
- `evals/anti-patterns.json` — 5 regression cases protecting anti-pattern rules
- `README.zh-CN.md` — Chinese README
- `CHANGELOG.md` — version history
- Epistemic precision rules in style policy (observed/inferred/assumed distinction)
- Unconditional read-before-write rule in preflight-checks policy
- Prose-first formatting guidance strengthened in style policy
- "Inventory before invent" principle in tools policy
- Single-question constraint reinforced in routing-examples policy
- Governance meta-principle in SYSTEM.md: rules must point to observed failures

### Changed
- `README.md` rewritten with architecture diagram, design origin, and core principles
- `harness.json` updated to register anti-patterns and coding-discipline policies (v0.2.0)
- `profiles/coding.json` now includes anti-patterns and coding-discipline cards
- `profiles/research.json` now includes anti-patterns card
- Eval coverage: 23 → 28 cases, 100% enforced_by

## 0.1.0 — 2026-06-17

### Added
- Core system prompt (`SYSTEM.md`) with mission, priority order, operating defaults, capability routing, tool use, file work, research, coding behavior, style, wellbeing, and completion check
- 10 policy cards: style, tools, routing-examples, preflight-checks, context-refresh, files, memory, research, verification, safety
- 3 profiles: core, coding, research
- 4 host adapters: core, codex, claude-code, ide
- Capability matrix (`capabilities.json`) with target requirements
- Done criteria (`done_criteria.json`) with 16 deterministic checks
- 5 eval files with 23 regression cases, 100% enforced_by coverage
- Zero-dependency Python CLI (`scripts/agent_harness.py`) — list, compile, doctor, install, eval, verify
- Design notes and source prompt map
