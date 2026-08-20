> **PROVENANCE COPY -- NOT AN ACTIVE DIRECTIVE.**
>
> Verbatim copy of `evidence/DECISION-RECOVERY-AUDIT-2026-08-16.md` from `klodebeers/workspace-governor-agents-hub-one`
> at commit `24798d0`, the predecessor backoffice for the same Hub.
>
> Source SHA-256: `2a5f9e4e86070df75ee615f5ab7ce0fa56f7edf94af0a18ddd48271076e2d249`
>
> Retained so no load-bearing information depends on a repository declared a
> non-authoritative input. **Not an authority.** Dispositions are recorded in
> `evidence/PREDECESSOR-BACKOFFICE-REVIEW-2026-08-20.md`.

# Decision Recovery and Documentation Audit

**Date:** 2026-08-16  
**Scope:** Current conversation, `File-first Output Request`, `Governance Levels in Coding`, live Workspace Governor files, and live Agent Hub files  
**Authority:** Evidence only; authoritative decisions remain in the owners cited below

## Verdict

**PASS.** The user-approved decisions were separated from assistant-only proposals, reconciled against the live files, and routed to one authoritative owner. Rejected and deferred approaches are recorded below so they cannot silently return as requirements. Independent post-edit correction verification passed.

No final implementation plan was created.

## Established decisions and authoritative documentation

| ID | Established decision | Authoritative owner | Documentation result |
| --- | --- | --- | --- |
| D-01 | The Workspace Governor governs Agent Hub architecture and lifecycle; it does not implement the separate dashboard-driven Workspace Orchestrator | Project `AGENTS.md` | Added explicit scope exclusion |
| D-02 | Governance is one contract with one authoritative owner per practical issue; equivalent and partially overlapping meaning must be folded together | Hub `rules\AGENTS.md`; `HUB-MANAGEMENT.md` for Hub reconciliation | Already authoritative; retained |
| D-03 | Global, Workspace, Project, and Component governance specialize by scope without silently weakening higher obligations | Hub `rules\AGENTS.md` | Already authoritative; retained |
| D-04 | Business authority, governance responsibility, and agent technical judgment are separate; the user is not the default technical validator | Hub `rules\ENGINEER-OWNERSHIP.md` | Already authoritative with examples; retained |
| D-05 | Complexity alone does not require escalation; agents resolve difficult technical problems and escalate only unresolved authority, protected boundaries, uncontrolled material risk, or reserved human judgment | Hub `rules\ENGINEER-OWNERSHIP.md`; `rules\AUTONOMY-AND-PROTECTED-BOUNDARIES.md` | Already authoritative; retained |
| D-06 | Actions that move money retain human approval while agents retain technical responsibility for implementation and evidence | Hub `rules\AUTONOMY-AND-PROTECTED-BOUNDARIES.md` | Already authoritative; retained |
| D-07 | Previously answered questions remain settled unless a recorded reopening condition applies; conflicts with higher authority are surfaced prominently | Hub `rules\ENGINEER-OWNERSHIP.md`; precedence in Hub `rules\AGENTS.md` | Already authoritative; retained |
| D-08 | Long work uses full-corpus intake, a complete outline first, one topic at a time using research -> write or implement -> audit -> correct -> next, cumulative prior findings, then a final overall audit | Hub `rules\CONTEXT-AND-ORCHESTRATION.md` | Already authoritative; retained |
| D-09 | Governance files are agent-authored, agent-maintained, and optimized for agent execution using precise standard technical terminology | `HUB-DOCUMENTATION.md` | Added project-local construction owner |
| D-10 | A human glossary is separate and non-authoritative; it may explain but never redefine canonical terms | `HUB-ARCHITECTURE.md`; construction boundary in `HUB-DOCUMENTATION.md` | Placement and authority boundary documented; glossary not created |
| D-11 | Durable non-obvious learnings are retained concisely; a learning never becomes a second rule | Retention in `HUB-MANAGEMENT.md`; format in `HUB-DOCUMENTATION.md` | Added `LEARNINGS.md` as non-authoritative record |
| D-12 | A new canonical governance owner requires a distinct issue and activation condition, singular ownership, known route and lifecycle, accepted content, and no semantic duplicate; length and fixed file counts are insufficient | Hub `rules\AGENTS.md` | Added canonical Governance Owner Creation Standard |
| D-13 | Reusable repository-rule scaffolding may be canonical Hub skill source; generated rules remain project-local; foreign generator markers cannot own Hub governance | `HUB-ARCHITECTURE.md` | Placement split documented; third-party adoption unresolved |
| D-14 | Author and test a skill first; package it as a plugin only when stable distribution is needed | `HUB-MANAGEMENT.md` | Lifecycle sequence documented; capability research supplies the current vendor basis; no skill or plugin created |
| D-15 | Discovery, audit, optimization, scaffolding, and placement components may contribute bounded patterns without becoming the Governor or creating competing owners | Capability-reuse research | Component dispositions recorded without installation or activation claims |
| D-16 | Material changes preserve the previous version and update one history index | `HUB-MANAGEMENT.md` | Added lifecycle step, exact snapshots, and `CHANGELOG.md` |
| D-17 | Hub root `README.md` and `CATALOG.md` provide navigation and inventory only | `HUB-ARCHITECTURE.md` | Files created without behavioral authority |
| D-18 | Project tree decision, refactor, and migration are separate phases in that order; source is preserved | `HUB-MANAGEMENT.md` | Already authoritative; retained |

