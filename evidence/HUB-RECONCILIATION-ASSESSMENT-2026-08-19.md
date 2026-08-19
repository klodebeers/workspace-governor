# Hub Reconciliation Assessment and Proposed Canonical Target Tree

**Date:** 2026-08-19
**Status:** Proposal. Not accepted. No source repository has been modified.
**Sources read:** `agents-hub-one` @ `47c0187`, `agents-hub-two` @ `0a222df`, `workspace-governor-agents-hub-one` @ `24798d0`
**Placement authority:** `workspace-governor-agents-hub-one/HUB-ARCHITECTURE.md`
**Procedure authority:** `workspace-governor-agents-hub-one/HUB-MANAGEMENT.md`

Classification verbs used are the recorded set: `Keep`, `Move`, `Generalize`,
`Specialize`, `Merge`, `Retire`, `Conflict`.

## 1. Identity conflict

Both sources declare themselves to be `.agents-hub`.

| Source | Claim | Evidence |
|---|---|---|
| `agents-hub-one` | "`.agents-hub` is the canonical runtime-neutral source system" | `README.md` line 3 |
| `agents-hub-two` | "the workspace root is `.` … which is the `.agents-hub` folder itself"; `"name": "agents-hub"` | `docs/README.md`; `package-layout.json` |

**Resolution:** neither is the canonical Hub. Both are inputs. The canonical
`.agents-hub` is the reconciled output.

**Basis — not age, filename, or apparent recency.** The two sources occupy
different placement layers under `HUB-ARCHITECTURE.md`:

- `agents-hub-one` supplies the **governance contract** — `rules/` with one
  authoritative owner per governed issue, plus the root control files
  (`README.md`, `CATALOG.md`, `STATE.md`) that the architecture requires.
- `agents-hub-two` supplies **ordinary non-governance artifacts** — agent
  definitions, discovery metadata, schemas, prompts and templates.

Measured, not asserted:

| Property | hub-one | hub-two |
|---|---|---|
| Governance contract | 5 owners, 3,159 words in `rules/` | 0 files contain "governance" |
| Precedence and routing | `rules/AGENTS.md` is the router | 0 files contain "precedence" |
| Runtime-neutral core | **0** occurrences of `claude`/`codex`/`cursor`/`copilot` across all 5 rule files | not applicable — no rule files |
| Inventory and continuity | `CATALOG.md`, `STATE.md` | 0 files contain "catalog" |
| Agent definitions | none | 15 |
| Reusable templates | 0 (four 0-byte placeholders) | 4 |

