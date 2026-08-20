# Decisions

Durable settled decisions. Append-only. Do not rewrite or delete an entry;
supersede it with a new one and mark the old one superseded.

Current state belongs in `STATE.md`, not here.

Every entry records who decided it. Under `rules/ENGINEER-OWNERSHIP.md` — currently in `agents-hub-one`, destined for
`.agents-hub/rules/` after consolidation — the user owns intended outcome, business rules, acceptance criteria and reserved
human decisions; the agent owns and must prove ordinary engineering decisions.

| ID | Decision | Decided by | Date |
|---|---|---|---|
| D-01 | `workspace-governor` is the management and orchestration repository for the final canonical `.agents-hub` and related control-plane work. | User | 2026-08-19 |
| D-02 | `agents-hub-one` and `agents-hub-two` are the two source repositories to be reconciled into the final canonical `.agents-hub`. | User | 2026-08-19 |
| D-03 | `workspace-governor-agents-hub-one` is the management and planning repository for the existing Hub One work. It is not `agents-hub-one` and is not a Hub. | User | 2026-08-19 |
| D-04 | The `mcp-gateway` directive is settled at 46 sections. The 15-section consolidation is not to be reopened. | User | 2026-08-19 |
| D-05 | Hub consolidation precedes final Gateway environment discovery. | User | 2026-08-19 |
| D-06 | Discovery tooling must not assume `.agents-hub` already exists. | User | 2026-08-19 |
| D-07 | `verification_rule` remains in the user SSOT as a reporting-format preference. It is not promoted into `rules/VERIFICATION-AND-EVIDENCE.md` (`agents-hub-one`). | Agent | 2026-08-19 |
| D-08 | SSOT `communication_preferences.tone` and `.format` own rendering. `agents-hub-one/rules/ENGINEER-OWNERSHIP.md` § Communication owns substance. No edit to either file. | Agent | 2026-08-19 |
| D-09 | The user SSOT is an asset, not a governance owner. | Agent | 2026-08-19 |
| D-10 | Durable project information must be written to this repository, not left only in session state. | User | 2026-08-19 |
| D-11 | The Codex stale-authority conflict is required before Gateway runtime integration and completion, but is not a blocker to the Hub consolidation phase. | User | 2026-08-19 |
| D-12 | Three of hub-two's four templates are Notion-specific and go owner-local under `agents/notion/`. Only `verification-checklist-template.json` is domain-neutral and belongs in shared `templates/`. | Agent | 2026-08-19 |
| D-13 | `runtime-adapters/` is retained as a declared logical domain in `CATALOG.md`. Its 0-byte placeholder files are retired and no empty directory is materialized. | Agent | 2026-08-19 |
| D-14 | `agents/` is subdivided into `general/` and `notion/`, and the registry is normalized to a symmetric domain-keyed model with full schema coverage. | Agent | 2026-08-19 |
| D-15 | The `references/` overlap is resolved by placement layer: the Hub keeps the live-state audit; the project keeps the authoring research; the project record's duplicated live-state narrative is replaced by a reference. Execution is deferred because it edits another repository. | Agent | 2026-08-19 |
| D-16 | Committed tooling must not hardcode absolute user-profile paths. Hub location is resolved from the environment, overridable by parameter, and the resolved path is recorded in the evidence. | Agent | 2026-08-19 |

## Rationale

**D-01.** Separates management from the thing being managed. The Gateway directive
requires `.agents-hub` to remain canonical desired state and forbids operational
state being written back into it; a distinct management repository keeps planning,
decisions and tooling out of the canonical governance tree.

**D-02.** Neither source repository alone satisfies what `.agents-hub` must own.
`agents-hub-one` supplies the governance contract — a five-file `rules/` set with
zero runtime-specific names across all five files, which is the hardest property to
retrofit. `agents-hub-two` supplies agent definitions, registry, schemas, prompts
and templates, and contains no governance layer at all. Both halves are required.

