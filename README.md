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

## Install

For Codex, copy the `skills/delegrix/` directory to one of:

- User-wide: `$HOME/.agents/skills/delegrix/`
- Repository-local: `<repo>/.agents/skills/delegrix/`

Verify `SKILL.md` exists at the resulting path, restart the agent session if needed, then invoke **`$delegrix`** in a compatible client. It can also be selected implicitly when the host supports Skill selection. This repository does not ship an installer or assume a specific client runtime.

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
│   └── handoff.md
├── references/
│   ├── decision.md
│   ├── dispatch-integration.md
│   ├── forgeguard-interop.md
│   ├── scenarios.md
│   └── worker-contract.md
└── scripts/validate.py
```

## Validation

```
python skills/delegrix/scripts/validate.py
```

This static validator checks package metadata, local references and basic policies. It **does not** exercise actual subagent spawning, cancellation, or integration behavior; runtime smoke tests must be done with a supported host and explicit approval.

## Status

- **v0.1.0**: Initial portable Skill and scoped worker templates.
- Compatibility intent: Codex and Agent Skills-capable hosts; exact features depend on host support.
- No production or multi-agent runtime acceptance is claimed yet.