hub-one's runtime-neutrality is the property hardest to retrofit and is the
reason its governance core survives intact. hub-two's 15 agent definitions are
the only real content for the `agents\` domain, which the architecture approves
but which does not yet exist.

**Both halves are required.** Neither source alone satisfies what `.agents-hub`
must own.

## 2. Semantically equivalent rules to fold

`HUB-ARCHITECTURE.md` creation test item 3 forbids an artifact that duplicates a
responsibility already owned, including partial overlaps.

22 `rules` entries exist across hub-two's agent definitions. 16 touch a concern
already owned by a hub-one governance file. Those 16 split into two classes, and
the distinction determines the action.

**Class A — general-form governance restated inside an agent. Fold up.**

| hub-two statement | Owner that already holds it |
|---|---|
| "Do not claim a task is complete without verification" (`AGENT-AUTOMATION-BUILDER`) | `rules/VERIFICATION-AND-EVIDENCE.md` — "Never claim success from agent confidence alone" |
| "Do not instruct a human to share secrets or credentials in chat" (`AGENT-IAM-ACCESS`) | `rules/AUTONOMY-AND-PROTECTED-BOUNDARIES.md` — protected boundaries |
| "Document assumptions … explicitly" / "Do not hide unknown assumptions" (`AGENT-INTEGRATION`, `AGENT-REPORTING-DASHBOARD`) | `rules/VERIFICATION-AND-EVIDENCE.md` — proportionate evidence record |
| "Prioritize official documentation … over secondary blogs" (`AGENT-RESEARCH-DOCUMENTATION`) | `rules/VERIFICATION-AND-EVIDENCE.md` — verification standard |

Action: `Merge` — remove the general statement from the agent definition and
replace it with a reference to the owning rule. The rule text is not copied.

**Class B — domain-specific constraint that no rule owns. Preserve.**

Examples: "Validate the property type before writing a formula against it";
"Account for Notion formulas 2.0 changes"; "Confirm the exact source and target
databases before modifying relations"; "Do not claim authority to execute payment
transactions"; "Do not assume payment approvals are the same across companies".

Action: `Keep` with the owning agent. These are not governance; they are domain
knowledge, and folding them would lose capability.

`AGENT-PAYMENTS-BILLING`'s two entries are the highest-value Class B items: they
encode a per-company authority distinction that matches the user SSOT and that no
`rules/` file expresses.

## 3. Proposed canonical target tree

Domains are only those approved by `HUB-ARCHITECTURE.md`. No domain is created
empty.

```text
.agents-hub/
├── README.md                    from hub-one            Keep    navigation
├── CATALOG.md                   from hub-one            Merge   must register hub-two artifacts
├── STATE.md                     from hub-one            Keep    hub continuity
│
├── rules/                       ESTABLISHED CORE — from hub-one, unchanged
│   ├── AGENTS.md                                        Keep    router, precedence, owner eligibility
│   ├── ENGINEER-OWNERSHIP.md                            Keep    responsibility, intake, execution ownership
│   ├── AUTONOMY-AND-PROTECTED-BOUNDARIES.md             Keep    authority standard, escalation
│   ├── CONTEXT-AND-ORCHESTRATION.md                     Keep    context, delegation, handoff
│   └── VERIFICATION-AND-EVIDENCE.md                     Keep    done, verification, audit, evidence
│
├── agents/                      NEW DOMAIN — first accepted artifacts from hub-two
│   ├── general/
│   │   ├── AGENT-COORDINATOR-ORCHESTRATOR.json          Move    + Class A folds
│   │   ├── AGENT-AUTOMATION-BUILDER.json                Move    + Class A folds
│   │   ├── AGENT-IAM-ACCESS.json                        Move    + Class A folds
│   │   ├── AGENT-INTEGRATION.json                       Move    + Class A folds
│   │   ├── AGENT-PAYMENTS-BILLING.json                  Move    Class B preserved intact
│   │   ├── AGENT-REPORTING-DASHBOARD.json               Move    + Class A folds
│   │   ├── AGENT-RESEARCH-DOCUMENTATION.json            Move    + Class A folds
│   │   ├── AGENT-SYSTEM-DEPENDENCIES.json               Move    dependency model
│   │   ├── general-coordinator.prompt.txt               Move    owner-local, from prompts/
│   │   └── general-specialist.prompt.txt                Move    owner-local, from prompts/
│   ├── notion/
│   │   ├── NOTION-COORDINATOR-ORCHESTRATOR.json         Move
│   │   ├── NOTION-SCHEMA-RELATIONS-AGENT.json           Move
│   │   ├── NOTION-FORMULA-LOGIC-AGENT.json              Move
│   │   ├── NOTION-VIEWS-DASHBOARD-AGENT.json            Move
│   │   ├── NOTION-AUTOMATION-AGENT.json                 Move
│   │   ├── NOTION-DATA-QUALITY-TROUBLESHOOTING-AGENT.json  Move
│   │   ├── NOTION-SYSTEM-DEPENDENCIES.json              Move
│   │   ├── notion-coordinator.prompt.txt                Move    owner-local, from prompts/
│   │   └── notion-specialist.prompt.txt                 Move    owner-local, from prompts/
│   ├── registry.json                                    Move    from config/agent-registry.json
│   └── registry.schema.json                             Move    from schemas/
│
├── templates/                   NEW DOMAIN — first accepted artifacts from hub-two
│   ├── task-brief-template.json                         Move    cross-agent
│   ├── technical-spec-template.json                     Move    cross-agent
│   └── verification-checklist-template.json             Move    cross-agent
│
├── references/                  ESTABLISHED CORE — from hub-one
│   └── AGENTS-MD-LIVE-AUDIT-2026-08-16.md               Keep    overlap reconciliation still pending
│
├── runtime-adapters/            ESTABLISHED CORE — from hub-one
│   ├── codex/                                           Conflict  empty; see 5.2
│   └── claude-code/                                     Conflict  empty; see 5.2
│
└── design-systems/
    └── .remember/                                       PRESERVE UNCHANGED — stop condition B-2
