# Evidence -- predecessor backoffice review and classification

**Date:** 2026-08-20
**Source:** `klodebeers/workspace-governor-agents-hub-one` @ `24798d0` ("Initial
Commit"), inspected from the local clone at `/workspace/`
**Relationship:** Predecessor dedicated backoffice/manager for the same Hub that
is now `agents-hub`. Predecessor management history. **Not a competing
authority.**
**Status:** Verified by direct file inspection. Source repository unmodified.
**Scope:** 47 files. All 9 named artifacts read. `tasks/`, `research/`,
`evidence/` and `versions/` inspected. `versions/` (23 files) reviewed at
inventory level only -- they are pre-edit snapshots of files also reviewed live.

## Revision 4 -- the predecessor repository has been modified

Recorded as a later revision rather than by editing revision 3. Revision 3's
statement that the predecessor repository was unmodified was **true when written**
and is left intact.

On 2026-08-20 a `SUPERSEDED, DO NOT EXECUTE` banner was prepended to all three
`tasks/` files, closing the residual risk that revision 3 recorded as open.

| | |
|---|---|
| Baseline SHA, before the change | `24798d032e39081a6885f3648430786019129ef4` |
| SHA containing the banners | `8d4513caa1809b96117e69e4e602bfff0d8d5c5c` |
| Change shape | Additive only, 3 lines per file, original content byte-identical after the banner |

The residual risk in revision 3 is therefore **closed**, not merely recorded. Git
preserves the pre-banner versions, so the provenance copies under
`plans/reference/` and every recorded source SHA remain valid against the baseline
commit. Authority for this change: `DECISIONS.md` D-31.

Also corrected in this revision: revision 3's file count. The correct figure is
**18** provenance copies -- 4 directly under `plans/reference/` and 14 under
`plans/reference/predecessor/`.

## Revision 3 -- information dependency closed

The revision 2 corrections identified content still held only in the predecessor
repository. That dependency is now closed, verified **by content hash rather than
by filename**.

| Group | Files | Disposition |
|---|---|---|
| Root records -- `AGENT-HUB-IMPLEMENTATION-PLAN.md`, `AGENTS.md`, `README.md`, `STATE.md`, `LEARNINGS.md`, `CHANGELOG.md`, and the three HUB owner files | 9 | Provenance copies under `plans/reference/`, each banner carrying the source SHA-256 |
| `research/` | 4 | Provenance copies. Two hold live design constraints, not history |
| `evidence/` | 5 | Provenance copies. Includes the decision register and the legacy-consolidation record with its pre-deletion gate |
| `CLAUDE.md` | 1 | **Excluded deliberately.** 11 bytes, containing only `@AGENTS.md` -- identical in substance to this repository's own, zero unique content |
| `tasks/` | 3 | **Archival, by instruction.** Not carried. Still reads as live instructions; residual risk recorded below |
| `versions/` | 25 | **Archival, by instruction.** Immutable snapshots |

**Verification:** every SHA-256 recorded in a provenance banner was matched against
a freshly computed hash of the source file. 18 of 18 non-archival files verified
present. Zero unaccounted for. The first attempt at this check compared
*filenames* and produced nine false negatives, because copies carry `research-`
and `evidence-` prefixes -- the check was replaced with a content-hash comparison
rather than adjusted.

### Substantive content migrated to owners, not merely preserved

| Content | Was | Now owned by |
|---|---|---|
| Learnings L-001 to L-006 | L-003 to L-006 unrepresented | **`LEARNINGS.md`**, created at this repository root. Carries the predecessor's retention and promotion rules. Six new entries added from this backoffice's own work |
| Five settled decisions with no representation | Silently absent | **`DECISIONS.md` D-30**, adopted explicitly with per-item owners: agent-first authoring, the glossary boundary, learning retention, skill-before-plugin, deferred scheduled audits |
| "Scan `LEARNINGS.md` for entries whose trigger matches the work" | A bootstrap step in the predecessor router, absent here | **`AGENTS.md` bootstrap order, step 4** |
| Architecture answers *what and where*; Management answers *how to change it*, and neither may redefine the other | Not recorded anywhere | **`plans/AGENT-HUB-CONSOLIDATION.md` delta D-m.** Without it the two provenance owners read as overlapping, which is the duplication this consolidation exists to remove |

The predecessor repository remains unmodified.

### Residual risk, unchanged and deliberate

`tasks/01` Phase 3 and `tasks/03` Parts B to D remain in the predecessor
repository as live imperative instructions authorising PATH edits, software
installation and deletion. They are classified superseded-for-execution **here**;
that classification is not visible in the files themselves. Recommended banner text
is ready. Applying it modifies a repository several records assert is unmodified,
so it stays a deliberate archive decision.

## Revision 2 -- corrections to this review

Revision 1 was audited by an independent subagent against all 47 predecessor
files. Every finding below was then verified by the parent agent against source.
The review's coarse structure held; its classifications did not.

| # | Revision 1 said | Correct classification |
|---|---|---|
| R1 | `CHANGELOG.md` / `versions/` -- **historical only**, "version numbering is not carried into the current backoffice" | **Wrong, and it blocked the plan.** The *mechanism* was discarded while four carried-forward obligations still required it. Step 4 was unreachable and Step 5 blocked by its own prerequisite. Resolved by `DECISIONS.md` D-28 and plan delta D-i |
| R2 | `evidence/DECISION-RECOVERY-AUDIT-2026-08-16.md` -- historical, "provenance for those rejections" | **Understated by half.** Only the 11 rejections were carried. Its 18 established decisions were not, including the long-work method, agent-first authoring, the glossary boundary, learning retention and the scaffolder split. Some are Hub-owned rather than backoffice-owned, which is a legitimate reason not to restate them -- but the reasoning was never given, so the effect was silent loss |
| R3 | `evidence/LEGACY-GOVERNANCE-MATERIAL-CONSOLIDATION-2026-08-17.md` -- historical | **Holds three live obligations.** A pre-deletion reinspection gate over ~20 files marked discard-as-active-governance, **none deleted**; an unrecorded requirement to establish a runtime-neutral continuity pattern; and the dated vendor citation behind C-03. Gate and continuity item now carried |
| R4 | `research/AGENTS-MD-RESEARCH-AND-LIVE-AUDIT-2026-08-16.md` -- reusable as B-3 evidence, "re-verify the vendor half" | **Narrowed too far.** It is a **live design constraint**: the 32 KiB budget, root-first consumption, one file per directory. Independently re-confirmed from pinned source four days later. A fresh Codex review was queued while this sat unquoted. It also holds the `CATALOG.md` requirement collision and an unresolved missing inbound reference |
| R5 | `research/GOVERNANCE-FILE-CREATION-GUIDE-2026-08-16.md` -- reusable "for Step 5 authoring" | **A bound dependency, not optional reading.** `HUB-DOCUMENTATION.md`, itself carried forward, explicitly binds it. It is also the sole holder of the per-file size and truncation budget class -- directly governing the root bootstrap under D-27 |
| R6 | `research/WORKSPACE-GOVERNANCE-CAPABILITY-REUSE-2026-08-16.md` -- historical, "rationale" | **Holds an open decision**, not rationale: per-component dispositions and the undecided scaffolder-versus-local-equivalent question. Its stop condition was also mis-mapped onto the unrelated toolkit fork; split into G-02a and G-02b |
| R7 | `LEARNINGS.md` -- L-001 and L-002 classified | **L-003 to L-006 were not classified at all.** L-003 bears on Step 5 authoring, L-006 on G-02a. Dropped by omission |
| R8 | Predecessor `STATE.md` -- status line and live-Hub facts superseded | **The ~20-item settled-decision list was never classified.** Five items have no representation anywhere here, including the agent-authored governance standard, the glossary boundary, learning retention, the skill-before-plugin lifecycle and deferred scheduled audits |
| R9 | `HUB-ARCHITECTURE.md` -- "reusable, use as-is" | **Contradicted the plan**, which classifies it reusable *with adaptation* and overrides it in five places. Worse, "as-is" reinstates backoffice ownership of Hub architecture -- the exact error D-25 corrected for the SSOT pair. Now: reusable with adaptation, **not an authority** |
| R10 | `versions/` holds 23 files | **25.** Stated while claiming an inventory-level pass |
| R11 | The carried sequence is "12-step" | **13 steps**, Step 0 to Step 12. Corrected in the plan |
| R12 | C-03 stated as "project instructions take priority" | **Withdrawn.** Conflated advisory instructions with enforced settings. Restated in the plan and `STATE.md`; three versions were briefly in circulation |

Two further corrections of my own: the three carried-forward owner files existed
only in a repository declared a non-authoritative input, reachable solely by local
path -- now copied to `plans/reference/` with source hashes. And the provenance copy
of the plan is verbatim in body but not byte-identical, so the predecessor's
recorded integrity hash no longer ran against it; the source hash is now recorded
in plan section 2.

### One risk this review cannot close from here

The predecessor repository is **unmodified and on local disk**, and
`tasks/01` Phase 3 and `tasks/03` Parts B to D contain live imperative instructions
authorizing PATH edits, software installation, and deletion. Those portions are
classified superseded-for-execution -- **but the classification exists only in this
repository.** Anyone opening the predecessor file itself sees live instructions.

The effective fix is a banner in the predecessor's own `tasks/` files or its
`STATE.md`. Not done here: it modifies a repository that several evidence records
assert is unmodified, so it trades one provenance property for a safety property.
Recommended, with the banner text ready, as a deliberate archive decision rather
than an unannounced edit.


## Headline finding

A complete, twice-verified, execution-ready plan for this exact consolidation
already existed and was never started. Work in the current backoffice partially
regenerated it. The plan is now carried forward rather than rewritten.

`AGENT-HUB-IMPLEMENTATION-PLAN.md` v0.4.2, 411 lines: 12-step sequence (Step 0
bootstrap through Step 12 completion declaration), each step carrying
prerequisites, affected paths, authoritative owner, intended result, actions,
prohibited changes, dependencies, verification method, evidence and a completion
gate. Plus an authority and boundary map, 10 common execution controls, a
target-tree baseline with a classification ledger, a conflict/gap register, a
rollback strategy and final completion criteria.

## Classification

### Reusable -- use as-is

| Artifact | Content | Disposition |
|---|---|---|
| `AGENT-HUB-IMPLEMENTATION-PLAN.md` § 6 | 12-step execution sequence with per-step gates | Carried forward unchanged into `plans/AGENT-HUB-CONSOLIDATION.md` § 3. Provenance copy at `plans/reference/`. |
| § 2 | Authority and boundary map: Governor / Hub / adapters / projects / future orchestrator | Carried forward. Matches the current authority relationship exactly. |
| § 5 | 10 execution controls: load routed owner, preserve pre-edit versions, smallest source-preserving change, verify actual state | Carried forward. |
| § 7, § 8 | Rollback and recovery strategy; final completion criteria | Carried forward. |
| `evidence/BASELINE-AUDIT-2026-08-16.md` | Read-only inventory of the live `C:\Users\Chloe\.agents-hub`: root structure, five-file `rules/` contract, empty `runtime-adapters/codex` and `/claude-code`, `references/` contents, four empty `governance-templates/` subdirectories, `.remember` present with runtime-like material | **Reusable as the prior dated baseline.** Its supersession rule -- never silently rewrite a dated baseline, issue a later dated audit citing it -- is adopted as the standard for every inventory this backoffice produces. |
| `LEARNINGS.md` L-001 | Canonical source placement does not establish runtime discovery, activation, adherence or enforcement | Already independently present in the current `AGENTS.md` evidence standard. Confirms it; no change needed. |
| `LEARNINGS.md` L-002 | Sentence comparison misses semantic duplicates and partial overlaps; compare obligations, triggers, boundaries, outcomes | Reusable. Directly applicable to the P-03 duplicate-ownership work. |
| `HUB-ARCHITECTURE.md` | Four placement layers, root control files, established vs candidate domains, artifact creation test, minimum artifact record | Reusable. Hub-side architecture owner; feeds Step 1 and Step 7. |
| `HUB-MANAGEMENT.md` | Required change sequence, classification meanings, project-records and prompt retention, refactor/migration order, promotion standard, runtime-state vocabulary | Reusable. Owns the classification procedure Step 1 depends on. |
| `HUB-DOCUMENTATION.md` | Construction standard for authorized Hub documents; agent-primary terminology; content-class separation; vendor-dependent content handling | Reusable when Hub documents are authored in Step 5. |

### Reusable with adaptation

| Artifact | Why adaptation is needed | Adaptation |
|---|---|---|
| § 4 target tree and § 4.1 classification ledger | Predates `agents-hub-two`. Covers the live Hub only, so it is an incomplete input set. | Use as the **starting ledger** for Step 1, then extend to the three inputs: live `.agents-hub`, canonical `agents-hub`, `agents-hub-two`. Recorded as delta D-a. |
| `tasks/01-WINDOWS-ENVIRONMENT-PATH-AUDIT.md`, `tasks/02-SHARED-CONFIGURATION-AUDIT.md`, `tasks/03-CODING-AGENT-BASELINE-INTEGRATION.md` (2,098 lines) | Local-session **prompts** for Windows environment, cross-runtime configuration and `.agents-hub` integration audits. They overlap Gateway directive § 5 discovery and `scripts/Invoke-GatewayDiscovery.ps1`. Different instrument: agent-session prompts versus a deterministic read-only script. | Adapt as **coverage checklists** for the discovery script rather than as separate runs. Task 01 and 02 name checks the script does not currently make -- notably dependency auditing and command-availability breadth. Task 03's integration steps belong to plan Step 9, adapters. |
| `research/GOVERNANCE-FILE-CREATION-GUIDE-2026-08-16.md` (304 lines) | Drafting reference for files intended for the Hub. Product-dependent claims are dated 2026-08-16. | Reusable for Step 5 authoring. Revalidate vendor-dependent claims against current authoritative sources before relying on them. |
| `research/AGENTS-MD-RESEARCH-AND-LIVE-AUDIT-2026-08-16.md` (197 lines) | Official OpenAI guidance plus live Codex instruction state, dated. | Reusable as evidence for the B-3 Codex reconciliation. Re-verify the vendor half. |

### Superseded

| Artifact / claim | Superseded by |
|---|---|
| `STATE.md` "Status: implementation not started; Step 0 checkpoint validation is next" and its live-Hub fact list | Current `workspace-governor/STATE.md`. The predecessor state is 3 days old and predates canonicalization, the SSOT pair, and the tooling. |
| Plan § 3.1 "The canonical Hub remains `C:\Users\Chloe\.agents-hub`" as the identity statement | `DECISIONS.md` D-24: `agents-hub` is the canonical Hub. The **local path** remains the runtime target; the **canonical source** is now a named repository. |
| Plan § 3.2 "no hash change in the 14 checkpointed files" drift check | Stale. Superseded by whatever the next live inventory reports. |
| `CHANGELOG.md` version history 0.1.0 to 0.4.1 | Historical only. Version numbering is not carried into the current backoffice, which uses git plus `DECISIONS.md`. |

### Historical / provenance only

| Artifact | Note |
|---|---|
| `versions/` -- 23 pre-edit snapshots incl. `versions/hub/rules/AGENTS.md-v0.1.0.md` | Recovery and provenance. Not carried forward as active content. `versions/hub/` is notable: it holds a snapshot of Hub files, useful if a Hub file needs restoring to its 2026-08-16 state. |
| `evidence/DECISION-RECOVERY-AUDIT-2026-08-16.md` | Authoritative disposition record for what was rejected: fixed seven-file package, fixed five-file limit, vendor-native directory names, PLAITED, non-dot `agents-hub` memory implementations. Keep as the provenance for those rejections so they are not silently reopened. |
| `evidence/LEGACY-GOVERNANCE-MATERIAL-CONSOLIDATION-2026-08-17.md` | Accepted meaning and rejection boundary for legacy material before external cleanup. |
| `evidence/AGENT-HUB-IMPLEMENTATION-PLAN-VERIFICATION-2026-08-17.md`, `...-CORRECTION-VERIFICATION-2026-08-17.md` | The two verification passes that made v0.4.2 execution-ready. Provenance for trusting the carried-forward sequence. |
| `research/AGENT-HUB-STRUCTURE-RESEARCH-2026-08-16.md`, `research/WORKSPACE-GOVERNANCE-CAPABILITY-REUSE-2026-08-16.md` | Rationale behind the placement layers and the scaffolder split. |
| `AGENTS.md`, `CLAUDE.md`, `README.md` | Predecessor project contract. Superseded by the current equivalents; retained as provenance. |

### Unresolved -- carried into the current register

| ID | Issue | Current status |
|---|---|---|
| C-03 | Claude Code project-versus-global loading can let project instructions take priority while semantic governance forbids lower layers weakening global governance | **Newly surfaced here.** Was not recorded in the current backoffice. Blocks Claude Code adapter finalization only. |
| G-01 | Hub reference audit overlaps project research; unique evidence and inbound references not mapped | Carried. Plan Step 6. |
| G-04 | Human glossary has no accepted artifact or placement | Carried. Blocks nothing. |
| G-05 | No accepted repository-delivery workflow artifact from the rejected legacy policy set | Carried. Blocks nothing. |
| C-01 / C-02 / G-02 / G-03 | Codex stale paths; `.remember` provenance; scaffolder provenance; runtime drift | Already tracked as B-3, B-2, the toolkit item, and B-5. Confirmed by an independent source. |
| `test4` discrepancy | `C:\KloWorkspaces\test4` described as deleted but found present on 2026-08-17 with five intake-validation artifacts | Carried as an excluded-material note. Not in scope. No action authorized. |

## Corrections to the current record

1. **Blocker B-6 was overstated.** It read "the content of the live local
   `.agents-hub` is unknown." A read-only inventory existed in the predecessor
   backoffice from 2026-08-16. B-6 is narrowed to "not currently verified": the
   evidence is 4 days stale and instructs re-inspection, so a current inventory is
   still required, but the content was not unknown.

2. **Duplicated planning work.** `evidence/HUB-RECONCILIATION-ASSESSMENT-2026-08-19.md`
   independently produced a target tree, ownership map and item classification that
   substantially re-derive v0.4.2 § 4. The classification verbs are identical. The
   assessment retains value the predecessor plan lacks -- it covers
   `agents-hub-two`, which v0.4.2 predates -- so it is not discarded, but it should
   have been an extension of the existing ledger rather than a parallel derivation.

3. **C-03 was missed.** A runtime precedence conflict affecting Claude Code
   adapter work existed in the predecessor register and was absent from the current
   one. Now carried.

## Method note

The predecessor repository was not named as a source until 2026-08-20. Nothing
here implies it was ignored while known. It is recorded because the same class of
loss -- regenerating existing valid work -- is what
`rules/VERIFICATION-RESOLUTION.md` § Simplicity exists to prevent, and the
prevention depends on knowing the input set.
