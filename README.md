# Workspace Governor

Persistent management and orchestration repository for the agent control plane.

This repository holds durable project state, settled decisions, operating
instructions, and control-plane build directives. It is the repository a new
agent session reads first to understand where the project stands.

It is **not** the Agent Hub, not the Gateway implementation, and not a runtime.

## Scope

| In scope | Out of scope |
|---|---|
| Durable project state and decisions | Canonical shared governance content (belongs in `.agents-hub`) |
| Control-plane build directives | Gateway runtime and operational state |
| Reconciliation planning for the two Hub source repositories | Secrets, credentials, session state, logs, caches |
| Discovery and verification tooling | Runtime-specific agent configuration |

## Managed components

Three architecture components. Only the first exists here.

| Component | Role | Status |
|---|---|---|
| `workspace-governor` | Management and orchestration. This repository. | Active |
| `.agents-hub` | Canonical desired state — shared governance, policies, skills, agent definitions, schemas, registries | **Does not yet exist.** To be produced by reconciling two source repositories |
| `mcp-gateway` | Enforcement and access layer for Gateway-routed capabilities | Directive settled; not implemented |

## Repository relationships

| Repository | Relationship | Verified content |
|---|---|---|
| `klodebeers/workspace-governor` | This repository | `mcp-gateway` directive; control files; discovery tooling |
| `klodebeers/agents-hub-one` | **Source A** for the final canonical `.agents-hub` | 16 files. Governance tree: `rules/` five-file contract, `CATALOG.md`, `STATE.md`, `README.md`. Seven 0-byte placeholder files. Single commit `47c0187` "Placeholders" |
| `klodebeers/agents-hub-two` | **Source B** for the final canonical `.agents-hub` | 27 files. Agent operating package: 15 agent definitions, `config/agent-registry.json`, schemas, prompts, templates. Single commit `0a222df` "Initial Commit" |
| `klodebeers/workspace-governor-agents-hub-one` | Management and planning repository for the **existing Hub One work**. Not a Hub. Not `agents-hub-one`. | 47 files. `HUB-ARCHITECTURE.md`, `HUB-MANAGEMENT.md`, `HUB-DOCUMENTATION.md`, `AGENTS.md`, `STATE.md`, plan, research, evidence, versions |
| `klodebeers/atrium_workspace` | Human visibility and approval surface. Consumes the control plane; never a governance source. | Tauri and React dashboard application |
| `klodebeers/agent-governance-toolkit` | Unmodified public fork of `microsoft/agent-governance-toolkit` (MIT). Reference only, not adopted. | 3,640 files, v3.5.0 |

Both source repositories currently declare themselves to be `.agents-hub`.
Resolving that is the reconciliation task.

## Files in this repository

| File | Owns |
|---|---|
| `README.md` | Purpose, scope, managed components, repository relationships |
| `STATE.md` | Current verified state, phase, blockers, open work, next action. **Canonical current-state record.** |
| `DECISIONS.md` | Settled decisions with rationale. Append-only. |
| `AGENTS.md` | Operating instructions and bootstrap order |
| `mcp-gateway` | Agent-Agnostic MCP Gateway build directive, 46 sections |
| `scripts/` | Discovery and verification tooling |
| `evidence/` | Dated evidence outputs |

Read `AGENTS.md` first for bootstrap order.