```

### Retired

| Item | Source | Verb | Basis |
|---|---|---|---|
| `governance-templates/{workspace,project,component,delegation}/` | hub-one | `Retire` | Four 0-byte `placeholder.md` files. `HUB-ARCHITECTURE.md`: candidate domains "must not be created empty"; `templates/` is the approved destination and hub-two supplies its first real artifacts |
| `docs/README.md` | hub-two | `Merge` | `HUB-ARCHITECTURE.md` excludes "generic `docs\` when root navigation or owner-local documentation is sufficient". Unique content folds into root `README.md` and `CATALOG.md` |
| `package-layout.json` | hub-two | `Retire` | Self-description of the pre-consolidation layout; superseded by `CATALOG.md`. Not a distribution bundle, so `packages\` does not apply |
| `prompts/` as a top-level directory | hub-two | `Retire` | `HUB-ARCHITECTURE.md` excludes "`prompts\` when the prompt belongs to an agent, skill, workflow, or template". All four belong to a coordinator or specialist |
| `config/`, `schemas/` as top-level directories | hub-two | `Retire` | Not approved domains. Contents move to owner-local placement under `agents/` |

### Domains deliberately not created

`skills/`, `tools/`, `orchestration/`, `evaluations/`, `packages/`, `archive/` —
approved as candidates but no accepted artifact exists in either source. Creating
them would violate the no-empty-domain rule.

## 4. Ownership map

One owner per concern. Verified against `agents-hub-one/CATALOG.md`.

| Concern | Sole owner | Source |
|---|---|---|
| Contract scope, normative precedence, issue routing, governance-owner eligibility | `rules/AGENTS.md` | hub-one |
| Responsibility, intake, settled decisions, technical decision resolution, execution ownership, communication substance | `rules/ENGINEER-OWNERSHIP.md` | hub-one |
| Authority decision standard, protected boundaries, escalation | `rules/AUTONOMY-AND-PROTECTED-BOUNDARIES.md` | hub-one |
| Context control, long-project workflow, checkpoints, delegation, handoff | `rules/CONTEXT-AND-ORCHESTRATION.md` | hub-one |
| Definition of done, verification, audit, correction, evidence | `rules/VERIFICATION-AND-EVIDENCE.md` | hub-one |
| Agent roles, capabilities, routing logic, handoff contracts | `agents/<domain>/*.json` | hub-two |
| Agent discovery metadata and routing table | `agents/registry.json` | hub-two |
| Registry validation | `agents/registry.schema.json` | hub-two |
| Cross-agent scaffolds | `templates/*.json` | hub-two |
| Source inventory, lifecycle status, discovery index | `CATALOG.md` | hub-one, extended |
| Hub boundary and bootstrap navigation | `README.md` | hub-one |
| Hub continuity and unresolved work | `STATE.md` | hub-one |
| Runtime-specific loading and translation | `runtime-adapters/<runtime>/` | neither — unimplemented |

**No concern has two owners under this map.** The only overlaps found were the
Class A statements in section 2, resolved by folding.

## 5. Unresolved — requires a decision before execution

### 5.1 `execution-record-template.json` placement
Its fields (`database_names`, `formula_or_property_details`) are Notion-specific,
unlike the other three templates. `HUB-ARCHITECTURE.md`: "A template specific to
one agent, skill, tool, package, or workflow remains with that owner." Proposed:
move to `agents/notion/` as owner-local rather than `templates/`. Marked
unresolved because it is a judgement on intended reuse, not a structural fact.

### 5.2 Empty `runtime-adapters/` subdirectories
`HUB-ARCHITECTURE.md` lists `runtime-adapters/` as an **established core** domain,
but also forbids empty domains for **candidate** domains. Both subdirectories
contain a single 0-byte placeholder. The two statements do not resolve each other.
Recorded as `Conflict`, not silently decided. Retaining an empty core domain is the
conservative option and matches `agents-hub-one/STATE.md`, which already records
them as existing but unimplemented.

### 5.3 `agents/` subdivision by domain
Proposing `agents/general/` and `agents/notion/` because the registry already
models one coordinator plus specialists per domain. `HUB-ARCHITECTURE.md` neither
requires nor forbids subdivision. A flat `agents/` with the existing `AGENT-*` and
`NOTION-*` prefixes is equally defensible.

### 5.4 `references/AGENTS-MD-LIVE-AUDIT-2026-08-16.md`
`agents-hub-one/CATALOG.md` records it as "pending reconciliation with project
research to remove overlap without losing unique findings". Consolidation does not
resolve that; it carries forward.

### 5.5 GitHub sources are not the live Hub
`agents-hub-one` HEAD is a single commit titled "Placeholders" containing seven
0-byte files. `governance-templates/*`, `runtime-adapters/*` and `design-systems/`
are stubs. The live local Hub content is not represented in the repository. This
tree is proposed against repository evidence only; it must be re-verified against
the live Hub before execution.

## 6. Coverage proof

| Source | Files | Classified | Unaccounted |
|---|---|---|---|
| `agents-hub-one` | 16 | 16 | 0 |
| `agents-hub-two` | 27 | 27 | 0 |

hub-one: 5 rules `Keep`, 3 root control files (2 `Keep`, 1 `Merge`), 1 reference
`Keep`, 7 placeholders (4 `Retire`, 2 `Conflict`, 1 preserved unchanged).
hub-two: 15 agents `Move`, 1 registry `Move`, 1 schema `Move`, 4 prompts `Move`,
4 templates (3 `Move`, 1 unresolved), 1 docs `Merge`, 1 layout `Retire`.

## 7. What was not done

- No source repository was read for write, modified, or refactored. Stop
  condition B-1 requires target-tree acceptance first.
- `design-systems/.remember` was not read, hashed, or classified.
- No Gateway discovery was run and no Gateway code was written.
- Semantic overlap beyond the 22 `rules` entries and the root control files was
  not exhaustively proven; a full pairwise semantic diff of the five rule files
  against all 15 agent definitions was not performed.
- The live local Hub was not inspected. See 5.5.
