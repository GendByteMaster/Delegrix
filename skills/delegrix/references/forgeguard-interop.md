# ForgeGuard and ForgeScope interoperability

Delegrix is a delegation-execution *skill*, not a replacement for either tool or a standalone subagent runtime. Load only the installed policies relevant to the current task; do not assume all installations are the same version.

| Responsibility | Owner |
| --- | --- |
| Explicit scope-specific approval | User and host; ForgeGuard policy when applicable |
| Goal measurability, risk classification, high-impact approval | ForgeGuard when active |
| Whether delegation is worthwhile | ForgeGuard Delegation Intelligence when active, otherwise Delegrix's conservative decision rubric |
| Review domains, finding severity, audit workspace, review synthesis | ForgeScope when active |
| Scoped worker brief, ownership isolation, dispatch waves, structured handoff | Delegrix |
| Runtime model/tool selection, actual spawn/stop/worktrees | Host agent runtime only |
| Overall plan, integration, final acceptance | Primary agent subject to project instructions |

See [optional integration workflows](integration-workflows.md) for an activation matrix, preflight procedure, read-only audit constraints, and failure handling.

## ForgeGuard

ForgeGuard v1.6.1 uses explicit current-conversation authorization, treats approval as permission rather than mandatory delegation, and defaults to delegation depth 1. Read and preserve the installed version's applicable `engineering-guardrails/SKILL.md`, `subagent-policy.md`, `delegation-intelligence.md`, `risk-gate.md` and `verification-policy.md`; do not recreate its gates in Delegrix or modify its managed runtime settings.

## ForgeScope

ForgeScope is a repository review and optimization Skill. When a ForgeScope review calls for delegated analysis, respect its own `skills/forgescope/references/subagents.md` guidance: partition by real risk domain and evidence, keep broad reviews primarily read-only, avoid duplicate findings, and have the primary agent independently verify high-impact claims. ForgeScope's `.forgescope/REVIEW.md` (if present) is a review workspace, not Delegrix state or a source of truth. Do not modify that workspace solely because Delegrix is active.

Independent read-only reviewers may inspect the same files; concurrent implementers must not write the same file or contract. A ForgeScope review must not silently widen the user's authorized delegation scope or permissions.

## Project-specific rules and conflicts

The repository's `AGENTS.md` may have a stricter project-defined substantive-worker minimum or other requirements (for example, Veridyn currently has a mandatory 8–28-worker workflow for covered work). Such rules do not themselves grant permission to spawn. A requested maximum is normally a ceiling, not a target, unless an applicable higher-priority project policy expressly requires a minimum. If authorization or platform capacity cannot satisfy a binding requirement, continue permitted work but mark that completion gate unmet; never manufacture workers or test results.

Preserve host and higher-priority instruction precedence. Do not edit ForgeGuard, ForgeScope, Codex configuration, model presets or third-party Skills as a side-effect of Delegrix invocation.
