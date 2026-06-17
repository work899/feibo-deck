# Source Prompt Map

This map records how `claude-fable-5-system-prompt.md` informs Agent Harness. It is a design trace, not a license to copy platform-specific content.

## Source Sections

- `claude_behavior/product_information`: teaches product-fact freshness and official-source verification. Agent Harness adapts this into `policies/research.md`; Claude/Anthropic product claims are not inherited.
- `claude_behavior/refusal_handling`: teaches concise boundaries and safe redirection. Agent Harness adapts this into `policies/safety.md`.
- `legal_and_financial_advice`: teaches decision-support framing for regulated domains. Agent Harness adapts this into `policies/safety.md` and `policies/research.md`.
- `tone_and_formatting/lists_and_bullets`: teaches minimal formatting and prose-first answers. Agent Harness adapts this into `policies/style.md`.
- `user_wellbeing`: teaches non-diagnostic, non-amplifying support patterns. Agent Harness adapts this into `policies/safety.md`.
- `anthropic_reminders`: teaches how to handle runtime reminders. Agent Harness keeps the concept but does not copy Anthropic-specific reminder names.
- `evenhandedness`: teaches fair presentation of contested positions. Agent Harness keeps this as a style and safety principle.
- `responding_to_mistakes_and_criticism`: teaches accountable correction without self-abasement. Agent Harness adapts this into `policies/style.md`.
- `knowledge_cutoff`: teaches dynamic recency handling. Agent Harness uses dynamic current date injection rather than hardcoded dates.
- `memory_system`: teaches explicit memory availability. Agent Harness adapts this into `policies/memory.md`.
- `persistent_storage_for_artifacts`: teaches persistent artifact state constraints. Agent Harness does not inherit the `window.storage` API unless the runtime supports it.
- `mcp_app_suggestions`: teaches connector routing and opt-in for external services. Agent Harness adapts the concept into `policies/tools.md`.
- `computer_use`: teaches file creation, file handling, package management, and artifacts. Agent Harness adapts this into `policies/files.md` and `policies/tools.md`.
- `search_instructions`: teaches freshness, source quality, citation, and copyright discipline. Agent Harness adapts this into `policies/research.md`.
- `using_image_search_tool`: teaches modality routing. Agent Harness should add an image policy only when its runtime supports image search.
- `Tool Definitions`: teaches that tool schemas belong to runtime context. Agent Harness does not copy unavailable tool schemas into `SYSTEM.md`.
- `Identity Preamble`: teaches that identity and date belong near the top. Agent Harness keeps identity compact and injects date dynamically.
- `anthropic_api_in_artifacts`: teaches API-powered artifact constraints. Agent Harness should create a separate policy only if it supports agent-powered artifacts.
- `citation_instructions`: teaches source attribution rules. Agent Harness adapts this into `policies/research.md`.
- `available_skills`: teaches skill discovery before specialized work. Agent Harness adapts this into `policies/tools.md`.
- `network_configuration` and `filesystem_configuration`: teach explicit environment assumptions. Agent Harness should keep environment details outside static prompt when possible.

## Extraction Principle

Retain mechanisms, not claims. The reusable mechanisms are routing, verification, memory honesty, source freshness, output contracts, and examples. The non-reusable material is identity, product claims, hardcoded dates, platform paths, tool syntax, and unsupported APIs.

