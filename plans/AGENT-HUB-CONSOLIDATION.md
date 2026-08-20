# Agent Hub Consolidation -- Active Plan

**Type:** Backoffice planning record. **Not live governance.** Must not become a
competing authority.
**Plan owner:** `workspace-governor` (Agent Hub backoffice)
**Target:** the single logical Agent Hub, in both its representations
**Version:** 0.6.0
**Baseline date:** 2026-08-20

**One Hub, two representations.** The `.agents-hub` repository is the canonical
source. `C:\Users\Chloe\.agents-hub` is its local materialized location for agent
consumption. They are **the same logical Hub**, not two authorities, and must not
drift independently. Any change lands in the repository and is materialized
locally; a local-only edit is drift, not a decision.
**Status:** Execution-ready for Step 1 onward; not started

## 1. Authority boundary

This plan **sequences work**. It creates no governance. Governance lives in the
canonical Hub: its root `AGENTS.md` is the bootstrap, router and precedence owner
and routes to the four topic owners. Load the Hub owner for any governed issue
encountered here. Do not restate, paraphrase, narrow or broaden a Hub rule in this
file.

`AGENT-SSOT.json` and `USER-SSOT.json` are Agent Hub assets. Copies in
`workspace-governor` are staging and provenance only (`DECISIONS.md` D-25).

## 2. Provenance -- what this plan is

This is **not a new plan.** It carries forward
`AGENT-HUB-IMPLEMENTATION-PLAN.md` v0.4.2 from the predecessor backoffice
`workspace-governor-agents-hub-one` @ `24798d0`, which was verified twice and left
execution-ready but never started. A verbatim provenance copy is at
`plans/reference/AGENT-HUB-IMPLEMENTATION-PLAN-v0.4.2-predecessor.md`.

Its 12-step sequence, authority and boundary map, execution controls, rollback
strategy and completion criteria are **reused unchanged** unless a delta is
recorded in section 4. Full classification of prior material:
`evidence/PREDECESSOR-BACKOFFICE-REVIEW-2026-08-20.md`.

## 3. Carried forward unchanged

Reuse these directly. Do not re-derive them.

| Carried forward | Source | Why still valid |
|---|---|---|
| 12-step execution sequence, Step 0 to Step 12, with prerequisites, prohibited changes, verification method, evidence and completion gate per step | v0.4.2 § 6 | Structure is target-agnostic; each gate remains correct |
| Authority and boundary map across Governor / Hub / adapters / projects | v0.4.2 § 2 | Matches the current authority relationship |
| Execution controls common to every step, 10 items | v0.4.2 § 5 | Version-preservation and smallest-change discipline unchanged |
| Rollback and recovery strategy | v0.4.2 § 7 | Unchanged |
| Final completion criteria | v0.4.2 § 8 | Unchanged |
| Four placement layers; one-owner-per-concern; governance-owner creation test | `HUB-ARCHITECTURE.md`, Hub `rules/AGENTS.md` | Already canonical |
| Classification verbs: Keep, Move, Generalize, Specialize, Merge, Retire, Conflict | v0.4.2 § 4.1, `HUB-MANAGEMENT.md` | Already in use in this backoffice |
| Dated-baseline supersession rule: never silently rewrite a dated baseline; issue a later dated audit citing it | `evidence/BASELINE-AUDIT-2026-08-16.md` | Adopted as the standard for every inventory this plan produces |

## 4. Deltas since v0.4.2

Only these change. Everything else in section 3 stands.