## Superseded or rejected approaches

- A Word file or task packet was not the correct output for the governance-recovery work.
- The assistant-proposed fixed seven-file control package and large fixed governance architecture from the early Workspace Orchestrator discussion were scope expansion, not approved requirements.
- A fixed five-file limit is rejected. A file must be justified by ownership and activation, not by an arbitrary count.
- Vendor-native Claude directory names are not adopted as the runtime-neutral Hub tree; only the separation logic is retained.
- The user is not required to pre-classify implementation actions or validate ordinary technical choices.
- Runtime loading order is not treated as the semantic governance authority model.
- Instruction files are not treated as deterministic enforcement, and file presence is not treated as runtime activation.
- The fixed approximate 2.5k-token target from `optimize-agents-md` is not a universal governance limit.
- The external `PLAITED-RULES` generator block is not accepted as canonical Hub governance.
- A plugin is not created before the workflow is stable, and scheduled audits are not part of this documentation phase.
- Glossary wording is not inserted into canonical governance merely to make technical terminology easier for a human reader.

## Deferred or unresolved work

- Complete live item-by-item classification and target-tree decision.
- Refactor only after the complete tree is accepted; migrate only after refactor and verification.
- Decide whether to adopt the third-party scaffolder or author a local equivalent after provenance and output review.
- Create and test the Workspace Governor skill; consider plugin packaging later.
- Choose the final location for the future human glossary after its actual scope exists.
- Reconcile the active Codex authority file's stale paths and overlapping governance before creating or activating a Codex adapter.
- Create and verify thin Codex and Claude Code adapters.
- Resolve provenance and sensitivity of `design-systems\.remember` before classification.
- Deduplicate the two AGENTS.md audit/research records without losing unique evidence.
- Create scheduled audits only after the workflow and runtime integration are stable.
- The separate dashboard-driven Workspace Orchestrator remains a different future project.

## Prominent unresolved conflict

**ACTIVE RUNTIME GOVERNANCE CONFLICT:** The active Codex authority file contains stale `C:\Users\ByteBoss\...` and `C:\Workspace` paths and overlaps responsibilities owned by the Agent Hub contract. Stop only runtime-adapter activation and dependent Codex-governance work until that file is separately reconciled. This conflict does not authorize changing active Codex configuration during this documentation pass.

## Source conversations

- Current Workspace Governor and Agent Hub conversation through the 2026-08-16 decision-recovery directive.
- `File-first Output Request` — conversation ID `6a7f38d4-6478-83ec-a601-580c81f33866`.
- `Governance Levels in Coding` — conversation ID `6a7f60ee-b00c-83ec-873f-f642d7daa7dc`.

Assistant proposals were treated as evidence only unless the user explicitly agreed, corrected them into the accepted form, directed implementation, or the decision was already present in an authoritative live owner.
