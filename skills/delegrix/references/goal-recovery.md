# Goal recovery — bounded correction and revalidation

Apply this guidance when substantial or explicitly goal-backed work has failed, stale or blocked mandatory criteria, or a material review finding. For routine work use the same principles without extra record keeping. This is a task-local decision loop, not a scheduler, autonomous service or native goal API.

## Diagnose before repair

1. Reconcile the current goal, relevant criterion IDs, integrated subject, actual validator output and active authorization. Preserve failed evidence and distinguish a product defect from an invalid validator, stale evidence, environmental failure, dependency failure, or an unresolved requirement.
2. Identify the smallest evidence-supported cause or an explicit hypothesis. Inspect only relevant code, tests, contracts and changes. Do not convert a hypothesis into a confirmed cause without evidence.
3. For blocked or stale criteria, first restore the missing prerequisite or reverify the current subject if possible. Do not modify implementation merely to compensate for an unavailable environment.
4. Select the smallest authorized action that tests the hypothesis or resolves the failure. Prefer targeted repair over broad restart. Consult [EngSense](engsense-interop.md) only when a material strategy trade-off remains; apply ForgeGuard risk and permission gates before consequential changes.

## Bound the loop

Before the first repair attempt, set a finite attempt limit appropriate to the current failure episode. Default to at most two repair attempts per episode; respect any stricter user, project, host or ForgeGuard limit. This is a repair-attempt ceiling, not a token budget or permission to launch workers. Count unsuccessful attempts and replacements; count actual worker launches separately under the existing delegation limits. Re-entering a turn, renaming a failure or changing the worker does not reset the episode. If a prior attempt count cannot be reconciled, do not assume a fresh budget.

For each attempt:
- Record affected criteria, prior evidence, hypothesis, proposed change/check, attempt number and remaining permitted attempts.
- Confirm scope, authorization, ownership, dependency readiness and risk. Reuse an existing owner when practical; never launch extra workers without current-task authorization.
- Apply the targeted change, invalidate evidence affected by that change, inspect integrated output and rerun the relevant validators.
- Compare actual results against the previous checkpoint. Reconcile all affected criteria with [lifecycle](goal-lifecycle.md) and [evaluation](goal-evaluation.md).

A new failure episode is justified only by evidence of a genuinely distinct cause and meaningful progress, not a renamed symptom. Preserve the cumulative attempt history within the task and stop if recurring episodes fail to converge.

## No-progress and stop conditions

A meaningful progress signal is a verified resolved defect, newly supported causal diagnosis that changes the next action, restored prerequisite, or current valid evidence that advances a mandatory criterion. File edits, elapsed time, worker reports, repeated identical failure output and a different model alone do not establish progress.

- Stop when the attempt limit is exhausted, an unchanged failure recurs without a new evidence-supported hypothesis, a previous failure state recurs (oscillation), or further work cannot materially advance the goal.
- Stop affected work immediately for revoked authorization, scope expansion requiring approval, unresolved safety/risk gate, conflicting native goal, or missing necessary capability.
- Do not weaken tests, delete required criteria, hide regressions or claim a blocked validator passed.
- Preserve verified unrelated work; do not discard user changes or perform a destructive rollback. Report the blocker, remaining criterion IDs, actual attempts, evidence and the smallest next action or approval needed.

## Revalidation and independent review

After repair, check affected dependencies and relevant integrated regression tests, not merely the repaired worker's local test. Re-run affected review on the current integrated subject. Use installed ForgeScope guidance at the narrowest useful scope; preserve analysis-only mode. Its findings need evidence and primary-agent adjudication; distinguish a confirmed issue from a hypothesis or preference.

If independent review is required by binding policy, obtain actual authorized independent review of the integrated result; do not label the implementer's self-review independent. If a required specialist or independent reviewer is unavailable, leave that gate unmet and report it. A missing optional ForgeScope installation alone is not a failure if no binding review gate requires it; perform permitted primary-agent verification and disclose the fallback.

A confirmed material finding affecting a required criterion or binding gate prevents completion until resolved or legitimately reconciled under applicable policy. Do not equate review-tool activation with completed review. The primary agent alone reconciles the completion gate. Confirm native completion only through supported host tools after all mandatory criteria and gates pass.

## Compact recovery record (when useful)

Criterion IDs | prior evidence | cause/hypothesis | attempt/limit | action | observed result | invalidated evidence | next decision

Keep this in current task context or an established project workflow. No mandatory new ledger, files, tasks, or background retries.

## Illustrative scenarios (not live execution evidence)

- Identical failing test after repair, no new diagnosis: stop, report failed criterion and remaining budget.
- Network required for integration test is unavailable: blocked, preserve local evidence; do not mark passed.
- Repair changes a public interface: mark dependent compatibility evidence stale and reverify before completion.
- Worker passes local tests but integrated tests fail: global criterion failed; investigate integration.
- User revokes delegation permission: stop launching workers, request cancellation only using supported tools, verify the result; report uncertain cancellation honestly.
- Required independent review unavailable: keep completion gate unmet, even when tests pass.