**D-03.** The naming invites the error. `workspace-governor-agents-hub-one`
contains `HUB-ARCHITECTURE.md`, `HUB-MANAGEMENT.md`, `HUB-DOCUMENTATION.md`, a
plan, research, evidence and versioned snapshots. It governs a Hub; it is not one.
Treating it as a Hub source would import planning records into canonical governance.

**D-04.** The directive's security content — authorization trust boundaries,
confused-deputy prevention, Streamable HTTP transport security — earns the length.
Reopening the structure risks losing requirements for a presentational gain. An
earlier consolidation to 15 sections dropped ten policy-validation checks, the
retry-storm prohibition and the entire non-goals section; those were restored in v3.

**D-05.** Directive section 29 requires folding semantically equivalent rules into
existing canonical locations. Those locations do not yet exist in final form.
Discovery against a hub that is still two competing repositories would produce an
evidence map that is invalid as soon as consolidation completes.

**D-06.** The final canonical `.agents-hub` is the output of consolidation, not an
input to it. Tooling that presupposes the hub biases discovery toward one source
repository and fails to represent the pre-consolidation state accurately.

**D-07.** `agents-hub-one/rules/VERIFICATION-AND-EVIDENCE.md` owns verification *sufficiency*. The
SSOT rule governs verification *reporting* to a specific person. Promoting it would
inject role-specific content — "exact UI path or API endpoint" presumes a UI exists —
into a file that is measurably runtime-neutral.

**D-08.** Substance and rendering are separable. `agents-hub-one/rules/ENGINEER-OWNERSHIP.md` prescribes
leading with the outcome, concision and evidence-backing, and prescribes no layout.
The SSOT prescribes layout and no substance. Non-overlapping.

**D-09.** The SSOT describes a principal's authority; it does not govern agent
behaviour. It is data consumed by the governance owners, not an owner itself. It
therefore fails the governance-owner eligibility test — no distinct governed issue
with distinct observable activation. Its placement remains open (`STATE.md` open
work item 3 and 5).

**D-11.** The conflict is confined to a runtime adapter's authority file. Hub
consolidation operates on two source repositories and produces a target tree; it
does not activate a Codex adapter and does not read the Codex authority file.
Gateway directive sections 34 and 43 still require Codex to connect, so the
conflict remains mandatory before Gateway completion — it is sequenced later, not
dismissed.

**D-10.** Session state is not durable. Project decisions and current state held
only in a conversation are lost when the session ends and are invisible to any
other agent or person. See `AGENTS.md` for the operating requirement.

**D-12.** Classified from field content, not filename. Coupling to Notion concepts:
`technical-spec` 5 of 12 fields, `task-brief` 3 of 12, `execution-record` 2 of 8,
`verification-checklist` **0 of 7**. `HUB-ARCHITECTURE.md`: "A template specific to
one agent, skill, tool, package, or workflow remains with that owner." This reverses
the first proposal, which mis-screened `human_review_required` as Notion-coupled on
the substring "view".

**D-13.** A logical domain and an empty directory are different things.
`HUB-ARCHITECTURE.md` establishes `runtime-adapters/` as a core domain — a declared
destination — without requiring an empty directory to hold the place. A 0-byte file
satisfies no part of the minimum artifact record, so retaining it preserves nothing
and falsely implies an adapter that `agents-hub-one/README.md` and `STATE.md` both
state does not exist.

**D-14.** The registry is structurally asymmetric: `entry_point` and `coordinator`
name only Notion, `specialists` holds 5 Notion agents, 8 general agents sit in a
separate `non_notion_agents` key, and `routing_rules` contains only a `notion` key.
`agent-registry.schema.json` declares 6 properties; `non_notion_agents` and
`routing_rules` are absent and therefore unvalidated. Entry shapes are identical, so
the asymmetry is structural, not semantic. A flat `agents/` would leave it in place
and keep general agents second-class.

