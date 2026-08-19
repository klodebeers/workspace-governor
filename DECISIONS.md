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

## Recorded as not decided

These arose in session and are **not** settled. Do not treat them as decisions.

- Placement of the user SSOT within the architecture.
- Whether to adopt, fork or ignore `agent-governance-toolkit`. Provenance and
  licence are established (unmodified MIT fork of a Microsoft project); adoption
  review is not done.
- Whether `atrium_workspace` in its current form satisfies the Gateway directive's
  Atrium integration contract.
- Target tree and ownership map for the consolidated Hub. Preliminary proposal exists; it cannot be accepted until the live Hub is inventoried.
