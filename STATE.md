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

### Predecessor information dependency -- closed

The backoffice no longer depends on unique load-bearing information held only in
`workspace-governor-agents-hub-one`. **18** files carried as provenance copies --
4 directly under `plans/reference/` and 14 under `plans/reference/predecessor/` --
with source SHA-256 for each. Substantive content migrated to
owners: `LEARNINGS.md` (created; L-001 to L-006 carried) and `DECISIONS.md` D-30
(five settled decisions that had no representation here).

Deliberately **not** carried, per instruction: `tasks/` (3 files) and `versions/`
(25 snapshots) remain archival in the predecessor repository.

**The predecessor repository is no longer unmodified.** A `SUPERSEDED, DO NOT
EXECUTE` banner was prepended to all three `tasks/` files on 2026-08-20 as a
deliberate archive-safety change, because the superseded classification existed
only here and did not protect anyone opening those files directly. Additive only,
3 lines per file, original content byte-identical after the banner; git preserves
the pre-banner versions, so only the current tip changed.

| | |
|---|---|
| Predecessor baseline SHA, before the banner | `24798d032e39081a6885f3648430786019129ef4` |
| Predecessor SHA containing the banners | `8d4513caa1809b96117e69e4e602bfff0d8d5c5c` |

Recorded as `DECISIONS.md` D-31. Dated evidence written before this change still
says the repository is unmodified; those statements were true when recorded and are
left intact.

### Authority relationship

**One Hub, two representations.** The `.agents-hub` repository is canonical source;
`C:\Users\Chloe\.agents-hub` is its local materialized location for agent
consumption. Same logical Hub, not two authorities; they must not drift
independently (`DECISIONS.md` D-33, renumbered from the second D-26). A local-only edit is drift, not a decision.

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

### Canonical Hub -- current verified state

`klodebeers/.agents-hub` at **`c6c966b`**, Step 1 restructuring applied and all
dangling references cleared. Verified against the extracted remote: 0 dangling
references across the 8 live documents, dated evidence excluded. Nine tracked files:

```text
AGENTS.md                                     root bootstrap, router, precedence
CATALOG.md                                    inventory
README.md                                     navigation
rules/ENGINEER-OWNERSHIP.md                   ownership, intake, decision resolution
rules/AUTONOMY-AND-PROTECTED-BOUNDARIES.md    autonomy, approval, boundaries
rules/CONTEXT-AND-ORCHESTRATION.md            context, delegation, continuity
rules/VERIFICATION-AND-EVIDENCE.md            done, testing, audit, evidence
references/AGENTS-MD-LIVE-AUDIT-2026-08-16.md retained dated audit
design-systems/placeholder.md                 EXCLUDED, Conflict, untouched
```

Retired: Hub `STATE.md`, and six placeholder files. `governance-templates/` and
`runtime-adapters/` no longer exist in the repository; the latter returns at Step 9
with its first accepted adapter. Detail in `DECISIONS.md` D-37.

**The live local Hub has not been re-materialized.** The repository is ahead of
`C:\Users\Chloe\.agents-hub`, which still carries the pre-restructuring layout
including `rules/AGENTS.md` and `STATE.md`. Per D-33 the two are one logical Hub and
must not drift, so materializing the change locally is the immediate next action.

`C:\Users\Chloe\.agents-hub` is confirmed a **git working copy**, stated by the
user 2026-08-21, and materialization by `git pull` is authorised on that basis.
Hand-copying files is excluded: it would leave the local path without a comparable
ref and make future drift undetectable. `DECISIONS.md` D-41. Execution requires the
local machine and is therefore recorded under Verification assignments, not
performed here -- blocker B-5.

### Step 1 gate -- satisfied

Both required results are in, from the operator's machine, committed at `12f93e6`:

| Script | Required | Returned |
|---|---|---|
| `Assert-RememberPruning.ps1` | `Proof verdict: PASS` | **PASS**, fail-closed. A1-A7 PASS. 12 directories visited, 1 safety-pruned, 0 violations |
| `Invoke-HubInventory.ps1` | `Completeness: COMPLETE` | **COMPLETE**. 9 live files, 0 only-in-live, 0 content differs |

