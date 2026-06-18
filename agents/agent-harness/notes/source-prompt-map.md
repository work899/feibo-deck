# Source Prompt Map

This map records how `claude-fable-5-system-prompt.md` informs Feibo Deck. It is a design trace, not a license to copy platform-specific content.

## Source Sections

- `claude_behavior/product_information`: teaches product-fact freshness and official-source verification. Feibo Deck adapts this into `policies/research.md`; Claude/Anthropic product claims are not inherited.
- `claude_behavior/refusal_handling`: teaches concise boundaries and safe redirection. Feibo Deck adapts this into `policies/safety.md`.
- `legal_and_financial_advice`: teaches decision-support framing for regulated domains. Feibo Deck adapts this into `policies/safety.md` and `policies/research.md`.
- `tone_and_formatting/lists_and_bullets`: teaches minimal formatting and prose-first answers. Feibo Deck adapts this into `policies/style.md`.
- `user_wellbeing`: teaches non-diagnostic, non-amplifying support patterns. Feibo Deck adapts this into `policies/safety.md`.
- `anthropic_reminders`: teaches how to handle runtime reminders. Feibo Deck keeps the concept but does not copy Anthropic-specific reminder names.
- `evenhandedness`: teaches fair presentation of contested positions. Feibo Deck keeps this as a style and safety principle.
- `responding_to_mistakes_and_criticism`: teaches accountable correction without self-abasement. Feibo Deck adapts this into `policies/style.md`.
- `knowledge_cutoff`: teaches dynamic recency handling. Feibo Deck uses dynamic current date injection rather than hardcoded dates.
- `memory_system`: teaches explicit memory availability. Feibo Deck adapts this into `policies/memory.md`.
- `persistent_storage_for_artifacts`: teaches persistent artifact state constraints. Feibo Deck does not inherit the `window.storage` API unless the runtime supports it.
- `mcp_app_suggestions`: teaches connector routing and opt-in for external services. Feibo Deck adapts the concept into `policies/tools.md`.
- `computer_use`: teaches file creation, file handling, package management, and artifacts. Feibo Deck adapts this into `policies/files.md` and `policies/tools.md`.
- `search_instructions`: teaches freshness, source quality, citation, and copyright discipline. Feibo Deck adapts this into `policies/research.md`.
- Search and file-decision examples teach concrete routing behavior. Feibo Deck adapts these into `policies/routing-examples.md` and `evals/routing-details.yaml`.
- Output self-checks, copyright checks, and completion checks teach pre-response discipline. Feibo Deck adapts these into `policies/preflight-checks.md`.
- Long conversation reminders teach lightweight context refresh. Feibo Deck adapts this into `policies/context-refresh.md`.
- `using_image_search_tool`: teaches modality routing. Feibo Deck should add an image policy only when its runtime supports image search.
- `Tool Definitions`: teaches that tool schemas belong to runtime context. Feibo Deck does not copy unavailable tool schemas into `SYSTEM.md`.
- `Identity Preamble`: teaches that identity and date belong near the top. Feibo Deck keeps identity compact and injects date dynamically.
- `anthropic_api_in_artifacts`: teaches API-powered artifact constraints. Feibo Deck should create a separate policy only if it supports agent-powered artifacts.
- `citation_instructions`: teaches source attribution rules. Feibo Deck adapts this into `policies/research.md`.
- `available_skills`: teaches skill discovery before specialized work. Feibo Deck adapts this into `policies/tools.md`.
- `network_configuration` and `filesystem_configuration`: teach explicit environment assumptions. Feibo Deck should keep environment details outside static prompt when possible.

## Extraction Principle

Retain mechanisms, not claims. The reusable mechanisms are routing, verification, memory honesty, source freshness, output contracts, and examples. The non-reusable material is identity, product claims, hardcoded dates, platform paths, tool syntax, and unsupported APIs.

## Second-Pass Extractions (v0.2.0)

Deeper patterns extracted from structural analysis of the source prompt:

- `tone_and_formatting/lists_and_bullets` → context-sensitive formatting rules (prose for reports, no bullets for refusals) → `policies/anti-patterns.md`
- `tone_and_formatting` "avoids more than one per response" → single-question constraint → `policies/routing-examples.md`
- `search_instructions` "Do not perform tool calls as theater" → tool-theater anti-pattern → `policies/anti-patterns.md`
- `responding_to_mistakes_and_criticism` accountable-without-self-abasement → over-apologizing anti-pattern → `policies/anti-patterns.md`
- `user_wellbeing` "does not want to foster over-reliance" → engagement-maximization anti-pattern → `policies/anti-patterns.md`
- `mcp_app_suggestions` "check available MCPs before reaching for the browser" → inventory-before-invent → `policies/tools.md`
- Overall prompt architecture: every rule maps to an observed failure → governance meta-principle → `SYSTEM.md`

## Third-Pass Extractions (v0.3.0)

Epistemological and research-craft patterns:

- `search_instructions/core_search_behaviors` "Scale tool calls to complexity... for complex queries, first make a research plan" → research planning rule → `policies/research.md`
- `search_instructions/critical_reminders` "appropriately skeptical of results for conspiracy-theory-adjacent topics" → calibrated skepticism → `policies/research.md`
- `search_instructions/critical_reminders` "When results report conflicting info, run more searches" → conflict-resolution-by-search → `policies/research.md`
- `search_instructions/core_search_behaviors` "partial recognition from training does not mean current knowledge" → partial-recognition trap → `policies/research.md`
- `search_instructions/core_search_behaviors` "Every query deserves a substantive response" + "Don't mention any knowledge cutoff" → substantive-response obligation → `policies/research.md`
- `search_instructions/CRITICAL_COPYRIGHT_COMPLIANCE` self-check-before-responding pattern → pre-output self-check gate → `policies/style.md`
- `using_image_search_tool` interleaving principle (each image next to its text) → evidence-narrative interleaving → `policies/style.md`
