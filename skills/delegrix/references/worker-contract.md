# Worker contracts and evidence

A contract is a *bounded delegation*, not a vague role title. Use [the worker brief](../assets/worker-brief.md), adjusting fields to the task. Contracts must state:

| Field | Required question |
| --- | --- |
| Objective | What observable result must exist? |
| Ownership | Which files, module, schema, tests, or read-only surfaces are assigned? |
| Exclusions | What must not be modified or executed? |
| Dependencies | Which contracts, inputs, or other worker outputs must be ready first? |
| Constraints | What architectural, type, security, compatibility and resource invariants apply? |
| Goal linkage (when applicable) | Which criterion IDs and predicates does this deliverable contribute to? |
| Acceptance | How will the result be judged independently? |
| Verification | Which *available* commands or inspections should be run and reported? |
| Handoff | Which changes, findings, evidence, limitations and unresolved issues must return? |

Do not distribute secrets, credentials, unapproved external service access or whole-repository conversation history merely because it is convenient.

## Ownership rules

- Single writer per shared code/contract in a wave; multiple read-only reviewers are acceptable.
- Worktrees are preferred when supported; without isolation, strictly partition edits and integrate serially.
- If a worker discovers that the assigned scope is insufficient, it must return to the coordinator rather than editing adjacent modules unilaterally.
- Worker reviews must identify concrete files, findings, repro cases and impact rather than generic assurances.

For substantial or explicit goal-backed work apply [goal decomposition](goal-decomposition.md). A worker owns a deliverable, not global criterion acceptance.

## Handoff quality

A handoff that says only `done` or `tests PASS` is incomplete. Use [the handoff template](../assets/handoff.md). Distinguish tests actually run from suggested or skipped tests. If a command fails, include the failure and why it remains unresolved.
