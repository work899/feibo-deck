# Deputy Agent Inspirations

This note records which ideas were borrowed from the Deputy Agent reference project and how they were adapted for Agent Harness Kit.

## Adopted

Deputy's provider-neutral runtime uses a capability matrix before optional behavior is called. Agent Harness adapts this as `capabilities.json` plus profile `requires` arrays. The current implementation is static and host-level rather than session-level, which matches this kit's lighter scope.

Deputy uses declarative `done_criteria.yaml` so completion checks are evaluated without an LLM. Agent Harness adapts this as `done_criteria.json` plus the `verify` command. The checks are intentionally small and deterministic.

Deputy's task capsule separates workspace artifacts from control state and event streams. Agent Harness partially adapts this by keeping generated prompts under a build directory and source behavior under the harness directory. A full task capsule is deferred.

Deputy's role/provider separation shows the value of profiles that declare requirements. Agent Harness adapts this as profile selection plus target capability checks rather than implementing a long-running role daemon.

## Not Adopted Yet

Deputy's host daemon, stage machine, message bus, watcher, reviewer, and Web UI are useful for long autonomous tasks but are intentionally not part of the current kit. Agent Harness is still a prompt governance and integration layer, not a multi-agent task runtime.

Deputy's file locking and recovery model are also deferred. They matter once Agent Harness manages concurrent long-running tasks, but the current CLI writes small prompt artifacts synchronously.

