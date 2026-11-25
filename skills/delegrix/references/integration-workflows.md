# Automatic companion activation and Goal workflow

Read on EVERY Delegrix invocation. Automatically attempt ForgeGuard and ForgeScope when installed; only the scope and depth of their work depends on the task. Native host Skill invocation is preferred. If unavailable, load installed Skill instructions instead, and report the distinction. Do not make up tool calls.

## Mandatory activation order

1. Read current-task approval, AGENTS.md and host capabilities. No Skill selection or Goal grants permission to spawn subagents.
2. ForgeGuard: activate the installed `engineering-guardrails` Skill through host-native invocation; else load and apply `engineering-guardrails/SKILL.md` and relevant policies. Record `host-activated`, `instructions-loaded` or `unavailable`.
3. Goal: create or reuse a measurable task-local Goal using [goal definition and routing](goal-definition.md) and [the goal template](../assets/task-goal.md), honoring installed ForgeGuard policy. It is attached to this task, NEVER a separate task, chat, thread, worktree or worker. For trivial tasks use local criteria; create native goal state only for explicit goal-backed intent, confirmed absence and supported host capabilities. Reuse compatible native state.
4. ForgeScope: activate the installed `forgescope` Skill using host-native selection; else load and apply its installed `SKILL.md` and relevant review rules. Record the actual mode. Select targeted review for coding tasks, analysis-only when requested, and full audit ONLY when justified. Do not mutate its ledger without review need.
5. Delegrix: decide meaningful delegation under existing permissions, build worker contracts, dispatch via host, verify handoffs, and reconcile Goal success and review findings using [lifecycle](goal-lifecycle.md) and [evaluation](goal-evaluation.md) for substantial work.
6. Report companion activation and Goal completion evidence honestly.

## Installed Skill detection

 The skills interact through **the primary agent's instructions**, not through APIs, imports, background processes or delegated permission grants. Delegrix remains usable on its own.

## Detect without side effects

1. Read applicable project instructions and the current user's authorization. Do not treat installing or invoking any Skill as permission to spawn workers.
2. Check for the installed `engineering-guardrails/SKILL.md` under supported agent-skill directories. Activate through the host if supported; otherwise read its installed Goal Intelligence, authorization, delegation, risk and verification policies. Do not rely solely on the version used while designing Delegrix.
3. On each Delegrix invocation, look for `forgescope/SKILL.md` and activate or load it when installed. Its review mode (especially analysis-only), evidence requirements and workspace ownership remain authoritative for that review.
4. Do not modify `AGENTS.md`, ForgeGuard-managed Codex configuration, or `.forgescope/REVIEW.md` as a consequence of detecting either Skill.
5. If either Skill is absent, mark its activation mode `unavailable`; disclose degraded integration and continue only when permitted by the user's scope and binding policies.

## Who owns which decision

| Decision or state | Primary authority |
| --- | --- |
| Whether delegation is permitted | User's current, scoped authorization + host platform; ForgeGuard policy when active |
| Goal guidance and risk gate | Delegrix [goal architecture](goal-architecture.md); installed ForgeGuard policy remains binding when active |
| Goal ownership and success evidence | Primary agent, within current task |
| Whether delegation is useful | ForgeGuard Delegation Intelligence, when active; Delegrix otherwise |
| Audit scope, finding severity and review evidence | ForgeScope, when active for a review |
| Worker assignment, dependency waves and write ownership | Delegrix, subject to all above constraints |
| Worker model, process, sandbox, actual spawn/cancel | Host runtime (no Skill may pretend to supply these) |
| Combined diff, tests and final acceptance | Primary agent; ForgeGuard/ForgeScope verification rules where relevant |

## Mode matrix

| Active Skills | Expected behavior |
| --- | --- |
| Delegrix only | Attempt both companions, mark unavailable, create local Goal, respect authorization and host capability |
| Delegrix + ForgeGuard | Auto-load ForgeGuard, create/reuse Goal, honor its policies and report ForgeScope missing |
| Delegrix + ForgeScope | Auto-load ForgeScope, create task-local Goal, select scoped review and report ForgeGuard missing |
| All three | Auto-activate ForgeGuard, establish Goal, auto-activate ForgeScope; Delegrix owns worker contracts; primary agent integrates and verifies |

## Delegation procedure

1. **Authorize and classify:** establish live-chat scope, applicable repository min/max and platform caps. If ForgeGuard is active, use its current delegation and Risk Gate policies. Authorization is permission, not a compulsory headcount unless a binding project rule explicitly sets one.
2. **Partition:** for a ForgeScope audit, partition by real subsystem or risk domain, request confirmed evidence with file/symbol references, and avoid overlapping implementation writes. Do not make speculative findings confirmed merely because a worker reported them.
3. **Preflight (optional):** prepare a temporary, deliberately non-secret JSON plan using [the example](../assets/preflight-example.json). Run `python skills/delegrix/scripts/check_plan.py path/to/plan.json`. Its `authorization.explicit` field is an **unverified declaration**, not an approval token. It cannot validate actual live user consent, worker competence, runtime capacities, or successful review. Resolve issues before dispatch and recheck on retries.
4. **Dispatch only through the host:** use capability-supported spawn/worktree/cancel methods and respect the total **launched** budget (including failed/replacement attempts), actual concurrency, depth and permissions.
5. **Handoff and verify:** apply the worker contract and handoff template, inspect real changes, make one primary-agent integration decision, and run relevant checks. ForgeScope retains control of `.forgescope/REVIEW.md` if it is active; ForgeGuard retains high-risk/critical approval rules.
6. **Report precisely:** distinguish planned, launched, meaningful, failed and replacement workers. Record whether validation was static, offline, CI, or live smoke testing. Do not report a passing preflight as proof of actual multi-agent execution.

## Conflict cases

- A project's `AGENTS.md` mandates eight meaningful workers, but the user authorizes three: do not exceed three, do not assert the project's completion gate passed, and do not fabricate worker count.
- A ForgeScope analysis-only review is requested: all workers remain read-only regardless of Delegrix's implementation capabilities. Producing a remediation plan is allowed; editing production code or creating a review ledger is not.
- ForgeGuard disallows or requires approval for a consequential operation: Delegrix cannot override the gate by allocating a different worker or provider.
- A worker finds a new high-risk issue outside its scope: return findings for the primary agent to review; don't silently enlarge scope or grant permissions.
- Two workers need one file or public contract: assign one writer and sequence dependent work, or use independent read-only reviews; avoid concurrent writes.

## Limits of the integration

This integration is **composable agent guidance**, not RPC or a live API bridge to ForgeGuard or ForgeScope. Neither project currently exposes a verified Delegrix-specific execution endpoint here. The optional preflight validator is a deterministic structural check only. Verify agent behavior with a real host runtime before claiming end-to-end interoperability.