**D-15.** Direct comparison, not deferral: 82 substantive lines in the Hub audit,
104 in the project research record, only 6 literally identical. Overlap is confined
to the audit's Findings 1–5 versus the research record's Live-State Problems 1–5;
76 lines are unique to one and 98 to the other. `HUB-ARCHITECTURE.md` layer 1
assigns cross-project canonical material to the Hub and layer 2 assigns
project-specific material to the project, and `agents-hub-one/CATALOG.md` already
records the combined record as relocated "because it is Workspace Governor project
research". Nothing unique is lost.

**D-16.** Stale hardcoded absolute paths in an authority file are precisely what
blocker B-3 consists of. `agents-hub-one` carries them in 4 files and
`workspace-governor-agents-hub-one` in 32. `workspace-governor` currently contains
none — its single `C:\Users` occurrence is a detection pattern that finds them.
Hardcoding a user-profile path into new committed tooling would reproduce the defect
the tooling exists to detect, and would introduce a username into the only clean
repository. Environment resolution plus a recorded resolved path yields the same
evidence without the defect.

**D-17.** A static structure gate is required before any script under `scripts/`
is handed to the local operator, and it must be proven to fail on the defects it
exists to catch. Decided by: Agent, under ENGINEER-OWNERSHIP.

Rationale: this repository is maintained from an environment with no PowerShell,
so nothing here can be executed before handoff. Delimiter balance was the only
static gate and it detects neither ordering nor naming defects. Two live defects
reached committed code and would have broken the two commands already assigned
for local execution. Three successive gate designs passed the defective source —
delimiter-only, then an existence check, then a case-folded scope-blind check —
because a leaked loop binding makes a name exist while holding the wrong type,
and a function-local name of the same spelling masks a file-scope defect. The
gate that detects the class requires a container constructor before the first
indexed write and is scope-aware. A gate that only ever passes is not evidence,
so the tool carries a self-test asserting it still fails on each defect class,
including cases that must not be flagged. Recorded in
`evidence/SCRIPT-STRUCTURE-DEFECTS-2026-08-20.md`. This gate is static only and
does not weaken or substitute for the PowerShell runtime verification assigned
in `STATE.md`.

**D-18.** Loop variables in this repository's PowerShell must not collide
case-insensitively with a container variable in the same or an enclosing scope.
Decided by: Agent, under ENGINEER-OWNERSHIP.

Rationale: PowerShell variable names are case-insensitive, so `foreach ($r in
...)` and a result object `$R` are one variable and the loop silently destroys
the container. This produced a certain failure in `Assert-RememberPruning.ps1`
and silent evidence loss in `Invoke-HubInventory.ps1`. Single-letter loop
variables are the whole cause; descriptive names cost nothing and remove the
class. Enforced as check S4 of the gate in D-17.

**D-19.** Verification and investigation work is governed by a standing rule:
choose the simplest reliable method proportionate to the risk and sufficient for
the next decision, gather evidence where it lives, and stop once the decision is
supported. Full rule in `rules/VERIFICATION-RESOLUTION.md`, which is its sole
owner. Bound as binding by `AGENTS.md`. Decided by: User.

Rationale: bounding the live-Hub divergence question escalated into custom
inventory tooling, traversal hardening, proof scripts, a static gate, and audits
of the verification machinery itself, before the decision, the authoritative
evidence source, the confidence the risk required, and the stopping condition had
been settled. Individual fixes were valid; the method was chosen before the
question was bounded, and the effort was disproportionate to the decision during
deadline-sensitive work. The rule is prospective and does not retire the tooling
already built and verified on `main` — that is now an available capability, and
using it is not licence to repeat the pattern. The rule is cross-agent, not local
to this repository; it is held here only until the canonical `.agents-hub` can
own it, per `PENDING-GLOBAL-PROMOTIONS.md`.

**D-20.** Syntax verification of PowerShell in this repository uses a real
PowerShell parser and runtime, not hand-rolled static checks. `.ps1` sources must
be pure ASCII. Decided by: Agent, under ENGINEER-OWNERSHIP.

