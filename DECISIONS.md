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

| # | Decision | Owner here |
|---|---|---|
| 1 | Governance documents are written primarily for execution by agents and maintained by agents acting within authority. Human-oriented synonym replacement must not weaken technical precision. | `LEARNINGS.md` L-003 routes it; substance owned by `plans/reference/HUB-DOCUMENTATION-predecessor.md` and `AGENT-SSOT.json` § `technical_translation_and_audience` |
| 2 | A human glossary is non-authoritative. It may explain canonical terms but never redefine them, and **must not be placed in `rules/`**. Its final placement is an architecture classification. | `plans/AGENT-HUB-CONSOLIDATION.md` G-04, which previously carried only "no accepted artifact or placement" and lost the substantive rule |
| 3 | Durable non-obvious learnings are recorded concisely, and normative outcomes are promoted to their sole owner. | **`LEARNINGS.md`**, created for this purpose. No owner for this concern existed here |
| 4 | Develop and validate a reusable governance workflow as a **skill first**; package it as a plugin only when it is stable and needs installable distribution. Packaging references canonical skill source and must not create a second authoritative copy. | `STATE.md` open work; deferred, not active |
| 5 | Scheduled audits remain separate, deferred runtime automation. Source, package, installed, enabled, discovered, active and verified are distinct states and are never inferred from one another. | `STATE.md` open work; deferred, not active. The state vocabulary is also carried in `LEARNINGS.md` L-001 |

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

**D-32.** The authority-carrier portion of **D-30 is superseded**. The
authoritative carrier for all five decisions adopted in D-30 is **`DECISIONS.md`
itself -- D-30 as amended by this entry** -- until each is promoted to its canonical
Hub owner. Decided by: User.

D-30's "Owner here" column named three artifacts that cannot own a decision:

| Named in D-30 | Why it cannot be an owner |
|---|---|
| `plans/reference/HUB-DOCUMENTATION-predecessor.md` | `plans/reference/` is explicitly never an authority. Its files carry a non-authority banner and exist as provenance only |
| `AGENT-SSOT.json` | An Agent Hub asset. The copy in this repository is backoffice staging pending placement in the canonical Hub, and is not a live authority here. `DECISIONS.md` D-25 |
| `plans/AGENT-HUB-CONSOLIDATION.md` | A backoffice planning record. It sequences work and creates no governance |

`LEARNINGS.md` is also **not** an owner. It is non-authoritative by its own
construction; it holds retrieval aids and promotes any finding that becomes
normative to the owner that governs it.

Corrected reading of D-30, replacing its third column:

| # | Decision | Where the material also appears, non-authoritatively |
|---|---|---|
| 1 | Agent-first authoring; human-oriented synonym replacement must not weaken technical precision | `LEARNINGS.md` L-003 as a retrieval aid; `plans/reference/HUB-DOCUMENTATION-predecessor.md` as provenance |
| 2 | The glossary may explain canonical terms but never redefine them, and must not be placed in `rules/` | `plans/AGENT-HUB-CONSOLIDATION.md` G-04 as a planning record |
| 3 | Durable learnings are recorded concisely; normative outcomes are promoted to their sole owner | `LEARNINGS.md`, which states these rules and applies them to itself |
| 4 | Skill first, plugin only when stable and needing installable distribution | `STATE.md` open work item 22. Settled but deferred |
| 5 | Scheduled audits remain separate deferred runtime automation; source, package, installed, enabled, discovered, active and verified are never inferred from one another | `STATE.md` open work item 23. Settled but deferred |

D-30's other content -- the five decisions themselves, their attribution, and the
settled-but-deferred status of items 4 and 5 -- stands unchanged.

**Procedural note.** The first attempt at this correction edited D-30 in place, in
commit `cc854b6`. `DECISIONS.md` is append-only per `AGENTS.md` § File ownership, so
that was not compliant regardless of the correction being right. D-30 has been
restored verbatim to its text at `cc854b6^` and the correction now lives here, in an
appended entry. The non-compliant edit and its restoration both remain visible in
git history; nothing was concealed. Recorded as a learning: a correct finding does
not license a non-compliant mechanism, and an append-only record is corrected by
appending a superseding entry, never by rewriting the original.

**D-33.** **Renumbering.** Two entries in this file were both numbered **D-26**,
making any citation of that identifier ambiguous. The **second** of the two -- the
canonical Hub identity decision, appearing after D-25 and before D-27 -- **is
renumbered to D-33 and is restated in full below.** Decided by: User.

`D-26` now refers unambiguously to the **first** of the two: that
`workspace-governor-agents-hub-one` is the predecessor backoffice for the same Hub
and is an **input** to the current backoffice, not a competing authority.

The original entry is **not edited**; this file is append-only. It retains its
`**D-26.**` heading in place, and this entry is the citable authority for its
content. A reader encountering the second `**D-26.**` heading should treat it as
the historical text of D-33.

### D-33, restated in full

The canonical Agent Hub repository is `.agents-hub`. The repository and
`C:\Users\Chloe\.agents-hub` are **the same logical Hub** in two representations --
canonical source, and local materialized location for agent consumption. They are
not separate governance authorities and must not drift independently. Decided by:
User.

This corrects the repository name recorded in D-24, which said `agents-hub`. The
authority relationship in D-24 is otherwise unchanged. 52 references across
`README.md`, `STATE.md`, `AGENTS.md`, `PENDING-GLOBAL-PROMOTIONS.md`,
`plans/AGENT-HUB-CONSOLIDATION.md` and the two PowerShell scripts were updated;
`agents-hub-two` and `workspace-governor-agents-hub-one` were left intact.

Operational consequence: a change lands in the repository and is materialized
locally. A local-only edit is drift, not a decision. Discovery tooling reports the
local path state without implying the canonical repository is absent.

### Citations repointed

Both existing citations of `D-26` outside this file referred to the renumbered
entry, not to the predecessor-as-input decision. Leaving them would have defeated
the renumbering, so they were repointed to D-33:

| Location | Cited for |
|---|---|
| `STATE.md` | the same-logical-Hub / no-independent-drift rule |
| `evidence/AGENTS-HUB-TWO-RECONCILIATION-2026-08-20.md` | superseding `agents-hub-two`'s self-declaration as `.agents-hub` |

No other file cited `D-26`. Verified by search across `*.md`, `*.json` and `*.ps1`.

**D-34.** Verification has two independent dimensions: **depth is proportionate to
risk; source is always the correct authority.** Proportionality never licenses
checking the wrong source. An authority map for recurring question classes is added
to `rules/VERIFICATION-RESOLUTION.md`, which already owns verification scoping.
Decided by: User.

Rationale: the failure pattern in this project was inconsistent verification
*quality*, not quantity. Early work over-verified low-risk questions by building
custom machinery; later work under-verified a high-consequence fact -- repository
identity -- by trusting a stale local record, then compounded it with two checks
that cannot answer the question at all: an unauthenticated `ls-remote` that fails on
credentials rather than absence, and the old repository name resolving, which
survives a rename by design. Both the rule and `AGENT-SSOT.json`
§ `verification_and_audit` already required identifying where authoritative
evidence exists. Neither named a source, so the choice was re-derived per task and
re-derived wrongly. The map names the authority and, for each class, what is
explicitly **not** authoritative -- the second column is the one that would have
prevented this error.

No obligation is restated, so `PENDING-GLOBAL-PROMOTIONS.md` P-03 is unaffected:
the addition is the part neither existing owner covers, and it travels with the
rule when P-03 is resolved at consolidation.

**D-35.** Step 1 outcomes, decided from the live inventory rather than inferred.
Decided by: Agent, under ENGINEER-OWNERSHIP. Full basis in
`evidence/HUB-TARGET-TREE-AND-CLASSIFICATION-2026-08-21.md`.

| # | Decision |
|---|---|
| 1 | **Hub-root `STATE.md` is retired from the Hub.** The taxonomy left this open. The live file is a mutable operational checkpoint, which is backoffice management state, not agent-consumable desired state -- and the directive states that management, migration and consolidation-progress state is not automatically added to the live Hub. `workspace-governor/STATE.md` already serves that role; keeping both creates two mutable state files for one concern and invites exactly the drift D-33 forbids |
| 2 | **`CATALOG.md` is kept, resolving plan delta D-l.** The taxonomy made it conditional on justification. The live Codex global instruction file requires Hub `README.md` and `CATALOG.md`, so a runtime consumer already depends on it, and the artifact exists with real content |
| 3 | **`policies/` and `prompts/` are not created yet.** No machine-verifiable policy artifact exists; the only candidate, the registry schema, must be rewritten first. The four `agents-hub-two` prompt files are loading instructions, so they are adapter material rather than canonical prompts. The directive's ownership rules define what a directory owns **if it exists**; the tree itself is content-driven, and both are created by their first accepted artifact |
| 4 | **`governance-templates/` and the 7 zero-byte placeholders are retired.** Verified empty on disk. Empty scaffolding is forbidden, and `templates/` is the accepted owner once real templates land |
| 5 | **`design-systems/` remains `Conflict`**, preserved in place and visibly excluded. B-2 is unresolved and the Conflict guard forbids silent reclassification |

B-6 is closed with its premise **disproved**, not aged out. It assumed the live Hub
might hold real content behind GitHub's placeholders. The inventory shows 9 live
files, all byte-identical to baseline `47c0187`, nothing live that the baseline
lacks, and nothing differing. This also verifies D-15's direction against live state
-- the shared audit is live in the Hub -- and confirms the predecessor ledger row
that said to retire the Hub copy was wrong.

Nothing is applied. Restructuring requires approval per
`plans/AGENT-HUB-CONSOLIDATION.md` § 6.7.

**D-36.** Committed evidence emitted by the PowerShell tooling carries a UTF-8 BOM
and CRLF line endings, because `Set-Content -Encoding UTF8` writes a BOM on Windows
PowerShell 5.1. Recorded as a defect; **not fixed now.** Decided by: Agent, under
ENGINEER-OWNERSHIP.

`evidence/LIVE-HUB-INVENTORY-2026-08-21.json` is machine-readable evidence that a
standard parser **rejects**: Python's `json.load` raises on the BOM and requires
`utf-8-sig`. Git also classifies one emitted markdown file as binary. The evidence
content is sound and was read correctly; the encoding makes it hostile to ordinary
tooling, which is a real defect in evidence intended for machine consumption.

Not fixed because `STATE.md` open work item 16 records that the tooling is not to be
modified during this reconciliation phase. The fix is to write with a
no-BOM UTF-8 encoder rather than `-Encoding UTF8`, and it belongs with the other
recorded tooling work.

**D-37.** Step 1 restructuring **applied** to the canonical Hub under approval.
`klodebeers/.agents-hub` `47c0187` -> `80dff05`, verified in sync with the remote.
Decided by: User (approval); Agent (execution). Detail in the Hub commit message.

Applied: `rules/AGENTS.md` moved to the repository root as `AGENTS.md`, with
references updated in **both** directions -- the routing table's four owner
filenames were bare and would have resolved to non-existent root files after the
move, and `rules/ENGINEER-OWNERSHIP.md` referenced it as a sibling. `README.md` and
`CATALOG.md` repointed. `STATE.md` retired. Six placeholder files retired.

`references/AGENTS-MD-LIVE-AUDIT-2026-08-16.md` was deliberately **not** updated: it
is dated evidence and its statements were true when recorded.

