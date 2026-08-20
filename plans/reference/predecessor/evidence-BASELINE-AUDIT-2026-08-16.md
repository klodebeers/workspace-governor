> **PROVENANCE COPY -- NOT AN ACTIVE DIRECTIVE.**
>
> Verbatim copy of `evidence/BASELINE-AUDIT-2026-08-16.md` from `klodebeers/workspace-governor-agents-hub-one`
> at commit `24798d0`, the predecessor backoffice for the same Hub.
>
> Source SHA-256: `d757f74416e7503a24b0360f2e69ebeaf318033656821deaa035c21ffce1dca2`
>
> Retained so no load-bearing information depends on a repository declared a
> non-authoritative input. **Not an authority.** Dispositions are recorded in
> `evidence/PREDECESSOR-BACKOFFICE-REVIEW-2026-08-20.md`.

# Agent Hub Baseline Audit

**Inspected:** 2026-08-16  
**Target:** `C:\Users\Chloe\.agents-hub`  
**Mode:** Read-only inspection  
**Purpose:** Dated starting-state evidence for the Workspace Governor

This report describes the observed baseline. It does not govern behavior, approve existing content, prove runtime activation, or replace a fresh inspection.

## Observed root

- `rules\`
- `runtime-adapters\`
- `references\`
- `governance-templates\`
- `design-systems\`
- `STATE.md`

Root `README.md` and `CATALOG.md` were not present.

## Governance contract

`rules\` contained:

- `AGENTS.md`
- `ENGINEER-OWNERSHIP.md`
- `AUTONOMY-AND-PROTECTED-BOUNDARIES.md`
- `CONTEXT-AND-ORCHESTRATION.md`
- `VERIFICATION-AND-EVIDENCE.md`

The root `rules\AGENTS.md` routes governed issues to the other owners. The contract was treated as authority for this project design; `STATE.md` was treated only as continuity evidence.

## Other observed areas

- `runtime-adapters\codex\` existed and was empty.
- `runtime-adapters\claude-code\` existed and was empty.
- `references\` contained `AGENTS-MD-LIVE-AUDIT-2026-08-16.md` and `AGENTS-MD-RESEARCH-AND-LIVE-AUDIT-2026-08-16.md`; the latter was subsequently relocated to this project's `research\` folder because it was project-owned.
- `governance-templates\workspace\`, `project\`, `component\`, and `delegation\` existed and were empty.
- `design-systems\.remember\` contained runtime-like material. Its raw content was not copied into this report. Its provenance, authority, sensitivity, and correct placement remain unresolved.

No candidate `agents`, `skills`, `tools`, `orchestration`, `evaluations`, `templates`, `packages`, or `archive` domains were created during this project bootstrap.

## Activation and configuration observations

- Presence in the Hub did not establish runtime discovery, activation, or enforcement.
- The active Codex global instruction file did not contain an observed route to the canonical Hub contract.
- The active Codex instruction file contained several stale `C:\Users\ByteBoss\...` path references while the inspected environment used `C:\Users\Chloe\...`.
- A central `RESEARCH-REGISTER.md` was not present at the checked Chloe or ByteBoss Codex locations.

These are baseline findings, not authorization to edit global runtime configuration.

## Historical material

`C:\KloWorkspace\Workspace Configurations\agents-hub-finalization` was inspected as historical planning material. It is not the canonical Hub and was not accepted as authority. Its fixed-domain proposals, singular workspace path, database suggestions, vendor-bound roles, and older activation assumptions require current evidence and explicit classification before reuse.

## Protected baseline decisions

- Preserve the live Hub and all unresolved material unchanged during the tree-decision phase.
- Do not infer approval from existence.
- Do not infer activation from placement.
- Do not classify or relocate `design-systems\.remember` before provenance and sensitivity review.
- Decide the complete target tree before refactoring.
- Refactor and verify before migration.

## Supersession rule

Do not silently rewrite this dated baseline as the Hub changes. Record corrections as an explicit correction note or create a later dated audit that cites this baseline and states what changed.