Rationale: `Assert-RememberPruning.ps1` failed to parse on Windows because 61 em
dashes in non-BOM UTF-8 were decoded as ANSI, and U+201D -- the third byte of the
mis-decoded sequence -- is accepted by PowerShell as a string delimiter. Three
hand-rolled static gates had passed the file, because none of them was a parser.
PowerShell 7 turned out to be obtainable in this environment as a self-contained
tarball needing no install; the premise that no PowerShell was available had been
accepted without testing it. The parser now handles syntax and the scripts are
executed against fixtures. `Assert-ScriptStructure.py` is retained only for the
semantic classes a parser cannot see -- indexed assignment before construction,
and case-insensitive loop/container collisions -- and is no longer described as a
syntax gate. ASCII-only is preferred over adding a BOM because pure ASCII decodes
identically under UTF-8 and any ANSI code page, so it removes the class instead of
depending on a BOM surviving future checkouts and editors. This is the first
application of `rules/VERIFICATION-RESOLUTION.md`, and it indicts the earlier
tooling built in this repository rather than vindicating it. Evidence:
`evidence/POWERSHELL-EXECUTION-2026-08-20.md`.

**D-21.** `AGENT-SSOT.json` is persisted at the `workspace-governor` repository
root and is authoritative for agent behavior, outranking this repository's
governance. Decided by: User (authority and content); Agent (placement).

Rationale: the user supplied it as an authoritative machine-readable agent
behavior contract. Root placement, not `rules/`, because it is a root behavior
contract rather than a routed topic owner -- the same structural distinction
recorded as Observation 1 for the canonical Hub. Its own `load_order` places it
before `USER-SSOT.json`, so it is bootstrap item 0 in `AGENTS.md`. One supplied
syntax defect was corrected: a missing comma after the `document` member, which
made the object unparseable; content is otherwise verbatim and validates under a
JSON parser. `USER-SSOT.json` is named in the load order but is not present in
any repository or accessible path, so the declared order cannot yet be satisfied.

**D-22.** No `CONFLICT-RESOLUTION.md` will be created. Decided by: Agent, under
ENGINEER-OWNERSHIP, per the user's instruction to assess before inventing.

Rationale: all five `agents-hub-one` rule owners were read, not the three named,
because absence from three files is not absence from the package -- and two
classes assumed uncovered proved owned by the two unnamed files
(`CONTEXT-AND-ORCHESTRATION.md` owns delegated-agent output conflict;
`VERIFICATION-AND-EVIDENCE.md` owns detection of evidence inconsistent with
accepted findings). Three genuine gaps remain: peer agent output conflict outside
any delegation hierarchy (live), same-level requirement or constraint
contradiction (plausible), and stakeholder-goal conflict (latent). Each is the
missing branch of a rule an existing owner already holds, so the hub root
contract's Governance Owner Creation Standard condition 6 forbids a new owner. A
single new file spanning all three would cut across three owners' concerns and
reintroduce the duplication the package exists to prevent. Recorded as gaps in
`PENDING-GLOBAL-PROMOTIONS.md` P-04.

**D-23.** `USER-SSOT.json` is persisted at the `workspace-governor` repository
root, completing the declared SSOT load order. It is **not** a candidate for
promotion into the canonical `.agents-hub`. Decided by: User (authority and
content); Agent (placement and promotion scope).

Rationale: the file is authoritative for the user's Greyed responsibilities,
decision authority and limits, and the agent file's `load_order` names it second,
so both must be resident for bootstrap to be complete. One supplied syntax defect
was corrected -- a missing comma after `profile_name`, the same class as in the
agent file -- and the content is otherwise verbatim and parses. Promotion is
withheld deliberately: the file is explicitly Greyed-scoped by its own
`agent_rules.company_scope`, and the Hub root contract requires shared governance
to be runtime- and business-neutral. Promoting it would put one company's
business scope into cross-agent governance. It belongs to workspace or company
governance instead. Agent duties are never inferred from it; `AGENT-SSOT.json`
§ meta states this and the two files are complementary rather than competing --
`agent_rules.technical_boundary` reinforces the agent file's
`must_not_transfer_to_user` rather than contradicting it. No governance conflict
between the pair was found.

