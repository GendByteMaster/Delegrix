# Optional integration workflows

Use this page only when ForgeGuard or ForgeScope is installed and the current task makes that integration useful. The skills interact through **the primary agent's instructions**, not through APIs, imports, background processes or delegated permission grants. Delegrix remains usable on its own.

## Detect without side effects

1. Read applicable project instructions and the current user's authorization. Do not treat installing or invoking any Skill as permission to spawn workers.
2. Check for ForgeGuard's installed `engineering-guardrails/SKILL.md` under supported agent-skill directories. If present, read its installed version's authorization, delegation-intelligence, risk and verification references **as applicable**. Do not rely solely on the version used while designing Delegrix.
3. If a repository audit is requested, check for `forgescope/SKILL.md` and its `references/subagents.md`. Its review mode (especially analysis-only), evidence requirements and workspace ownership remain authoritative for that review.
4. Do not modify `AGENTS.md`, ForgeGuard-managed Codex configuration, or `.forgescope/REVIEW.md` as a consequence of detecting either Skill.
5. If neither is installed, apply Delegrix's bounded-worker policy and repository instructions without claiming either integration was used.

## Who owns which decision

| Decision or state | Primary authority |
| --- | --- |
| Whether delegation is permitted | User's current, scoped authorization + host platform; ForgeGuard policy when active |
| Goal and risk gate | ForgeGuard, when active |
| Whether delegation is useful | ForgeGuard Delegation Intelligence, when active; Delegrix otherwise |
| Audit scope, finding severity and review evidence | ForgeScope, when active for a review |
| Worker assignment, dependency waves and write ownership | Delegrix, subject to all above constraints |
| Worker model, process, sandbox, actual spawn/cancel | Host runtime (no Skill may pretend to supply these) |
| Combined diff, tests and final acceptance | Primary agent; ForgeGuard/ForgeScope verification rules where relevant |

## Mode matrix

| Active Skills | Expected behavior |
| --- | --- |
| Delegrix only | Explicit approval and host capability first; bounded, evidence-backed independent assignments |
| Delegrix + ForgeGuard | Reuse ForgeGuard authorization/delegation/risk/verification decisions; Delegrix builds and checks concrete worker contracts |
| Delegrix + ForgeScope | ForgeScope selects review depth and evidence standards; Delegrix partitions authorized investigative scopes, preferably read-only |
| All three | ForgeGuard gates actions; ForgeScope owns the review and any ledger; Delegrix owns dispatch briefs, isolation and handoffs; primary agent synthesizes and verifies |

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
