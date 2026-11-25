# Dispatch, integration and recovery

## Wave preparation

1. Confirm scope-specific delegation authorization and project rules.
2. Establish a dependency/ownership table: task, owner, files, blockers, acceptance, verification. For goal-backed work include criterion IDs using [goal decomposition](goal-decomposition.md).
3. Check worktree or shared working-copy safety and current uncommitted changes.
4. Allocate workers only to ready, independent tasks. Reserve the capacity and time for main-agent integration.
5. Log *actual* launched workers, including failed/replacement attempts, separately from meaningful contributors.

## In-flight behavior

- Do not pretend the skill has a queue, observer, model router, worktree tool or cancellation API. If the host lacks a capability, adapt the plan.
- Prompt workers with bounded briefs, not generic instructions to 'finish the issue'.
- Respect serialized dependencies; shared-contract evolution occurs before downstream edits. Require accepted upstream interface evidence before downstream dispatch; process completion alone is insufficient.
- Do not spawn nested workers by default. A worker may recommend another scope but cannot assume permission to create it.

## Integration barrier

For each handoff:

1. Verify the handoff against the assigned contract; check actual file changes and conflict with existing edits.
2. Reject unrelated changes; don't silently discard user work.
3. Check public contracts, data/transaction boundaries and regression coverage where applicable.
4. Run focused checks first; then relevant integrated lint, typecheck, tests, build, migration, smoke or conformance checks.
5. Recheck the requested acceptance criteria and outstanding risk/approval gates. Reconcile criterion coverage and stale evidence after integration.
6. Use independent *integrated-code* review for high-risk work when required by project policy.
7. Only the primary agent decides completion. Do not create PRs, merge or deploy unless user and platform authority allow it.

## Failure handling

- Worker unavailable: continue solo where possible; report mandatory delegation gate if unmet.
- Scope conflict: suspend overlapping writers; agree one owner and ordered merge.
- Incorrect output: return concise defect/reproduction to the owner; avoid duplicate full restarts.
- Budget exhausted: stop dispatch; preserve verified work and disclose unfinished acceptance criteria.
- Permission revoked: do not launch more workers; request cancellation of affected ones using available runtime controls, and verify outcome before claiming stopped.
- External tool/approval failure: do not bypass policy or silently use another provider/account.