**Six placeholders retired, not the seven classified.** The approved list said
retire all seven and also preserve `design-systems/` untouched. Those contradict,
because `design-systems/placeholder.md` is one of the seven. Resolved in favour of
the explicit preservation instruction and the Conflict guard, which forbids changing
a Conflict-classified area. `design-systems/` verified untouched by staged-diff and
by blob hash identity.

Because git does not track empty directories, retiring the placeholders also removed
`runtime-adapters/` from the repository. That is consistent with creating a
directory only with its first real artifact; it returns at Step 9 with an accepted
adapter.

**Not created, deliberately outside the approved scope:** `agents/`,
`orchestration/`, `registry/`, `templates/`, `context/`. Each requires an Adapt
transformation on `agents-hub-two` content -- stripping duplicated governance
blocks, deduplicating four routing copies, splitting identity from routing,
extracting quadruplicated domain knowledge. That is Step 2 change work, gated
separately, and creating them now would have expanded scope.

**D-38.** Instruction-file precedence is resolved for both runtimes, from vendor
documentation. Decided by: User, supplying the sourced answer.

**Codex.** A repository-level `AGENTS.md` normally outranks
`~/.codex/AGENTS.md` on conflict, because the global file is concatenated first and
repository then nested files follow, so the more specific text appears later.
Effective order: system/developer/user, then machine, then repository root, then
nested. Within one level, `AGENTS.override.md` replaces `AGENTS.md` at that same
location; an override does not let a machine-level file outrank repository
instructions. This confirms the depth-based reading inferred from implementation
source and withdraws the third-party claim that a home override beats everything.

**Claude Code.** Applicable `CLAUDE.md` files are **additive** -- all stay in
context, loaded broader to more specific: managed policy, user, repository, nested,
project-local. Project instructions load after user instructions, so project
guidance normally takes effective precedence on conflict, and more-specific
directories outrank broader ones. The correct reading is "more specific wins on
conflict", not "the repository file replaces the machine file". Managed organization
policy is higher authority by design, for requirements users should not override.

**The distinction that matters is preserved and still open.** `CLAUDE.md` guidance
is **not an enforcement mechanism.** Precedence decides which guidance wins when two
files disagree; it does not make any of it binding. C-03 is therefore closed on
precedence and open on enforcement: anything that must hold regardless needs an
enforcement carrier -- a managed setting or a hook -- chosen per rule. Machine-level
placement is not a ceiling in either runtime, which strengthens rather than weakens
that conclusion.

**D-39.** A confirmed defect is treated as an instance of a **class**. On
confirmation, the class is swept across the scope the same change affected, every
confirmed instance inside the approved change is fixed, the class is verified, and
work stops before anything outside that boundary. The person who reports the first
defect is not responsible for enumerating the rest. Recorded in
`rules/VERIFICATION-RESOLUTION.md` § Defect class. Decided by: User.

Rationale: one stale reference was reported after the Step 1 restructuring. Rather
than sweeping the class, the literal instance was fixed and the siblings were listed
back for approval -- making the user the defect enumerator. The sweep found **twelve**
instances where five had been reported.

The class was dangling references created by one commit. Its cause was checking one
direction only: references to the file that **moved** were verified, references to
the files that were **deleted** were never checked, and the result was reported as
"dangling references verified".

Eleven instances fixed, one deliberately not: the `CATALOG.md` row for
`design-systems/.remember`, which is absent from the repository but present in the
materialized Hub, sits inside a `Conflict`-classified area preserved untouched, and
correctly instructs preservation. Recorded as a documented exception in the check.

The check itself needed two corrections before its result meant anything. It
resolved paths from the repository root, so valid sibling references between rule
files read as dangling -- acting on that would have broken six correct references.
And it discarded trailing-separator tokens as bare words, so directory references
were never examined, which is why the first pass reported five of twelve. Both are
recorded in the rule: a sweep is only as good as its check, and the check must be
verified against a known instance and a known-good one before its output is trusted.

**D-40.** Dangling references introduced by the Step 1 restructuring are cleared.
`klodebeers/.agents-hub` `80dff05` -> `0517a4b` -> `c6c966b`. Verified against the
extracted remote, not a working copy: 0 dangling references across the 8 live
documents, dated evidence excluded. Decided by: Agent, under ENGINEER-OWNERSHIP.

`README.md`: step 4 repointed to the fully qualified Workspace Governor path so it
cannot read as repo-relative; the `runtime-adapters/` and `governance-templates/`
source-area lines removed; the blockers pointer repointed. `CATALOG.md`: the
`STATE.md` row removed, the two runtime-adapter rows replaced with the true state,
the four governance-template rows removed.

A retirement row was briefly written in place of the removed rows and then removed
as well. A live inventory lists what exists, not what was removed or what may exist
later; retirement belongs in the backoffice record. `design-systems/` untouched,
verified by zero staged and unstaged changes.

**D-41.** The local Hub at `C:\Users\Chloe\.agents-hub` is materialized by
**git**, not by copying files. The user confirmed 2026-08-21 that the path is a git
working copy, and authorised materializing `c6c966b` there. Decided by: user, on the
mechanism question the agent raised.

Rationale: D-33 makes the repository and that path one logical Hub which must not
drift. Drift is only detectable if both sides carry a comparable ref. A hand-copied
tree has no ref, so divergence would be invisible until something broke, and every
future Hub change would need the copy repeated by hand. `git pull` makes the local
state provable in one command.

Consequence: whenever the canonical Hub gains a commit, materializing it locally is
an open item until `git rev-parse HEAD` matches on both sides. Recorded as a standing
verification assignment with a recheck trigger rather than rediscovered each time.
Execution needs the local Windows machine and cannot be performed from a cloud
session -- blocker B-5.

**D-42.** The fourth item under § Recorded as not decided -- target tree and
ownership map for the consolidated Hub, "cannot be accepted until the live Hub is
inventoried" -- is **settled** and no longer open. Decided by: user, at the Step 1
approval. Superseded by D-35 (Step 1 outcomes accepted, all 46 inputs classified,
live Hub inventory returned COMPLETE) and D-37 (the restructuring applied at
`80dff05`). Its precondition was met by the Step-1 gate.

Recorded as an appended correction because `DECISIONS.md` is append-only; the stale
bullet is left in place rather than edited. Same class as D-32, which corrected D-30
the same way.

**D-43.** Step 2 is applied. Five Hub domains created with six artifacts, at
`d1a8553` in the canonical Hub. Decided by: user authorisation 2026-08-21
("proceed with Step 2"); executed by agent.

`registry/agent-registry.json`, `registry/agent-registry.schema.json`,
`orchestration/routing.json`, `agents/notion-formula-logic.json`,
`context/NOTION-FORMULA-V2.md`, `templates/verification-checklist.json`. A
directory is created by its first real artifact, so Step 2 is six artifacts, not
the 27-file source package. The remaining source artifacts keep their recorded
dispositions. Evidence:
`evidence/HUB-STEP-2-FIRST-ARTIFACTS-2026-08-21.md` revision 2.

**D-44.** The Hub has one domain-neutral entry point, and domain selection is a
step after entry rather than a choice of door. Decided by: agent.

The source declared its entry point in eight disagreeing locations, and the only
machine-readable one named the Notion coordinator as the sole entry -- so a general
request reached the Notion domain and then met a registry with no routing rules for
any general specialist. `orchestration/routing.json` is the single owner of the
entry point, the pre-routing condition, domain selection and every route; the eight
source locations are listed there as superseded.

Domain selection is **carried, not invented**: the source stated the step in prose
in `package-layout.json`, `docs/README.md` and
`prompts/general-coordinator.prompt.txt`. What is new is the machine-readable
condition and its placement after a single entry point. An earlier draft claimed
the source had no such step; that claim was false and was corrected before commit.

Where two copies of the same routes disagreed in wording, the coordinator's copy
was taken and the other superseded -- chosen, not blended into a third phrasing
neither source states. The routes are generated from the source files at authoring
time, so fidelity is structural rather than asserted.

**D-45.** The Notion coordinator identity is folded into the orchestrator entry,
whose domain is `shared`. Decided by: agent, applying the reconciliation's settled
Finding 6.

It is the same orchestrator role instantiated for a domain, not a distinct agent.
The registry therefore holds twelve identities, and the fold is recorded on the
entry that absorbs it rather than left implicit. `shared` means one orchestrator
serves every domain after domain selection; without it, the `notion-operations`
domain had no orchestrator to receive routed work while the schema described a
per-domain model.

**D-46.** A reference to something that does not exist yet is recorded as `null`
with a status, never as the path it will eventually have. Decided by: agent.

Eleven of twelve registry entries have no normalized definition. They carry
`definition: null` and `definition_status: pending`, and the schema enforces the
pairing in both directions. Writing the eventual paths would have manufactured
eleven dangling references -- the class D-39 exists to prevent. The same rule
applies to the migrated definition's template dependencies.

**D-47.** An agent-definition schema is owed and deliberately not written in Step 2.
Decided by: agent.

The source used two incompatible vocabularies for the same concepts and had no
schema for either. The one migrated definition fixes the vocabulary. Authoring a
schema from a single migrated file would encode one shape as though it were
thirteen, so the schema is required before a second definition migrates and must be
written against all thirteen source shapes.

**D-48.** `policies/` is not created for the registry schema. Decided by: agent.

The schema is machine-verifiable, which is what `policies/` holds, but nothing
enforces it in any runtime; placing it there would assert an enforcement boundary
that does not exist. It sits in `registry/`, which the accepted target tree already
specified as holding the registry plus its schema. `policies/` is created by its
first artifact that something actually enforces.

**D-49.** New Hub asset domains are indexed in `CATALOG.md`, are **not** added to
the root `AGENTS.md` routing table, and are given normative placement by a
`README.md` bootstrap step. Decided by: agent.

The root routing table maps governed conditions to governance owners, and the root
contract states it "does not govern ordinary non-governance artifacts or Hub domain
placement". The six Step 2 artifacts are canonical source data; listing them as
routed owners would present each as a rule owner.

Catalog presence alone was **not sufficient**, and an earlier draft treated it as
if it were. `CATALOG.md` declares itself non-authoritative and proving nothing, and
the root contract tells an agent to load only routed owners -- so nothing instructed
an agent to enter work through the routing file, and an artifact declaring itself
"the single entry point" was self-appointed. `README.md`, which owns bootstrap
navigation, now carries step 4: enter agent work through `orchestration/routing.json`
and resolve identity through `registry/agent-registry.json`, neither being a
governance owner and neither granting permission. Precedence is untouched.

This is D-d's lesson applied, in both halves: placement without a route leaves an
asset unreachable, and the route must be both the right kind and normatively real.

**D-50.** A canonical template does not ship a default answer to a question another
owner governs. Decided by: agent.

`templates/verification-checklist.json` carried `human_review_required: false` from
its source. Whether human approval is required is owned by
`rules/AUTONOMY-AND-PROTECTED-BOUNDARIES.md`, so a template shipping `false`
supplies a no-approval-needed default outside that owner. The value is `null`,
which requires whoever fills the checklist to answer it. This is the only field
where the template diverges from its source.

**D-51.** Two adversarial review findings are rejected, and the reasons are settled
so they are not reopened without new evidence. Decided by: agent.

