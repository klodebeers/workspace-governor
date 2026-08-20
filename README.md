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
| `mcp-gateway` (repository) | Enforcement and access layer for Gateway-routed capabilities | Directive settled at `plans/MCP-GATEWAY.md`; not implemented |

## Authority relationship

```
agents-hub        = current canonical Agent Hub and live governance authority
workspace-governor = Agent Hub backoffice; manages, researches, reconciles,
                     backs up, archives, and improves the Hub
agents-hub-two     = source material pending reconciliation
```

`agents-hub` is **canonical now**. It is **not final**: it is under active
consolidation and is structurally incomplete where known gaps remain -- see
`STATE.md` for the current gap list and `evidence/` for the findings behind it.
Canonical status means governed agents and runtimes take their governance from
it, not that its structure is settled.

`agents-hub-two` is source material pending reconciliation. It is **not a
competing authority** and must not be treated as one, notwithstanding its own
self-description.

## Repository relationships

| Repository | Relationship | Verified content |
|---|---|---|
| `klodebeers/agents-hub` | **Current canonical Agent Hub and live governance authority.** Renamed from `agents-hub-one` on 2026-08-20. Canonical now; under active consolidation; structurally incomplete where known gaps remain. | 16 files at `47c0187`. Governance tree: `rules/` five-file contract, `CATALOG.md`, `STATE.md`, `README.md`. Seven 0-byte placeholder files |
| `klodebeers/workspace-governor` | This repository. **Agent Hub backoffice:** research, reconciliation, change preparation, evidence, backups, archives, recovery and provenance, and the implementation work that updates or corrects the canonical Hub. | `mcp-gateway` directive; control files; SSOT pair; discovery and inventory tooling; evidence |
| `klodebeers/agents-hub-two` | **Source material pending reconciliation.** Not a competing authority. | 27 files. Agent operating package: 15 agent definitions, `config/agent-registry.json`, schemas, prompts, templates. Single commit `0a222df` "Initial Commit" |
| `klodebeers/workspace-governor-agents-hub-one` | **Predecessor backoffice for the same Hub.** Predecessor management history, not a competing authority. Reviewed and classified 2026-08-20; still-valid work carried forward into `plans/`. Not a Hub. A different repository from `agents-hub`. | 47 files. `HUB-ARCHITECTURE.md`, `HUB-MANAGEMENT.md`, `HUB-DOCUMENTATION.md`, `AGENTS.md`, `STATE.md`, plan, research, evidence, versions |
| `klodebeers/atrium_workspace` | Human visibility and approval surface. Consumes the control plane; never a governance source. | Tauri and React dashboard application |
| `klodebeers/agent-governance-toolkit` | Unmodified public fork of `microsoft/agent-governance-toolkit` (MIT). Reference only, not adopted. | 3,640 files, v3.5.0 |

`agents-hub-two` still declares itself to be `.agents-hub` in its own content.
That self-description is superseded: authority is settled per the table above.
Correcting the stale claim is part of the reconciliation task, not an open
question about which repository is canonical.

A GitHub repository rename leaves redirects in place, so existing clone URLs and
remotes for `agents-hub-one` continue to resolve. A local clone directory is
**not** renamed by it; the discovery tooling therefore probes both `agents-hub`
and the legacy `agents-hub-one` leaf.

## Contents

| Path | What it is |
|---|---|
| `AGENTS.md` | Operating instructions. **Read first.** Defines bootstrap order and file ownership. |
| `STATE.md` | Canonical current-state record |
| `DECISIONS.md` | Settled decisions, append-only |
| `plans/MCP-GATEWAY.md` | Agent-Agnostic MCP Gateway build directive, 46 sections. Moved from the repository root 2026-08-20; content unchanged |
| `plans/AGENT-HUB-CONSOLIDATION.md` | Active Hub consolidation plan, carrying forward the predecessor plan v0.4.2 |
| `plans/reference/` | Provenance copies of superseded plans. Never executable |
| `scripts/` | Discovery and verification tooling |
| `evidence/` | Dated evidence outputs |

`AGENTS.md` § File ownership is authoritative on which file owns which concern.
