# Workspace Governor State

**Updated:** 2026-08-19
**Phase:** Hub consolidation — reconciliation assessment in progress. Repository bootstrap complete.
**Authority:** Non-authoritative continuity record. Settled decisions live in `DECISIONS.md`.

This file records current state only. It defines no rules. Replace stale
content rather than accumulating a transcript.

## Current verified state

Verified by direct inspection during the session dated 2026-08-19.

| Fact | Evidence |
|---|---|
| `workspace-governor` `main` is at `d57deb9` and contained only the Gateway directive file before this bootstrap | `git ls-tree -r --name-only origin/main` |
| The Gateway directive is settled: 46 sections, 1,940 lines, contiguous numbering 1–46, 41 Done-When checkboxes. Now at `plans/MCP-GATEWAY.md`; moved 2026-08-20, content unchanged | 22-check verification pass against `origin/main`; post-move byte comparison |
| Directive revision history | `30229ae` v1 45 sections → `b8e38d2` v2 15 sections → `85ac462` v3 46 sections → `d57deb9` three defect fixes |
| `.agents-hub` (renamed from `agents-hub-one` 2026-08-20) is a governance tree with a five-file `rules/` contract, zero runtime-specific names across all five files, and seven 0-byte placeholder files | Clone inspection; `grep -ric` for runtime names returned 0 on all five |
| `agents-hub-two` is an agent operating package: 15 agent definitions, a registry, a JSON schema, 4 prompts, 4 templates. Contains no governance layer — zero occurrences of "governance", "precedence", "runtime-neutral", "catalog", "provenance" | Clone inspection and keyword scan |
| `agents-hub-two` still declares itself to be `.agents-hub` in its own content. Superseded by D-24; correcting the stale claim is reconciliation work, not an open authority question. | `agents-hub-two/docs/README.md` and `package-layout.json`; the same claim in `.agents-hub/README.md` is now correct |
| `agent-governance-toolkit` is an unmodified fork of `microsoft/agent-governance-toolkit`, MIT, HEAD authored upstream 2026-05-11, zero local commits | `git log -1 --format='%an %ad'`; `LICENSE`; `MAINTAINERS.md` |
| Four engineering items resolved from evidence under `ENGINEER-OWNERSHIP`; zero items remain classified `Conflict` or unresolved | `DECISIONS.md` D-12 to D-16; assessment revision 2 |
| GitHub `.agents-hub` @ `47c0187` -- captured while named `agents-hub-one` -- holds 16 files, 7 of them 0-byte placeholders; baseline manifest captured for live comparison | `evidence/AGENTS-HUB-ONE-BASELINE-2026-08-19.json` |
| Gateway discovery no longer presupposes the canonical Hub, and canonical-Hub semantics are kept separate from pre-consolidation-source findings. `hubState` is computed before the report object; hub-derived sections carry `canonicalHubApplicable` plus separate `preConsolidation*` fields rather than substituting source results into canonical field names; overlapping scan roots are disclosed and findings deduplicated by canonical full path; section 14 probes `.agents-hub`, the legacy `agents-hub-one` leaf, and `agents-hub-two` and states canonical `.agents-hub` absence explicitly. Satisfies D-06 | `scripts/Invoke-GatewayDiscovery.ps1` |
| Live-Hub inventory procedure prepared, unexecuted. Requires no network and no clone; compares the live Hub against the committed baseline | `scripts/Invoke-HubInventory.ps1` |
| Traversal consolidated into one owner with pre-descent pruning. Six recursive enumerations that traversed `.remember` before filtering it from output were removed; zero `Get-ChildItem -Recurse` remain in executable code | `scripts/lib/SafeTraversal.ps1`; `scripts/Assert-RememberPruning.ps1` |
| Reparse points of either kind, file and directory, are detected by attribute **before** the directory/file split and are never traversed, returned, or hashed. A file link routed to the file branch would have been hashed, and `Get-FileHash` follows links | `scripts/lib/SafeTraversal.ps1` — `Test-IsReparsePoint`; A4 and A7 in the pruning proof |
| The pruning proof verdict is fail-closed: PASS requires the Hub to exist, A1 to A7 to pass, the runtime test to pass, and completeness to be COMPLETE. A skipped runtime proof is no longer PASS | `scripts/Assert-RememberPruning.ps1` |
| A supplied root that is itself safety-pruned yields INCOMPLETE, not an empty success | `scripts/lib/SafeTraversal.ps1` |
| Inventory completeness fails closed. Item cap, depth cap, or enumeration error forces `INCOMPLETE`, reported in the evidence and exit code 2 | `scripts/Invoke-HubInventory.ps1`; A5 and A6 in the pruning proof |
| Six static invariants A1 to A6 verified PASS. Both the PowerShell and the local checker were corrected to strip string literals in one pass; the earlier regex approach mis-parsed lines mixing quote types | `scripts/Assert-RememberPruning.ps1` |
| Evidence filenames carry the date the script runs, from `Get-Date`; they are not fixed dates | script source |
| Reconciliation assessment and proposed canonical target tree produced; 43 source files classified with 0 unaccounted | `evidence/HUB-RECONCILIATION-ASSESSMENT-2026-08-19.md` |
| Neither source is the canonical Hub. hub-one supplies the governance contract (5 owners, 0 runtime-specific names); hub-two supplies agent definitions, registry, schemas, prompts, templates and contains no governance layer | Section 1 of the assessment |
| 16 of hub-two's 22 agent `rules` entries touch a concern a hub-one rule already owns; they split into general-form statements to fold and domain-specific constraints to preserve | Section 2 of the assessment |
| Discovery tooling is present on `main` (`scripts/`), never executed | `git ls-tree -r --name-only origin/main`; no PowerShell in the authoring environment |
| Root `CLAUDE.md` is tracked on `main`, is 11 bytes, and contains only the line `@AGENTS.md` | `wc -c`; `grep -cv '^@AGENTS.md$'` returned 0 |

