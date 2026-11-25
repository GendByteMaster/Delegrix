# Criterion evidence and completion

Use with [goal definition](goal-definition.md) and [goal lifecycle](goal-lifecycle.md). This is an instruction-level evaluation contract. It does not execute tests or prove host behavior.

## Evidence mapping

For each required criterion, identify what would establish its predicate and inspect the actual result. A compact task-local record may contain:

- Criterion ID and expected predicate/threshold.
- Evidence kind and reference: executed command plus result, inspected diff or artifact, observed behavior, measured sample, or reviewed source and finding.
- Subject identity: relevant revision and dirty changes, artifact/version or exact inspected source; environment and inputs when they affect validity.
- Observed result, limitations, and status (pending, passed, failed, blocked, stale).
- Dependency or invalidation reason when relevant.

Use existing task context, host-supported state, or established repository workflow; no mandatory new database, ledger file or separate task. Avoid credentials and unrelated private data in evidence.

## Evidence hierarchy is contextual

A static check can prove static structure but not live behavior. CI results apply to the revision and environment actually tested. Runtime evidence must come from observed execution; passing a JSON plan does not prove consent or worker execution. A source citation can support research but cannot prove a code change. Independent reviewer findings must be checked against the integrated subject. If a test cannot be run, say why and report what remains unverified. Do not replace a required validator with a weaker check merely to obtain a pass.

## Completion gate

Before reporting completion:
1. Confirm current user intent, scope and applicable risk/approval gates.
2. Inspect integrated changes and re-evaluate evidence freshness and relevant dependencies.
3. Require every mandatory criterion to be passed with sufficient current evidence. Optional criteria may remain unmet and must be disclosed when relevant. No required criteria may be dropped silently.
4. If any mandatory criterion is failed, stale, pending or blocked, do not report completed. Choose bounded repair when authorized and useful, otherwise report blocked or incomplete with exact remaining conditions.
5. Primary agent owns the final decision. If native completion is supported and authorized, follow the actual host tool contract only after the gate passes; confirm the result. If native completion cannot be confirmed, distinguish the local assessment from native status.

## Example (illustrative, not a test result)

| Criterion | Required | Evidence | State |
| --- | --- | --- | --- |
| C1: Regression fixed | yes | Integrated regression test passed on current revision | passed |
| C2: Public API compatibility | yes | Prior verification; interface subsequently changed | stale |
| C3: Optional refactor | no | Not attempted | pending |

Decision: not completed. Reverify C2 against the integrated subject. C3 is not a substitute for C2. Do not report production or release readiness without separate applicable gates.
