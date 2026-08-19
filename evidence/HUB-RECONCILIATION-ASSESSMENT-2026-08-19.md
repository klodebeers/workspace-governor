# Hub Reconciliation Assessment and Proposed Canonical Target Tree

**Date:** 2026-08-19
**Status:** Preliminary proposal, revision 2. Not accepted and not acceptable yet —
the GitHub sources are not the live Hub (section 5.5). No source repository has been
modified.

**Revision 2 (2026-08-19):** the four items previously listed as unresolved in
section 5 are resolved under `ENGINEER-OWNERSHIP` and recorded as `DECISIONS.md`
D-12 to D-15. One resolution reverses part of revision 1: field analysis shows
**three** of four templates are Notion-specific, not one. Section 3 and section 5
are updated accordingly.
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
│   │   ├── notion-specialist.prompt.txt                 Move    owner-local, from prompts/
│   │   ├── task-brief-template.json                     Move    owner-local (D-12): 3/12 fields Notion-coupled
│   │   ├── technical-spec-template.json                 Move    owner-local (D-12): 5/12 fields Notion-coupled
│   │   └── execution-record-template.json               Move    owner-local (D-12): 2/8 fields Notion-coupled
│   ├── registry.json                                    Move    from config/agent-registry.json
│   └── registry.schema.json                             Move    from schemas/
│
├── templates/                   NEW DOMAIN — one accepted artifact (D-12)
│   └── verification-checklist-template.json             Move    domain-neutral: 0 of 7 fields coupled
│
├── references/                  ESTABLISHED CORE — from hub-one
│   └── AGENTS-MD-LIVE-AUDIT-2026-08-16.md               Keep    overlap reconciliation still pending
│
├── runtime-adapters/            ESTABLISHED CORE — declared in CATALOG.md, not
│                                materialized as empty directories (D-13)
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

## 5. Engineering items — resolved

Resolved under `ENGINEER-OWNERSHIP`, from evidence, not routed to the user.
Recorded as `DECISIONS.md` D-12 to D-15.

### 5.1 Template placement — D-12

Classified from actual field content, not filename. Fields were tested for
coupling to Notion concepts (database, property, relation, formula, view, rollup):

| Template | Coupled fields | Verdict |
|---|---|---|
| `technical-spec-template.json` | 5 of 12 — `database_scope`, `properties_involved`, `relation_paths`, `formula_logic`, `view_requirements` | Notion-specific |
| `task-brief-template.json` | 3 of 12 — `database_name`, `properties_affected`, `related_databases` | Notion-specific |
| `execution-record-template.json` | 2 of 8 — `database_names`, `formula_or_property_details` | Notion-specific |
| `verification-checklist-template.json` | **0 of 7** — `check_name`, `method`, `expected_result`, `pass_criteria`, `fail_criteria`, `human_review_required`, `notes` | **Domain-neutral** |

`HUB-ARCHITECTURE.md`: "A template specific to one agent, skill, tool, package, or
workflow remains with that owner." Three templates go owner-local under
`agents/notion/`. Only `verification-checklist-template.json` is a cross-domain
scaffold and creates `templates/`.

This reverses revision 1, which had it backwards. An initial screen flagged
`human_review_required` as coupled; that was a false positive matching "view"
inside "review". Re-tested against field names and values: zero genuine coupling.

### 5.2 `runtime-adapters/` — D-13

The apparent contradiction dissolves once the logical domain is distinguished from
its filesystem materialization. `HUB-ARCHITECTURE.md` establishes
`runtime-adapters/` as a core **domain** — a declared destination. It does not
require an empty directory to exist to hold that place.

Both subdirectories contain one 0-byte `placeholder.md`. A 0-byte file is not an
artifact; it satisfies no part of the minimum artifact record. Retaining it
preserves nothing and creates a false impression of an adapter that
`agents-hub-one/README.md` and `STATE.md` both state does not exist.

Resolution: `Retire` the placeholder files. Declare `runtime-adapters/` in
`CATALOG.md` with lifecycle status "reserved; no accepted adapter; not installed,
active, or verified" — which is what the existing `CATALOG.md` already records.
Materialize the directory when the first real adapter is accepted.