1. **The verification checklist is not a narrowed copy of the evidence record.**
   `rules/VERIFICATION-AND-EVIDENCE.md` § Proportionate Evidence Record governs what
   an evidence record contains after a change; the template is a pre-action
   checklist, which the same rule's § Verification Standard asks for. Two artifacts,
   no duplication. The review did surface a real gap: **no accepted evidence-record
   template exists**, and the source's `execution_record_template` is the candidate.
   Recorded as open work. `CATALOG.md` states the distinction so the checklist is
   not mistaken for the record.
2. **Domain instantiations inside a specialist definition are legitimate and
   required.** The reconciliation settled this: deleting them "leaves the domain
   with no statement of what evidence counts". "Verify formula output against actual
   database data, not just syntax" states what evidence counts *for formulas*; the
   general obligation stays with its owner. The definition names the boundary in its
   `authority` block. Reopening this would reverse a settled finding without new
   evidence, which `rules/ENGINEER-OWNERSHIP.md` forbids.

**D-52.** Migration narrative, retirement arguments and progress ledgers do not go
into live Hub artifacts. Decided by: agent, applying the directive.

Management, migration and consolidation-progress state are not Hub material, and
§ 6.8 requires no backoffice history in live authority. An earlier draft of all six
artifacts carried retirement narratives, rename maps, "why this file exists"
sections, a schema description that argued with its predecessor, and
not-yet-migrated ledgers. Live artifacts now carry short provenance identifiers and
a superseded-source list; the reasoning lives in the backoffice evidence record.

**D-53.** A durable verification claim must have a re-runnable artifact behind it.
Decided by: agent.

An earlier draft stated "validated against 8 negative cases" in the Hub catalog
with nothing in any repository that could reproduce it -- agent confidence presented
as verification, which the evidence standard forbids. Two scripts now hold the
claims: `scripts/Test-HubRegistrySchema.py` (schema validity, instance validation,
eight negative cases, one positive control, four cross-artifact consistency checks)
and `scripts/Assert-ReferenceIntegrity.py` (every Markdown backtick path and every
JSON `$schema`, `$id`, `definition` and `path` field). Verification results belong
in the backoffice record, not in the live catalog, and the catalog's own header says
its presence proves nothing about verification.

**D-54.** The Step 2 artifacts are corrected after four independent blind audits, at
`df33f07` in the canonical Hub. Decided by: agent, on findings verified against
source. Evidence: `evidence/HUB-STEP-2-FIRST-ARTIFACTS-2026-08-21.md` revision 3.

Four reviewers audited the committed state against the source package and the
approved scope with no access to the implementer's rationale. Their factual claims
were checked against source before any change. The corrections are recorded in the
evidence file; the settled positions they establish are D-55 through D-61.

**D-55.** Three audit findings are rejected, with reasons settled so they are not
reopened without new evidence. Decided by: agent.

1. **"Step 2 had no recorded approval" is wrong on the facts.** The user authorised
   it in session on 2026-08-21. The reviewer was blind to that by design. The
   finding does identify a real record defect: `STATE.md` carried the approval stop
   condition with nothing recording that approval had been given. Corrected there.
2. **A negative scope disclaimer is not a restatement of a routed rule.** "This file
   grants no capability" denies that the file answers a question; it does not answer
   it. The accepted taxonomy requires exactly this boundary, and an artifact read in
   isolation must carry it. Each disclaimer now names the owner, which is what the
   root contract asks of a non-owning file.
3. **A statement about platform causality is not sequencing content.** "A formula
   that depends on a retyped property is in scope of that change" is a domain fact.
   The taxonomy's `orchestration/` sequencing concerns the ordering of agents and
   steps. The imperative form was removed so it cannot be read as a rule.

**D-56.** The registry records identity, not migration progress or derived state.
Decided by: agent.

`canonical_status` is `accepted` or `retired`, not two flavours of accepted, so an
identity can be withdrawn without deleting the record that it existed.
`definition_status` is removed: `definition: null` already carries that fact, and a
required field encoding migration progress made progress into canonical data.
`dependencies[].available` is removed from the agent definition for the same reason.
Discretionary `version` and `updated` fields are removed per D-28, which settles that
git carries version identity.

A folded source id is recorded in `folded_ids`, so a consumer resolving
`notion-coordinator-orchestrator` resolves to the agent that absorbed it instead of
failing. Uniqueness of ids and names, which JSON Schema cannot express, is enforced
by `scripts/Test-HubRegistrySchema.py`.

**D-57.** D-12 and D-14 are superseded in the parts that describe Hub structure.
Decided by: agent, applying the directive taxonomy settled in D-27 and the target
tree accepted in D-35.

D-14 required `agents/` subdivided into `general/` and `notion/` and a
"domain-keyed" registry, and argued that "a flat `agents/` would leave [the
asymmetry] in place and keep general agents second-class". D-12 placed three
Notion-specific templates "owner-local under `agents/notion/`".

The accepted taxonomy has a flat `agents/`. The asymmetry D-14 targeted is real and
is resolved differently: the source's two-list model, where general agents sat in a
key named for what they are not, is replaced by one list with an explicit `domain`
field, and the schema covers every key. General agents are not second-class under
that model. D-14's diagnosis stands; its prescribed structure does not.

Surfaced rather than silently replaced, because two blind reviewers independently
found the contradiction and this repository requires a conflict to be reported.
D-12's template-placement half is superseded with it; template placement follows the
accepted tree.

**D-58.** One identifier per artifact concept, and the retirement of the general
verification-checklist synonyms is a decision, not only an observation. Decided by:
agent.

The source used `verification-checklist-template` and `verification_checklist_template`
for one concept, and the reconciliation recorded that a consumer would need a mapping
table. The canonical identifier is `verification-checklist`: lowercase kebab, no
`-template` suffix, since the directory conveys the type. JSON path values use
forward slashes; Markdown prose uses the Windows form already used throughout the
Hub's documents.

The general contract's `expected_output` and `human_action_required` are retired in
favour of `expected_result` and `human_review_required`. The two contracts differed
only in synonyms, and building a second variant for that would have created a
needless divergence. This was recorded only in evidence and in the Hub catalog;
recorded here now, because it is a settled decision and the catalog declares itself
non-authoritative.

**D-59.** `validated_references` is classified as domain operating context. Decided
by: agent, closing reconciliation open item 4 for that half.

The four cited Notion documentation URLs are platform references, not planning
state, so they belong with the domain context rather than in `references/`, which the
taxonomy narrows to supporting references and not backoffice history. They are held
at subsystem scope in the source and are carried in full, including the views
reference, so nothing is stranded while the domain has one context file. The
`planning_model` half remains unclassified and is not migrated.

**D-60.** Bounded, blind adversarial subagent review is the mechanism for the
independent pre-edit review the plan requires. Decided by: user instruction
2026-08-21, recorded here. Closes `STATE.md` open work item 21.

Each reviewer is given the authoritative source, the approved scope and the
resulting implementation, and is denied the implementer's own rationale, so it
cannot prime the review. Reviewers report findings only and must not implement an
alternative architecture. Every finding is verified against source by the
implementer before it is accepted or rejected, and a rejection is recorded with its
reason. Confirmed defects are fixed within the approved boundary, and sibling
instances of the same class are swept without being enumerated by the user.

Reviews are used where independent research, classification or verification
materially reduces self-review risk -- not mechanically for simple operations. The
practice has now found material defects in three successive rounds, including four
provenance claims that overstated novelty and three source obligations dropped in a
consolidation.

**D-61.** An obligation orphaned by a consolidation is recorded as owed, never
absorbed silently. Decided by: agent.

Consolidating the quadruplicated formula material moved platform facts into
`context/`, and three source obligations travelled with them and were dropped: a
formula must be validated after a schema change; schema and formulas must be
reviewed together when migrating older logic; and a coordinator must validate actual
behavior on any formula migration. Two belong to `notion-schema-relations-agent` and
one to the orchestrator, neither of which has an accepted definition.

The context file now states that it does not absorb such obligations and that where
the owning definition is not yet accepted, nothing there carries them. The
obligations are listed in `STATE.md` open work so they land when their owners
migrate. A record that an obligation was dropped is not a carrier for it; the record
exists so the carrier is not forgotten.

**D-62.** A source obligation met by structure is recorded as met, not left as an
attribution. Decided by: agent, on the fifth audit's finding.

The source states that formula logic must be treated as a dedicated domain with its
own verification model. The consolidation turned that into "which the source package
gives as the reason for treating it as a dedicated domain" -- an attribution of
rationale, with nothing saying whether the obligation was met. Three sibling
obligations from the same material were recorded as owed; this fourth was handled
differently and silently, which is the defect D-39 exists to prevent: a class swept
three quarters of the way.

It is in fact met: the `notion-operations` domain and its formula specialist exist,
and that specialist's rules state what evidence counts for formula work. The context
file now states the obligation and how it is met, and `STATE.md` records it as met
rather than owed. Either outcome is acceptable; leaving a reader unable to tell which
is not.

**D-63.** A governance gap surfaced inside the governed tree is also recorded in the
backoffice. Decided by: agent.

`orchestration/routing.json` surfaces an unowned obligation from the source -- define
the required fields and produce a decision brief before technical work -- because the
root contract requires surfacing rather than answering. That disclosure is correct
and stays. But open work is owned by `STATE.md`, and a gap visible only to a reader
of the governed tree is not recorded as owed. Both records are required: the tree
tells a consumer that no owner carries it; the backoffice tells whoever schedules
work that it needs an owner.

**D-64.** A route's `output` is the routing-time expectation; an agent definition's
`outputs` govern. Decided by: agent.

Both answer what an agent produces, both are carried from the source, and they
disagree in content for the one migrated agent. The definition owns the agent's
deliverables, as its own authority block already claims. `orchestration/routing.json`
now states the relationship in its `does_not_own` block, so the duplication has an
owner before the remaining ten migrations replicate it eleven times. Assigned rather
than blended: neither wording was rewritten to match the other.

**D-65.** A verification script must fail the defect it was written to catch, and
that is proved by building the defect. Decided by: agent, on the fifth audit's
demonstrations.

The fifth audit built defective trees and showed the checks passing them: the whole
consequences section of the context file deleted; a falsified agent name masked by an
unrelated marker; the one deliberate template divergence reverted, with the check
count silently dropping while the script still reported that every check ran; two
source governance blocks the approved record names absent from the leak list;
markdown never scanned; ten of fourteen real references unexamined because only two
JSON keys were read; a governance document accepted as a resolved schema declaration
because the file existed; and no check at all for the permission-shaped keys that all
three scripts exist to prevent.

All are closed, and the eleven defect cases the audit built are now regression cases
that each produce a non-zero exit. The standing rule: a check is not evidence until
it has failed on a built instance of the defect and passed on clean content. A
recorded exemption **requires** its divergence rather than merely excusing it, since
an exemption that only excuses lets a settled decision be reverted silently.

**D-66.** Conflict C-04 is resolved. `context/` owns scoped knowledge and supporting
operating context; it owns no authority. Decided by: user, as taxonomy owner,
2026-08-21. Supersedes the gloss "scoped operating context, not knowledge or
authorization" and confirms the accepted Step-1 target tree.