**D-24.** `agents-hub` -- the repository formerly named `agents-hub-one` -- is
the current canonical Agent Hub and live governance authority for all governed
agents and runtimes. `workspace-governor` is the Agent Hub backoffice.
`agents-hub-two` is source material pending reconciliation and is not a competing
authority. Decided by: User.

Status is **canonical now, under active consolidation, structurally incomplete
where known gaps exist**. It must not be described as final. Canonical status
settles which repository governs; it does not assert that the structure is
settled. Known gaps remain recorded in `STATE.md` and `evidence/`.

This supersedes the identity question in D-01 (neither source repository is
canonical; both are inputs) and closes blocker B-4's authority dimension. It does
not disturb D-02 or D-05: consolidation is still required, and `agents-hub-two`
content still has to be reconciled into the canonical Hub. What changed is that
consolidation now proceeds *into a named canonical repository* rather than toward
an unnamed future one.

Decisions D-01 through D-23 and the records in `evidence/` retain the name
`agents-hub-one` where they describe inspections performed under that name.
`DECISIONS.md` is append-only and evidence records what was observed; rewriting
either would falsify the record. The baseline manifest keeps its filename
`AGENTS-HUB-ONE-BASELINE-2026-08-19.json` for the same reason, and because
`Invoke-HubInventory.ps1` discovers it by that pattern.

The GitHub rename was **not** performed by the agent: no rename capability exists
in the GitHub tooling available to this session, and creating a new repository
plus copying content is not a rename -- it loses the redirect and history
association and leaves two repositories competing for authority. Recorded as a
pending assignment in `STATE.md` with execution method and verification step.
Repository references in this repository were updated to `agents-hub` ahead of the
rename, so they become correct the moment it completes.

Not done in this step, per instruction: `AGENTS.md` placement inside `rules/` and
the rule-structure reorganisation. Recorded for the next Hub-maintenance step in
`evidence/GOVERNANCE-STRUCTURE-OBSERVATIONS-2026-08-20.md` and
`PENDING-GLOBAL-PROMOTIONS.md`.

**D-25.** `AGENT-SSOT.json` and `USER-SSOT.json` are **Agent Hub assets**, not
`workspace-governor` governance. Copies held in `workspace-governor` are
backoffice staging, backup, archive or provenance only and must never act as
competing live authorities. The Hub's root `AGENTS.md` remains the bootstrap,
router and authority mechanism, routing agents to the applicable SSOT or rule by
scope. Decided by: User.

This **corrects D-21 and D-23.**

D-21 placed `AGENT-SSOT.json` at bootstrap item 0 of `workspace-governor/AGENTS.md`
and described it as binding and as outranking this repository's governance. That
installed a live governing authority inside the Hub backoffice, which by
definition is not the live source of agent governance. The authority claims have
been removed; the file is unmoved and relabelled as a staging copy.

D-23 concluded `USER-SSOT.json` was not a candidate for the Hub because it is
Greyed-scoped, and belonged to workspace or company governance instead. **That
conclusion is withdrawn.** It confused scope with placement. Greyed scope is a
loading condition -- the file is loaded and applied only when Greyed context is
relevant -- not a reason to hold it outside the Hub. It is a Hub asset and goes to
`agents-hub`, scope-gated at the routing layer.

Consequence recorded, not acted on: every entry in
`PENDING-GLOBAL-PROMOTIONS.md` was pending on the premise that no canonical Hub
existed to own the rule. D-24 discharges that premise. The interim arrangement of
holding cross-agent rules in the backoffice and binding them there no longer has
a justification, which applies directly to `rules/VERIFICATION-RESOLUTION.md`
(P-01). Not moved in this step: it exceeds the current directive, and that file
and its promotion record were created on explicit user instruction, so retiring
the local binding is the user's call.

Exact change list for once `agents-hub` is established, including the Hub root
routing entries without which placement alone leaves the assets unreachable:
`evidence/HUB-ASSET-PLACEMENT-CORRECTION-2026-08-20.md`.

**D-26.** `workspace-governor-agents-hub-one` is the predecessor backoffice for the
same Hub and is an **input** to the current backoffice, not a competing authority.
Active planning directives live in `workspace-governor/plans/`. Decided by: User.

