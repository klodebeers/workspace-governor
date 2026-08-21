# Agent Hub Consolidation -- Active Plan

**Type:** Backoffice planning record. **Not live governance.** Must not become a
competing authority.
**Plan owner:** `workspace-governor` (Agent Hub backoffice)
**Target:** the single logical Agent Hub, in both its representations
**Version:** 0.7.2
**Baseline date:** 2026-08-20. **Amended 2026-08-21:** § 6.5's resolved open
question marked resolved, and its routing-artifact count corrected from five to
four. Amendments are recorded inline where they occur; the plan is not rewritten to
match executed work.

**One Hub, two representations.** The `.agents-hub` repository is the canonical
source. `C:\Users\Chloe\.agents-hub` is its local materialized location for agent
consumption. They are **the same logical Hub**, not two authorities, and must not
drift independently. Any change lands in the repository and is materialized
locally; a local-only edit is drift, not a decision.
**Status:** Steps 1 and 2 applied and verified. Step 3 onward not started. Current
state and blockers are owned by `STATE.md`, not by this file.

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
execution-ready but never started. A provenance copy is at
`plans/reference/AGENT-HUB-IMPLEMENTATION-PLAN-v0.4.2-predecessor.md`. Its **body**
is verbatim; the file is not byte-identical because a 12-line banner was prepended.
Source SHA-256 for identity checks:
`fbf32864381c5e29cffdf401bf1d561902d62616d4f8387b048a6558884642ea`.

The three carried-forward owner files are also copied, with banners and source
hashes, to `plans/reference/HUB-{ARCHITECTURE,MANAGEMENT,DOCUMENTATION}-predecessor.md`.
They previously existed only in a repository declared a non-authoritative input,
which left carried obligations depending on an external path.

Its 12-step sequence, authority and boundary map, execution controls, rollback
strategy and completion criteria are **reused unchanged** unless a delta is
recorded in section 4. Full classification of prior material:
`evidence/PREDECESSOR-BACKOFFICE-REVIEW-2026-08-20.md`.

## 3. Carried forward unchanged

Reuse these directly. Do not re-derive them.

