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
