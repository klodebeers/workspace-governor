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
| `workspace-governor` `main` is at `d57deb9` and contained only the `mcp-gateway` file before this bootstrap | `git ls-tree -r --name-only origin/main` |
| The `mcp-gateway` directive is settled: 46 sections, 1,940 lines, contiguous numbering 1–46, 41 Done-When checkboxes | 22-check verification pass against `origin/main` |
| Directive revision history | `30229ae` v1 45 sections → `b8e38d2` v2 15 sections → `85ac462` v3 46 sections → `d57deb9` three defect fixes |
| `agents-hub-one` is a governance tree with a five-file `rules/` contract, zero runtime-specific names across all five files, and seven 0-byte placeholder files | Clone inspection; `grep -ric` for runtime names returned 0 on all five |
| `agents-hub-two` is an agent operating package: 15 agent definitions, a registry, a JSON schema, 4 prompts, 4 templates. Contains no governance layer — zero occurrences of "governance", "precedence", "runtime-neutral", "catalog", "provenance" | Clone inspection and keyword scan |
| Both source repositories declare themselves to be `.agents-hub` | `agents-hub-one/README.md`; `agents-hub-two/docs/README.md` and `package-layout.json` |
| `agent-governance-toolkit` is an unmodified fork of `microsoft/agent-governance-toolkit`, MIT, HEAD authored upstream 2026-05-11, zero local commits | `git log -1 --format='%an %ad'`; `LICENSE`; `MAINTAINERS.md` |
| Four engineering items resolved from evidence under `ENGINEER-OWNERSHIP`; zero items remain classified `Conflict` or unresolved | `DECISIONS.md` D-12 to D-16; assessment revision 2 |
| GitHub `agents-hub-one` @ `47c0187` holds 16 files, 7 of them 0-byte placeholders; baseline manifest captured for live comparison | `evidence/AGENTS-HUB-ONE-BASELINE-2026-08-19.json` |
| Gateway discovery no longer presupposes the canonical Hub, and canonical-Hub semantics are kept separate from pre-consolidation-source findings. `hubState` is computed before the report object; hub-derived sections carry `canonicalHubApplicable` plus separate `preConsolidation*` fields rather than substituting source results into canonical field names; overlapping scan roots are disclosed and findings deduplicated by canonical full path; section 14 probes `agents-hub-one` and `agents-hub-two` and states canonical `.agents-hub` absence explicitly. Satisfies D-06 | `scripts/Invoke-GatewayDiscovery.ps1` |
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

## Blockers

Current phase is Hub consolidation. Blockers are grouped by the phase they bind.

### Binding the current phase

| # | Blocker | Effect | Owner |
|---|---|---|---|
| B-1 | Hub One target tree and ownership map not accepted. `workspace-governor-agents-hub-one/STATE.md` stop condition: do not refactor before acceptance. | Assessment and a proposed target tree are permitted. Refactoring either source repository is not. | Resolved by accepting the deliverable of this phase |
| B-2 | `design-systems/.remember` has unresolved provenance and sensitivity. | Must not be read, hashed, moved, or classified | Requires separate review |
| B-6 | The content of the live local `.agents-hub` is unknown. GitHub `agents-hub-one` is a placeholder skeleton: 7 of its 16 files are 0-byte. | The proposed target tree cannot be accepted as canonical, because the consolidation inputs are not fully known. | Local agent runs `scripts/Invoke-HubInventory.ps1` and commits the evidence |

### Required before Gateway runtime integration and completion — not binding this phase

| # | Blocker | Effect | Owner |
|---|---|---|---|
| B-3 | Codex authority file contains stale absolute paths and overlaps Hub-owned responsibilities. Recorded as an active conflict in `workspace-governor-agents-hub-one/STATE.md`, which halts Codex adapter activation. | Gateway directive sections 34 and 43 require Codex to connect, so the Gateway cannot reach DONE until this is reconciled. Does not block Hub consolidation. | Requires user authorization to open as a separate scoped change (`DECISIONS.md` D-11) |
| B-4 | Final canonical `.agents-hub` does not exist. Two source repositories both claim the identity. | Blocks Gateway directive section 29 rule-folding and final environment discovery | Resolved by Hub consolidation |
| B-5 | Live Windows environment is unreachable from a cloud session. | Gateway directive section 5 items covering local MCP, Claude Code, Codex, secrets and audit mechanisms cannot be collected remotely | Local agent executes discovery |