Step 1 is therefore complete: the target tree and item classification are in
`evidence/HUB-TARGET-TREE-AND-CLASSIFICATION-2026-08-21.md`. **Applying it needs
approval** per `plans/AGENT-HUB-CONSOLIDATION.md` § 6.7.

## Blockers

Current phase is Hub consolidation. Blockers are grouped by the phase they bind.

### Binding the current phase

| # | Blocker | Effect | Owner |
|---|---|---|---|
| B-1 | Hub One target tree and ownership map not accepted. `workspace-governor-agents-hub-one/STATE.md` stop condition: do not refactor before acceptance. | Assessment and a proposed target tree are permitted. Refactoring either source repository is not. | Resolved by accepting the deliverable of this phase |
| B-2 | `design-systems/.remember` has unresolved provenance and sensitivity. | Must not be read, hashed, moved, or classified | Requires separate review |
| B-6 | ~~Live local `.agents-hub` content not currently verified.~~ **CLOSED 2026-08-21 on evidence, premise disproved.** The live Hub holds 9 files, all byte-identical to baseline `47c0187`; 0 files exist live that the baseline lacks; 0 content differs; the 7 baseline-only files are the zero-byte placeholders, absent on disk. B-6 assumed the live Hub might hold real content behind those placeholders, leaving inputs unknown. It does not. | Consolidation inputs are now fully known | Closed by `evidence/LIVE-HUB-INVENTORY-2026-08-21.md` and `evidence/REMEMBER-PRUNING-PROOF-2026-08-21.md` |

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

### Local Hub materialization -- PENDING

| Field | Value |
|---|---|
| Status | **PENDING.** Authorised 2026-08-21; awaiting local execution |
| Requirement | D-33: the repository and `C:\Users\Chloe\.agents-hub` are one logical Hub and must not drift. The repository carries the Step 1 layout at `c6c966b`; the local path does not |
| Why no remote action can do it | The path is on the operator's Windows machine, unreachable from a cloud session (blocker B-5). No cloud-side change can move it |
| Assigned executor | Klo, on the local Windows machine |
| Method | `cd C:\Users\Chloe\.agents-hub` then `git pull`. Mechanism settled as git, not hand-copying, per D-41 |
| Verification | `git rev-parse HEAD` returns `c6c966b3dfcc03a2f76c7f79330ae7797283df23`, and `git status` reports a clean tree. Tree afterwards: `AGENTS.md` at the root; no `STATE.md`; no `governance-templates/`; no `runtime-adapters/`; `design-systems/` unchanged |
| Known wrinkle | The local clone's `origin` may still carry the pre-rename URL `.../agents-hub-one`. It resolves through GitHub's redirect, so `git pull` works; `git remote set-url origin https://github.com/klodebeers/.agents-hub` re-points it when convenient. A repository rename never renames a clone or rewrites its remote |
| Recheck trigger | Any later commit to the canonical Hub. Every Hub change reopens this until the two are equal |

### Fresh-agent bootstrap and runtime activation

| Field | Value |
|---|---|
| Status | PENDING, **unassigned until now** |
| Requirement | v0.4.2 Step 11, completion criterion 18, and predecessor learning L-001 all require fresh-agent bootstrap and per-runtime activation evidence |
| Why no script can do it | Activation is a property of a new session, not of the filesystem. `Collect-LocalEvidence.ps1` collects configuration presence, which is explicitly **not** evidence of discovery, loading or enforcement |
| Assigned executor | Klo, in a fresh session of each runtime |
| Method | Start a new Claude Code session and a new Codex session in a governed directory. In each, ask the agent to state which instruction files it loaded and from where, without being told the answer. Record the reply verbatim |
| Verification | The reply names the canonical Hub route. Silence, a guess, or a different file is a negative result and must be recorded as such |
| Recheck trigger | Any change to instruction placement, adapter projection, or the root bootstrap file |
| Note | This was previously folded into blocker B-5, which is scoped to evidence **collection** from an unreachable machine. Bootstrap **testing** is a different obligation and would have been rediscovered at Step 11 |

### GitHub repository rename -- COMPLETE

