# Agent Hub Consolidation -- Active Plan

**Type:** Backoffice planning record. **Not live governance.** Must not become a
competing authority.
**Plan owner:** `workspace-governor` (Agent Hub backoffice)
**Target:** the single logical Agent Hub, in both its representations
**Version:** 0.8.0
**Baseline date:** 2026-08-20. **Amended 2026-08-21:** § 6.5's resolved open
question marked resolved and its routing-artifact count corrected from five to four;
§ 3a added, naming the thirteen steps this plan previously carried by citation; § 6.2a
to § 6.2c added for the `context/` definition, the capability shape and the adapter
rename; § 7 rewritten to own per-step requirements after its position table moved to
`STATE.md`; **§ 9 and § 10 appended** for the deltas established that day and what
Step 5 needs. Amendments are recorded inline and appended, never renumbered, and the
plan is not rewritten to match executed work.

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
| **13-step** execution sequence, Step 0 to Step 12, with prerequisites, prohibited changes, verification method, evidence and completion gate per step. **The step names are listed in section 3a below**; the full per-step definitions stay in the source | v0.4.2 § 6 | Structure is target-agnostic. **Corrected from "12-step": Step 0 to Step 12 is thirteen steps.** Each gate remains correct except where section 4 records a delta |
| Authority and boundary map | v0.4.2 § 2 | Carried **with two declared edits**, not unchanged. The predecessor map has five layers; its fifth, a future dashboard-driven Workspace Orchestrator, is out of scope here and its exclusion is restated in section 7. The map has **no Gateway layer**, so `mcp-gateway` is added per section 6.3 |
| Execution controls common to every step, 10 items | v0.4.2 § 5 | Smallest-change discipline unchanged. **Version preservation is NOT unchanged** -- see delta D-i. Controls 1 and 2 route to `rules/AGENTS.md` as the owner to load, superseded by D-27's root router. Control 7 requires a `research/` directory this backoffice does not have |
| Rollback and recovery strategy | v0.4.2 § 7 | **Not unchanged.** Four of its seven rows recover by "restore exact pre-edit version" or "rollback manifest". See delta D-i |
| Final completion criteria | v0.4.2 § 8 | **Not unchanged.** Criterion 1 makes the tree conform to `HUB-ARCHITECTURE.md`, superseded as taxonomy authority by D-27. **Criterion 3 says "five-file" contract, re-importing a constraint the predecessor's own decision record explicitly rejects** -- read it as "the routed contract", with no fixed count. Criterion 7 presumes a Hub-root `STATE.md` that section 6.2 leaves undecided. Criterion 13 depends on delta D-i |
| Four placement layers; one-owner-per-concern; governance-owner creation test | `HUB-ARCHITECTURE.md`, Hub `rules/AGENTS.md` | Already canonical |
| Classification verbs: Keep, Move, Generalize, Specialize, Merge, Retire, Conflict | v0.4.2 § 4.1, `HUB-MANAGEMENT.md` | Already in use. **`Generalize` and `Specialize` are opposite directions** and must not be collapsed: Generalize extracts a reusable core *into* the Hub leaving specifics outside; Specialize keeps the core in the Hub and creates a thin representation *elsewhere* |
| **Conflict guard:** a `Conflict` classification cannot be silently converted. Other classifications may change only if new evidence invalidates a premise **and the decision record explains why** | v0.4.2 § 4.1 | Restated explicitly. This is the protection against a blocked area being quietly reclassified, and it did not survive into version 0.6.0 |
| Dated-baseline supersession rule: never silently rewrite a dated baseline; issue a later dated audit citing it | `evidence/BASELINE-AUDIT-2026-08-16.md` | Adopted as the standard for every inventory this plan produces |

## 3a. The sequence, in full

Added 2026-08-21. Section 3 previously carried the sequence by citing its source, so
this plan stated that thirteen steps exist without naming them, and the names lived
only in a provenance copy marked never executable. A reader of this plan could not
learn what the steps were, which is how step labels drifted in practice
(`DECISIONS.md` D-73). The names are here now; the full per-step prerequisites,
prohibitions, verification methods and completion gates remain in the source, which
section 3 cites.