It owns domain concepts, architecture explanations, domain and product terminology,
design rationale, integration constraints, project-specific workflows, historical and
operational references, supporting technical background, and detail that would
otherwise bloat the root instruction files. It is version-controlled and travels with
the Hub.

It does **not** own governance, permissions, approvals, protected boundaries,
behavioral obligations, verification authority or instruction precedence. Those stay
with `rules/` or another explicitly assigned Hub owner.

Two clauses carry beyond `context/` and are now stated in the Hub itself:

1. **A file is not mandatory because it exists.** Anything under `context/` is loaded
   only when explicitly routed by the Hub bootstrap, the orchestration layer, an agent
   definition, or a runtime adapter.
2. **A runtime adapter is a discovery entry point, not a definition.** Codex, Claude
   Code and future runtimes may load or expose canonical Hub context through their own
   mechanisms; they must not redefine what `context/` means, what it owns, what
   authority it has, or where canonical knowledge belongs. The Hub stays
   agent-agnostic.

`context/NOTION-FORMULA-V2.md` is confirmed correctly placed: supporting domain
knowledge, absorbing no obligation, granting no authority. Backoffice separation is
restated with it -- `workspace-governor` keeps research, evidence, migration work,
provenance, recovery, planning, project state and history, and none of that becomes
runtime context by being useful. Full text: `plans/AGENT-HUB-CONSOLIDATION.md`
section 6.2a.

**D-67.** General reusable capability knowledge belongs in global context; exact
domain implementation belongs in domain or project context. Decided by: user,
2026-08-21, corrected the same day.

Global context is `context/global/` **inside the Hub** -- user-level and
version-controlled. The first statement of this rule placed it outside the repository
in `~/.codex/` or `~/.claude/`; the corrected sample keeps it in the Hub, which is the
"another explicitly managed global location" that rule already allowed. Those runtime
directories are discovery locations an adapter projects into, which is what runtime
separation says they are, and it keeps global knowledge version-controlled instead of
unmanaged on one machine.

Accepted shape: `context/global/` with `user-preferences/`, `user-stack/`,
`tooling/{git,powershell,python,node,mcp}/`,
`services/{notion,excel,dashboards}/` and `terminology/`. Exact domain
implementation -- named databases and their ids, exact properties and allowed values,
relations between specific databases, project formulas and views, domain workflow
rules and terminology, for Greyed, Fina, Klo Professional, Klo Personal or a specific
dashboard schema -- is held per owner outside `context/global/`.

Applied to the one artifact this affects: `NOTION-FORMULA-V2.md` is general Notion
platform behavior, not any project's schema, so it moved to
`context/global/services/notion/`. **No empty branches were created.** Every other
directory in the shape arrives with its first accepted artifact, as everywhere else in
this taxonomy.

**D-68.** The adapter directory is `adapters/`, with `claude/`, `codex/` and
`generic/` beneath it. Decided by: user, as taxonomy owner, 2026-08-21. Supersedes
`runtime-adapters/` in the accepted taxonomy and in the Hub `CATALOG.md`.

Surfaced rather than applied silently: two accepted records said
`runtime-adapters/`, and D-13 and D-37 both refer to it by that name. The corrected
sample is the later statement from the owner of the taxonomy, so the new name governs
and the earlier name is superseded wherever it appears. `generic/` is new -- the
earlier taxonomy named only per-runtime adapters.

Nothing is built. No adapter exists, the directory is created with its first accepted
adapter, and this is therefore a rename of an unbuilt domain. `CATALOG.md` states the
accepted names so the rename is visible where a reader looks for adapters, and the
adapter projection that `agents/` now owes (D-29) will land under the new name.

**D-69.** There is no `global/` folder in the Hub. The Hub is the global layer.
Decided by: user, as taxonomy owner, 2026-08-21. Corrects D-67.

Everything under `.agents-hub/context/` already applies across projects, so a
`global/` subdirectory is a redundant level inside a repository whose stated purpose
is reusable cross-project source. The `context/global/...` path created under D-67 is
withdrawn; `NOTION-FORMULA-V2.md` returns to `context/NOTION-FORMULA-V2.md`, where the
owner had already confirmed it was correctly placed.

What survives from D-67: `context/` holds general reusable capability knowledge, and
exact domain implementation is a different thing. The accepted substructure --
`user-preferences/`, `user-stack/`, `tooling/{git,powershell,python,node,mcp}/`,
`services/{notion,excel,dashboards}/`, `terminology/` -- stands with the `global/`
wrapper removed, and every branch still arrives with its first accepted artifact.
`~/.codex/` and `~/.claude/` are runtime discovery locations an adapter projects into,
not a second home for canonical knowledge.

**Recording the error, because it repeated.** I applied a sample tree as an
instruction to relocate an accepted artifact, one message after the owner had
confirmed that artifact's placement. I did the same thing in the same round with the
`adapters/` rename, where it happened to be correct. A sample illustrating how
content is organised is not authority to restructure live content: the classification
model and the placement of an existing file are separate decisions, and only the
second needs the owner's word. `LEARNINGS.md` L-033.

**Left open, not resolved by inference.** Two owner statements disagree about where
exact domain implementation lives. The C-04 definition lists domain knowledge and
project-specific workflows as suitable Hub `context/` content; "everything in
agents-hub is global" reads against holding one project's schemas there. No such
content exists in the Hub, so nothing is blocked. Recorded as `STATE.md` open work
28b.

**D-70.** Local Hub materialization is routine, not a reported action. Decided by:
user, 2026-08-21: the operator always pulls the changes.

D-41 settled that the repository and `C:\Users\Chloe\.agents-hub` are one logical
Hub carried by git, and D-33 that they must not drift. Neither is weakened. What
changes is the reporting: materialization stops being restated as a next action, and
the pull command stops being handed back after every commit.

Practical form. `STATE.md` records the current expected HEAD under Verification
assignments so a mismatch can be checked against something. The recheck trigger is an
observed mismatch -- a reported HEAD that differs, a failed pull, a local edit --
rather than the existence of a new commit. Nothing is asked for unless the two have
actually diverged.

This is a communication decision, not a governance one. If the SSOT communication
owner is the durable home for it, it belongs there at SSOT placement (open work 4);
recorded here meanwhile so it is not rediscovered.

**D-71.** Two corrections to D-70. Decided by: user, 2026-08-21.

**Mechanism: GitHub Desktop, not a terminal.** The operator pulls with the GitHub
Desktop app. D-41 is unaffected -- a desktop client is git, so the ref-comparable
materialization it requires still holds -- but the PowerShell command blocks handed
back repeatedly were never the right instruction. Stop producing them for this.

**Scope: while nothing is in flight, not unconditionally.** D-70 recorded the routine
as standing. The user scoped it to the present situation, with no ongoing work. The
practical difference: silence is right when the repository and the local copy are both
idle, and a mismatch that would affect work actually in progress is still worth
raising. Absence of a reminder is not an assertion that the two are equal at any given
moment.

Recorded because the overstatement was mine: an instruction given for now was written
into the record as a permanent rule, which is the same class of error as treating a
sample tree as a directory spec (D-69). A preference stated in the present tense is
recorded with its scope, not generalised.

**D-72.** D-70 and D-71 restated in plain language, and the jargon retired. Decided
by: agent, after the user said the earlier wording was not understandable.

The situation, without the vocabulary: there are two copies of the Agent Hub. One is
the GitHub repository. One is the folder `C:\Users\Chloe\.agents-hub` on the
operator's PC. Only the repository can be changed from a cloud session. The folder
catches up when the operator pulls in GitHub Desktop.

**"Materialization" is retired as a term.** It meant nothing more than "the folder has
caught up with the repository", and saying that costs no more words. Records that use
it are not rewritten -- this file is append-only -- but nothing new uses it, and
`STATE.md` now says it plainly.

**"While nothing is in flight" is retired too, as over-specified.** The practical rule
is one sentence: do not tell the operator to pull; raise the folder's state only when a
specific task needs it current. The clear case is the fresh-session bootstrap test,
where a new agent reads these files from that disk, so a stale copy produces a wrong
answer about what the Hub contains.

Nothing about D-33 or D-41 changes: the two copies are still one logical Hub carried by
git, and divergence is still a defect. This is about how it is described and when it is
mentioned.

**The lesson, recorded because it is mine.** A term invented for convenience became
load-bearing across several records, and its meaning was never checked against the
person who had to read them. If a record cannot be read by the person it is written
for, its precision is worth nothing. `LEARNINGS.md` L-036.

**D-73.** The step labels used in this project did not match the plan's sequence.
The mapping is recorded and the labels are corrected going forward. Decided by:
agent, on inspection prompted by the user asking what the plan says is next.

The authoritative sequence is the 13 steps carried forward in
`plans/AGENT-HUB-CONSOLIDATION.md` section 3. "Step 2" was used here to mean *create
each new domain with its first accepted artifact*. That is the plan's **Step 7**
(refactor structural domains and accept reusable artifacts) together with **Step 8**
(migrate accepted external source). The plan's actual Step 2 is provenance,
sensitivity and external-source gating, and it was never done.

Similarly, the restructuring recorded as part of "Step 1" -- moving `AGENTS.md` to the
root, retiring the Hub `STATE.md` and the placeholders -- is the plan's **Step 5**.
Step 1 prohibits moves, renames and deletions outright, so that work was never Step 1
under any reading.

**The executed work stands.** It is verified by three scripts and five independent
audits, and nothing about it changes. What was wrong was the label, and labels matter
here because each step carries prerequisites and a completion gate that the wrong
label silently skips.

**The ordering cost, recorded rather than glossed.** Steps 7 and 8 ran before Steps 2
and 3, which are their stated prerequisites. Step 3 produces the semantic ownership
map -- the artifact whose job is to decide duplicate ownership before anything is
edited. It was skipped, and five audits then found duplicate-ownership defects in the
Step 7 output: a route's `output` against a definition's `outputs`, the agent-to-domain
mapping held in two files, one authorization boundary restated across several
artifacts. Each was fixed when found. Finding them one at a time through adversarial
review is the expensive path, and ten agent definitions remain to migrate.

**Consequent next action:** the plan's Step 2, which has two open gates and is cheap,
then Step 3. Detail in section 7 of the plan. `STATE.md` carries it as the next action.

**How this went unnoticed.** The plan does not enumerate its own steps -- section 3
carries them forward by reference to the predecessor document -- so every claim about
"the next step" in this project was made from memory of a list held in another file.
Section 7 now names the position explicitly, so the answer is readable in the plan
rather than reconstructed. `LEARNINGS.md` L-037.

**D-74.** A plan owns its sequence and what each step requires. `STATE.md` owns where
the work stands in that sequence. Decided by: agent, prompted by the user's diagnosis
that the plan was not reachable from the bootstrap.

Three structural fixes, none of them a promise to be more careful:

1. **The plan now lists its own steps.** Section 3a names all thirteen. Until today
   section 3 carried the sequence by citing its source, so the plan asserted that
   thirteen steps existed without naming them, and the names lived only in a
   provenance copy marked never executable. Reading the plan would not have prevented
   D-73's label drift; the plan did not contain the answer.
2. **`AGENTS.md` forbids naming a step from memory.** Bootstrap step 5 now states that
   a step, phase or position claim requires reading the plan's step list and then
   `STATE.md`, in that order, and says why: a step label carries prerequisites and a
   completion gate, so a wrong label skips both with no error surfacing. Plan routing
   adds that a plan which cites its sequence elsewhere is unusable for this and must be
   fixed first.
