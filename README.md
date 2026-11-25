# Delegrix

**Delegate intelligently. Execute safely. Verify everything.**

Delegrix is a portable, instruction-only **Agent Skill** for goal-driven agent orchestration and bounded AI subagent delegation. It helps a primary coding agent choose useful independent work, prepare precise worker assignments, avoid overlapping edits, verify worker handoffs, and integrate changes safely.

> Delegrix does **not** provide a subagent runtime, launch permissions, model router, or background workers. Actual operations depend on the capabilities and approvals of the host agent.

## How it fits

- **[ForgeGuard](https://github.com/GendByteMaster/ForgeGuard)**: engineering guardrails, user authorization, risk gates, applicable goal policy, verification policy and delegation decision policy, when installed.
- **[ForgeScope](https://github.com/GendByteMaster/ForgeScope)**: broad engineering reviews, issue prioritization and evidence-based findings; Delegrix can help partition authorized specialist review work.
- **[EngSense](https://github.com/GendByteMaster/EngSense)**: optional engineering judgment for material strategy, decomposition and repair decisions.
- **Delegrix**: measurable goals, criterion-linked delegation, evidence tracking, bounded recovery, and integration checks.
- **Project `AGENTS.md`**: local instructions and any stricter team-size, security or verification rules. Repository instructions never themselves authorize subagent spawning.

**Automatic startup:** when invoked, Delegrix proactively activates installed ForgeGuard first, defines/reuses a measurable Goal in the CURRENT task, then activates installed ForgeScope for proportionate review. If no host-native Skill invocation exists, it loads installed Skill instructions rather than inventing process execution. ForgeGuard and ForgeScope remain optional and are attempted by default. EngSense is consulted conditionally; missing companions never grant permissions or satisfy mandatory gates.

See [Goal contract](skills/delegrix/assets/task-goal.md) and [integration workflows](skills/delegrix/references/integration-workflows.md) for behavior with ForgeGuard alone, ForgeScope alone, both together, or neither. These are **instruction-level integrations**: no hidden API calls, dependency on their CLI installers, or automatic modification of their state.

## Goal Intelligence v2

Use a single logical goal within the current task. Native goal creation requires explicit goal-backed intent, confirmed absence of a compatible active goal and supported host tools. Routine work uses concise local criteria. No extra task, thread, goal database or automatic worker launch is required.

- [Goal definition and routing](skills/delegrix/references/goal-definition.md)
- [Lifecycle, evidence freshness and drift](skills/delegrix/references/goal-lifecycle.md)
- [Criterion-linked decomposition](skills/delegrix/references/goal-decomposition.md)
- [Evaluation and completion gate](skills/delegrix/references/goal-evaluation.md)
- [EngSense integration](skills/delegrix/references/engsense-interop.md)
- [Bounded recovery](skills/delegrix/references/goal-recovery.md)

A worker contributes to criteria; the primary agent verifies the integrated result. All mandatory criteria and applicable review/approval gates must pass. Default repair limits are two attempts per episode and four per goal, with stricter policies taking precedence.

## Install

For Codex, copy the `skills/delegrix/` directory to one of:

- User-wide: `$HOME/.agents/skills/delegrix/`
- Repository-local: `<repo>/.agents/skills/delegrix/`

Verify `SKILL.md` exists at the resulting path, restart the agent session if needed, then invoke **`$delegrix`** in a compatible client. It can also be selected implicitly when the host supports Skill selection. The repository also ships a portable CLI installer. Installing it does not configure a runtime or grant subagent authorization.

## Example

```
Use $delegrix to partition this authorized task into independent components,
assign non-overlapping ownership, and integrate only evidence-backed work.
You may use up to 3 subagents for this scope.
```

A worker assignment includes **objective, owned and forbidden scope, constraints, acceptance criteria, verification, and required handoff**. The primary agent checks actual diffs and test evidence before accepting a worker's output.

## Repository layout

```
skills/delegrix/
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── worker-brief.md
│   ├── task-goal.md
│   ├── handoff.md
│   ├── preflight-example.json
│   └── goal-preflight-example.json
├── references/
│   ├── integration-workflows.md
│   ├── decision.md
│   ├── dispatch-integration.md
│   ├── forgeguard-interop.md
│   ├── engsense-interop.md
│   ├── goal-architecture.md
│   ├── goal-definition.md
│   ├── goal-lifecycle.md
│   ├── goal-decomposition.md
│   ├── goal-evaluation.md
│   ├── goal-recovery.md
│   ├── scenarios.md
│   └── worker-contract.md
└── scripts/
    ├── validate.py
    └── check_plan.py
tests/
├── fixtures/preflight_cases.json
├── test_preflight.py
└── test_packaging.py
.github/workflows/ci.yml
```

## Validation and CI

Run the offline checks (Python standard library only):

```bash
python skills/delegrix/scripts/validate.py
python -m unittest discover -s tests -p "test_*.py" -v
```

GitHub Actions runs these checks on Linux and Windows with Python 3.11 and 3.13 for pushes and pull requests. The tests cover static skill packaging and **20+ deterministic preflight scenarios**: worker authorization declarations, overlapping writes, dependency cycles, project and runtime caps, replacement budgets, and ForgeScope read-only mode.

Optionally validate a proposed worker plan before delegating:

```bash
python skills/delegrix/scripts/check_plan.py skills/delegrix/assets/preflight-example.json
python skills/delegrix/scripts/check_plan.py skills/delegrix/assets/goal-preflight-example.json
```

Schema v1 remains supported. Schema v2 adds goal criterion coverage; it does not prove evidence or completion.

The JSON flag `authorization.explicit` is only an *assertion* written in the plan: the primary agent must still verify live, scope-specific permission in the current conversation. A passing preflight checks structure, not worker behavior or actual consent. See the [interoperability guide](skills/delegrix/references/integration-workflows.md) for ForgeGuard and ForgeScope rules.

**These tests do not exercise actual subagent spawning, cancellation, approval handling, or multi-agent integration.** Real Codex/runtime smoke testing remains a separate acceptance gate.

## Status

- **v0.1.0**: previous released baseline.
- **v0.2.0**: release with documented runtime limitations for [issue #2](https://github.com/GendByteMaster/Delegrix/issues/2); see [release notes](docs/releases/v0.2.0.md). Full runtime acceptance remains open.
- Compatibility intent: Codex and Agent Skills-capable hosts; exact features depend on host support.
- The pre-promotion candidate passed automated CI and two user-reported Copilot smoke scenarios, including a controlled recovery and independent review. Codex, Claude Code, Cursor and negative recovery acceptance remain open. No general production-readiness claim is made.
## ForgeGuard-style CLI installation

Install from GitHub (no npm registry publication needed):

```bash
npx --yes github:GendByteMaster/Delegrix install --client codex --global
npx --yes github:GendByteMaster/Delegrix status --client codex --global
```

For a project install, omit `--global`. To use Claude Code or Cursor, select `--client claude` or `--client cursor`. `--client all` installs all clients, deduplicating shared project paths. `--dry-run` previews changes, `--force` refreshes managed files, and `uninstall` removes Delegrix files while leaving unrelated files alone. The CLI does not manage Codex subagent runtime configuration, approvals or ForgeGuard/ForgeScope workspaces.

For the previous published baseline, install reproducibly:

```bash
npx --yes github:GendByteMaster/Delegrix#v0.1.0 install --client codex --global
```

For v0.2.0, after the tag is published, pin `github:GendByteMaster/Delegrix#v0.2.0` for reproducible installation.

After optional npm publication: `npx @gendbytemaster/delegrix install --client codex --global`.

## Git checkout installation (when npm rejects Git dependencies)

If npm reports `EALLOWGIT`, leave its policy unchanged. Clone the candidate to a separate source directory and run the bundled CLI directly from the intended target project:

```powershell
$src = Join-Path $env:TEMP ("delegrix-src-" + [guid]::NewGuid().ToString("N"))
git clone https://github.com/GendByteMaster/Delegrix.git $src
# Review the checkout and record the source commit before installing.
git -C $src rev-parse HEAD
node "$src/bin/delegrix.js" install --client codex
node "$src/bin/delegrix.js" status --client codex
```

For an existing managed project installation, use `node "$src/bin/delegrix.js" update --client codex --dry-run` and then `node "$src/bin/delegrix.js" update --client codex`. Add `--global` only for a deliberate user-wide installation or update. Pin a reviewed commit with `git -C $src checkout --detach <commit-sha>` when reproducibility matters.

## Updating Delegrix

Use the `update` command to refresh an **existing** Delegrix Skill from the source package currently invoked:

```powershell
# Latest repository default branch (after the PR is merged):
npx --yes github:GendByteMaster/Delegrix update --client codex --global

# Preview file changes without writing:
npx --yes github:GendByteMaster/Delegrix update --client codex --global --dry-run

# Verify the installed Skill version:
npx --yes github:GendByteMaster/Delegrix status --client codex --global
```

To update from the published v0.2.0 tag (once available):

```powershell
npx --yes "github:GendByteMaster/Delegrix#v0.2.0" update --client codex --global
```

`update` verifies that the installation belongs to Delegrix, compares shipped files, refreshes changed managed files and leaves unrelated files in the Skill directory untouched. It refuses missing or unmanaged installations (use `install` for first-time setup), and refuses symbolic-link traversal. `--dry-run` previews the operation. Restart the coding-agent session after updating.

**Source semantics:** the CLI does not poll GitHub or self-upgrade a permanently installed npm executable. To fetch newer source, invoke `npx --yes github:GendByteMaster/Delegrix ...`, optionally pinning a branch/tag. Using `delegrix update` with a globally installed CLI only reapplies the version already packaged with that CLI. Updates may overwrite user edits to shipped Skill files; keep custom policy in the repository's own instructions, not inside managed Skill files.

## Release process

Before merging PR, verify Python checks, Node CLI tests and Windows/Linux GitHub Actions. Document outstanding runtime validation explicitly; release with unresolved runtime checks requires maintainer approval and must not claim full interoperability. On `main`, run **Create GitHub Release** (Actions → workflow_dispatch) with the tag matching approved package metadata and versioned release notes; it validates the artifact and publishes the tag and GitHub Release. Because releases created with the GitHub Actions token do not automatically trigger other GitHub Actions workflows, run **Publish npm** manually with the published tag if you want registry publication. This requires `NPM_TOKEN` to be configured. [v0.2.0 release notes](docs/releases/v0.2.0.md) · [v0.1.0 release notes](docs/releases/v0.1.0.md).