| | Step | Name | Status, and why not |
|---|---|---|---|
| [x] | 0 | Execution bootstrap and checkpoint validation | Done informally. No dated drift-check record was produced; the baseline was re-inspected repeatedly in practice. Low consequence, not re-opened |
| [x] | 1 | Accept the final target tree and complete classification | Done. All 46 inputs classified. D-35, D-37 |
| [x] | 2 | Resolve provenance, sensitivity, and external-source gates | Done, retrospectively — it ran after its dependents. Gate PASS. D-76 |
| [~] | 3 | Establish the semantic owner and dependency map | **Map produced, gate not met.** 64 issues, 31 contested, 25 dispositions settled, 6 blocked. The gate fails only on issues blocked by **U-1** — whether `AGENT-SSOT.json` is a governance owner or an asset — which is a reserved user decision. D-77 |
| [x] | 4 | Prepare version preservation and rollback manifests | Satisfied by substitution: git is the mechanism, the pre-edit commit SHA is the snapshot. D-28 |
| [x] | 5 | Refactor the runtime-neutral core and root controls | Done — the root `AGENTS.md` move, retiring the Hub `STATE.md` and the placeholders, and the later `AGENTS.md` edits. **Recorded at the time under the wrong labels**, "Step 1" and "Step 2". D-73 |
| [~] | 6 | Consolidate references and evidence without losing unique findings | Disposition settled by D-15; execution edits another repository and is sequenced separately. Not blocking |
| [x] | 7 | Refactor structural domains and accept reusable artifacts | Done — `registry/`, `orchestration/`, `agents/`, `context/`, `templates/` with their first artifacts. Recorded at the time as "Step 2" |
| [x] | 8 | Migrate accepted external source into the canonical Hub | Done for the six artifacts. **Eleven agent definitions remain**, gated by the agent-definition schema (D-47) and the handoff contract |
| [ ] | 9 | Reconcile and implement thin runtime adapters | Not started. `adapters/` per D-68; the files to wire are `.claude/CLAUDE.md` and `.codex/AGENTS.md` (D-75). **Why not:** requires Step 3's owner map, and is wired on the local machine. issue #9 |
| [~] | 10 | Update routes, registries, continuity, and references atomically | Partly done — the `CATALOG.md` and `README.md` updates that accompanied Step 7. The remainder lands with each later migration |
| [ ] | 11 | Fresh-agent bootstrap and runtime-activation verification | Assigned, not executed. **Why not:** needs a fresh session per runtime on the operator's machine, which no cloud session can start |
| [ ] | 12 | Final audit, rollback readiness, and completion declaration | Not started. **Why not:** must not begin before Step 3 has an accepted owner map |

Legend: `[x]` done or satisfied by substitution · `[~]` partly done, or done with a
stated gap · `[ ]` not started, with the reason named.

**This checklist is a convenience, not the authority.** `STATE.md` § Position in the
plan sequence owns where the work stands, and if the two ever disagree, **`STATE.md`
governs and this table is the stale one.** Kept here by directive (`DECISIONS.md` D-86)
because a plan you cannot read your position from is the defect that caused D-73.

Required order: **target-tree decision, then refactoring, then migration, then
runtime integration and verification.** Do not begin a later phase before the
preceding phase's completion gate passes, or is explicitly evidenced NOT APPLICABLE
where the plan permits that result.

**Never name a step from memory.** The sequence is this table. **Where the work
currently stands in it is owned by `STATE.md`, not by this plan** -- position is
current state, and duplicating it here would create two answers that drift.

## 4. Deltas since v0.4.2

Only these change. Everything else in section 3 stands.