| The predecessor backoffice `workspace-governor-agents-hub-one` @ `24798d0` holds a twice-verified, execution-ready 12-step consolidation plan (v0.4.2) that was never started, plus a 2026-08-16 read-only inventory of the live `.agents-hub` | Direct inspection of all 9 named artifacts, `tasks/`, `research/`, `evidence/`; `evidence/PREDECESSOR-BACKOFFICE-REVIEW-2026-08-20.md` |
| Active planning directives are at `plans/`. The Gateway directive moved there from the repository root with content byte-identical | `sha256sum` comparison of `HEAD:mcp-gateway` against `plans/MCP-GATEWAY.md` |

### Authority relationship

**One Hub, two representations.** The `.agents-hub` repository is canonical source;
`C:\Users\Chloe\.agents-hub` is its local materialized location for agent
consumption. Same logical Hub, not two authorities; they must not drift
independently (`DECISIONS.md` D-26). A local-only edit is drift, not a decision.

```
.agents-hub         = current canonical Agent Hub and live governance authority
workspace-governor = Agent Hub backoffice; manages, researches, reconciles,
                     backs up, archives, and improves the Hub
agents-hub-two     = source material pending reconciliation
```

Canonical **now**; **not final**. Under active consolidation and structurally
incomplete where known gaps remain -- gaps are listed under Blockers and Open
work below. `README.md` owns the full relationship table. `DECISIONS.md` D-24
records the decision.

**The GitHub rename itself is not yet done.** See Verification assignments.

## Blockers

Current phase is Hub consolidation. Blockers are grouped by the phase they bind.

### Binding the current phase

| # | Blocker | Effect | Owner |
|---|---|---|---|
| B-1 | Hub One target tree and ownership map not accepted. `workspace-governor-agents-hub-one/STATE.md` stop condition: do not refactor before acceptance. | Assessment and a proposed target tree are permitted. Refactoring either source repository is not. | Resolved by accepting the deliverable of this phase |
| B-2 | `design-systems/.remember` has unresolved provenance and sensitivity. | Must not be read, hashed, moved, or classified | Requires separate review |
| B-6 | The content of the live local `.agents-hub` directory is not **currently** verified. **Narrowed 2026-08-20:** a read-only inventory of it exists in the predecessor backoffice -- `workspace-governor-agents-hub-one/evidence/BASELINE-AUDIT-2026-08-16.md` -- covering root structure, the five-file `rules/` contract, empty `runtime-adapters/`, `references/`, empty `governance-templates/`, and `.remember` presence. It is 4 days stale and instructs re-inspection, so a current inventory is still required, but the content was not unknown. The canonical `.agents-hub` repository is a placeholder skeleton at `47c0187`: 7 of its 16 files are 0-byte. Note the distinction -- the canonical *repository* is settled; the local runtime *directory* content is not. | The proposed target tree cannot be accepted as canonical, because the consolidation inputs are not fully known. | Local agent runs `scripts/Invoke-HubInventory.ps1` and commits the evidence |