| # | Delta | Effect on the plan |
|---|---|---|
| D-a | **A second source repository exists.** v0.4.2 knew only the live Hub. `agents-hub-two` holds 27 files -- 15 agent definitions, `config/agent-registry.json`, schemas, prompts, templates -- and is source material pending reconciliation. | Step 1 classification must cover three inputs: the live `.agents-hub`, canonical `.agents-hub`, and `agents-hub-two`. Step 8 migration now has a real accepted-source candidate, where v0.4.2 anticipated possibly none. |
| D-b | **The canonical Hub is now named and settled.** `.agents-hub` is canonical (`DECISIONS.md` D-24), superseding the two-repositories-both-claiming-identity condition. | Removes the identity question from Step 1. Step 1 decides structure, not which repository governs. |
| D-c | **Hub root `AGENTS.md` is misplaced inside `rules/`.** Verified: `.agents-hub` has `rules/AGENTS.md` and no root `AGENTS.md`. | Add to Step 1 classification as a `Move`, executed in Step 5. Structural only, no content change. Deferred by instruction from the canonicalization step. |
| D-d | **The SSOT pair must be placed in the Hub** with scope-based routing, `USER-SSOT.json` loaded only in Greyed context. | New work inside Step 5 and Step 10. Placement alone is insufficient: the Hub root router needs entries or the assets are unreachable. See `evidence/HUB-ASSET-PLACEMENT-CORRECTION-2026-08-20.md`. |
| D-e | **Three conflict-resolution coverage gaps** are recorded: peer agent output conflict (live), same-level requirement contradiction (plausible), stakeholder-goal conflict (latent). | Step 3 semantic-owner work must close G-1 and G-2 as sections in existing owners. No new rule file. `PENDING-GLOBAL-PROMOTIONS.md` P-04. |
| D-f | **Verification scoping is now a rule** and duplicates an SSOT section. | Step 3 must resolve the duplicate ownership. `PENDING-GLOBAL-PROMOTIONS.md` P-01, P-03. |
| D-g | **Live-Hub evidence exists but is stale.** `BASELINE-AUDIT-2026-08-16.md` inventories the live `.agents-hub` as of 2026-08-16. It is 4 days old and says to re-inspect. | Step 1 does not start from zero. Use it as the prior baseline and produce a later dated audit citing it, per the supersession rule. Read-only tooling exists: `scripts/Invoke-HubInventory.ps1`. |
| D-h | **Read-only inventory tooling now exists and is executed-verified** under PowerShell 7 against fixtures. | Step 1 inventory is a tooling run, not a manual walk. Windows PowerShell 5.1 and the live Hub remain unverified. |

## 5. Conflict and gap register

Predecessor identifiers mapped to current ones. One row per real issue; no duplicates.

| v0.4.2 | Current | Issue | Status |
|---|---|---|---|
| C-01 | B-3 | Codex authority file has stale `C:\Users\ByteBoss\...` paths and overlaps Hub-owned responsibilities | Open. Blocks Codex adapter activation only. Needs user authorization to open as a scoped change (D-11). |
| C-02 | B-2 | `design-systems/.remember` provenance and sensitivity unresolved | Open. Existence-only handling enforced in tooling. Blocks classification of that area only. |
| C-03 | -- | Claude Code instruction placement enforces nothing on its own; an enforcement carrier must be chosen per rule | Open, **narrowed and restated 2026-08-20**. The carried-forward wording -- "project instructions outrank global governance" -- conflated advisory instructions with enforced settings. Managed settings cannot be overridden by a project. Blocks adapter finalization only. `evidence/RUNTIME-CONVENTIONS-2026-08-20.md` |
| G-01 | -- | Hub reference audit overlaps project research; unique evidence not mapped | Open. Carried forward. Step 6. |
| G-02 | -- | Third-party scaffolder provenance and licence not accepted | Open. Matches the `agent-governance-toolkit` open item. |
| G-03 | B-5 | Runtime discovery, permissions, hooks and activation behavior may drift | Open. Local execution required. |
| G-04 | -- | Human glossary has no accepted artifact or placement | Open. Blocks nothing. |
| G-05 | -- | No accepted repository-delivery workflow artifact | Open. Blocks nothing. |
| -- | B-1 | Target tree and ownership map not accepted | Open. This plan's Step 1 resolves it. |
| -- | B-6 | Live `.agents-hub` content not currently verified | Open, **narrowed** by D-g. |

## 6. Accepted canonical taxonomy

Directive-given, 2026-08-20. **Validate every directory against actual content
before creating it.** The final tree is the smallest structure real artifacts
justify. Do not create empty or speculative directories, and do not add a
directory because another system uses the name.