| # | Delta | Effect on the plan |
|---|---|---|
| D-a | **A second source repository exists.** v0.4.2 knew only the live Hub. `agents-hub-two` holds 27 files -- 15 agent definitions, `config/agent-registry.json`, schemas, prompts, templates -- and is source material pending reconciliation. | Step 1 classification must cover three inputs: the live `.agents-hub`, canonical `.agents-hub`, and `agents-hub-two`. Step 8 migration now has a real accepted-source candidate, where v0.4.2 anticipated possibly none. |
| D-b | **The canonical Hub is now named and settled.** `.agents-hub` is canonical (`DECISIONS.md` D-24), superseding the two-repositories-both-claiming-identity condition. | Removes the identity question from Step 1. Step 1 decides structure, not which repository governs. |
| D-c | **Hub root `AGENTS.md` is misplaced inside `rules/`.** Verified: `.agents-hub` has `rules/AGENTS.md` and no root `AGENTS.md`. | Add to Step 1 classification as a `Move`, executed in Step 5. Structural only, no content change. Deferred by instruction from the canonicalization step. |
| D-d | **The SSOT set must be placed with scope-based routing.** Corrected 2026-08-21 by `DECISIONS.md` D-80: it is not a pair. `.agents-hub/context/USER-SSOT.json` is the global shared user-context asset; `Greyed/context/GREYED-SSOT.json` and `Fina/context/FINA-SSOT.json` are scope-specific and are not universal user profiles. The file staged here as `USER-SSOT.json` carries Greyed content and becomes `GREYED-SSOT.json`. None is a general governance owner. | New work inside Step 5 and Step 10. Placement alone is insufficient: the Hub root router needs entries or the assets are unreachable. See `evidence/HUB-ASSET-PLACEMENT-CORRECTION-2026-08-20.md`. |
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
Hub, so nothing is blocked; recorded as issue #21 rather than settled
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
  policy granting the capability. This applies directly to every scoped user-context
  SSOT: each describes operational ownership within its scope and grants nothing
  (`DECISIONS.md` D-80).
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

## 7. What each remaining step requires

**Corrected 2026-08-21, twice.** This section first said "Step 1", which was true when
written and went stale. It was then replaced with a table of where the work stands --
which put current position in the plan, when `STATE.md` owns position. That table has
moved to `STATE.md`; two copies would drift. `DECISIONS.md` D-73 and D-74.

This section owns what each remaining step *requires*. `STATE.md` owns which of them
are done.

**Step 2 -- provenance, sensitivity and external-source gates.** Two gates:
`design-systems\.remember`, which is an isolated conflict under a standing stop
condition and closes by being recorded as explicitly blocked and excluded, which the
step's gate permits; and the rights, ownership and provenance of any external source
whose content enters the Hub. Step 8 names the latter as its prerequisite.

**Step 3 -- semantic owner and dependency map.** An issue-to-owner matrix and an
artifact-to-owner matrix, with duplicate and overlap dispositions and unresolved gaps
named. Gate: no included governed issue or artifact has two active owners. This is the
step that decides duplicate ownership *before* editing, and skipping it is what left
the duplicate-ownership class to be found by audit instead.

**Step 6 -- consolidate references and evidence.** Disposition settled by D-15;
execution edits another repository and is sequenced separately.

**Step 9 -- thin runtime adapters.** Requires Step 3's owner map, and each of
`agents/`, `skills/`, `tools/` and `prompts/` needs a projection per delta D-k.

The two files to be wired are **`.claude/CLAUDE.md`** and **`.codex/AGENTS.md`**,
directive-given 2026-08-21 (`DECISIONS.md` D-75). Each is its runtime's own discovery
location, which is what makes the projection work: a file placed under `adapters/`
would never be discovered by either runtime. `adapters/` per D-68 remains the home for
adapter material that is not discovery-critical.

Wired on the local machine, sequenced last. issue #9.

**Step 10 -- routes, registries, continuity and references, atomically.** Partly done
alongside Step 7; the remainder lands with each later migration.

**Step 11 -- fresh-agent bootstrap and runtime-activation verification.** Presence is
never activation. Requires a fresh session per runtime on the operator's machine.

