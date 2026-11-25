# Delegrix — task-local Goal

Define or reuse this contract after ForgeGuard startup and before ForgeScope review and subagent dispatch. Keep it within the CURRENT task.

```text
Goal:
- Outcome: observable final state
- Target: module, artifact, behavior or environment
- Success criteria: binary or meaningful quantitative acceptance threshold
- Evidence: actual tests, diffs, build, reviews or observations
- In scope: authorized changes
- Out of scope: prohibited/unrelated changes
- Stop / escalate: permission limits, failed validator, important risks or blocked dependencies
```

- Check for a compatible existing goal in the current task before generating another.
- For routine work, use concise local criteria without creating native goal state.
- Follow the [goal architecture contract](../references/goal-architecture.md) and installed ForgeGuard policy when applicable. Create native goal state only for explicit goal-backed intent after inspecting existing state and confirming host support. Never invent `create_goal` or similar APIs.
- Never create a separate task, chat, thread, worktree or worker solely for goal definition/storage.
- A Goal does not grant permission to launch subagents, bypass risks, merge, release or deploy.
- For substantial or explicit goal-backed work, use [goal definition](../references/goal-definition.md), [lifecycle](../references/goal-lifecycle.md) and [evaluation](../references/goal-evaluation.md). Keep the expanded record in the current task.
- Reconcile the actual end state against the Goal and report unmet success conditions.

## Expanded criterion record (when justified)

```text
Criterion: C1
Required: yes/no
Predicate and threshold:
Evidence method:
Status: pending / passed / failed / blocked / stale
Observed evidence and result:
Subject revision / dirty changes / relevant environment:
Limitations / next action:
```

Use stable IDs. Do not silently downgrade required criteria. The record supports the authoritative goal; it is not a second persistent goal.
