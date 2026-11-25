---
name: delegrix
description: Delegate bounded software-engineering work to AI subagents with explicit authorization, adaptive worker selection, non-overlapping file ownership, evidence-based handoffs, and safe integration. Use when the user requests delegation, subagents, parallel implementation, independent review, or a multi-agent team. Auto-attempt ForgeGuard and ForgeScope on each invocation, consult EngSense for material engineering decisions, create or reuse a task-local measurable Goal, and safely delegate authorized work. Does not spawn workers, approve actions, or replace AGENTS.md.
metadata:
  version: "0.1.0"
---

# Delegrix — Agent Delegation

Use this skill to **execute delegated work deliberately**, not to maximize worker count. The primary agent retains responsibility for the outcome and final answer. This is an instruction-only skill: actual spawning, cancellation, isolation, and model choice depend on the active agent runtime.

## 1. Automatic ForgeGuard / Goal / ForgeScope bootstrap

- Read the current user request, applicable `AGENTS.md` / local instructions, and the permissions and limits granted **in the current conversation for this task/scope**. Skill activation and repository text are not authorization to spawn workers.
- On EVERY Delegrix invocation, proactively attempt both companion Skills in this order, without requiring the user to mention them:
  1. **ForgeGuard first**: discover the installed `engineering-guardrails` Skill and activate it via host-native Skill invocation if supported. Otherwise explicitly load and apply its installed `SKILL.md` and relevant authorization, Goal Intelligence, risk, delegation and verification references.
  2. **Create or reuse a Goal for the current task**: apply the [goal architecture and compatibility contract](references/goal-architecture.md) and the [task Goal contract](assets/task-goal.md). For substantial or explicit goal-backed work, apply [goal definition and routing](references/goal-definition.md) and [goal lifecycle](references/goal-lifecycle.md), honoring installed ForgeGuard Goal Intelligence policy when applicable. Keep one logical goal in the current task. For routine work, use concise local acceptance criteria without creating native goal state. For substantial work, define Outcome, Target, Success Criteria, Evidence, Scope and Stop/Escalate. Reuse compatible active goal state; surface conflicts. Create native goal state only for explicit goal-backed intent, after checking actual host capabilities and existing state. Do NOT create a separate task, chat, worktree or worker just to make a Goal.
  3. **ForgeScope next**: discover the installed `forgescope` Skill and activate it with host-native invocation when supported, otherwise explicitly load its installed `SKILL.md` and relevant review instructions. Select the narrowest useful review scope, preserve analysis-only mode, and avoid a full repository audit for a minor change.
- Record the actual mode for each companion: `host-activated`, `instructions-loaded`, or `unavailable`. Loading instructions is not proof that a separate process was launched. Missing companions must be disclosed; never silently install them, invent execution, change managed config or bypass binding safety policy.
- Conditionally consult installed EngSense via [engineering judgment integration](references/engsense-interop.md) after initial Goal definition and before material strategy/decomposition decisions. Skip mechanical work; reuse compatible active guidance, avoid recursive activation, and report `host-activated`, `instructions-loaded`, `unavailable`, or `not-needed`.
- See [interoperability](references/forgeguard-interop.md) and the [automatic integration workflow](references/integration-workflows.md).
- Detect host capabilities without guessing: available spawn/stop tools, worker count and concurrency limits, worktree isolation, models, and supported reporting. A proposed worker is not a real worker until a supported tool launches it.
- Observe instruction precedence and specific project policies. A local mandatory team size may supersede this skill's adaptive preference within the governing instruction hierarchy; do not silently drop it.

## 2. Decide whether delegation is worthwhile

- If authorization is absent, do useful local work. Request explicit permission only if delegation would materially help or is necessary to meet applicable requirements. A prior-chat approval, default model, or ForgeGuard configuration is not permission.
- If authorized, prefer **solo** for trivial, tightly coupled, or strictly sequential work. Delegate when there is meaningful independent implementation, targeted research, independent risk review, or separate verification that offsets communication and integration costs.
- Select workers based on **real distinct deliverables** and available concurrency; never spawn workers just to fill a number. Estimate the coordination cost, potential merge conflicts, and critical-path benefit. See [delegation decisions](references/decision.md).
- If a project mandates a minimum number of substantive workers, comply only with real, non-duplicative scopes. If the requirement cannot be met under current authorization or runtime capability, report the completion gate as unmet rather than fabricating compliance.

