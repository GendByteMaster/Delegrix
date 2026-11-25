# EngSense integration — engineering judgment

EngSense is an optional static Skill (technical name: `engsense`), not a worker runtime, a permission authority, or a replacement for ForgeScope. Use the installed EngSense instructions as the source of its engineering guidance. This integration does not vendor its modules, invoke an external model service, or change companion configuration.

## Decision routing

Evaluate the need after ForgeGuard policy and initial Goal definition, before committing to a material engineering strategy or delegation partition. Re-evaluate at a material recovery decision or changed assumption. Preserve the existing ForgeGuard-first, Goal, ForgeScope activation sequence; EngSense consultation is conditional, not a new mandatory bootstrap stage.

| Situation | Action |
| --- | --- |
| Routine formatting, simple rename, deterministic fix | not-needed; continue without loading EngSense |
| Architecture, compatibility, abstraction or migration trade-off | consult EngSense before choosing strategy |
| Coupled modules or uncertain ownership boundaries | consult when the decomposition decision is material; prefer cohesive solo work if splitting adds coordination cost |
| Failed verification | diagnose first; consult only if a material engineering choice remains |
| Specialist correctness concern | use EngSense for routing if useful; require appropriate specialist evidence or report an unresolved gate |
| Review finding | ForgeScope owns its review; use EngSense only for a material decision about remediation, not duplicate review |

Explicit user instructions, host policy, current authorization and applicable ForgeGuard gates remain binding. A recommendation may refine the plan within scope, but cannot change the requested outcome, downgrade mandatory criteria, authorize new workers or override specialist invariants.

## Discovery and activation

1. If the trigger is absent, record `not-needed`; do not load EngSense merely because Delegrix is active.
2. When needed, reuse already active compatible EngSense guidance or discover the installed `engsense/SKILL.md` through host-supported Skill discovery and configured locations. Read the installed version, not a presumed release.
3. Prefer supported native Skill invocation. Otherwise load and apply the installed root instructions and only relevant modules. Record `host-activated` or `instructions-loaded` according to observed behavior.
4. If unavailable, ambiguous, or activation cannot be confirmed and no usable installed instructions exist, record `unavailable` with the reason. Continue permitted local engineering analysis without claiming EngSense was used; preserve any mandatory specialist or verification gates.
5. Avoid recursive Skill invocation: if an active EngSense workflow refers back to Delegrix, reuse current task context rather than re-entering bootstrap. Do not launch a worker merely to activate a Skill. Never auto-install, fetch remote instructions as a substitute for installed Skill discovery, or edit managed AGENTS/configuration as a side effect.

## Minimal context and decision handoff

Provide only relevant Goal criteria, current constraints, observed repository evidence, alternatives, uncertainty and affected interfaces. Let EngSense choose relevant modules through its own progressive-disclosure router. Do not force a fixed lens sequence or load its full corpus. Respect research-gated source-specific lenses and specialist boundaries.

For nontrivial decisions, retain a concise task-local record: decision question, affected criterion IDs, relevant evidence, alternatives/trade-offs, chosen strategy, assumptions, verification and revisit trigger. The primary agent decides whether to accept the recommendation under current scope and policy. A judgment is not proof of implementation, test success, or global goal completion.

## Integration checkpoints

- Planning: choose a safe strategy before assigning deliverables.
- Decomposition: use the accepted strategy to identify independent ownership, coupling and dependency order. Do not split work merely to increase parallelism.
- Recovery: compare targeted repair, safer alternative and escalation when the original strategy is invalidated. Preserve mandatory predicates; reverify affected evidence and recheck authorization.
- Completion report: state EngSense mode, material decision and any unresolved specialist/evidence gap. Report only actual activation, not hypothetical consultation.

## Reference

[EngSense repository](https://github.com/GendByteMaster/EngSense) and its [root Skill](https://github.com/GendByteMaster/EngSense/blob/main/SKILL.md) define EngSense behavior. Delegrix remains independently usable and does not require its installer or any new package dependency.