| Carried forward | Source | Why still valid |
|---|---|---|
| **13-step** execution sequence, Step 0 to Step 12, with prerequisites, prohibited changes, verification method, evidence and completion gate per step | v0.4.2 § 6 | Structure is target-agnostic. **Corrected from "12-step": Step 0 to Step 12 is thirteen steps.** Each gate remains correct except where section 4 records a delta |
| Authority and boundary map | v0.4.2 § 2 | Carried **with two declared edits**, not unchanged. The predecessor map has five layers; its fifth, a future dashboard-driven Workspace Orchestrator, is out of scope here and its exclusion is restated in section 7. The map has **no Gateway layer**, so `mcp-gateway` is added per section 6.3 |
| Execution controls common to every step, 10 items | v0.4.2 § 5 | Smallest-change discipline unchanged. **Version preservation is NOT unchanged** -- see delta D-i. Controls 1 and 2 route to `rules/AGENTS.md` as the owner to load, superseded by D-27's root router. Control 7 requires a `research/` directory this backoffice does not have |
| Rollback and recovery strategy | v0.4.2 § 7 | **Not unchanged.** Four of its seven rows recover by "restore exact pre-edit version" or "rollback manifest". See delta D-i |
| Final completion criteria | v0.4.2 § 8 | **Not unchanged.** Criterion 1 makes the tree conform to `HUB-ARCHITECTURE.md`, superseded as taxonomy authority by D-27. **Criterion 3 says "five-file" contract, re-importing a constraint the predecessor's own decision record explicitly rejects** -- read it as "the routed contract", with no fixed count. Criterion 7 presumes a Hub-root `STATE.md` that section 6.2 leaves undecided. Criterion 13 depends on delta D-i |
| Four placement layers; one-owner-per-concern; governance-owner creation test | `HUB-ARCHITECTURE.md`, Hub `rules/AGENTS.md` | Already canonical |
| Classification verbs: Keep, Move, Generalize, Specialize, Merge, Retire, Conflict | v0.4.2 § 4.1, `HUB-MANAGEMENT.md` | Already in use. **`Generalize` and `Specialize` are opposite directions** and must not be collapsed: Generalize extracts a reusable core *into* the Hub leaving specifics outside; Specialize keeps the core in the Hub and creates a thin representation *elsewhere* |
| **Conflict guard:** a `Conflict` classification cannot be silently converted. Other classifications may change only if new evidence invalidates a premise **and the decision record explains why** | v0.4.2 § 4.1 | Restated explicitly. This is the protection against a blocked area being quietly reclassified, and it did not survive into version 0.6.0 |
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
| D-h | **Read-only inventory tooling now exists and is executed-verified** under PowerShell 7 against fixtures. | Step 1 inventory is a tooling run, not a manual walk. Windows PowerShell 5.1 and the live Hub remain unverified. `scripts/Collect-LocalEvidence.ps1` is the single-run collector. |
| **D-i** | **Version preservation has no mechanism in this backoffice.** v0.4.2 § 5 control 5, Step 4 in full, four rows of § 7, and criterion 13 all require an immutable pre-edit snapshot under `versions/project/` or `versions/hub/`, hash-verified and registered in `CHANGELOG.md`. **Neither directory nor file exists here**, and nothing stated that git satisfies the obligation. Step 4's completion gate was therefore unreachable and Step 5, which lists Step 4 as a prerequisite, was blocked by its own plan. | **Resolved by substitution, per `DECISIONS.md` D-28.** Git is the snapshot mechanism: the pre-edit commit SHA per edit set is the snapshot, recorded in that step's evidence record; `git diff <sha>..HEAD -- <path>` is the deterministic rollback instruction; `DECISIONS.md` plus commit history replace `CHANGELOG.md` registration. Discretionary version *numbering* stays retired. The obligation does not. |
| **D-m** | **The Architecture / Management boundary was not recorded here.** The predecessor router states it explicitly: Architecture answers *what and where*; Management answers *how to change it*. Architecture must not define editing or migration procedure, and Management must not redefine domains or placement rules. A task may load both, but only for its distinct question. | Carried forward as a constraint on Steps 1, 5 and 7, which use both provenance copies. Without it the two files can be read as overlapping owners, which is the duplication this consolidation exists to remove. Source: `plans/reference/predecessor/AGENTS.md`. |
| **D-j** | **The taxonomy authority changed.** Section 6 and D-27 override the tree authority that carried-forward Steps 1, 5 and 7 and criterion 1 point at. Version 0.6.0 declared section 4 exhaustive while overriding it elsewhere in the same document. | Recorded as a delta so the exhaustive claim holds. `HUB-ARCHITECTURE.md` is **reusable with adaptation, and is not an authority** -- it declares itself owner of Hub architecture, which is the error D-25 corrected for the SSOT pair. Adaptations in section 6.2. |
| **D-k** | **Vendor constraints are now evidenced**, independently and twice for Codex. | Binding on Steps 5 and 9. The root `AGENTS.md` has a hard **32 KiB shared instruction budget consumed root-first with silent truncation**, so an oversized root file starves nested files with no error. Governance goes behind router references, not inline. Symlinks are the verified affordance for resolving a runtime-bound path to neutral content. `skills/`, `agents/`, `tools/` and `prompts/` are canonical source only and each needs an adapter projection. A **nested git checkout severs the bootstrap chain**. `evidence/RUNTIME-CONVENTIONS-2026-08-20.md`. |
| **D-l** | **The live Codex global instruction file requires Hub `README.md` and `CATALOG.md`.** Section 6 makes `CATALOG.md` conditional. | A runtime consumer already depends on it. Resolve in Step 1: either the requirement is stale and the inbound reference is corrected, or `CATALOG.md` is not conditional. Recorded from the predecessor's dated Codex research. |

## 5. Conflict and gap register

Predecessor identifiers mapped to current ones. One row per real issue; no duplicates.