## Verification assignments

Verification that cannot be performed in the current environment is recorded here
with its assigned executor, rather than repeated as an open caveat. An assigned
pending verification is not a defect and is not re-flagged each session; see
`AGENTS.md` § Evidence standard.

### PowerShell runtime verification

| Field | Value |
|---|---|
| Status | PENDING |
| Assigned environment | Local Windows |
| Assigned executor | Klo / local Windows agent |
| Cloud Claude responsibility | Static review and preparation only |
| Cloud blocker | No |
| Current phase blocker | Yes, only when the live-Hub inventory result is required to continue consolidation |
| Recheck trigger | Local execution evidence is committed to `workspace-governor` |

Scope: `scripts/Invoke-HubInventory.ps1`, `scripts/Assert-RememberPruning.ps1`,
`scripts/Invoke-GatewayDiscovery.ps1`, `scripts/Assert-DiscoveryReadOnly.ps1`,
`scripts/lib/SafeTraversal.ps1`.

Completed in cloud: delimiter validation on all five files; static invariants A1
to A7; source-level review across five rounds. No script has been executed.

Still required: the Windows runtime test. It is not waived. Live-Hub evidence
cannot be accepted until `Assert-RememberPruning.ps1` returns `PASS` and
`Invoke-HubInventory.ps1` reports `Completeness: COMPLETE` on the local machine.

## Open work

1. Inventory the live local Hub against the committed GitHub baseline, then revise the preliminary target tree against that evidence.
2. ~~Revise the Gateway discovery tooling so it does not presuppose `.agents-hub` exists.~~ **Closed** — semantics verified across the full report, and the `00_hubState` ordering defect fixed. Still unexecuted; awaits the local Windows runtime test recorded under Verification assignments.
3. Execute the accepted classification once the target tree is accepted. Assessment and classification are complete; `change`, `reference-update` and `verify` remain. See `evidence/HUB-RECONCILIATION-ASSESSMENT-2026-08-19.md`.
4. Persist the user SSOT. `USERSSOT.json` was supplied in session as an authoritative user-side responsibilities file and exists in no repository. Its placement is undecided.
5. Open B-3 as a separate scoped change once authorized.
6. Determine placement of the three agent rulings recorded in `DECISIONS.md` under D-07 through D-09.
7. Trim the duplicated live-state narrative in `workspace-governor-agents-hub-one/research/` per D-15. Edits another repository; sequenced separately.
8. ~~Correct the case-insensitive variable collisions found in four scripts, two of them live defects in the assigned local commands.~~ **Closed** — fixed, and a static gate added to prevent the class. See `evidence/SCRIPT-STRUCTURE-DEFECTS-2026-08-20.md`.

## Next action

Run the local Hub inventory on the Windows machine and commit the evidence files
it emits. This is the only remaining input needed to make the target tree
acceptable.

**Do not run any script copied earlier.** The corrected versions are commit
`3a9d964` on branch `claude/add-github-repos-projects-6r1jgy`, pending merge to
`main`. Pull that commit before running. The versions at `068dfa4` and before
carried case-insensitive variable collisions;
`Assert-RememberPruning.ps1` would have failed before writing its verdict, and
`Invoke-HubInventory.ps1` would have dropped its unverified list whenever the
inventory came back INCOMPLETE. Both are fixed. See
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
- Do not hand any script under `scripts/` to the local operator until
  `python3 scripts/Assert-ScriptStructure.py --selftest` and the same tool run
  over `scripts/*.ps1 scripts/lib/*.ps1` both pass. This gate is static only; it
  does not satisfy the PowerShell runtime verification recorded above.

Reinspect live sources before acting. This record is continuity evidence, not proof that anything remains unchanged.