`plans/` holds backoffice planning records only. They sequence work, are not live
governance, and must not become competing authority. The canonical Hub's root
`AGENTS.md` remains the bootstrap, router and precedence authority, and Hub
governance is never duplicated into a plan. `AGENTS.md` routes to
`plans/AGENT-HUB-CONSOLIDATION.md` for Hub consolidation work and
`plans/MCP-GATEWAY.md` for Gateway work.

The Gateway directive moved from the repository root to `plans/MCP-GATEWAY.md`.
Content is byte-identical, verified by SHA-256 against the pre-move commit. D-04
stands: the 46 sections are settled and are not reopened by relocation.

`plans/AGENT-HUB-CONSOLIDATION.md` v0.5.0 **carries forward** predecessor plan
`AGENT-HUB-IMPLEMENTATION-PLAN.md` v0.4.2 rather than replacing it. Its 12-step
sequence, authority map, execution controls, rollback strategy and completion
criteria are reused unchanged; eight deltas are recorded for what changed since
2026-08-17. A verbatim provenance copy is retained at
`plans/reference/AGENT-HUB-IMPLEMENTATION-PLAN-v0.4.2-predecessor.md`, marked
non-executable, so the carried-forward sequence does not depend on another
repository remaining available.

Full classification of the 47 predecessor files -- reusable, reusable with
adaptation, superseded, historical/provenance, unresolved -- is in
`evidence/PREDECESSOR-BACKOFFICE-REVIEW-2026-08-20.md`.

Three corrections to this repository's record follow from the review, and are
recorded because they were errors rather than mere gaps:

- **B-6 was overstated.** It stated the live `.agents-hub` content was unknown. A
  read-only inventory existed from 2026-08-16. Narrowed to "not currently
  verified": the evidence is stale and instructs re-inspection, so a current
  inventory is still required, but the content was not unknown.
- **Planning work was duplicated.** `evidence/HUB-RECONCILIATION-ASSESSMENT-2026-08-19.md`
  independently re-derived a target tree, ownership map and classification that
  v0.4.2 § 4 already held, down to identical classification verbs. It is retained
  because it covers `agents-hub-two`, which the predecessor plan predates, but it
  should have extended the existing ledger rather than paralleled it.
- **C-03 was missed.** A Claude Code runtime precedence conflict was in the
  predecessor register and absent from this one. Now open work item 13.

**D-26.** The canonical Agent Hub repository is `.agents-hub`. The repository and
`C:\Users\Chloe\.agents-hub` are **the same logical Hub** in two
representations -- canonical source and local materialized location for agent
consumption. They are not separate governance authorities and must not drift
independently. Decided by: User.

This corrects the repository name recorded in D-24, which said `agents-hub`. The
authority relationship in D-24 is otherwise unchanged. 52 references across
`README.md`, `STATE.md`, `AGENTS.md`, `PENDING-GLOBAL-PROMOTIONS.md`,
`plans/AGENT-HUB-CONSOLIDATION.md` and the two PowerShell scripts were updated;
`agents-hub-two` and `workspace-governor-agents-hub-one` were left intact.

Operational consequence: a change lands in the repository and is materialized
locally. A local-only edit is drift, not a decision. Discovery tooling reports the
local path state without implying the canonical repository is absent.

**D-27.** The canonical Hub taxonomy is directive-given as of 2026-08-20 and
recorded in `plans/AGENT-HUB-CONSOLIDATION.md` § 6, with root `.agents-hub/AGENTS.md`
as the non-negotiable bootstrap, router and precedence entrypoint. Decided by: User.

This supersedes the predecessor decision placing the router at `rules/AGENTS.md`,
in both v0.4.2 § 4.1 and `HUB-ARCHITECTURE.md`. Three further taxonomy conflicts
with the predecessor architecture are surfaced rather than blended and are
resolved in favour of the directive: `policies/` and `prompts/` are required where
the predecessor said not to create them, and `references/` is narrowed to exclude
backoffice history. `archive/` is not a Hub domain -- history belongs to this
backoffice. Full table in § 6.2.