| v0.4.2 | Current | Issue | Status |
|---|---|---|---|
| C-01 | B-3 | Codex authority file has stale `C:\Users\ByteBoss\...` paths and overlaps Hub-owned responsibilities | Open. Blocks Codex adapter activation only. Needs user authorization to open as a scoped change (D-11). |
| C-02 | B-2 | `design-systems/.remember` provenance and sensitivity unresolved | Open. Existence-only handling enforced in tooling. Blocks classification of that area only. |
| C-03 | -- | Claude Code instruction placement enforces nothing on its own; an enforcement carrier must be chosen per rule | Open, **narrowed and restated 2026-08-20**. The carried-forward wording -- "project instructions outrank global governance" -- conflated advisory instructions with enforced settings. Managed settings cannot be overridden by a project. Blocks adapter finalization only. `evidence/RUNTIME-CONVENTIONS-2026-08-20.md` |
| G-01 | -- | Hub reference audit overlaps project research | **Disposition settled by `DECISIONS.md` D-15**, not open: the Hub keeps the live-state audit, the project keeps the authoring research, the project's duplicated narrative becomes a reference. Execution deferred only because it edits another repository. **The v0.4.2 § 4.1 ledger row says the opposite** -- retire the Hub copy -- and Step 1 must not consume it as written. |
| G-02a | -- | Third-party **rules scaffolder** (`scaffold-rules`): provenance, licence and generated-output not accepted. Its generator-owned block is overwritten on rerun, so it must never own Hub governance | Open. **Distinct from the toolkit fork** -- version 0.6.0 wrongly mapped these together. Predecessor learning L-006 applies. |
| G-02b | -- | `agent-governance-toolkit`, an unmodified MIT fork of a Microsoft project: adoption not reviewed | Open. Recorded in `STATE.md`. |
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
|-- context/             scoped knowledge and supporting operating context; not authority
|-- adapters/            mappings to runtime-native representations (renamed from runtime-adapters/, section 6.2c)
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

### 6.2a Canonical definition of `context/` -- C-04 resolved

Directive-given 2026-08-21, superseding the earlier gloss "scoped operating
context, not knowledge or authorization", which conflicted with the accepted
Step-1 target tree. This is the single agent-agnostic definition. `DECISIONS.md`
D-66.

`context/` **owns** scoped knowledge and supporting operating context needed by
agents: domain concepts, architecture explanations, domain and product terminology,
design rationale, integration constraints, project-specific workflows, historical or
operational references, supporting technical background, and detail that would
otherwise bloat the root instruction files. It is version-controlled and travels
with the Hub.

`context/` **does not own** governance, permissions, approvals, protected
boundaries, behavioral obligations, verification authority, or instruction
precedence. Those stay with their canonical owners, primarily `rules/` or another
explicitly assigned Hub owner.

**A file is not mandatory because it exists under `context/`.** It is loaded only
when explicitly routed or referenced by the Hub bootstrap, the orchestration layer,
an agent definition, or a runtime adapter.

**Scope separation.** **The Hub is the global layer.** Everything under
`.agents-hub/context/` already applies across projects, so there is no `global`
subdirectory: it would be a redundant level inside a repository whose whole purpose
is reusable cross-project source. Corrected by the taxonomy owner 2026-08-21;
`DECISIONS.md` D-69.

Suitable content is what applies broadly: personal response and coding preferences,
the user's stack, preferred tools and package managers, general engineering habits,
cross-project terminology, centrally managed organization-wide defaults, and
references to global workflows.

`~/.codex/` and `~/.claude/` are runtime discovery locations that an adapter projects
into. They are not a second home for canonical knowledge, and knowledge is not placed
there to make it global -- it is already global by being in the Hub.

**Runtime separation.** Codex, Claude Code and future runtimes may each use their own
global and project instruction mechanisms. Those are adapters and discovery entry
points only. They may load or expose canonical Hub context; they must not redefine
what `context/` means, what it owns, what authority it has, or where canonical
knowledge belongs. The Hub stays agent-agnostic.

**Backoffice separation.** `workspace-governor` remains the backoffice for research,
evidence, migration work, provenance, recovery, planning, project state and
historical records. Backoffice material does not become runtime context merely by
being useful; it enters the live Hub only once accepted, classified, and assigned to
a canonical Hub owner.