3. **Position moved out of the plan into `STATE.md`.** An earlier fix today put a
   where-we-stand table in the plan, which is the wrong owner and would have drifted
   against `STATE.md`. The file-ownership table now names the split explicitly:
   `STATE.md` owns position; the plan owns the sequence and the per-step requirements.

**What this does not do.** `CLAUDE.md` and its imports are guidance, not an enforcement
mechanism -- C-03, unchanged. `CLAUDE.md` here is a one-line `@AGENTS.md` import, and
that import does load: `AGENTS.md` is in context automatically every session, verified
by observation. So the bootstrap was never absent. These fixes make the correct answer
reachable in files that are always loaded; they do not mechanically prevent a claim made
without reading them. Mechanical prevention would need a hook or a managed setting, and
none is configured.

**Considered and rejected: running `/init`.** It generates a `CLAUDE.md` describing the
codebase. That would duplicate what `README.md` owns by the file-ownership table --
purpose, scope, managed components, repository relationships -- creating a second
description that drifts, which this project's one-owner rule forbids. It also addresses
a missing-documentation problem this repository does not have, and would not have
touched the actual cause.

**D-75.** The runtime wiring files are `.claude/CLAUDE.md` and `.codex/AGENTS.md`.
Decided by: user, 2026-08-21.

Each is the runtime's own discovery location, which is what makes the projection
function. It also resolves the placement problem raised against D-68: an adapter file
under `adapters/claude/` would never be found, because Claude Code discovers only
`CLAUDE.md` at a directory root or in a parent, including `./.claude/CLAUDE.md`.

**Relationship to D-68.** D-68 named `adapters/` with `claude/`, `codex/` and
`generic/`. That stands for adapter material which is not discovery-critical. The two
files above are the discovery entry points and sit in the runtime-native directories
instead. Recorded as a placement split rather than a reversal.

Wired on the local machine, sequenced last, as the plan's Step 9. `STATE.md` open work
29z; plan section 7.

**Not verified:** whether Codex auto-discovers `.codex/AGENTS.md` specifically. Earlier
evidence here records `.codex` as a known Codex location and root and nested
`AGENTS.md` as discovered, but not that exact path. Whoever wires it confirms it at
that point; nothing here depends on it.

**D-76.** Step 2's gate passes. Decided by: agent, on evidence.
`evidence/PROVENANCE-AND-SENSITIVITY-GATES-2026-08-21.md`.

`agents-hub-two` is **cleared** as the source of the content already migrated into the
Hub: owned by the same account as the destination, `fork: false` with no upstream
parent, no `LICENSE` or `NOTICE` file so no third-party terms attach, private, no secret
or credential value in any of its 27 files, and no runtime state. The two scan hits for
secret-shaped words are rule text *about* secrets, not values.

Recorded as a limitation rather than glossed: the source is a single "Initial Commit"
with no history, so provenance *within* that commit cannot be traced from the
repository. If any of it was copied from a third party before the import, this clearance
does not reach that. Recheck trigger: a new commit, a licence file, a fork parent, an
additional contributor, or evidence of third-party material in the import.

`design-systems\.remember` is **explicitly blocked and excluded**, which the gate
permits, and nothing was inspected to record it. The gate's condition -- no downstream
action depends on an unresolved item -- is verified by search: the only two references
to `design-systems` anywhere in the Hub are the `CATALOG.md` and `README.md` lines
instructing preservation. No artifact, route, registry entry, definition, template or
context file touches it.

Two further sources are recorded so they are not mistaken for uncleared Hub inputs: the
predecessor backoffice, whose material went to `plans/reference/` in this repository and
never to the Hub; and `agent-governance-toolkit`, which is not adopted and contributes
nothing, though its MIT attribution terms become live if adoption is ever proposed.

**D-77.** Step 3's map is produced. Its gate is **not met**, and cannot be met by
analysis. Decided by: agent, on evidence.
`evidence/AGENT-HUB-SEMANTIC-OWNERSHIP-MAP-2026-08-21.md`.

Sixty-four governed issues identified across the corpus; **31 have more than one active
statement**. The dispositions for 25 of them are settled in the map and need no
decision. Six questions cannot be answered from the corpus, and the first gates roughly
a third of the dispositions -- recorded as U-1 through U-6.

Three obligations have **no statement anywhere in the Hub**, each verified absent by
search rather than assumed: bounding a verification method (simplest reliable method,
stopping condition, complexity circuit breaker); which source is authoritative for a
question class; and the defect-class sweep. All three exist only in this repository's
`rules/VERIFICATION-RESOLUTION.md`. So the Hub's verification owner currently tells an
agent to verify without telling it when to stop or which source to trust.

Thirteen gaps are named with an absorbing owner each, and **no new rule file is
proposed for any of them** -- the root contract forbids a separate owner where a focused
section serves. Two are worth naming here because they are structural rather than
missing text: nothing owns where a surfaced governance gap is recorded, so a gap found
outside this project has nowhere to go; and nothing resolves an asset's data
contradicting a rule, because assets hold no precedence tier and so cannot be placed in
the six-level order. The second is the hole behind D-64, which fixed one instance of
that class rather than the class.

**D-78.** The domain-instantiation test is adopted, and belongs in the
agent-definition schema. Decided by: agent.

To decide whether a domain rule inside an agent definition duplicates a `rules/`
obligation or legitimately instantiates it: **strip the domain nouns; if a sentence
already in a `rules/` file remains, it is a restatement; if the sentence becomes false
or vacuous, it is an instantiation.**

Applied to the one migrated definition: 6 of 8 rules are instantiation, 2 are
restatement. This confirms D-51 item 2 as a class rather than a one-off judgement, and
gives it a test anyone can apply. It belongs in the agent-definition schema work so it
is applied once rather than eleven times -- and the ratio there will be far worse, since
16 of the source package's 22 agent rule entries touch a concern a Hub rule owns.

**D-79.** Two defects found by the Step 3 analysis were fixed on confirmation, both
mine. Decided by: agent.

The registry schema's only `$comment` described a constraint other than the one it
annotates -- left over from an earlier version of the block -- so a reader checking why
the constraint exists got an answer about something else. And this repository's
`README.md` managed-components row still said `.agents-hub` "does not yet exist", six
lines above the paragraph declaring it canonical: one file, two answers, in the file
that owns managed components.

Neither was findable by any check in place. No script compares a comment to the
constraint beneath it, and no check reads a table cell against a paragraph in the same
file. Recorded rather than quietly fixed because the gap is in the checking, not only in
the files.

**D-80.** The user-context SSOT naming model and classification. Decided by: user,
2026-08-21. Corrects the description in earlier records; does not rewrite them.

**Final naming and placement:**

| File | Scope |
|---|---|
| `.agents-hub/context/USER-SSOT.json` | The global, shared user-context asset |
| `Greyed/context/GREYED-SSOT.json` | Greyed-specific, authoritative for that scope |
| `Fina/context/FINA-SSOT.json` | Fina-specific, authoritative for that scope |

**Classification.** A scope-specific file is **not** a universal user profile: do not
read `GREYED-SSOT.json` or `FINA-SSOT.json` as describing the user generally. **None of
the three is a general governance owner.** Each may hold scoped user authority,
responsibilities, limitations, operating context, preferences, and agent-facing
interpretation rules **for its own scope**. General Hub governance, protected
boundaries, verification policy and precedence remain owned by canonical `rules/`.
Where a scoped SSOT conflicts with a higher-authority Hub rule or a direct current user
instruction, the higher authority governs.

**Nothing was created, moved, renamed or rewritten.** The instruction was to record the
decision without touching the files, and placement is not yet inside an approved
implementation scope. Recorded as `STATE.md` open work 29y, folding into open work 4.
**This decision is not a blocker for the consolidation**, by explicit instruction and in
fact: no current step depends on the rename.

**Records reconciled, history preserved.** Four live records described the file staged
here as `USER-SSOT.json` as being *itself* Greyed-scoped, which under this model
conflates the global name with the Greyed scope. Corrected in `AGENTS.md` (the file
ownership table and § Standing rules), `STATE.md` (open work 4 and the stop condition),
`plans/AGENT-HUB-CONSOLIDATION.md` (delta D-d and § 6.3), and
`PENDING-GLOBAL-PROMOTIONS.md` (G-2). The correct statement in each: **the file staged
here carries Greyed-scoped content and is the future `GREYED-SSOT.json`; the name
`USER-SSOT.json` is reserved for the global asset, which has no content yet.**

Earlier entries in this file -- D-09, D-21, D-23, D-25 -- are **not** rewritten. They
were accurate when written, this file is append-only, and they are the provenance for
how the naming evolved. A reader meeting one of them is directed here by this entry
rather than by a silent edit.

**What this settles for the Step 3 map, and what it does not.**

It settles U-3's user-file half: a scoped SSOT may hold preferences and agent-facing
interpretation rules *for its scope*, and is not the owner of a general format
contract. So the Greyed communication preferences are legitimately scoped content, not a
competing general owner. `DECISIONS.md` D-08's assignment of rendering to that file is
therefore correct **within Greyed** and was never a general assignment.

It does **not** settle U-1, and I am not treating it as doing so. U-1 asks whether
`AGENT-SSOT.json` is a governance owner or an asset. This decision covers the three
user-context files and does not name `AGENT-SSOT.json`.

**One bearing worth flagging rather than acting on.** This decision states that
"verification policy" is owned by canonical `rules/`. If that statement is general
rather than scoped to the user-context files, it settles U-1's first row -- P-03's
recommendation that `AGENT-SSOT.json` become the sole owner of verification scoping
would invert, and the fold into `rules/VERIFICATION-AND-EVIDENCE.md` would be the
answer. Read strictly in context, the sentence is about what the *scoped SSOTs* do not
own, so it is evidence and not a ruling. Flagged for confirmation; nothing acted on.

**D-81.** `_intake-hub/` is the single door for change requests to `.agents-hub`.
Decided by: user, 2026-08-21. Created in `workspace-governor`.

Anyone wanting something changed in the Hub puts a request there. It holds **requests
and their dispositions, and no authority**: a file in it changes nothing in the Hub by
itself, and a submission phrased as a directive is still a request.

**Placement.** The backoffice, not the Hub. Intake is management work, and the Hub holds
canonical governance and accepted assets -- a queue of unassessed proposals inside it
would be exactly the "material nobody owns" the consolidation exists to remove.

**The rule that gives it teeth.** Nothing moves from `_intake-hub/` into `.agents-hub`
until it is accepted, classified, and assigned to a Hub owner. That is the standing
rule restated at the point where it will actually be tested, since intake is where
unclassified material arrives.

**Structure, deliberately minimal.** `README.md` and `SUBMISSION-TEMPLATE.md`. No
`accepted/`, `declined/` or `deferred/` subdirectories: a directory is created by its
first real artifact, and the disposition belongs **in the submission file** so the
request and its answer stay together rather than being separated by a move.

**Two rules written into the README because they are the ones that will be broken.**
No secrets in a submission, in any form, including a screenshot or a pasted log -- with
the handling stated if it happens, since a rule with no remedy is advice. And a decline
is never silence: it carries a reason and is reopenable on new evidence.