| Field | Value |
|---|---|
| Status | **DONE.** Verified 2026-08-20 |
| Action | Rename `klodebeers/agents-hub-one` to `.agents-hub` |
| Executed by | Klo |
| Verification | Authenticated repository listing returns `klodebeers/.agents-hub`; `agents-hub-one` no longer appears as an accessible repository. Content unchanged since the baseline: last push 2026-08-19, consistent with `47c0187` |
| Residual | The session clone at `/workspace/agents-hub-one` still carries the old remote URL. It resolves through GitHub's redirect, so it works; re-point it when convenient. A local clone directory is never renamed by a repository rename |
| Recheck trigger | None. Closed |

**Recording error, corrected.** This assignment was reported to the user as still
PENDING **after it had been completed**, because this record was read instead of
the live source. `AGENTS.md` states that `STATE.md` is continuity evidence and not
proof that anything remains unchanged, and requires live sources to be reinspected
before acting. That was not done.

Two checks then misled the correction attempt before an authoritative one was used:
`git ls-remote` on the new name failed on **credentials**, not on absence, and
shell `&&` logic reported that failure as existence; and `git ls-remote` on the
**old** name succeeded, which proves nothing either way because GitHub preserves
redirects after a rename. The authenticated repository listing is the reliable
method. Recorded as `LEARNINGS.md` L-014.

### PowerShell runtime verification -- COMPLETE

| Field | Value |
|---|---|
| Status | **DONE 2026-08-21.** Both scripts executed on the operator's Windows machine and emitted their evidence. `Assert-RememberPruning.ps1`: `PASS`, fail-closed, A1-A7 all PASS, `.remember` found and pruned, 0 violations, 0 reparse points in returned items. `Invoke-HubInventory.ps1`: `Completeness: COMPLETE`. Committed at `12f93e6` |
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
11. ~~Correct `AGENTS.md` placement in the canonical Hub: root, not `rules/`.~~ **Closed 2026-08-21**, applied at `80dff05` with references updated in both directions.
12. Close conflict-resolution gaps G-1 and G-2 as sections in existing owners at consolidation. G-3 deferred. `PENDING-GLOBAL-PROMOTIONS.md` P-04. No new rule file.
13. Resolve C-03 as restated: Claude Code instruction placement enforces nothing on its own, so an enforcement carrier -- managed setting or hook -- must be chosen per rule. The earlier wording, "project instructions outrank global governance", conflated advisory instructions with enforced settings and is withdrawn. `evidence/RUNTIME-CONVENTIONS-2026-08-20.md`.
14. ~~Adapt the predecessor `tasks/` audit prompts into coverage checklists for `scripts/Invoke-GatewayDiscovery.ps1`.~~ **Closed** -- item-level comparison done: `evidence/PREDECESSOR-AUDIT-SPEC-COVERAGE-2026-08-20.md`. Four inventory gaps identified and scoped as item 16. Spec 01 Phase 3 and spec 03 Parts B-D are classified **superseded for execution, provenance-only** -- the consolidation directive already supersedes any older instruction authorizing remediation, installation, deletion, restructuring or machine changes during reconciliation. Preserved historically; never handed to a local agent as live instructions.
15. Carry G-01, G-04 and G-05 from the predecessor register: Hub reference/research overlap mapping (plan Step 6); human glossary placement; repository-delivery workflow artifact. None currently blocking.

16. Close the four discovery-tooling inventory gaps, read-only and additive. **Do not modify the tooling during this reconciliation phase.** Recorded for later implementation: probe `gh`, WSL, Windows Terminal and search utilities; cross-check command resolution with `where.exe` and record every hit so shadowing and multiple installations are detectable; read User and System PATH separately from the effective PATH; detect duplicate PATH entries. Deferred deliberately -- Gateway discovery is under a stop condition until consolidation completes, and the plan's process gate limits current work to reconciliation. `evidence/PREDECESSOR-AUDIT-SPEC-COVERAGE-2026-08-20.md`.
17. Carry the predecessor spec-02 analysis fields into Step 1 and Step 3 of the consolidation: per-config-source scope, loading mechanism, precedence, and whether a file is actually active; plus intent-based semantic duplication, which `Invoke-GatewayDiscovery.ps1` section 11 cannot supply -- it groups byte-identical content only. Agent analysis, not scriptable.