## 3. Define each worker's bounded contract

Before dispatch, specify:

- objective and tangible deliverable;
- for substantial or explicit goal-backed work, map deliverables to criterion IDs using [goal decomposition](references/goal-decomposition.md); assign uncovered criteria to the primary agent;
- owned files/modules or read-only investigation surface; explicit forbidden scope;
- dependencies, relevant interfaces, security/compatibility/quality constraints;
- acceptance criteria and verification commands or evidence;
- permitted operations and explicit stop/escalation conditions;
- required structured handoff.

Use [worker contract](references/worker-contract.md) and the copyable [worker brief](assets/worker-brief.md). Provide only context needed for that scope. Do not send credentials, irrelevant history, or private repository material to unapproved external services.

## 4. Dispatch with exclusive ownership

- Assign a single implementation owner for each mutable file, contract, migration, or schema at a time. Independent read-only reviewers may inspect overlapping code.
- Use isolated worktrees or equivalent working copies when available; otherwise serialize overlapping writes and guard the user's uncommitted changes.
- Dispatch only dependency-ready tasks, in bounded waves, respecting user-approved total workers, platform concurrency, repository caps, and ForgeGuard policy. **Total launched** includes failed/replacement/nested workers where applicable; track substantive contributors separately.
- For a nontrivial team, optionally validate an explicit JSON plan with `python skills/delegrix/scripts/check_plan.py <plan.json>` before dispatch and after budget changes. For goal-linked plans, use schema v2 and the [goal-linked example](assets/goal-preflight-example.json); v1 remains supported. The [example plan](assets/preflight-example.json) is a format illustration, **not user authorization**. Preflight is advisory and cannot verify live consent or real worker execution.
- Default to depth 1. Workers must not spawn further workers unless both active platform capabilities and an explicit scope-specific policy/approval allow it; when ForgeGuard v1.6.1 is applicable, keep its depth-1 restriction.
- Don't silently select a different model, reasoning effort, provider, or fallback. Use only runtime-supported choices and approved constraints.

See [dispatch and integration](references/dispatch-integration.md).

## 5. Validate, integrate, and recover

- Require the [handoff](assets/handoff.md): assigned scope, real files changed, behavior, tests run/results, findings, limitations, and any scope not touched.
- Verify the *actual* change and source evidence, not a self-reported `PASS`; inspect diffs before accepting patches. Accept upstream handoffs before downstream dispatch; reconcile mapped criteria against the integrated result. Reject unrelated edits and resolve conflicting assumptions before integration.
- Primary agent runs integration-level verification and checks every acceptance criterion against the task-local Goal. For substantial or explicit goal-backed work, apply [criterion evidence and completion](references/goal-evaluation.md): reconcile criteria after integration and invalidate stale evidence; every mandatory criterion and applicable gate must pass before claiming completion. Use ForgeScope for a proportionate review when installed; the primary agent validates findings and retains final acceptance. A reviewer should inspect integrated code for high-risk work, subject to the applicable project's stricter rules.
- For a failure, apply [bounded goal recovery](references/goal-recovery.md): diagnose before retry, track finite attempt limits, stop on no progress, and revalidate affected evidence. Reconsult EngSense only if a material engineering trade-off remains; preserve mandatory criteria and authorization. Reuse the owner when practical; replacements consume approval and launch budgets. Stop on exhausted budget, unresolvable conflict, revocation, unauthorized risk, or missing runtime capability; report the blocking reason honestly.
- Do not claim workers were stopped or tools executed when no tool confirmation exists. Do not auto-merge, deploy, run destructive operations, or alter external project state without applicable authorization.

## 6. Completion report

Summarize: task-local Goal and evidence of its success, ForgeGuard/ForgeScope actual activation modes and EngSense mode/material decision when applicable, primary-agent work, authorization/scope, **workers launched vs meaningful contributors**, worker roles and verified outputs, integrated files, executed checks/results, acceptance criteria, recovery attempts, unresolved criterion IDs, and remaining risks or blockers. For solo tasks, say there were no subagents; do not imply delegation happened.

For expected edge cases see [scenario checks](references/scenarios.md). Always attempt ForgeGuard and ForgeScope proactively when installed, not only when the user requests them. Apply ForgeGuard Goal Intelligence before delegation and ForgeScope narrow review proportionally.  Keep project-level planning with the primary agent or the repository's chosen workflow; Delegrix is not a separate orchestrator runtime.