### 6.2b Capability knowledge, and where domain implementation goes

Directive-given 2026-08-21, corrected twice the same day. The rule that survives
both corrections: **`context/` holds general reusable capability knowledge.** Exact
domain implementation is a different thing and does not belong beside it.

Accepted shape, with the `global/` wrapper removed per D-69:

```text
context/
|-- user-preferences/
|-- user-stack/
|-- tooling/
|   |-- git/
|   |-- powershell/
|   |-- python/
|   |-- node/
|   `-- mcp/
|-- services/
|   |-- notion/
|   |-- excel/
|   `-- dashboards/
`-- terminology/
```

For Notion, general reusable capability knowledge means database creation and
editing, property types, relations and rollups, views, filters and sorts, formula
fundamentals, page and database structure, common database patterns, and general
migration, cleanup, validation, limitation and behavior knowledge.

Exact domain implementation means named databases and their ids, exact properties and
allowed values, relations between specific databases, project-specific formulas and
views, domain workflow rules and domain terminology -- for Greyed, Fina, Klo
Professional, Klo Personal, or a specific dashboard schema.

**Open, and not resolved here.** Two owner statements pull in opposite directions on
where that implementation lives. The C-04 definition lists "domain knowledge" and
"project-specific workflows" as suitable Hub `context/` content and says
project-specific knowledge stays in the Hub or with an explicitly assigned project
owner. The correction says everything in the Hub is global, which reads against
holding one project's schemas there. No domain implementation content exists in the
Hub, so nothing is blocked; recorded as `STATE.md` open work 28b rather than settled
by inference. `DECISIONS.md` D-69.

**Empty branches are not created.** Each directory above comes into existence with
its first accepted artifact. `NOTION-FORMULA-V2.md` sits at `context/` root, not in a
`services/notion/` branch, because one file does not justify two passthrough
directories -- the branch is created when the Notion capability content that fills it
is accepted.

### 6.2c Adapter directory name -- superseded, surfaced

The corrected sample names the adapter directory **`adapters/`**, with `claude/`,
`codex/` and `generic/` beneath it. The accepted taxonomy in section 6 and the Hub
`CATALOG.md` both say `runtime-adapters/`.

Recorded as a supersession by the taxonomy owner rather than resolved silently: the
sample is the later statement and comes from the owner of the taxonomy. `adapters/`
governs. Nothing in the Hub changes yet -- no adapter exists, and the directory is
created with its first accepted adapter -- so the correction is a name change to an
unbuilt domain. `generic/` is new: the earlier taxonomy named only per-runtime
adapters. `DECISIONS.md` D-68.

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
- Routing logic is duplicated across **four** artifacts:
  `AGENT-COORDINATOR-ORCHESTRATOR.json`,
  `NOTION-COORDINATOR-ORCHESTRATOR.json`,
  `NOTION-SYSTEM-DEPENDENCIES.json`, `config/agent-registry.json`.
  **Corrected 2026-08-21 from "five":** `AGENT-SYSTEM-DEPENDENCIES.json` has no
  `routing_logic` key. Verified directly; the reconciliation record and D-37 both
  said four, and this line disagreed with them. Establish one
  authoritative owner per routing or dependency concept; the others reference it.
- ~~Open question for Step 1, decided from content: does the Notion coordinator
  become one general orchestrator plus domain-specific orchestration definitions,
  or is it a genuinely separate agent?~~ **Resolved.** One orchestrator role; the
  Notion coordinator is folded into it. `DECISIONS.md` D-45.

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

Do not finalize uncertain names or structures -- the exact `context/`
substructure is now shaped by section 6.2b, and other structures -- until existing material has been compared.

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

## 7a. Scope exclusion carried forward

A future dashboard-driven **Workspace Orchestrator** is explicitly **out of scope**.
It is the fifth layer of the predecessor authority map, with its own ownership
boundary, and this plan neither designs nor implements it. Carried forward from
v0.4.2 § 1; the exclusion was lost in version 0.6.0.

## 8. Stop conditions

Live stop conditions are owned by `STATE.md`. Read them before acting. This plan
adds none.