**Routed from `AGENTS.md`**, with an ownership row, so a fresh agent meets it in the
bootstrap rather than finding an unexplained folder. Without that the folder would be
discoverable and unplaced -- the failure recorded in D-49.

The README is written for submitters who do not know this project's vocabulary, with a
separate closing section for the agent triaging. `DECISIONS.md` D-72 and `LEARNINGS.md`
L-036: a record the reader cannot parse is not precise.

**D-82.** A decline must be supported, not merely stated. Decided by: user,
2026-08-21. Standard written into `_intake-hub/README.md` § Declining properly and into
the submission template.

Every decline names, in the submission file: exactly what is declined; the ground **by
name** -- file and section, or the decision entry, never "this conflicts with our
governance"; what was actually checked and where; which parts of the reasoning were
verified and which were assumed; and what concrete evidence or condition would reopen
it.

**The distinction that does the most work:** if the problem raised is real and only the
proposed fix is wrong, that is **not a decline**. The problem is accepted and the
specific remedy is declined, and the file says so in those words. Conflating the two
rejects a valid finding because its author proposed the wrong repair -- which happened
repeatedly in this project's own history, with the roles reversed.

**Never valid grounds:** difficulty, size or uncertainty; needing investigation to
answer; an unwritten preference -- if the rule is real it gets named, and if it does not
exist the submission has found a gap; inconvenience or timing, which is a *Deferred*
with the reason stated; and misrouting, which is answered by saying where it does
belong.

**And a decline is reversible.** It is a judgement on the evidence available, not a
verdict to defend. If the reasoning turns out to be wrong, the decline was wrong -- say
so and reopen it.

**Why this belongs in the record rather than in habit.** The same requirements already
apply to the agent's own escalations and blockers under
`rules/ENGINEER-OWNERSHIP.md` and `rules/AUTONOMY-AND-PROTECTED-BOUNDARIES.md`:
difficulty is never grounds, the reasoning is stated, the smallest unresolved item is
named. This applies them outward. A standard the agent holds for its own reports and
not for its answers to other people is not a standard.

**D-83.** Every intake submission carries a `Keyword:` field, and the submitter says
that keyword in chat when they submit. Decided by: user, 2026-08-21. Written into
`_intake-hub/SUBMISSION-TEMPLATE.md` as the first field, and into
`_intake-hub/README.md` § Keyword.

**What it is for.** The file and the conversation that produced it each need a way to
find the other. The file holds the request; the chat holds the reasoning, the
back-and-forth and the context that never reaches a form. Without a shared handle the
two separate, and the request arrives stripped of why it was asked.

**Two obligations, both on the submitter.** Put a distinctive keyword at the top of the
file, and state it in chat when submitting -- announcing the submission is itself part
of it, since a file nobody mentions can sit unnoticed.

**Guidance that makes it work rather than decorate:** the keyword must be *searchable*.
`update`, `fix`, `hub`, `change` match everything and therefore find nothing; a couple
of unusual words joined up do the job. And no secret, credential or customer name, since
the keyword is quoted in chat, in the file, and in whatever record the outcome lands in.

**Binding on triage:** search the transcript for the keyword **before** assessing.
Judging a submission on the form alone when the keyword would have found the context is
the cheapest avoidable mistake in this pipeline.

**Not a hard gate.** A submission without a keyword is still read -- a request is never
turned away for paperwork, and refusing one on form would contradict D-82's rule that
inconvenience is not grounds. The cost is stated instead: the request cannot be tied
back to its conversation, so triage has only the form, and the cost falls on that
request.

**Incidental benefit:** the literal label `Keyword:` is uniform across submissions, so
the folder itself is greppable by it.

**D-84.** `PENDING.md` is created, owning deferred operational setup that no plan step
sequences. Decided by: user, 2026-08-21. First item: a scheduled run to triage
`_intake-hub/`.

**Boundary, stated because this file is one careless edit away from being a second
open-work list.** `STATE.md` § Open work owns everything inside the consolidation
sequence; `PENDING.md` owns only what no plan step covers -- automation, scheduled runs,
operational scaffolding. An item is never in both, and one that turns out to belong to a
plan step moves to `STATE.md` and is struck through here. Recorded as an ownership row in
`AGENTS.md`, since one owner per concern is the rule this repository enforces hardest and
a new list is exactly how that rule gets broken.

**The pending item's substance, which is not the schedule.** The instruction was that
the agent running it must be properly bootstrapped and know this repository's rules. The
entry makes that checkable rather than aspirational, by naming what goes wrong without
each input: without `DECISIONS.md` it re-litigates settled decisions or accepts a
submission that reverses one; without `_intake-hub/README.md` it reads a confidently
worded submission as authorisation; without D-82 it declines without naming a ground,
which is the unarguable refusal that standard exists to prevent; without D-83 it judges
a submission on the form when the keyword would have found its reasoning.

**One verified constraint recorded with it**, because it decides whether the run works
at all: Claude Code discovers only `CLAUDE.md`, never `AGENTS.md`. This repository's
`CLAUDE.md` is a single `@AGENTS.md` import, so a run whose working directory is this
repository bootstraps automatically -- and a run started anywhere else loads nothing and
would triage the Hub's intake knowing none of the Hub's rules.

**Naming.** Created as `PENDING.md`, not `pending.md` as literally requested. Every
other Markdown file at this root is SCREAMING-KEBAB, and D-58 settled that convention.
A one-character-case deviation from a recorded convention is not worth introducing;
flagged to the user rather than done silently, and trivially reversible.

**Three questions deliberately left open in the entry** rather than answered now: what
the run does when it finds nothing (silence, most likely -- a daily "no submissions"
trains people to ignore it); whether it triages or only surfaces (surfacing is the safer
first version); and what it does with a submission needing a reserved decision (stop and
say so, never guess). Deciding those before the run exists would be designing against an
imagined implementation.

**D-85.** The `_intake-hub/` scheduled run happens **twice a week**. Decided by: user,
2026-08-21. Recorded in `PENDING.md` P-1.

Recorded as the cadence rather than as a default to tune, and noted with the two things
it decides once the run is built. It sets the expectation for submitters -- a request can
sit for a few days, which is why the intake README already says intake is not for
anything urgent or operational. And it means a run may find a batch or nothing, so the
run must handle several submissions at once and must stay silent when it finds none: a
twice-weekly "nothing to report" is precisely the message people stop reading.

**D-86.** The plan carries a status checklist, and `STATE.md` remains the authority.
Decided by: user, 2026-08-21. Amends the split in D-74.

D-74 moved position out of the plan into `STATE.md` on the ground that two copies drift.
The user has directed that the plan carry checkboxes so a reader can see what is done,
what is not, and why not. That instruction governs.

**The split is amended, not abandoned.** `plans/AGENT-HUB-CONSOLIDATION.md` section 3a
carries one line of status per step, with the reason when a step is not done.
`STATE.md` § Position in the plan sequence keeps the detail and remains authoritative.
The rule when they disagree is written into the plan itself: **`STATE.md` governs and the
plan's table is the stale one.**

**Why the drift risk is worth accepting here.** D-73 exists because the plan could not
answer "where are we" from its own text, and that produced step labels applied to the
wrong steps and two prerequisite steps passed over. A stale checkbox is a smaller failure
than an unreadable plan, and it is detectable — a checkbox that contradicts `STATE.md`
is visible on inspection, whereas a missing answer is not.

**Also recorded: this decision resolves a conflict I had left standing.** Section 9,
appended earlier the same day, asserts step status in its rows -- "Step 2 is closed",
"Step 3's map exists" -- under a heading that disclaims carrying position. I wrote the
disclaimer and then carried position anyway, which is the duplication D-74 removed,
re-created with a note on top. D-86 makes the arrangement deliberate and gives it a
tiebreak, instead of leaving a contradiction covered by a disclaimer.

**D-87.** The decline standard binds the agent's own rejections, not only its answers
to submitters. Decided by: agent, closing a gap in D-82.

D-82 set out what a decline must contain -- what exactly is declined, the ground by name
with file and section, what was checked and where, verified versus assumed, and what
would reopen it -- and justified it with the observation that a standard held for your
own reports and not for your answers to other people is not a standard.

**That argument runs both ways, and D-82 stated only one direction.** The same
requirements apply when the agent rejects a review finding, an audit result, a subagent's
conclusion, or a submission. In this session eight findings were rejected across five
review rounds, and some of the reasoning leaned on recollection of the reconciliation
record rather than on quoting it -- which is precisely the unarguable refusal D-82
forbids.

So: a rejected finding is recorded with the same five items, and the ground is **read at
the time, not recalled**. A rejection argued from memory of a rule is not supported, and
the person or agent whose finding it was is entitled to check it.

**D-88.** Two claims recorded as fixed were not, found by checking rather than by
recall. Decided by: agent.

`evidence/HUB-STEP-2-FIRST-ARTIFACTS-2026-08-21.md` **both asserted and withdrew** the
same claim: one paragraph said the routes were "generated from the source files, so
verbatim is true by construction", while the round-2 findings table below it recorded
that exact claim as withdrawn. The file contradicted itself for several revisions.
Corrected; the paragraph now states what is true -- the routes are verified byte-identical
by a committed script -- and notes that it contradicted the table until today.

