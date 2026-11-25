# Goal-driven decomposition and delegation

For substantial or explicitly goal-backed work, apply [definition](goal-definition.md), [lifecycle](goal-lifecycle.md) and [evaluation](goal-evaluation.md) before delegating. A worker's assignment is a contribution to the current goal, never an independent authoritative goal.

## Plan from criteria, not worker count

1. Identify required and optional criteria with stable IDs. Map each required criterion to at least one deliverable or explicit primary-agent work/verification. A criterion can require several contributors; no contributor can accept it on behalf of the coordinator.
2. Choose distinct deliverables with bounded scope, dependency inputs, expected output and verification. Map each delegated deliverable to one or more criterion IDs; independent read-only reviews may map the same IDs as implementers.
3. Prefer solo work for tightly coupled or small changes. Obtain live scope-specific authorization before dispatch; goal-backed intent alone does not authorize workers. Do not force workers to fill a quota.
4. Sequence dependency-ready waves. An upstream deliverable is ready only after the primary agent accepts its actual handoff and interface evidence. A completed worker process is not sufficient. Keep exclusive mutable ownership; if shared paths are unavoidable, serialize in separate plans/waves with fresh evidence. Preserve existing preflight caps, depth and analysis-only constraints.
5. Reconcile the plan after integration, invalidated assumptions or failed checks. Reassign only within existing authorization, preserve criterion IDs, count replacement launches, and disclose gaps.

## Handoff and acceptance

Give each worker only the relevant criterion IDs, predicates, allowed evidence method and local deliverable acceptance. Require the handoff to map actual evidence and limitations back to those IDs. Unknown IDs, changed predicates, missing evidence or out-of-scope edits are not accepted. The coordinator checks actual integrated changes, reruns affected validators and marks stale evidence per the lifecycle contract. A worker may report a local pass but cannot mark the global criterion passed or complete native goal state.

## Optional structural preflight v2

The existing schema version 1 remains supported without goal mapping. For a goal-linked plan use schema version 2, with:
- goal.criteria: nonempty array of objects with unique identifier id and boolean required;
- goal.coordinator_criteria: array of criterion IDs assigned to primary-agent work/verification, including criteria already covered by accepted work from earlier waves;
- workers[].criterion_ids: nonempty array of distinct IDs declared in goal.criteria.

All required criteria must be covered by a worker mapping or coordinator_criteria. Optional criteria may be unmapped. A worker mapping indicates contribution, not completion or permission. The coordinator remains responsible for final verification of every required criterion irrespective of mapping. The validator retains all v1 safety checks and conservatively rejects overlapping writes across the entire submitted plan, even if dependencies exist. Use separate dependency-ready plans for serialized writers. Do not treat plan v2 as a goal database or evidence validator. See [v2 example](../assets/goal-preflight-example.json).

Use the [worker brief](../assets/worker-brief.md) and [handoff](../assets/handoff.md); routine work can keep the existing concise v1 workflow.
