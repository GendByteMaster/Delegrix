# Goal Intelligence v2 — architecture and compatibility contract

Status: M1 foundation for [issue #2](https://github.com/GendByteMaster/Delegrix/issues/2). This is an instruction-level contract, not a runtime implementation. M2 defines [goal routing](goal-definition.md), [criterion lifecycle and drift](goal-lifecycle.md) and [evidence-based completion](goal-evaluation.md). M3 adds [criterion-linked delegation](goal-decomposition.md). Detailed recovery remains a follow-up milestone.

## Authority

- Host: actual capabilities, native goal state, worker execution, permissions and cancellation.
- Primary agent: interpretation of user intent, task-local goal, decisions, integrated evidence and final acceptance.
- Delegrix: goal execution guidance, decomposition, coordination and completion criteria.
- ForgeGuard (optional): applicable engineering policy, authorization, risk and verification constraints, including its installed goal policy.
- EngSense (optional, planned M4): contextual engineering judgment; never a permission or verification authority.
- ForgeScope (optional): scoped review and evidence-backed findings.

Host instruction hierarchy and user authorization remain binding. A goal cannot extend scope or grant execution rights. Do not modify companion configurations or automatically install any skill.

## One logical goal, one authority

A goal describes an outcome for the current task, not a worker assignment or another chat. Keep one authoritative representation. If the host exposes a compatible active native goal, use that state as authoritative; local criteria and evidence are supporting context, not a competing persistent goal. Otherwise keep the contract in the current task. Never invent a persistence API or create another task, thread, worktree or worker just to store it.

| Situation | Required decision |
| --- | --- |
| Routine task; no explicit goal-backed intent | Use concise local acceptance criteria; do not create native goal state. |
| Compatible active native goal | Reuse it; preserve the existing objective and binding constraints. |
| Conflicting active goal | Surface the conflict; do not replace, complete or duplicate it silently. |
| Explicit goal-backed request; supported native inspection and creation; no active goal | Create only after the objective is measurable and scope is clear. Follow actual tool contracts. |
| Goal-backed request; no usable native goal API | Use a task-local contract and disclose the capability limit. |
| Goal state cannot be inspected reliably | Do not create potentially duplicate native state; report the uncertainty. |
| ForgeGuard installed | Apply its current goal policy and reuse its compatible contract; do not create a second logical goal. |
| ForgeGuard unavailable | Use Delegrix's local contract, respecting host and user constraints. |

Do not assume tool names are present. Do not set an unrequested token budget. If missing scope or evidence materially changes the intended result, seek a focused clarification instead of guessing.

## Minimum contract

For substantial work identify the outcome, target, success criteria, evidence method, scope, exclusions and stop/escalation conditions. Criteria must be observable and preserve important repository invariants. A narrow task may express these in one concise statement. The existing [task-goal template](../assets/task-goal.md) remains compatible.

For substantial or explicit goal-backed work, stable criterion IDs, required/optional classification and evidence freshness are required by the M2 guidance. No required criterion may be silently weakened or removed to declare completion. Evidence must correspond to the integrated result; a worker claim or structural preflight alone cannot establish success.

## Companion interoperability

Preserve the existing ForgeGuard-first and ForgeScope review workflow during M1. A later EngSense routing module should select relevant guidance only for material engineering trade-offs, decomposition or repair. Avoid recursive skill invocation and competing goal ownership. A missing companion must not prevent permitted standalone execution. Actual activation modes must be reported accurately.

## Compatibility and boundaries

Codex, Claude Code and Cursor share portable instructions; native goal and worker features must be discovered on the current host rather than inferred from the client name. Keep the existing package and CLI lifecycle intact. This contract adds no native tools, runtime, scheduler, background workers, database or external permissions. Static packaging checks are not live behavior evidence.

## Design references

- [OpenAI define-goal](https://github.com/openai/skills/tree/main/skills/.curated/define-goal) — inspected 2026-11-25; goal formulation and native creation are the reference scope, not execution orchestration.
- [Upstream license](https://github.com/openai/skills/blob/main/skills/.curated/define-goal/LICENSE.txt) — Apache-2.0. This document is independently authored for Delegrix; no upstream instruction text or code is vendored. Any future redistribution of upstream material requires separate license/notice review.
- [ForgeGuard goal policy](https://github.com/GendByteMaster/ForgeGuard/blob/master/engineering-guardrails/references/goal-policy.md).
- [EngSense](https://github.com/GendByteMaster/EngSense).
- [Existing integration workflow](integration-workflows.md).