**Step 12 -- final audit, rollback readiness and completion declaration.** Not before
Step 3 has an accepted owner map.

## 7a. Scope exclusion carried forward

A future dashboard-driven **Workspace Orchestrator** is explicitly **out of scope**.
It is the fifth layer of the predecessor authority map, with its own ownership
boundary, and this plan neither designs nor implements it. Carried forward from
v0.4.2 § 1; the exclusion was lost in version 0.6.0.

## 8. Stop conditions

Live stop conditions are owned by `STATE.md`. Read them before acting. This plan
adds none.

## 9. Deltas established 2026-08-21

Appended, not renumbered. These are additions to what the plan carries: new
constraints, new work, and corrections to earlier deltas. **Where the work stands is
not here** — that is `STATE.md` § Position in the plan sequence (D-74). Each row names
its decision so the reasoning is one hop away, not restated.

| # | Delta | Effect on the sequence |
|---|---|---|
| D-n | **Step labels used in this project did not match this plan's sequence.** What was called "Step 2" was Step 7 plus Step 8; the restructuring called "Step 1" was Step 5. `DECISIONS.md` D-73 | Steps 7 and 8 ran before Steps 2 and 3, their prerequisites. Step 2 has since been closed (D-76) and Step 3's map produced (D-77). The executed work is verified and stands |
| D-o | **This plan now lists its own steps** (section 3a) and states what each remaining step requires (section 7). It previously carried the sequence by citation, so it asserted a count without naming the steps. `DECISIONS.md` D-74 | Removes the cause of the label drift. Position moved out of this plan into `STATE.md`; the ownership split is recorded in `AGENTS.md` § File ownership |
| D-p | **Step 2 is closed retrospectively, gate PASS.** `agents-hub-two` cleared with evidence; `design-systems\.remember` explicitly blocked and excluded with nothing depending on it, verified by search. `DECISIONS.md` D-76; `evidence/PROVENANCE-AND-SENSITIVITY-GATES-2026-08-21.md` | Step 8's stated prerequisite -- source rights, owner, destination known -- is now supported by evidence rather than assumption |
| D-q | **Step 3's map exists; its gate is not met.** 64 governed issues, 31 contested, 25 dispositions settled, 6 blocked. `DECISIONS.md` D-77; `evidence/AGENT-HUB-SEMANTIC-OWNERSHIP-MAP-2026-08-21.md` | **Gates Step 5.** Step 5's prerequisite is Steps 1-4 complete *for the core edit set*, so Step 5 can proceed on an edit set that excludes what U-1 blocks. See section 10 |
| D-r | **Three obligations have no Hub statement at all**, each verified absent by search: bounding a verification method; which source is authoritative for a question class; the defect-class sweep. All three exist only in `workspace-governor/rules/VERIFICATION-RESOLUTION.md` | New Step 5 work: fold them into `rules/VERIFICATION-AND-EVIDENCE.md` as sections. Partly settles P-01, whose "retired into it" wording must not be executed as deletion -- two of the three are unique in the whole corpus |
| D-s | **Thirteen gaps named, each assigned to an existing owner as a section. No new rule file for any.** `DECISIONS.md` D-77 | Step 5 and Step 3 work. Two are structural rather than missing text: nothing owns where a surfaced governance gap is recorded, and nothing resolves an asset contradicting a rule -- assets hold no precedence tier, so they cannot be placed in the six-level order |
| D-t | **The domain-instantiation test.** Strip the domain nouns; if a sentence already in a `rules/` file remains it is a restatement, if it becomes vacuous it is an instantiation. `DECISIONS.md` D-78 | Belongs in the agent-definition schema so it is applied once rather than eleven times. Gates the remaining agent migrations under Step 8 |
| D-u | **`context/` is defined; there is no `global/` folder.** The Hub is the global layer. `context/` owns scoped knowledge and supporting operating context and owns no authority. A file there is not mandatory by existing -- it loads only when routed. `DECISIONS.md` D-66, D-67, D-69; sections 6.2a and 6.2b | Closes conflict C-04. Section 6.2b's shape governs `context/` growth; branches arrive with their first accepted artifact |
| D-v | **The adapter directory is `adapters/`**, with `claude/`, `codex/` and `generic/`, superseding `runtime-adapters/`. The two files to wire are `.claude/CLAUDE.md` and `.codex/AGENTS.md`, each the runtime's own discovery location. `DECISIONS.md` D-68, D-75 | Step 9. Nothing is built. **Verified constraint:** Claude Code discovers only `CLAUDE.md`, never `AGENTS.md`, so an adapter file inside `adapters/claude/` would never be found -- the projection must sit at a discovery location. `evidence/RUNTIME-CONVENTIONS-2026-08-20.md` addendum |
| D-w | **The user-context SSOT naming model.** `.agents-hub/context/USER-SSOT.json` is the global shared asset; `Greyed/context/GREYED-SSOT.json` and `Fina/context/FINA-SSOT.json` are scope-specific and are not universal user profiles. None is a general governance owner. `DECISIONS.md` D-80 | Corrects delta D-d: it is not a pair. Placement is Step 5 and Step 10 work, recorded as issue #15, and **deliberately not a blocker** -- no step depends on the rename |
| D-x | **Intake exists.** `_inbox/` in the backoffice is the single door for change requests to the Hub, with a decline standard and a keyword rule. `DECISIONS.md` D-81, D-82, D-83 | Nothing enters the Hub from it until accepted, classified, and assigned to a Hub owner -- this plan's standing rule, restated where it will be tested. Triage is not a plan step; the scheduled run is `PENDING.md` P-1, twice weekly (D-85) |
| D-y | **Verification tooling now exists and is proven in both directions.** `scripts/Test-HubRegistrySchema.py` (32 assertions), `scripts/Assert-HubSourceFidelity.py` (21, the only one reading the source package), `scripts/Assert-ReferenceIntegrity.py` (58 tokens, URI semantics, catalog coverage). `DECISIONS.md` D-53, D-65 | Available as the verification method for every later step. Each was proven by building the defect it must catch; eleven defect trees from the audits are retained as regression cases |
| D-z | **Blind adversarial subagent review is the independent pre-edit review** that Step 5 lists as a prerequisite. Reviewers get source, approved scope and result, and are denied the implementer's rationale. `DECISIONS.md` D-60 | Satisfies Step 5's second prerequisite as a mechanism. It has found material defects in three consecutive rounds, including on states two earlier reviews had passed |