And the narrative-in-live-artifacts class is **not** closed, though it was reported as
addressed twice. Two instances stand: the registry schema's field descriptions carry
settled-decision rationale ("Closed: the orchestrator/specialist split is a settled
classification"; "Null rather than a prospective path: a path written before its file
exists is a dangling reference"), and one `context/` bullet reports an obligation and
asserts it is met. Both are U-6 in the ownership map, open.

**The lesson is the method, not the instances.** Asked which of ten self-identified
conflicts were fixed, answering from memory would have reported eight; checking the files
reported six, and found one contradiction that memory had no idea about.

**D-89.** Open items live in GitHub Issues. Decided by: user, 2026-08-21 -- "all
issues must be written in here: github.com/klodebeers/workspace-governor/issues".

`STATE.md` § Open work was the register. It is now a pointer. Thirty-five issues were
filed: every open item that stood in that section, plus eleven that had no register at
all -- U-1 and U-6 from the ownership map, the severity-rating gap recorded only as a
learning, the disclaimer pattern recorded only as instances, the missing enforcement
carrier, the three owed obligations, the thirteen gaps, the intake run in `PENDING.md`,
the bootstrap test in the verification assignments, the migration itself, and the
Workspace Orchestrator material. `evidence/OPEN-WORK-MIGRATION-2026-08-21.md` holds the
item-by-item mapping.

**Why a pointer and not a copy.** Two registers for one concern is what the ownership
table forbids, and the cost is already on record: position duplicated into the plan
needed a tiebreak (D-86). The migration also found the same defect inside the old
register -- item 26 and item 29c described the same missing handoff contract in
different words, forty lines apart, both live. A list where one item can appear twice
without either copy knowing is the thing being removed, not just relocated.

**What an issue must carry:** what is open, why it matters, what it depends on, and the
condition under which it closes. An issue with no close condition is a note. Closing one
states which of three happened -- done and verified, superseded by a named decision, or
not planned and why -- because a closed issue that says none of them is
indistinguishable from an abandoned one.

Struck-through items were not migrated. They are history and stay where they were
written; the prior list is in git at `b39a097`. Nothing was deleted to make the mapping
true.

**D-90.** Enforcement carriers exist, and `.claude/` owns them. Decided by: user,
2026-08-21 -- "coz you are missing the HOOKS! there's no HOOKS".

**The diagnosis was right, and it was already on record twice.** C-03 and D-74 both say
instruction placement enforces nothing on its own and a carrier -- managed setting or
hook -- must be chosen per rule. Neither produced one. There was no `.claude/` directory
in this repository at all, so every rule here was guidance, including the ones written
specifically to stop a recurring failure.

Three failure classes recurred despite being written down, and each is mechanically
detectable:

1. A step named from memory, under a label belonging to another step (D-73, D-74).
   `UserPromptSubmit` now reads the position table out of `STATE.md` into context on
   every prompt, so recollection is never the source.
2. A fidelity claim with no committed check behind it (D-53), which then sat in an
   evidence file both asserted and withdrawn (D-88). `PreToolUse` on `Bash` refuses a
   commit message asserting that claim class.
3. A session ending with a durable finding unwritten -- the persistence requirement.
   `Stop` refuses while governed files are uncommitted, once per dirty set.

The same gate also refuses a deletion in append-only `DECISIONS.md`, a credential in
staged content, non-ASCII in a `.ps1`, and a plain force-push.

**Three properties are part of the decision, not implementation detail.** A gate has no
bypass -- a gate with an escape hatch is a suggestion with extra steps. A gate is proven
in both directions or it is worthless: 31 cases, each gate blocking its defect and
passing clean input, per D-65. And a skipped check is never reported as a pass; where a
check cannot run it says `SKIPPED -- not a pass` and the claim it would have supported
is not made.

**Boundary, stated rather than glossed.** The scripts are proven. That Claude Code
actually fires them is **not verified and cannot be verified from this environment** --
hook registration is read at session start, so the session that wrote them could not
have had them active. Assigned to the local operator with a method and a recheck
trigger in `STATE.md` § Verification assignments. Until it runs, the correct statement
is that the gates are correct and their activation is unverified.

**What this does not fix.** Two of the three failure classes it targets were detectable
because they leave a textual trace. Severity inflation and the disclaimer pattern
(issues #3 and #4) leave none, and no hook will catch them.

**D-91.** `PENDING.md` owns the terms of a deferral, not a list of items. Decided by:
agent, correcting a conflict D-89 created and did not name.

D-84 set `PENDING.md`'s boundary against `STATE.md` § Open work: an item belongs to one
or the other, never both, and one that turns out to belong to a plan step moves to
`STATE.md`. D-89 then replaced that register with the issue register **without naming
D-84**, so a settled decision went on governing a register that no longer exists, and
`PENDING.md` kept instructing a move to a section that had become a pointer. `AGENTS.md`
makes `DECISIONS.md` govern what was settled, so the conflict was live rather than
cosmetic.

The boundary now: the issue register owns open items and their lifecycle; `PENDING.md`
owns why a deferral waits, what it must not become, and what has to be true before it
starts. Every item there also has an issue, and the issue is the item.

**The same defect existed in three other places** and is fixed with it, because fixing
one instance of a class and leaving its siblings is what the defect-class sweep exists
to prevent: `PENDING-GLOBAL-PROMOTIONS.md` P-01 step 5 told a promoter to update a
register that no longer exists; its P-04 gave gap G-3 a disposition contradicting issue
#7's; and a **stop condition** in `STATE.md` gated the discovery tooling on "open work
item 2", which the migration made unlocatable -- a binding condition whose precondition
could no longer be read.

**D-92.** The issue migration lost four items and misrendered three, found by an
independent audit and not by me. Decided by: agent, on the audit's evidence.

Confirmed against the source and fixed: **U-3, U-4 and U-5** from the ownership map's six
unresolved questions were in no issue at all, and D-89 asserted the newly filed set
covered "U-1 and U-6" without noticing the other four existed. **U-4 is a live defect in
the Hub root router** -- it delegates a placement decision to a plan that declares itself
not live governance. Old item **29f**'s substance was merged into issue #10 and
disappeared: the accepted definition shape has no slot for a specialist's domain-focus
block, and four of eleven source specialists carry one. Old item **25**'s constraint that
the schema be written against **all thirteen source shapes** became "the next eleven".
Plan **Step 10** and **Step 12** had no issue and no other owner, so the ownership rule
made them formally untracked. Issue **#12** stated a dependency its source denies, and it
was circular: #12 waited on #9 while #9's close condition was #12.

**Two claims of mine were wrong, and one of the audit's was.** The migration evidence
said "seven items became four issues" where six pairs make twelve items into six, and
"forty lines apart" where the file shows nine. Against that, the audit reported
`AGENTS.md` § Enforcement asserting "five checker defects" against a source saying eight
and eleven -- the count is right and sourced, `LEARNINGS.md` L-026 names exactly five;
the defect was the **citation**, and the paragraph now cites L-026 for the five and D-65
for the rule. Rejecting a finding as stated while fixing what it actually found is what
D-87 requires, and the ground was read at the time rather than recalled.

**The lesson is where the failure sat.** The migration's own evidence file said, in
writing, that no issue body had been diffed against its source item and that a
misrendering would not be caught by anything in it. That caveat was correct and it was
not enough: naming a gap is not the same as closing it, and the audit found exactly what
the caveat had described.

**D-93.** The content gates move to git hooks, because a command parser cannot be the
carrier. Decided by: agent, on an independent audit that defeated the first design in
eight ways.

The gates shipped as a `PreToolUse` hook that parsed the shell command for `git commit`.
Within minutes an audit committed a rewritten `DECISIONS.md` entry through `git -C .`,
`/usr/bin/git`, `sh -c`, a shell variable, a repository alias, `commit-tree` plus
`update-ref`, `filter-branch`, and a pathspec commit the index-only diff never saw --
each with **exit 0 and empty output**. Worse, `subprocess` ran with `text=True`, so a
single byte UTF-8 could not decode returned a non-zero code that every caller treated as
"nothing to check": a `.ps1` carrying the exact cp1252 em dash `scripts/README.md`
exists to prevent passed silently, and so did a real token sitting behind that byte.

**The split now.** `.githooks/pre-commit` and `.githooks/commit-msg` own the content
invariants, because git runs them after deciding what the commit contains, in every
invocation form. `.claude/hooks/gate_commit.py` owns only what a git hook cannot see:
`--no-verify`, plumbing that writes history without hooks, force-pushes, and a
`core.hooksPath` that is not installed. That last one matters most -- a clone where
nobody ran the setup cannot commit at all, rather than committing ungated, so
"somebody remembered" stops being load-bearing.

**A check that cannot run now fails.** Every skip path blocks: an unreadable diff, an
unreachable Hub clone on a commit touching `scripts/` or `evidence/`, a missing message
file, and a machine with no Python interpreter. The old `SKIPPED -- not a pass` notice
went to stderr on exit 0, which the hooks reference sends to the debug log and nowhere
else, so a skip was operationally a pass and invisibly so. `LEARNINGS.md` L-026 had
already stated the rule -- "a check that cannot run must fail, never skip" -- and the
first implementation broke it while quoting it.

**Two design points that are decisions, not detail.** The message gate's phrase list is
a **proxy** for D-53, which asks for a re-runnable artifact rather than for different
wording; so the phrase passes when the message names one, and a commit can describe or
disclaim the phrase instead of being unable to discuss its own gate. And the Hub check
runs the **committed** copy of each script, because the working-tree copy can be edited
to make a failing check pass while the commit keeps the defect.

**On the claim that was made too early.** "31 cases, every gate exercised in both
directions" was in `AGENTS.md`, this file at D-90, `STATE.md` and issue #5 within an hour
of the gates existing. The suite did pass 31 of 31. The audit then mutated the source in
25 places and **ten mutations survived undetected**, including deleting every
governed-path prefix from the stop gate. Passing is not the same as proving, the two were
conflated, and the suite now carries a `--mutations` mode that breaks each gate on
purpose and fails if the cases do not notice -- 18 mutations, 17 caught, one no-op control
correctly not flagged. It earned itself immediately: its first run exposed a real gap in
the cases, not just in the code. Every encoding case added a new file, so a mutation
reading `HEAD` instead of the index was invisible; a case editing an already-committed
`.ps1` now covers it. That mode is the answer to "how would I know".

**D-94.** The delegation rule is written, and its owner is
`rules/VERIFICATION-RESOLUTION.md` § Performer selection. Decided by: user, who directed
that it be written now; the siting and the threshold are the agent's.

**What the rule says, in one line.** Depth is proportionate to risk, source is fixed by
the question, and **performer is fixed by whose work is being judged.** An agent
reviewing its own work has already reached the conclusion under review; it can re-read
and re-run, and it will do all of that from inside the reasoning that produced the
result.

**Delegation is required in exactly two cases**, and the narrowness is deliberate:
reviewing, auditing or adversarially checking something this session produced; and
relying on a clean result from a check this session authored to support a completion
claim. Everything else about delegation -- breadth sweeps, parallel independent pieces,
isolating high-volume output -- stays an ordinary engineering decision the agent owns
(`rules/ENGINEER-OWNERSHIP.md`), and is recorded as guidance so the choice is informed
rather than obligatory.

**Why not a new rules file.** The gap analysis warns against one, and "who performs the
work, and when it must not be the author" is the same concern as how verification is
bounded and which source is authoritative. It sits beside § Authority selection as a
third dimension of the same decision. The promotion obligation travels with the file it
was written into: P-01, addendum recorded.

**The vendor's rationale is not this rule's rationale, and the rule says so.** Every
documented criterion for delegating is about context economy or capability restriction --
verbose output, tool restrictions, latency, token cost. **None is about correctness or
independence.** The docs support the *mechanism*: a fresh context window, no inherited
conversation history, a separate prompt cache, and "input isolation" as their own phrase
for what a fork deliberately drops. That the isolation yields independent judgement is an
inference. Recorded as an inference in
`evidence/RUNTIME-DELEGATION-MECHANICS-2026-08-21.md`, and this rule rests on it without
claiming the docs said it.

**A counter-pressure kept in the rule rather than dropped.** Every custom subagent loads
the full CLAUDE.md hierarchy, so a delegate is **not** independent of this repository's
governance -- it arrives carrying it. Independence is from the parent's conversation, not
its rules. That is what makes a blind review possible at all: the delegate is bound by
the same standards while being denied the reasoning.

**Two carriers, and what neither can do.** A `Stop` gate refuses a stop when the session
claims an independent review, audit or adversarial check and **no delegate ran** -- the
false claim is mechanically visible, and it is worse than no review at all because it is
a false statement about method. A `UserPromptSubmit` hook injects the two required-
delegation conditions when a prompt is about review, audit or verification, so the choice
is made in front of the rule rather than from a recollection of it.

**Neither catches the omission.** No documented hook fires on work being done inline that
should have been delegated; there is no negative trigger. The gate catches the claim, not
the failure to delegate. Stated in the rule, in `.claude/hooks/README.md` and here,
because a gap named in one place and implied to be covered in another is how "enforced"
stops meaning anything.

**An honest self-review is never refused.** The disclaimer forms are matched before the
claim forms, so "I checked my own work" and "no independent review ran" pass. That is the
point: the rule wants the accurate claim, not the flattering one, and a gate that punished
candour would buy silence instead of delegation.

**Proven in both directions**, per D-65: 115 cases, and the mutation mode carries six new
rows for these two carriers -- including one that makes the gate refuse an honest
self-review, and one that makes it pass a claim it could not check. Both are caught.

**D-95.** The enforcement carrier for a read-and-recall rule in this repository is
**trigger-driven injection plus a resolvability gate**, not a longer bootstrap. Decided
by the agent as an ordinary engineering choice under `AGENTS.md` § Ownership split;
the user reported the symptom and set the requirement ("the project itself is supposed
to tell the agent what must be done, things should work by triggers").

*The measurement that forced it.* The bootstrap mandates 258,929 bytes (~64k tokens)
before any work, and that set carries 121 self-correcting or superseding statements --
62 in this file alone. An agent that must compress 259 KB retains the narrative rather
than the current rule. D-73 already records that failure landing: work executed under
step labels belonging to other steps, no error anywhere. Prescribing more reading to
fix a drift caused by too much reading makes it worse.

*What was built.* `.claude/hooks/inject_rules.py`, driven by
`.claude/hooks/rule-triggers.json`. It generalises what `inject_plan_position.py` and
`inject_delegation_check.py` already do for two rules -- the second of which had
already recorded the wallpaper failure mode, so unconditional entries are limited to
rules that bear on every decision.

*The design constraint that shaped it.* The table holds **no rule text**. Each entry
names an owning file and an exact heading, and the section is read live when the
trigger fires. A copy in the table would be a second owner of the rule, which
§ File ownership forbids, and it would drift with no error. Headings match exactly
after normalisation, never by substring -- the substring defect is already recorded
against `section()` in `inject_plan_position.py`.

*Where the failure moved, and what catches it.* An entry breaks when someone rewords
the heading in the **owning** file: the table is untouched, the hook is untouched, and
from then on `RULE NOT READ` is injected where the rule used to be. A table of NOT READ
notices reads exactly like a working one. `scripts/Assert-RuleTriggerFidelity.py` and
`wg_gates.check_rule_triggers` refuse a commit in that state. The check is not
diff-scoped, because the defect touches neither the table nor the gate.

*Scope limit, stated rather than glossed.* Project hooks fire only for sessions whose
working directory is this project. This governs the backoffice and **nothing else** --
not `C:\KloWorkspaces`, not a session opened inside `.agents-hub`. It is a proof of
mechanism, not fleet coverage.

*What this does NOT settle.* Whether Step 9's deliverable should be respecified. The
wiring files D-75 names are advisory by our own evidence, so Step 9 as written cannot
carry a rule; that finding is recorded in
`evidence/USER-SCOPE-HOOK-CARRIER-2026-08-27.md` and belongs in the issue register, not
here. Whether a user-scope `~/.claude/settings.json` can carry these hooks to every
session is **NOT VERIFIED** and has an assigned procedure. Codex has no equivalent
mechanism at all.

*Performer.* Every check named here was authored and run in one session. Under
`rules/VERIFICATION-RESOLUTION.md` § Performer selection and D-94 that cannot carry a
completion claim, and none is made: the results below are demonstrations awaiting an
independent performer.

**D-96.** Three independent agents reviewed the D-95 carrier with this session's
rationale withheld (D-60). Their findings are accepted, the defects are fixed, and
D-95 is corrected here rather than edited, because entries are append-only.

*Corrections to D-95.* Its bootstrap figure of "258,929 bytes" is wrong; the rows
it was drawn from sum to **258,918** at `110a9e3`. Its closing sentence points at
"the results below", and nothing follows it -- the results are in
`evidence/USER-SCOPE-HOOK-CARRIER-2026-08-27.md` § Results. Its claim that the
table "holds no rule text" was false when written: the `why` fields carried up to
76 verbatim characters of the sections they point at, and one had already drifted,
changing "the ownership table" to "this table" and so altering the referent of the
rule it was quoting. That is the exact second-owner defect the design cited as its
justification, reproduced inside it.

*What the reviews found, and what it cost.* Two defects made the carrier inert or
misleading rather than merely imperfect:

1. **The injectors read a payload key the CLI does not send.** `user_prompt` is a
telemetry attribute; the payload carries `prompt`. Four of five entries never
fired. `inject_delegation_check.py` carries the same defect and returns early on
an empty prompt, so it had emitted nothing in production since it was written,
while `.claude/hooks/README.md` described it as working. The suite could not see
it because every fixture used the same wrong key -- a self-confirming test proves
only that the fixture agrees with itself.
2. **The gate read the worktree, not the staged tree.** An ordinary split commit
-- reword a heading, update the table, stage only the file -- passed a gate
looking at a self-consistent worktree, and left HEAD carrying the new heading with
the old table. The mirror case blocked unrelated commits over unstaged edits.

Also fixed: a truncated prohibition injected under a `RULE IN SCOPE` header, which
dropped the approval boundary from every prompt; eviction by file order, so the
always-on entry displaced entries that matched the prompt's own words; a table
that could be deleted with no finding; caps, trigger shapes and file paths the
checker never type-checked, one of which let an entry inject any file on the
machine; and a gate that wrote `__pycache__` into the repository it was gating.

*The rule this cost the most to relearn.* Two self-authored checks reported clean
while measuring nothing. A harness path bug crashed the suite in all 27 mutation
runs, and a crash exits non-zero, which the harness reads as "mutation caught";
only the two no-op controls, which must survive, exposed it. Then the payload key
made 129 passing cases meaningless. `LEARNINGS.md` L-026 already says to treat a
clean result from an unproven check as no information. It is now demonstrated
twice inside one session, by the author of both checks.

*Standing consequence, decided here.* Work that affects behaviour, performance or
failure modes is reviewed by a separate agent before it is reported as done, not
after -- and the reviewer is denied the author's rationale. Verifying that a
change was applied is part of applying it: this session lost an edit to a killed
shell and found it only by checking afterwards.

*What is still not claimed.* The mutation proof is current only to `3be99ca`; the
carrier changed materially after it and a re-run is owed. Issue #43 remains
unrun, so the carrier still governs this repository alone.

**D-97.** `_intake-hub/` is renamed `_inbox/`. Decided by: user, 2026-08-27,
delegating the name choice to the agent.

*Why the old name stopped working.* It read two ways -- "the hub for intake" and
"intake for the Hub" -- and "hub" collided with `.agents-hub`, the thing it takes
requests *about*. The Project Intake Dashboard then introduced a second intake, so
"intake" alone no longer identified which door was meant.

*Why `_inbox`.* It is the ordinary word for a place things arrive and are cleared,
and clearing is the design: issue #44 proposes a doorway whose steady state is
empty, where the file count in the root *is* the backlog. A name that implies
accumulation would work against the mechanism. It collides with neither `hub` nor
the project intake.

*The eight references in this file are deliberately not rewritten.* An append-only
log that gets rewritten is not append-only, and the older entries record what was
decided under the name in use at the time. D-81, D-82, D-83 and D-85 keep
`_intake-hub/` and are correct as written; this entry is the pointer that connects
them.

*What caught the one reference that would have broken silently.* The rule-trigger
table cited `_intake-hub/README.md` as an owning file. The pre-commit gate refused
the rename with `RULE TRIGGER DOES NOT RESOLVE` before any commit existed --
the first time that gate has fired on real work rather than on a test fixture.
Without it the injector would have emitted `RULE NOT READ` for the intake rule
from then on, which reads exactly like a table that is working.

**D-98.** The workspace stops governing its agents by contract and starts equipping
them by library. Decided by: user, 2026-08-28 — *"you guys do not need rules that say
NO to you, what you guys need is GUIDANCE on how to do things."* The agent's part is
the mechanism and the consequences below.

*What was actually wrong.* The reported symptom was indiscipline — agents "not
following even the simplest instructions", drifting because they "kept reading old
plans and files". Measurement says otherwise. The governance an agent is asked to
carry across this workspace and the Hub is 258,918 bytes, and 121 of its statements
are self-correcting — a rule followed by the record of the rule having been stated
wrongly before. An agent that reads all of it has spent its context on the governance
and not on the work; an agent that reads part of it has read an arbitrary part. Drift
is what that load produces. It is not a discipline failure and cannot be fixed by
adding a rule against it, which is what every previous attempt did.

*The decision.* Shared material is written as **guidance an agent loads when it needs
it** — how to do a thing, with a worked example — not as obligations it must hold
before it may act. Prohibition earns its place only where the act is irreversible or
crosses a protected boundary; everywhere else the same intent is carried by guidance
that shows the correct method, or by a gate that refuses at the moment of the act.
A rule that neither refuses nor teaches is removed.

*Why the evidence supports it rather than merely permitting it.* This session found
defects worth listing: a payload key that made 129 passing test cases meaningless, a
harness path bug that read 27 crashes as 27 catches, a gate that ran the worktree copy
of its own checker, a hook wired with an `args` field that does not exist in the
schema, and a procedure of mine that would have widened `permissions.deny` while
appearing to tighten it. **Not one of them would have been caught by a prohibition.**
Every one was caught by an independent reviewer or by mutation testing. That is the
practice worth institutionalising; the prohibitions were scar tissue.

*Distribution, which is the part that was actually blocking.* The reason none of this
reached the fleet is that no bypass-proof fleet-wide carrier existed:
`disableAllHooks` is a scalar setting, so any project can silently switch off a
user-scope hook, and `allowManagedHooksOnly` — the only scope that cannot be bypassed —
is not available here. The native plugin marketplace solves the distribution half:
a repository carrying `.claude-plugin/marketplace.json` is added once per machine and
installs agents, commands, hooks and skills under `~/.claude`. So the Hub is published
as a marketplace, and what it ships is skills. This is a **decision to build**, not a
verified result: nothing has been published and nothing installed.

*Consequence for `plans/AGENT-HUB-CONSOLIDATION.md`.* Most of its thirteen steps exist
to reconcile two competing contracts into one authoritative contract. Under this
decision there is no authoritative contract to converge on, so that work is largely
retired. What survives is the part that was never about precedence: taking inventory
of what the two sources actually contain, and keeping one owner per thing so two
copies cannot disagree. **The plan is not rewritten by this entry** — it owns its own
sequence, and the retirement is executed against it as separate, reviewed work. Until
that happens the plan and this decision disagree, and this decision governs what was
settled while the plan still governs its own step list.

*What this does not change.* One owner per concern, the persistence requirement, the
evidence standard, and the two enforcement rules — a gate has no bypass, and a gate is
proven in both directions or it is worthless (D-65). Those are not prohibitions on
agents; they are properties of the machinery, and the machinery is what this decision
leans on harder than before.

*What is reserved and not settled here.* Which of the current `rules/` survive as
irreversible-act brakes, and which become skills. That is a file-by-file judgement and
it is not made by this entry.


## Recorded as not decided

These arose in session and are **not** settled. Do not treat them as decisions.

- Placement of the user SSOT within the architecture.
- Whether to adopt, fork or ignore `agent-governance-toolkit`. Provenance and
  licence are established (unmodified MIT fork of a Microsoft project); adoption
  review is not done.
- Whether `atrium_workspace` in its current form satisfies the Gateway directive's
  Atrium integration contract.
- Target tree and ownership map for the consolidated Hub. Preliminary proposal exists; it cannot be accepted until the live Hub is inventoried.