### Required before Gateway runtime integration and completion — not binding this phase

| # | Blocker | Effect | Owner |
|---|---|---|---|
| B-3 | Codex authority file contains stale absolute paths and overlaps Hub-owned responsibilities. Recorded as an active conflict in `workspace-governor-agents-hub-one/STATE.md`, which halts Codex adapter activation. | Gateway directive sections 34 and 43 require Codex to connect, so the Gateway cannot reach DONE until this is reconciled. Does not block Hub consolidation. | Requires user authorization to open as a separate scoped change (`DECISIONS.md` D-11) |
| B-4 | ~~Canonical Hub identity contested.~~ **Resolved 2026-08-20** by `DECISIONS.md` D-24: `.agents-hub` is the canonical Agent Hub and live governance authority. The remaining gap is **structural, not authority** -- the canonical Hub is under active consolidation and incomplete where known gaps exist, so Gateway directive section 29 rule-folding still waits on consolidation, not on deciding which repository governs. | Section 29 rule-folding waits on consolidation completeness | Resolved by Hub consolidation |
| B-5 | Live Windows environment is unreachable from a cloud session. | Gateway directive section 5 items covering local MCP, Claude Code, Codex, secrets and audit mechanisms cannot be collected remotely | Local agent executes discovery |

## Verification assignments

Verification that cannot be performed in the current environment is recorded here
with its assigned executor, rather than repeated as an open caveat. An assigned
pending verification is not a defect and is not re-flagged each session; see
`AGENTS.md` § Evidence standard.

### GitHub repository rename

| Field | Value |
|---|---|
| Status | PENDING |
| Action | Rename `klodebeers/agents-hub-one` to `.agents-hub` |
| Assigned executor | Klo |
| Reason not done in cloud | No rename capability exists in the GitHub tooling available to this session. `create_repository` and `fork_repository` exist; no update or rename operation does. Creating a new repository and copying content is **not** a rename: it loses the redirect and history association and leaves two repositories competing for authority. Not attempted. |
| Execution method | GitHub web UI: repository -> **Settings** -> **General** -> **Repository name** -> enter `.agents-hub` -> **Rename**. |
| Verification step | `https://github.com/klodebeers/.agents-hub` loads and the page header shows `.agents-hub`; `https://github.com/klodebeers/agents-hub-one` redirects to it. Then locally: `git -C <clone> remote -v` still resolves via the redirect, and `git -C <clone> fetch` succeeds. |
| Effect while pending | Repository references in this repository already point to `.agents-hub`, so they are correct on completion and stale until then. Cloning `.agents-hub` fails until the rename is done; `agents-hub-one` still works. |
| Recheck trigger | Rename confirmed, or a decision to keep the current name |

### PowerShell runtime verification

| Field | Value |
|---|---|
| Status | PENDING |
| Assigned environment | Local Windows |
| Assigned executor | Klo / local Windows agent |
| Cloud Claude responsibility | Parse and execute under PowerShell 7 on Linux against synthetic fixtures. Done. |
| Cloud blocker | No |
| Current phase blocker | Yes, only when the live-Hub inventory result is required to continue consolidation |
| Recheck trigger | Local execution evidence is committed to `workspace-governor` |

Scope: `scripts/Invoke-HubInventory.ps1`, `scripts/Assert-RememberPruning.ps1`,
`scripts/Invoke-GatewayDiscovery.ps1`, `scripts/Assert-DiscoveryReadOnly.ps1`,
`scripts/lib/SafeTraversal.ps1`.

**Correction to a premise this phase was built on.** "No PowerShell in this
environment" was accepted without testing it. PowerShell 7 is available here as a
self-contained tarball and needs no install. The scripts have now been parsed and
executed in cloud. The three hand-rolled static gates built earlier were an
avoidable substitute for an existing capability -- see
`rules/VERIFICATION-RESOLUTION.md` and
`evidence/POWERSHELL-EXECUTION-2026-08-20.md`.

Completed in cloud: parse of all five files with `[Parser]::ParseFile` (0
errors); execution of `Assert-RememberPruning.ps1` on both the no-Hub and
Hub-present paths, and `Invoke-HubInventory.ps1` on both the COMPLETE and
INCOMPLETE paths, against synthetic fixtures including `.remember`, a file
symlink and a directory symlink; confirmation that no `.remember` content reaches
any emitted file; static invariants A1 to A7.