## 10. What Step 5 needs before it starts

Step 5's prerequisites, verbatim from the carried-forward source: *"Steps 1-4 complete
for the core edit set; independent pre-edit review accepted for governance/architecture
changes."*

| Prerequisite | State |
|---|---|
| Step 1 complete | **Yes.** D-35, D-37 |
| Step 2 complete | **Yes.** Gate PASS, D-76 |
| Step 3 complete **for the edit set** | **Conditional.** The map exists; its gate fails only on issues blocked by U-1. An edit set that excludes those satisfies the prerequisite. The gate is written per edit set -- "no **included** governed issue or artifact has two active owners" |
| Step 4 | **Satisfied by substitution.** Git is the mechanism, D-28. The pre-edit commit SHA is the snapshot |
| Independent pre-edit review | **Mechanism accepted** (D-60). The review of the specific edit set has not run, and runs before edits, not after |
| Approval to modify live Hub governance | **Not given.** `STATE.md` stop condition and section 6.7 both require it. This is the actual gate |

**So three things are needed, in this order:**

1. **A defined edit set**, excluding everything U-1 blocks. Proposed, not assumed --
   the agent lists exactly which files change and which disposition each edit executes.
2. **Approval** to modify live Hub governance for that set.
3. **A blind pre-edit review** of the set, before any edit lands.

**U-1 is not required to start Step 5.** It determines only whether the
`AGENT-SSOT.json` cluster is in the edit set or excluded from it. Answering it enlarges
the set; leaving it open does not block the rest.