### 5.3 `agents/` organization — D-14

Chosen from the artifacts and registry, not preference. Two findings decide it.

**The registry is structurally asymmetric.** It carries 8 top-level keys:

- `entry_point` → the Notion coordinator only
- `coordinator` → singular, Notion only
- `specialists` → 5 entries, all Notion
- `non_notion_agents` → 8 entries in a separate key
- `routing_rules` → contains only a `notion` key; no general routing exists

**The schema does not cover it.** `agent-registry.schema.json` declares 6
properties. `non_notion_agents` and `routing_rules` are absent, so both are
unvalidated. Entry shape is identical across `specialists` and
`non_notion_agents` (`id`, `name`, `path`, `role`), so the asymmetry is naming and
structure, not data shape.

Resolution: subdivide `agents/general/` and `agents/notion/`, matching the
coordinator-plus-specialists model the registry already implies, and normalize the
registry to a symmetric domain-keyed form so each domain declares its own
coordinator, specialists and routing, with all keys covered by the schema. A flat
`agents/` would leave the asymmetry unaddressed and keep general agents
second-class.

### 5.4 `references/` overlap — D-15

Investigated by direct comparison rather than carried forward.

| | `agents-hub-one/references/AGENTS-MD-LIVE-AUDIT` | `workspace-governor-agents-hub-one/research/AGENTS-MD-RESEARCH-AND-LIVE-AUDIT` |
|---|---|---|
| Substantive lines | 82 | 104 |
| Literally identical lines | 6 | 6 |
| Content | Live-state audit: 7 findings, correction sequence, completion status | Research (official guidance, what an AGENTS.md should contain, 8 subsections) **plus** an overlapping live-state narrative |

The overlap is real but confined: the audit's Findings 1–5 correspond to the
research document's Critical Live-State Problems 1–5. Everything else in each file
is unique — 76 lines unique to the audit, 98 to the research record.

Resolution by placement layer, which the existing rules already determine.
`HUB-ARCHITECTURE.md` layer 1 assigns cross-project canonical material to the Hub;
layer 2 assigns project-specific material to the project. A live-state audit **of
the Hub** is Hub evidence and stays in `references/`. Research about how to author
an `AGENTS.md` is project research — and `agents-hub-one/CATALOG.md` already
records that the combined record was relocated to the governor "because it is
Workspace Governor project research."

The duplicated live-state narrative in the project record should be replaced by a
reference to the Hub audit. Nothing unique is lost.

**Execution deferred, resolution not.** That trim edits
`workspace-governor-agents-hub-one`, a repository outside this consolidation's
scope. The decision is settled; the edit is sequenced separately.

## 6. Coverage proof

| Source | Files | Classified | Unaccounted |
|---|---|---|---|
| `agents-hub-one` | 16 | 16 | 0 |
| `agents-hub-two` | 27 | 27 | 0 |

hub-one (16): 5 rules `Keep`; 3 root control files — 2 `Keep`, 1 `Merge`;
1 reference `Keep` (D-15); 7 placeholders — 6 `Retire` (4 governance-templates,
2 runtime-adapters per D-13), 1 `design-systems` preserved unchanged (B-2).

hub-two (27): 15 agents `Move`; 1 registry `Move` and normalize (D-14); 1 schema
`Move` and extend (D-14); 4 prompts `Move` owner-local; 4 templates `Move` —
3 owner-local to `agents/notion/`, 1 to `templates/` (D-12); 1 docs `Merge`;
1 layout `Retire`.

Zero items remain classified `Conflict` or unresolved.

## 7. What was not done

- No source repository was read for write, modified, or refactored. Stop
  condition B-1 requires target-tree acceptance first.
- `design-systems/.remember` was not read, hashed, or classified.
- No Gateway discovery was run and no Gateway code was written.
- Semantic overlap beyond the 22 `rules` entries and the root control files was
  not exhaustively proven; a full pairwise semantic diff of the five rule files
  against all 15 agent definitions was not performed.
- The live local Hub was not inspected. See 5.5.