Two concerns are recorded as already owned, so no new rule file is created for
either: Technical Translation is owned by `AGENT-SSOT.json`
§ `technical_translation_and_audience`, and verification scoping reconciles into
the existing verification and engineering-ownership owners rather than carrying
`rules/VERIFICATION-RESOLUTION.md` into the Hub. See § 6.4, and
`PENDING-GLOBAL-PROMOTIONS.md` P-01 and P-03.

The immediate task remains reconciliation, not implementation. Approval is
required before applying any canonical restructuring or touching live Hub
governance, runtime configuration, code, manifests or lockfiles.

**D-28.** Git is the version-preservation and rollback mechanism for this
backoffice. The pre-edit commit SHA for an edit set is its snapshot, recorded in
that step's evidence record; `git diff <sha>..HEAD -- <path>` is the deterministic
rollback instruction; `DECISIONS.md` plus commit history replace `CHANGELOG.md`
registration. Discretionary version numbering stays retired. Decided by: Agent,
under ENGINEER-OWNERSHIP.

Rationale: an independent review of the predecessor classification found that the
`versions/` and `CHANGELOG.md` mechanism had been classified historical while the
carried-forward plan still required it in four places -- execution control 5, the
whole of Step 4, four rows of the rollback table, and completion criterion 13.
Neither directory nor file exists in this repository, so Step 4's completion gate
was unreachable and Step 5, which lists Step 4 as a prerequisite, **was blocked by
its own plan**. Retiring a mechanism by silence while keeping the obligations that
depend on it is the defect. Git provides immutability, hash identity and
deterministic reversal natively; what was missing was saying so. Recorded as plan
delta D-i.

**D-29.** Vendor-imposed constraints are accepted as binding on the consolidation,
in particular that the canonical root `AGENTS.md` must stay small. Decided by:
Agent, under ENGINEER-OWNERSHIP, on evidenced vendor behaviour.

Rationale: Codex applies a 32 KiB instruction budget shared across the whole
root-to-cwd chain, consumed root-first, and **truncates mid-content with no signal
to the model**. An oversized root bootstrap therefore silently starves every nested
instruction file. Since D-27 makes the root file the non-negotiable always-loaded
bootstrap, its size is a correctness property. Governance content goes behind
router references from a small root file, never inline. Confirmed twice
independently -- the predecessor's 2026-08-16 research and a 2026-08-20 read of
pinned implementation source -- which is why it is treated as settled rather than
provisional.

Two further constraints follow. Symlinks are the verified mechanism for resolving a
runtime-bound path to canonical neutral content, alongside Claude Code's `@path`
imports. And `skills/`, `agents/`, `tools/` and `prompts/` in the accepted taxonomy
are **canonical source only** -- none is discovered natively at a top-level
location, so each requires an adapter projection. Evidence:
`evidence/RUNTIME-CONVENTIONS-2026-08-20.md`. Recorded as plan delta D-k.

**D-30.** Five settled decisions from the predecessor backoffice are adopted
explicitly. They were settled there and had **no representation anywhere in this
backoffice**, so they were load-bearing information existing only in a repository
declared a non-authoritative input. Decided by: User, in the predecessor project,
2026-08-16/17. Carried forward by: Agent.

**Authoritative carrier: this entry, `DECISIONS.md` D-30**, for all five, until they
are promoted to their canonical Hub owners. The files listed in the third column
are non-authoritative -- retrieval aids, provenance copies, or planning records --
and are named only to say where the material also appears. None of them is an
owner.