Still required: **Windows PowerShell 5.1** specifically, against the **live
Hub**. Neither is waived, and cloud execution does not substitute for either.
Windows junction semantics, ACL-denied directories and long paths remain
unexercised. Live-Hub evidence cannot be accepted until
`Assert-RememberPruning.ps1` returns `PASS` and `Invoke-HubInventory.ps1` reports
`Completeness: COMPLETE` on the local machine.

## Open work

1. Inventory the live local Hub, then complete Step 1 of `plans/AGENT-HUB-CONSOLIDATION.md`: accept the target tree and classify every item across the three inputs -- live `.agents-hub`, canonical `.agents-hub`, `agents-hub-two`. Start from the carried-forward v0.4.2 ledger and the 2026-08-16 baseline, not from zero.
2. ~~Revise the Gateway discovery tooling so it does not presuppose `.agents-hub` exists.~~ **Closed** — semantics verified across the full report, and the `00_hubState` ordering defect fixed. Still unexecuted; awaits the local Windows runtime test recorded under Verification assignments.
3. Execute plan Steps 2 onward once the target tree is accepted. Assessment and classification are complete; `change`, `reference-update` and `verify` remain. See `evidence/HUB-RECONCILIATION-ASSESSMENT-2026-08-19.md`.
4. Place the SSOT pair in `.agents-hub` as Hub assets, then reduce the `workspace-governor` copies to backups/provenance. Both files are staged here and validated; placement is the remaining step. `AGENT-SSOT.json` v1.1, `USER-SSOT.json` v1.3 (Greyed-scoped, scope-loaded). Blocked on the rename landing. See `evidence/HUB-ASSET-PLACEMENT-CORRECTION-2026-08-20.md`.
5. Open B-3 as a separate scoped change once authorized.
6. Determine placement of the three agent rulings recorded in `DECISIONS.md` under D-07 through D-09.
7. Trim the duplicated live-state narrative in `workspace-governor-agents-hub-one/research/` per D-15. Edits another repository; sequenced separately.
8. ~~Correct the case-insensitive variable collisions found in four scripts, two of them live defects in the assigned local commands.~~ **Closed** — fixed, and a static gate added to prevent the class. See `evidence/SCRIPT-STRUCTURE-DEFECTS-2026-08-20.md`.
9. Promote the Verification Resolution Rule into the canonical `.agents-hub` once its structure and rule ownership are finalized. Held locally as an interim binding; terms and on-promotion steps in `PENDING-GLOBAL-PROMOTIONS.md` P-01. Blocked by the same absence of a canonical Hub as B-4.
10. Resolve the duplicate ownership between `AGENT-SSOT.json` and `rules/VERIFICATION-RESOLUTION.md` / `rules/ENGINEER-OWNERSHIP.md` at consolidation. Open governance conflict, surfaced not blended. `PENDING-GLOBAL-PROMOTIONS.md` P-03.
11. Correct `AGENTS.md` placement in the canonical Hub: root, not `rules/`. Structural only. `evidence/GOVERNANCE-STRUCTURE-OBSERVATIONS-2026-08-20.md` Observation 1. Do not refactor `.agents-hub` now.
12. Close conflict-resolution gaps G-1 and G-2 as sections in existing owners at consolidation. G-3 deferred. `PENDING-GLOBAL-PROMOTIONS.md` P-04. No new rule file.
13. Resolve C-03, carried from the predecessor backoffice: Claude Code project-versus-global loading can let project instructions take priority while semantic governance forbids lower layers weakening global governance. Blocks Claude Code adapter finalization only. Plan Step 9.
14. ~~Adapt the predecessor `tasks/` audit prompts into coverage checklists for `scripts/Invoke-GatewayDiscovery.ps1`.~~ **Closed** -- item-level comparison done: `evidence/PREDECESSOR-AUDIT-SPEC-COVERAGE-2026-08-20.md`. Four inventory gaps identified and scoped as item 16. Spec 01 Phase 3 and spec 03 Parts B-D are classified **superseded for execution, provenance-only** -- the consolidation directive already supersedes any older instruction authorizing remediation, installation, deletion, restructuring or machine changes during reconciliation. Preserved historically; never handed to a local agent as live instructions.
15. Carry G-01, G-04 and G-05 from the predecessor register: Hub reference/research overlap mapping (plan Step 6); human glossary placement; repository-delivery workflow artifact. None currently blocking.

