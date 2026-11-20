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
- For a small well-scoped task use a concise goal; persistent goal creation is not mandatory.
- Use ForgeGuard's installed Goal Intelligence policy and real goal tools when available. Never invent `create_goal` or similar APIs.
- Never create a separate task, chat, thread, worktree or worker solely for goal definition/storage.
- A Goal does not grant permission to launch subagents, bypass risks, merge, release or deploy.
- Reconcile the actual end state against the Goal and report unmet success conditions.
