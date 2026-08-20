# Agent Hub Consolidation -- Active Plan

**Type:** Backoffice planning record. **Not live governance.** Must not become a
competing authority.
**Plan owner:** `workspace-governor` (Agent Hub backoffice)
**Target:** `agents-hub` -- current canonical Agent Hub -- and the live local
`.agents-hub` runtime path
**Version:** 0.5.0
**Baseline date:** 2026-08-20
**Status:** Execution-ready for Step 1 onward; not started

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
execution-ready but never started. A verbatim provenance copy is at
`plans/reference/AGENT-HUB-IMPLEMENTATION-PLAN-v0.4.2-predecessor.md`.

Its 12-step sequence, authority and boundary map, execution controls, rollback
strategy and completion criteria are **reused unchanged** unless a delta is
recorded in section 4. Full classification of prior material:
`evidence/PREDECESSOR-BACKOFFICE-REVIEW-2026-08-20.md`.

## 3. Carried forward unchanged

Reuse these directly. Do not re-derive them.

| Carried forward | Source | Why still valid |
|---|---|---|
| 12-step execution sequence, Step 0 to Step 12, with prerequisites, prohibited changes, verification method, evidence and completion gate per step | v0.4.2 § 6 | Structure is target-agnostic; each gate remains correct |
| Authority and boundary map across Governor / Hub / adapters / projects | v0.4.2 § 2 | Matches the current authority relationship |
| Execution controls common to every step, 10 items | v0.4.2 § 5 | Version-preservation and smallest-change discipline unchanged |
| Rollback and recovery strategy | v0.4.2 § 7 | Unchanged |
| Final completion criteria | v0.4.2 § 8 | Unchanged |
| Four placement layers; one-owner-per-concern; governance-owner creation test | `HUB-ARCHITECTURE.md`, Hub `rules/AGENTS.md` | Already canonical |
| Classification verbs: Keep, Move, Generalize, Specialize, Merge, Retire, Conflict | v0.4.2 § 4.1, `HUB-MANAGEMENT.md` | Already in use in this backoffice |
| Dated-baseline supersession rule: never silently rewrite a dated baseline; issue a later dated audit citing it | `evidence/BASELINE-AUDIT-2026-08-16.md` | Adopted as the standard for every inventory this plan produces |

## 4. Deltas since v0.4.2

Only these change. Everything else in section 3 stands.

| # | Delta | Effect on the plan |
|---|---|---|
| D-a | **A second source repository exists.** v0.4.2 knew only the live Hub. `agents-hub-two` holds 27 files -- 15 agent definitions, `config/agent-registry.json`, schemas, prompts, templates -- and is source material pending reconciliation. | Step 1 classification must cover three inputs: the live `.agents-hub`, canonical `agents-hub`, and `agents-hub-two`. Step 8 migration now has a real accepted-source candidate, where v0.4.2 anticipated possibly none. |
| D-b | **The canonical Hub is now named and settled.** `agents-hub` is canonical (`DECISIONS.md` D-24), superseding the two-repositories-both-claiming-identity condition. | Removes the identity question from Step 1. Step 1 decides structure, not which repository governs. |
| D-c | **Hub root `AGENTS.md` is misplaced inside `rules/`.** Verified: `agents-hub` has `rules/AGENTS.md` and no root `AGENTS.md`. | Add to Step 1 classification as a `Move`, executed in Step 5. Structural only, no content change. Deferred by instruction from the canonicalization step. |
| D-d | **The SSOT pair must be placed in the Hub** with scope-based routing, `USER-SSOT.json` loaded only in Greyed context. | New work inside Step 5 and Step 10. Placement alone is insufficient: the Hub root router needs entries or the assets are unreachable. See `evidence/HUB-ASSET-PLACEMENT-CORRECTION-2026-08-20.md`. |
| D-e | **Three conflict-resolution coverage gaps** are recorded: peer agent output conflict (live), same-level requirement contradiction (plausible), stakeholder-goal conflict (latent). | Step 3 semantic-owner work must close G-1 and G-2 as sections in existing owners. No new rule file. `PENDING-GLOBAL-PROMOTIONS.md` P-04. |
| D-f | **Verification scoping is now a rule** and duplicates an SSOT section. | Step 3 must resolve the duplicate ownership. `PENDING-GLOBAL-PROMOTIONS.md` P-01, P-03. |
| D-g | **Live-Hub evidence exists but is stale.** `BASELINE-AUDIT-2026-08-16.md` inventories the live `.agents-hub` as of 2026-08-16. It is 4 days old and says to re-inspect. | Step 1 does not start from zero. Use it as the prior baseline and produce a later dated audit citing it, per the supersession rule. Read-only tooling exists: `scripts/Invoke-HubInventory.ps1`. |
| D-h | **Read-only inventory tooling now exists and is executed-verified** under PowerShell 7 against fixtures. | Step 1 inventory is a tooling run, not a manual walk. Windows PowerShell 5.1 and the live Hub remain unverified. |

## 5. Conflict and gap register

Predecessor identifiers mapped to current ones. One row per real issue; no duplicates.

| v0.4.2 | Current | Issue | Status |
|---|---|---|---|
| C-01 | B-3 | Codex authority file has stale `C:\Users\ByteBoss\...` paths and overlaps Hub-owned responsibilities | Open. Blocks Codex adapter activation only. Needs user authorization to open as a scoped change (D-11). |
| C-02 | B-2 | `design-systems/.remember` provenance and sensitivity unresolved | Open. Existence-only handling enforced in tooling. Blocks classification of that area only. |
| C-03 | -- | Claude Code project-versus-global loading can let project instructions outrank global governance | Open. Carried forward. Blocks Claude Code adapter finalization only. **Not previously recorded in this backoffice.** |
| G-01 | -- | Hub reference audit overlaps project research; unique evidence not mapped | Open. Carried forward. Step 6. |
| G-02 | -- | Third-party scaffolder provenance and licence not accepted | Open. Matches the `agent-governance-toolkit` open item. |
| G-03 | B-5 | Runtime discovery, permissions, hooks and activation behavior may drift | Open. Local execution required. |
| G-04 | -- | Human glossary has no accepted artifact or placement | Open. Blocks nothing. |
| G-05 | -- | No accepted repository-delivery workflow artifact | Open. Blocks nothing. |
| -- | B-1 | Target tree and ownership map not accepted | Open. This plan's Step 1 resolves it. |
| -- | B-6 | Live `.agents-hub` content not currently verified | Open, **narrowed** by D-g. |

## 6. Immediate next action

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

## 7. Stop conditions

Live stop conditions are owned by `STATE.md`. Read them before acting. This plan
adds none.