| # | Decision | Also appears in (non-authoritative) |
|---|---|---|
| 1 | Governance documents are written primarily for execution by agents and maintained by agents acting within authority. Human-oriented synonym replacement must not weaken technical precision. | `LEARNINGS.md` L-003 as a retrieval aid; `plans/reference/HUB-DOCUMENTATION-predecessor.md` as provenance |
| 2 | A human glossary is non-authoritative. It may explain canonical terms but never redefine them, and **must not be placed in `rules/`**. Its final placement is an architecture classification. | `plans/AGENT-HUB-CONSOLIDATION.md` G-04 as a planning record. Previously that plan carried only "no accepted artifact or placement" and had lost the substantive rule |
| 3 | Durable non-obvious learnings are recorded concisely, and normative outcomes are promoted to their sole owner. | `LEARNINGS.md`, which states these rules and applies them to itself. That file is non-authoritative by construction and is not the owner of this decision |
| 4 | Develop and validate a reusable governance workflow as a **skill first**; package it as a plugin only when it is stable and needs installable distribution. Packaging references canonical skill source and must not create a second authoritative copy. | `STATE.md` open work item 22, as current-state tracking. Settled but deferred |
| 5 | Scheduled audits remain separate, deferred runtime automation. Source, package, installed, enabled, discovered, active and verified are distinct states and are never inferred from one another. | `STATE.md` open work item 23. Settled but deferred |

**Correction, same day.** An earlier revision of this entry named
`plans/reference/`, `AGENT-SSOT.json` and `plans/AGENT-HUB-CONSOLIDATION.md` in an
"Owner here" column. All three are wrong as owners: `plans/reference/` is explicitly
never an authority, `AGENT-SSOT.json` is an Agent Hub asset whose local copy is
backoffice staging and not a live authority here (D-25), and the consolidation plan
is a planning record that creates no governance. `LEARNINGS.md` is likewise
non-authoritative. Naming any of them as owner would have reinstated the same
category error D-25 corrected.

Item 3 is why `LEARNINGS.md` now exists at this repository root. It is
non-authoritative by construction: it carries the predecessor's retention and
promotion rules, and an entry whose finding becomes normative is replaced by a
pointer to the owner that governs it.

Items 4 and 5 are recorded as **settled but deferred**. They constrain future work
without authorising any now.

**D-31.** A `SUPERSEDED, DO NOT EXECUTE` banner is prepended to the three
predecessor `tasks/` files as a deliberate archive-safety modification. Decided by:
User.

| | |
|---|---|
| Repository | `klodebeers/workspace-governor-agents-hub-one` |
| Baseline SHA, before the change | `24798d032e39081a6885f3648430786019129ef4` |
| SHA containing the banners | `8d4513caa1809b96117e69e4e602bfff0d8d5c5c` |
| Files | `tasks/01-WINDOWS-ENVIRONMENT-PATH-AUDIT.md`, `tasks/02-SHARED-CONFIGURATION-AUDIT.md`, `tasks/03-CODING-AGENT-BASELINE-INTEGRATION.md` |
| Change shape | Additive only. 3 lines prepended per file. Original content **byte-identical** after the banner, verified by comparison against pre-change copies |

Rationale: those files read as live imperative instructions authorising PATH
edits, software installation and deletion. Their superseded classification existed
only in this backoffice, which does not protect anyone who opens a predecessor file
directly. Git preserves every pre-banner version, so provenance is not destroyed --
only the current tip of the predecessor repository changed. That is the correct
trade: a provenance property that git already guarantees, exchanged for a safety
property that nothing else provided.

Consequence for the record: statements in this backoffice asserting the predecessor
repository is unmodified are now false going forward. `STATE.md`, which owns what is
currently true, is corrected. Dated evidence written before the change is left
intact, because those statements were true when recorded; the change is recorded as
a later revision note in
`evidence/PREDECESSOR-BACKOFFICE-REVIEW-2026-08-20.md` instead.

## Recorded as not decided

These arose in session and are **not** settled. Do not treat them as decisions.

- Placement of the user SSOT within the architecture.
- Whether to adopt, fork or ignore `agent-governance-toolkit`. Provenance and
  licence are established (unmodified MIT fork of a Microsoft project); adoption
  review is not done.
- Whether `atrium_workspace` in its current form satisfies the Gateway directive's
  Atrium integration contract.
- Target tree and ownership map for the consolidated Hub. Preliminary proposal exists; it cannot be accepted until the live Hub is inventoried.
