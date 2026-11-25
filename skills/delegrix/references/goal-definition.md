# Goal definition and routing

Apply the [architecture contract](goal-architecture.md) before defining or changing a goal. This is portable agent guidance, not an API implementation.

## Choose the lightest adequate contract

- Routine work with an unambiguous result: state concise acceptance criteria in the current task; no native goal creation.
- Substantial work: define a task-local outcome and explicit criteria before decomposition or implementation.
- Explicit goal-backed intent: prefer the native goal facility only if its actual inspection and creation capabilities are available and permitted. Reuse a compatible active native goal even when the new request does not require creating one.

## Route native and local state

1. Identify the current task, user outcome, applicable instructions, authorization and available host tools. Apply installed ForgeGuard policy. Do not interpret a skill invocation or a broad request to improve something as permission to spawn workers.
2. If native state can be inspected, inspect it before creating or modifying goal state. Distinguish an observed absence from an inspection error or unknown state.
3. If an active goal exists, compare its outcome, scope and binding success conditions to the current request. Reuse a compatible goal and attach criteria as supporting context. If materially conflicting, surface the conflict and continue only work that does not conflict; do not silently replace, complete or duplicate it.
4. If absence is confirmed and the user explicitly requests goal-backed work, create native state only if the host actually supports it and the definition meets the quality bar. Follow the real tool schema, do not invent fields or set an unsolicited token budget.
5. Confirm native mutations from tool results or readback. If a creation result is ambiguous, inspect state before any retry; never blindly repeat creation. If inspection is unavailable, do not create potentially duplicate state.
6. If native tools are unsupported or a permitted mutation cannot be confirmed, retain the local task contract and report the limitation. If a compatible native goal is known to exist, the local contract is supporting context, not a second authority. Never create a new thread, task, worktree or worker just to store goal state.

## Goal quality bar

A substantial goal is ready when it specifies:
- Outcome and target: observable final behavior or artifact, not activities.
- Scope and exclusions: authorized boundaries and preserved invariants.
- Criteria: stable IDs (for example C1, C2), required or optional classification, observable predicate, evidence method and threshold.
- Stop or escalation conditions: missing permissions, unsafe scope expansion, unavailable dependencies or an applicable risk gate.

Assign IDs once in the current goal. Required criteria cover the user's outcome and binding project/verification requirements. Optional criteria may describe improvements, never substitutes for required criteria. When the exact command or measurement is unknown, first inspect relevant project instructions or specify the discovery step; do not invent a validator or numeric threshold. Use a binary validator when a useful metric is unavailable. If materially different outcomes remain plausible, ask a focused question rather than silently narrowing the task.

## Domain examples (illustrative)

| Domain | Observable criterion | Evidence |
| --- | --- | --- |
| Bug | Reproduction fails before and passes after when practical | Regression test output, integrated diff |
| Feature | Requested behavior and compatibility invariant hold | Relevant unit/integration or acceptance checks |
| Performance | Agreed metric meets a meaningful threshold under stated conditions | Baseline, workload, environment, repeat measurements as needed |
| Research | Named decision is supported by relevant sources and explicit uncertainty | Source references and comparison |
| Operations | Authorized target reaches agreed healthy state | Health checks, monitoring window, rollback criteria |

Use the [task goal template](../assets/task-goal.md) and [lifecycle](goal-lifecycle.md). Do not add a persistent artifact unless the user or existing project workflow calls for one.