18. Carry the predecessor's runtime-neutral project-continuity pattern into the plan. Required by `evidence/LEGACY-GOVERNANCE-MATERIAL-CONSOLIDATION-2026-08-17.md` item 5 and absent from every current record.
19. Resolve the `CATALOG.md` collision: the live Codex global instruction file requires Hub `README.md` and `CATALOG.md`, while the accepted taxonomy makes `CATALOG.md` conditional. Plan delta D-l.
20. ~~Resolve the unverified Codex precedence question.~~ **Closed 2026-08-21** by `DECISIONS.md` D-38: repository-level normally outranks machine-level, by concatenation order; within a level `AGENTS.override.md` replaces `AGENTS.md`.
21. Define who performs the independent pre-edit review that v0.4.2 Step 5 lists as a prerequisite, and how it is evidenced. Subagent review is now demonstrated to work; formalise it as the mechanism.

22. Package a validated governance workflow as a plugin only after it is stable and needs installable distribution. Settled but deferred per `DECISIONS.md` D-30 item 4. Skill first; packaging must not create a second authoritative copy.
23. Scheduled audits remain separate deferred runtime automation. Settled but deferred per D-30 item 5.
24. Decide the glossary's placement when a glossary artifact actually exists. It may explain canonical terms but never redefine them, and must not be placed in `rules/`. D-30 item 2; plan G-04.

## Next action

**Materialize `c6c966b` into the live local Hub.** Authorised; awaiting execution
on the local Windows machine, which no cloud session can reach. The canonical
repository and `C:\Users\Chloe\.agents-hub` are one logical Hub under D-33 and must
not drift independently. The repository now carries the Step 1 layout; the local
path does not.

```powershell
cd C:\Users\Chloe\.agents-hub
git pull
git rev-parse HEAD
git status --short
```

The path is confirmed a git working copy, so `git pull` is the mechanism and
hand-copying is excluded (D-41).

Verification: `git rev-parse HEAD` returns
`c6c966b3dfcc03a2f76c7f79330ae7797283df23` and `git status --short` prints nothing.
Expected tree afterwards: `AGENTS.md` at the root, no `STATE.md`, no
`governance-templates/`, no `runtime-adapters/`, `design-systems/` unchanged.

If `origin` still points at `agents-hub-one`, the pull still works through GitHub's
redirect; `git remote set-url origin https://github.com/klodebeers/.agents-hub`
tidies it. Full detail under Verification assignments § Local Hub materialization.

Then, in either order:

- **Fresh-agent bootstrap test.** Still open, still assigned, and now more
  informative: the bootstrap file has moved, so the test measures whether the new
  root location is actually discovered. Method in Verification assignments -- ask a
  new session which instruction files it loaded and from where, without supplying
  the answer.
- **Step 2 change work.** Creating `agents/`, `orchestration/`, `registry/`,
  `templates/` and `context/`, each with its first accepted artifact. Deliberately
  excluded from the Step 1 approval because each requires an Adapt transformation of
  `agents-hub-two` content. Requires approval before it touches the Hub.

Closed this round: B-6, the PowerShell runtime verification, the GitHub rename, and
the Codex and Claude Code precedence questions. C-03 is closed on precedence and
open on enforcement.

## Stop conditions

- Do not read, hash, move, or classify `design-systems/.remember` before its provenance and sensitivity review.
- Do not activate a Codex adapter while B-3 is unresolved.
- Do not fold existing Hub rules before the target tree and ownership map are accepted.
- Do not reopen the 46-section directive structure (`DECISIONS.md` D-04).
- Do not run the discovery tooling in `scripts/` until it is revised per open work item 2 **and** Hub consolidation is complete (`DECISIONS.md` D-05, D-06).
- Do not adopt `agent-governance-toolkit` without provenance, licence, and generated-output review.
- Do not adopt the third-party **rules scaffolder** without provenance, licence and generated-output review. Its generator-owned block is overwritten on rerun and must never own Hub governance. This is a **different artifact** from the `agent-governance-toolkit` fork; both stop conditions apply independently.
- Do not migrate before refactoring passes source-preserving verification. Carried from the predecessor; it survived only implicitly inside the step ordering.
- Do not delete any predecessor or legacy material before reinspecting each proposed target for unique unrelated content and required recovery evidence. Carried from `evidence/LEGACY-GOVERNANCE-MATERIAL-CONSOLIDATION-2026-08-17.md`, where roughly 20 files are marked discard-as-active-governance and **none has been deleted**.
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
