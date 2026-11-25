# Goal lifecycle, progress and drift

Use this guidance for substantial or explicitly goal-backed work. Keep routine tasks lightweight. All states here are logical task-local concepts; do not assume a host exposes matching native statuses. The primary agent owns the assessment, not a worker or a progress counter.

## Lifecycle

| State | Meaning | Allowed next states |
| --- | --- | --- |
| defined | Outcome, scope and acceptance contract established | executing, blocked, cancelled |
| executing | Authorized work in progress | verifying, blocked, cancelled |
| verifying | Integrated result evaluated against criteria and gates | completed, needs-repair, blocked, cancelled |
| needs-repair | A failed or stale criterion can be addressed within scope | executing, blocked, cancelled |
| blocked | A required dependency, permission, evidence or risk gate is unresolved | executing, verifying, cancelled after blocker resolution or explicit cancellation |
| completed | All mandatory criteria currently pass and required gates are satisfied | terminal for this goal revision |
| cancelled | User explicitly abandons the goal or cancellation is confirmed | terminal |

Do not equate ending an agent turn with completed or cancelled. If work cannot finish, report the actual state and unresolved criteria. On resumed work, reconcile actual repository/environment state and native state before relying on prior evidence. If new information invalidates a previous completion claim, explicitly correct the report and assess a new authorized goal revision; never silently reopen or overwrite a native goal.

## Criterion states

Each criterion has a stable ID, required/optional flag, predicate and evidence method. Track independently:

- pending: not yet verified; no usable evidence.
- passed: current, relevant evidence supports the predicate and all dependencies needed by that predicate.
- failed: actual relevant verification contradicts the predicate.
- blocked: verification or delivery cannot proceed because of a named obstacle.
- stale: previous evidence is no longer applicable to the present result or criterion.

Only the primary agent can accept a criterion after inspecting evidence. A worker may propose evidence or a status. Never treat a handoff, planned test, skipped test or preflight pass as evidence of integrated behavior. A skipped required validator is pending or blocked, not passed.

## Checkpoints

Reconcile criteria after meaningful changes, integration waves, failed verification, scope changes, resumption, and immediately before completion. For each checkpoint record only useful details: criterion ID, state, evidence reference, relevant subject/revision/environment, blocker and next action. Track verified required criteria as a count (for example 3 of 5). Do not interpret the count as effort, release readiness, or a probability of success.

## Drift and invalidation

Compare the current outcome, scope, criteria, assumptions, actual changes and permissions to the agreed contract. Distinguish implementation strategy changes within scope from a change to the requested outcome or authorization.

- If relevant code, configuration, dependencies, environment, validator, input or criterion changes, invalidate affected previous evidence and mark the criterion stale until reverified. Include uncommitted changes in the subject identity; a commit SHA alone does not identify a dirty worktree.
- Preserve unaffected evidence only when its applicability can be justified; if dependency impact is uncertain, invalidate conservatively. Do not erase known failures to manufacture progress.
- A changed success predicate or required/optional designation requires explicit reconciliation with user intent and binding policies. Never silently relax or remove a required condition. Adding scope or permissions requires applicable approval.
- Unexpected edits, conflicting native goals, lost authorization or unresolved risk stop the affected work. Report the difference and choose an authorized correction or escalation.
- If native state is lost or a mutation cannot be confirmed, disclose it, retain available supporting evidence and do not invent a state transition.

Use the [evidence and evaluation contract](goal-evaluation.md) before any completion decision. Targeted recovery is permitted only within existing authorization and [bounded retry rules](goal-recovery.md).
