# Delegrix

**Delegate intelligently. Execute safely. Verify everything.**

Delegrix is a portable, instruction-only **Agent Skill** for bounded AI subagent delegation. It helps a primary coding agent choose useful independent work, prepare precise worker assignments, avoid overlapping edits, verify worker handoffs, and integrate changes safely.

> Delegrix does **not** provide a subagent runtime, launch permissions, model router, or background workers. Actual operations depend on the capabilities and approvals of the host agent.

## How it fits

- **[ForgeGuard](https://github.com/GendByteMaster/ForgeGuard)**: engineering guardrails, user authorization, risk gates, goal definition, verification policy and delegation decision policy, when installed.
- **[ForgeScope](https://github.com/GendByteMaster/ForgeScope)**: broad engineering reviews, issue prioritization and evidence-based findings; Delegrix can help partition authorized specialist review work.
- **Delegrix**: the concrete delegated-work contract, worker ownership, dispatch waves, structured handoffs, and integration checks.
- **Project `AGENTS.md`**: local instructions and any stricter team-size, security or verification rules. Repository instructions never themselves authorize subagent spawning.

Both integrations are optional. Delegrix works without either Skill, using a conservative delegated-work flow and the host's actual capabilities.

See [integration workflows](skills/delegrix/references/integration-workflows.md) for behavior with ForgeGuard alone, ForgeScope alone, both together, or neither. These are **instruction-level integrations**: no hidden API calls, dependency on their CLI installers, or automatic modification of their state.

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
│   ├── handoff.md
│   └── preflight-example.json
├── references/
│   ├── integration-workflows.md
│   ├── decision.md
│   ├── dispatch-integration.md
│   ├── forgeguard-interop.md
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
```

The JSON flag `authorization.explicit` is only an *assertion* written in the plan: the primary agent must still verify live, scope-specific permission in the current conversation. A passing preflight checks structure, not worker behavior or actual consent. See the [interoperability guide](skills/delegrix/references/integration-workflows.md) for ForgeGuard and ForgeScope rules.

**These tests do not exercise actual subagent spawning, cancellation, approval handling, or multi-agent integration.** Real Codex/runtime smoke testing remains a separate acceptance gate.

## Status

- **v0.1.0**: Initial portable Skill and scoped worker templates.
- Compatibility intent: Codex and Agent Skills-capable hosts; exact features depend on host support.
- No production or multi-agent runtime acceptance is claimed yet.
## ForgeGuard-style CLI installation

Install from GitHub (no npm registry publication needed):

```bash
npx --yes github:GendByteMaster/Delegrix install --client codex --global
npx --yes github:GendByteMaster/Delegrix status --client codex --global
```

For a project install, omit `--global`. To use Claude Code or Cursor, select `--client claude` or `--client cursor`. `--client all` installs all clients, deduplicating shared project paths. `--dry-run` previews changes, `--force` refreshes managed files, and `uninstall` removes Delegrix files while leaving unrelated files alone. The CLI does not manage Codex subagent runtime configuration, approvals or ForgeGuard/ForgeScope workspaces.

After the tagged release, install reproducibly:

```bash
npx --yes github:GendByteMaster/Delegrix#v0.1.0 install --client codex --global
```

After optional npm publication: `npx @gendbytemaster/delegrix install --client codex --global`.

## Release process

Before merging PR, verify Python checks, Node CLI tests, Windows/Linux GitHub Actions and real authorized Codex subagent handoff behavior. On `main`, run **Create GitHub Release** (Actions → workflow_dispatch) with `v0.1.0`; it validates the artifact and publishes the tag and GitHub Release. Because releases created with the GitHub Actions token do not automatically trigger other GitHub Actions workflows, run **Publish npm** manually with the published tag if you want registry publication. This requires `NPM_TOKEN` to be configured. [Release notes](docs/releases/v0.1.0.md).
