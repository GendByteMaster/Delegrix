# Delegation decision rubric

Use a qualitative decision, not an invented numerical score.

1. **Authority**: Is there scope-specific approval in the current conversation? If no, do not spawn.
2. **Runtime**: Is a real subagent interface available and within permitted limits? If no, proceed solo or report an unmet project requirement.
3. **Project policy**: Check mandatory minimum, maximum, nesting, review, worktree and evidence rules. A cap is not a target. Never pretend a 28-worker cumulative ceiling is a 28-worker concurrency allowance.
4. **Decomposition**: Are there independent, bounded scopes or a genuinely independent review? Avoid parallel writes to a shared contract and duplicate analysis.
5. **Benefit**: Would specialization or elapsed-time savings exceed communication, review, merge and context costs? Focus on critical path, failure coverage and reliability.
6. **Selection**: Launch the smallest useful team that meets binding project constraints, not a fixed default number.
7. **Reporting**: State why workers were or were not needed; never assert their contribution without a concrete handoff.

## Candidate patterns

- Small targeted bug fix: solo; add focused regression test.
- Distinct API module + independent test fixture: two scoped implementers if interface is stable.
- High-risk migration: one owner of schema/migration; separate read-only transactional review and failure-path tests; serialize shared contracts.
- Cross-package refactor: freeze public contract first; implement isolated packages in waves; verify integration centrally.
- Spec-only exploration: a read-only specialist may add value; no workers if the question is small.
- Project requires 8–28 substantive workers: find real distinct work and satisfy approval/budgets, or report the requirement unmet. Do **not** invent eight near-identical assignments.

## Approval boundary

Authorization must cover the proposed action's worker count/scope. Approval for one read-only reviewer does not permit multiple code editors. A user can revoke; stop additional dispatch immediately and request cancellation of affected running workers only if the runtime exposes it. Preserve independent authorization for critical or production actions under ForgeGuard risk policy.