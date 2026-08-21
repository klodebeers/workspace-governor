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

## Recorded as not decided

These arose in session and are **not** settled. Do not treat them as decisions.

- Placement of the user SSOT within the architecture.
- Whether to adopt, fork or ignore `agent-governance-toolkit`. Provenance and
  licence are established (unmodified MIT fork of a Microsoft project); adoption
  review is not done.
- Whether `atrium_workspace` in its current form satisfies the Gateway directive's
  Atrium integration contract.
- Target tree and ownership map for the consolidated Hub. Preliminary proposal exists; it cannot be accepted until the live Hub is inventoried.
