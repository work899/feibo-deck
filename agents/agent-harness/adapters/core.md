# Core Adapter

Use this compiled prompt as a standalone system or developer instruction. It is host-neutral and assumes tools, filesystem permissions, current date, and memory availability are injected by the runtime.

## Runtime Injection Requirements

- Current date and timezone.
- Available tools and their exact invocation rules.
- Filesystem roots and write permissions.
- Network/search availability.
- Memory availability and persistence rules.
- Host-specific formatting or final-answer requirements.

## Rule

If a host instruction conflicts with this harness, the host instruction wins. The harness governs behavior only within the available runtime.