```text
.agents-hub/
|-- AGENTS.md            root bootstrap, router, precedence -- non-negotiable
|-- README.md
|-- CATALOG.md           only if existing registry/discovery work justifies it
|-- rules/               human- and agent-readable governance
|-- policies/            machine-verifiable enforcement definitions
|-- registry/            canonical identity and classification
|-- agents/              agent definitions -- who or what can act
|-- skills/              reusable procedural capabilities
|-- prompts/             reusable canonical prompts only
|-- tools/               canonical tool/capability definitions, not discovery state
|-- orchestration/       selection, routing, sequencing, coordination, handoff,
|                        composition, verification
|-- runbooks/            durable operational procedures for agents
|-- templates/
|-- context/             scoped operating context, not knowledge or authorization
|-- runtime-adapters/    mappings to runtime-native representations
`-- references/          supporting references, not backoffice history
```

`orchestration/`, never `workflows/`. Do not add `packages/`, `evaluations/`,
`workflows/` or any other top-level directory without actual shared artifacts.

### 6.1 Non-negotiable bootstrap

`.agents-hub/AGENTS.md` at the **root** is the visible repository-level router,
bootstrap and precedence entrypoint. `rules/AGENTS.md` is **not** the canonical
router.

**This supersedes the predecessor decision** that placed the router at
`rules/AGENTS.md` (v0.4.2 § 4.1, `HUB-ARCHITECTURE.md` § Root control files).
Preserve the governing meaning when moving the file, update inbound references,
and do not combine the move with unrelated refactoring. Recorded as delta D-c.

### 6.2 Taxonomy conflicts with the predecessor architecture

Surfaced, not blended. `HUB-ARCHITECTURE.md` is classified *reusable with
adaptation*; these are the adaptations, and the directive governs.

| Concern | Predecessor position | Directive position | Resolution |
|---|---|---|---|
| `policies/` | Do not create; governance belongs to `rules/` | Required, for machine-verifiable enforcement | Directive governs. `rules/` holds readable governance; `policies/` holds executable enforcement. Machine policies must trace to their governing rule. Do not state the same requirement in both. |
| `prompts/` | Do not create; a prompt belongs to its agent, skill, workflow or template | Required, for reusable canonical prompts only | Directive governs, narrowly: only prompts that are canonical and reusable in their own right. An agent- or skill-specific prompt still stays with its owner. |
| `evaluations/`, `packages/`, `archive/` | Approved candidate domains | Not in the taxonomy; `archive/` conflicts with "no backoffice history in live authority" | Directive governs. Archive and history belong in `workspace-governor`. `evaluations/` and `packages/` are not created without justifying artifacts -- both documents already forbid empty domains, so no real conflict. |
| `references/` | Non-authoritative research, audits and retained source material | Supporting references, **not** backoffice history | Directive narrows it. Audit and research history moves to the backoffice. |
| `STATE.md` in Hub root | Mutable operational checkpoint, a root control file | Do not add management state, migration state or consolidation progress to the live Hub | Directive governs. Distinguish agent-consumable desired state -- potentially canonical -- from backoffice management state, which is `workspace-governor` material. Whether the Hub retains any `STATE.md` is a Step 1 decision from actual content. |

### 6.3 Special ownership boundaries

Binding on Step 1 and Step 3 classification.

- **Registry vs runtime state.** The registry describes desired identity and
  classification: IDs, owners, providers, classifications, related policies and
  adapters, canonical status. Runtime discovery describes observed state:
  reachability, health, negotiated protocol, currently available capabilities.
  Runtime state must never silently become canonical Hub state. Do not create
  competing Hub, Gateway, Claude and Codex registries.
- **Tools vs discovery.** A Hub tool definition is canonical identity,
  classification, ownership, policy relationship and intended use. Runtime
  discovery is observed availability, metadata, health and upstream state.
  Upstream MCP descriptions, annotations, instructions, `_meta`, capability
  declarations and risk hints are **inputs to classification, not governance
  authority**. They must not lower a risk classification, grant privilege, or
  remove an approval requirement by themselves.
- **Context vs authorization.** Context may describe responsibility, scope or
  operating conditions. It never grants permission. Do not infer Gateway
  authorization from a statement such as "user manages X" without an explicit
  policy granting the capability. This applies directly to `USER-SSOT.json`,
  which describes broad operational ownership and grants nothing.
- **Gateway separation.** `.agents-hub` holds canonical desired governance and
  configuration; `mcp-gateway` is executable enforcement; Gateway runtime state is
  operational, not Hub authority. Do not move Gateway source, logs, caches, tests,
  connections, metrics, credentials, session state or audit events into the Hub for
  centralization. Capabilities that do not pass through the Gateway remain governed
  by the native runtime or adapter -- do not claim centralized enforcement where no
  enforcement boundary exists.
- **KloWorkspaces exclusion.** Do not import KloWorkspaces domains. The Hub is not
  a work or knowledge vault. No Hub domains for tasks, projects, decisions,
  research records, communications, vendors, operational systems, personal
  knowledge or intake. The Hub may hold governance, context or runbooks that help
  agents operate on those systems.

### 6.4 Concerns already owned -- do not create a rule file

| Concern | Existing owner | Action |
|---|---|---|
| Technical Translation, audience-aware communication | `AGENT-SSOT.json` § `technical_translation_and_audience` and § `communication_and_format` | Already owned. Do **not** create a Technical Translation rule file. Reconcile into Hub context scope via the SSOT placement in D-d. Overlap with `ENGINEER-OWNERSHIP.md` § Communication is recorded in `PENDING-GLOBAL-PROMOTIONS.md` P-03. |
| Verification scoping and stopping condition | `AGENT-SSOT.json` § `verification_and_audit`; `rules/VERIFICATION-AND-EVIDENCE.md`; `rules/ENGINEER-OWNERSHIP.md` | Reconcile against these. Do **not** carry `rules/VERIFICATION-RESOLUTION.md` into the Hub as a new permanent owner -- P-01 and P-03 resolve it into an existing owner. |

### 6.5 `agents-hub-two` reconciliation targets

Read the actual definitions. Do not classify from filenames, and do not flatten
useful specialist separation without reviewing content.

- These are **system and orchestration artifacts, not agent definitions**:
  `agents/AGENT-SYSTEM-DEPENDENCIES.json`,
  `agents/NOTION-SYSTEM-DEPENDENCIES.json`. Classify their routing, topology,
  dependency, handoff and sequencing content under `orchestration/`.
- Routing logic is duplicated across five artifacts:
  `AGENT-COORDINATOR-ORCHESTRATOR.json`,
  `NOTION-COORDINATOR-ORCHESTRATOR.json`, `AGENT-SYSTEM-DEPENDENCIES.json`,
  `NOTION-SYSTEM-DEPENDENCIES.json`, `config/agent-registry.json`. Establish one
  authoritative owner per routing or dependency concept; the others reference it.
- Open question for Step 1, decided from content: does the Notion coordinator
  become one general orchestrator plus domain-specific orchestration definitions,
  or is it a genuinely separate agent?

### 6.6 Required record per artifact

Step 1 classification records, for every relevant artifact:

```text
Current location | Actual purpose | Canonical owner
Disposition: Keep / Fold / Move / Adapt / Retire
Overlaps or conflicts | References requiring updates | Runtime implications
```

Directive dispositions map onto the predecessor's seven verbs, which stay in use
for the finer distinction: `Fold` covers `Merge`; `Adapt` covers `Generalize` and
`Specialize`; `Keep`, `Move` and `Retire` are unchanged; `Conflict` remains a
valid outcome and is not a disposition but a stop.

### 6.7 Process gate

The immediate task is **reconciliation, not implementation**: inspect the current
Hub, Hub Two and predecessor backoffice; read and classify actual content; identify
ownership, duplication, conflicts and runtime implications; produce the
artifact-by-artifact reconciliation; derive the smallest justified tree.

Permitted now: reconciliation reports, evidence, backoffice working records, and
the analysis needed to complete them.

**Stop for approval before** applying the proposed canonical restructuring or
modifying live Hub governance, runtime configuration, code, manifests or
lockfiles. Do not perform broad refactoring while resolving one structural issue.
Preserve working behavior and bootstrap paths unless the reconciliation explicitly
requires a change.

### 6.8 Completion criteria

The reconciliation is complete when it establishes all nine:

one canonical Hub; one visible bootstrap; one owner per governed concern;
runtime-neutral source; thin existing adapters; clear orchestration; no semantic
duplication; no backoffice history in live authority; no runtime state in
canonical governance.

Do not finalize uncertain names or structures -- including the exact `context/`
substructure -- until existing material has been compared.

## 7. Immediate next action

Step 1. Its only remaining input is a current live-Hub inventory:

```powershell
.\scripts\Assert-RememberPruning.ps1     # must report: Proof verdict: PASS
.\scripts\Invoke-HubInventory.ps1        # must report: Completeness: COMPLETE
```

Run from the `workspace-governor` repository root on the Windows machine. Both are
read-only. Commit the emitted evidence, then execute Step 1 classification across
the three inputs in D-a, starting from the v0.4.2 § 4.1 ledger and the
2026-08-16 baseline rather than from zero.

Do not refactor, migrate, create adapters, or activate runtime instructions during
the tree-decision phase.

## 8. Stop conditions

Live stop conditions are owned by `STATE.md`. Read them before acting. This plan
adds none.