16. Close the four discovery-tooling inventory gaps, read-only and additive. **Do not modify the tooling during this reconciliation phase.** Recorded for later implementation: probe `gh`, WSL, Windows Terminal and search utilities; cross-check command resolution with `where.exe` and record every hit so shadowing and multiple installations are detectable; read User and System PATH separately from the effective PATH; detect duplicate PATH entries. Deferred deliberately -- Gateway discovery is under a stop condition until consolidation completes, and the plan's process gate limits current work to reconciliation. `evidence/PREDECESSOR-AUDIT-SPEC-COVERAGE-2026-08-20.md`.
17. Carry the predecessor spec-02 analysis fields into Step 1 and Step 3 of the consolidation: per-config-source scope, loading mechanism, precedence, and whether a file is actually active; plus intent-based semantic duplication, which `Invoke-GatewayDiscovery.ps1` section 11 cannot supply -- it groups byte-identical content only. Agent analysis, not scriptable.

## Next action

Run the local Hub inventory on the Windows machine and commit the evidence files
it emits. This is the only remaining input needed to make the target tree
acceptable.

**Pull current `main` first. Do not run any script copied earlier.** The versions
before `main` failed to parse on Windows PowerShell 5.1: 61 em dashes in
non-BOM UTF-8 sources were decoded as ANSI, and one of the resulting bytes is a
character PowerShell treats as a string delimiter. All `.ps1` files are now pure
ASCII. Earlier versions also carried case-insensitive variable collisions:
`Assert-RememberPruning.ps1` would have failed before writing its verdict, and
`Invoke-HubInventory.ps1` would have dropped its unverified list whenever the
inventory came back INCOMPLETE. Both are fixed on `main`. See
`evidence/SCRIPT-STRUCTURE-DEFECTS-2026-08-20.md`.

From the repository root, in order:

```powershell
.\scripts\Assert-RememberPruning.ps1
.\scripts\Invoke-HubInventory.ps1
```

The first must report `Proof verdict: PASS`; the second, `Completeness: COMPLETE`.
Neither result is acceptable if the other did not hold.

Both are read-only, make no network calls, emit no file contents, resolve the Hub
path from the environment and record the resolved path, and do not read or
enumerate inside `design-systems\.remember`.

Do not accept the target tree before that evidence exists. Do not execute
consolidation. Do not run Gateway discovery.

## Stop conditions

- Do not read, hash, move, or classify `design-systems/.remember` before its provenance and sensitivity review.
- Do not activate a Codex adapter while B-3 is unresolved.
- Do not fold existing Hub rules before the target tree and ownership map are accepted.
- Do not reopen the 46-section directive structure (`DECISIONS.md` D-04).
- Do not run the discovery tooling in `scripts/` until it is revised per open work item 2 **and** Hub consolidation is complete (`DECISIONS.md` D-05, D-06).
- Do not adopt `agent-governance-toolkit` without provenance, licence, and generated-output review.
- Do not commit a `.ps1` under `scripts/` containing any byte above 0x7F. Windows PowerShell 5.1 reads non-BOM sources as ANSI, and U+2014 becomes a string delimiter.
- Do not apply canonical restructuring, or modify live Hub governance, runtime configuration, code, manifests or lockfiles, without approval. The current task is reconciliation, not implementation (`plans/AGENT-HUB-CONSOLIDATION.md` § 6.7).
- Do not create a Technical Translation rule file or carry `rules/VERIFICATION-RESOLUTION.md` into the Hub. Both concerns already have owners (`plans/AGENT-HUB-CONSOLIDATION.md` § 6.4).
- Do not treat `AGENT-SSOT.json` or `USER-SSOT.json` in this repository as live governing authorities. They are Agent Hub assets; the copies here are backoffice staging and provenance. The Hub root `AGENTS.md` is the bootstrap and routing authority. Do not restate their content here either.
- Do not choose a verification method before reading `rules/VERIFICATION-RESOLUTION.md`. It is binding, and it bounds the method, the stopping condition, and when new tooling is justified.
- Do not hand any script under `scripts/` to the local operator until
  `python3 scripts/Assert-ScriptStructure.py --selftest` and the same tool run
  over `scripts/*.ps1 scripts/lib/*.ps1` both pass. This gate is static only; it
  does not satisfy the PowerShell runtime verification recorded above.

Reinspect live sources before acting. This record is continuity evidence, not proof that anything remains unchanged.
