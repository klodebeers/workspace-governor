# Evidence -- predecessor audit specs vs. current discovery tooling

**Date:** 2026-08-20
**Decision this supports:** whether the predecessor `tasks/` audit specs can be
retired as covered, or contain coverage the current tooling lacks.
**Sources:** `workspace-governor-agents-hub-one` @ `24798d0` --
`tasks/01-WINDOWS-ENVIRONMENT-PATH-AUDIT.md` (478 lines),
`tasks/02-SHARED-CONFIGURATION-AUDIT.md` (604),
`tasks/03-CODING-AGENT-BASELINE-INTEGRATION.md` (1016); and
`workspace-governor` `scripts/Invoke-GatewayDiscovery.ps1`,
`scripts/Invoke-HubInventory.ps1`.
**Method:** requirement-by-requirement read of both sides. Field-level comparison
against the actual code, not against section titles.
**Status:** Verified by source inspection. No script changed. Neither repository
modified.

## Headline

The specs and the tooling are **different instruments**, not competing versions of
one. The specs are session prompts for a *local agent with change authority*
across four activities: inventory, classification, remediation, and bootstrap
verification. The tooling is *read-only cloud-authored evidence collection*.

The tooling covers most of the **inventory** activity and almost none of the other
three. That is by design, not a defect -- but three of the four gaps below are
real inventory gaps the tooling should close, and one spec activity now conflicts
with current governance.

## Coverage matrix

| Spec requirement | Tooling | Status |
|---|---|---|
| 01 P1: per-tool name, present, executable path, version | `Get-CommandFact` | **Covered** |
| 01 P1: installation method | -- | **Not covered** |
| 01 P1: installation directory, distinct from executable path | -- | **Not covered** (only `source`) |
| 01 P1: whether multiple versions/installations exist | -- | **Not covered.** See Gap 2 |
| 01 P1: "do not rely on only one discovery method when results conflict" | `Get-Command` only | **Not satisfied.** See Gap 2 |
| 01 P1: runtimes to probe | node, npm, npx, pnpm, yarn, python, pip, git, docker, uv, PowerShell, Claude Code CLI, Codex CLI | **Partial.** See Gap 1 |
| 01 P2: effective PATH inherited by the shell | `$env:PATH` split, per entry | **Covered** |
| 01 P2: User PATH; System PATH; User/System conflicts | -- | **Not covered.** See Gap 3 |
| 01 P2: entries pointing to nonexistent locations | `exists` per entry | **Covered** |
| 01 P2: duplicate entries | -- | **Not covered.** See Gap 4 |
| 01 P2: executable shadowing / precedence problems | -- | **Not covered.** Depends on Gap 2 |
| 01 P2: per-issue risk and recommended action | -- | Out of scope -- analysis, not collection |
| 01 P3: safe corrections to PATH | -- | **Out of scope and now blocked.** See Conflict below |
| 01 P4 / 03 Part E: fresh-session bootstrap verification | -- | **Cannot be covered by any script.** Matches predecessor L-001 and blocker B-5 |
| 02 P1: config roots per runtime, file, purpose | Sections 2, 3, 4 | **Covered** |
| 02 P1: scope -- global/user/machine/repository/project | -- | **Not covered** |
| 02 P1: loading mechanism; precedence | -- | **Not covered.** Requires vendor documentation, not filesystem facts |
| 02 P1: "do not assume a file is active merely because it exists" | Presence only | **Not satisfied.** The tooling records presence and says so; activity is undetermined |
| 02 P2: classify A-G (shareable / with-adapter / runtime-specific / machine-specific / project-specific / secret / obsolete) | -- | Out of scope -- classification, not collection |
| 02 P3: semantic duplication by intent | Section 11, identical **content** groups by hash | **Partial and materially narrower.** Byte-identical only. Two files stating one rule in different words are invisible to it |
| 02 P4-P5: shared-asset architecture; runtime differences | -- | Out of scope. Owned by `plans/AGENT-HUB-CONSOLIDATION.md` |
| 03 Part A: dependency presence and version | Section 6 | **Covered** |
| 03 Part A: requirement level (required / recommended / optional) and machine status classification | -- | Out of scope -- classification |
| 03 Part A: verify current vendor requirements against official docs | -- | **Not covered.** Requires documentation research |
| 03 Part B: remediate baseline gaps -- installs | -- | **Out of scope and now blocked** |
| 03 Part C: finalize `.agents-hub` | -- | **Superseded.** Owned by `plans/AGENT-HUB-CONSOLIDATION.md` |
| 03 Part D: clean consolidation, incl. deletion | -- | **Superseded and blocked** |
| 03 Part F: final self-audit; baseline declaration | -- | Out of scope |
| Secrets: names and locations only, never values | Section 9, `Protect-Value` redaction | **Covered, and stronger than the spec requires** |

## Four inventory gaps worth closing

These are cheap, additive, and stay read-only. Each names a real detection the
tooling cannot currently make.

1. **Missing runtime probes.** The spec lists GitHub CLI, WSL, Windows Terminal
   and search/file utilities; the tooling probes none of them. `gh` matters most:
   spec 03 treats repository tooling and its authentication prerequisites as a
   baseline category, and the Gateway directive assumes repository access.
2. **Single-method resolution.** `Get-CommandFact` calls `Get-Command` and stops.
   The spec explicitly requires more than one method where results conflict, and
   requires detecting multiple installations. Adding `where.exe <name>` and
   recording every hit would satisfy both, and is the prerequisite for any
   shadowing finding -- the failure mode where an old executable wins on PATH.
3. **Effective PATH only.** Section 5 reads `$env:PATH`, which is the merged
   process view. User and System PATH are not read separately, so a User/System
   conflict cannot be seen and a proposed fix cannot say which scope to change.
   `[Environment]::GetEnvironmentVariable('Path','User')` and `'Machine'` are both
   read-only.
4. **No duplicate-entry detection.** Entries are listed with an `exists` flag but
   never compared to each other, so duplicates and near-duplicates go unreported.

Gaps 1-4 are recorded as scoped follow-up, **not applied now**: the plan's process
gate limits current work to reconciliation, and Gateway discovery is under a stop
condition until consolidation completes, so there is no operational pressure to
change that script mid-reconciliation.

## Superseded for execution -- classification, not an open question

**Resolved 2026-08-20.** No new decision was required. The Agent Hub Consolidation
directive already supersedes any older instruction authorizing remediation,
installation, deletion, restructuring or machine changes during this
reconciliation phase. Raising it as a user decision was an error: the governing
directive had already answered it.

Classification applied:

| Spec portion | Class |
|---|---|
| `01` Phase 3 -- safe corrections to PATH | **Superseded for execution. Provenance-only.** |
| `03` Part B -- remediate baseline gaps, installs | **Superseded for execution. Provenance-only.** |
| `03` Part C -- finalize `.agents-hub` | **Superseded for execution.** Concern now owned by `plans/AGENT-HUB-CONSOLIDATION.md`. |
| `03` Part D -- clean consolidation, incl. deletion | **Superseded for execution. Provenance-only.** |

Preserved historically in `workspace-governor-agents-hub-one`, which is unmodified.
Not executed, and not to be handed to a local agent as live instructions. The
inventory, configuration-analysis, dependency, semantic-duplication and
fresh-session verification requirements in the same specs remain valid and are
carried forward.

## The superseded portions, in detail

Spec 01 Phase 3 and spec 03 Parts B, C and D **authorize machine changes** --
PATH edits, dependency installation, finalizing the Hub, and consolidation
including deletion. Read as live instructions today they contradict:

- `STATE.md` stop conditions and the approval gate in
  `plans/AGENT-HUB-CONSOLIDATION.md` § 6.7 -- reconciliation, not implementation;
- the read-only constraint on all tooling in this repository;
- `DECISIONS.md` D-05 and D-06 -- consolidation sequencing.

They were written when this backoffice expected to execute a remediation session.
They must not be handed to a local agent as-is.

## Classification of the three specs

| Spec | Class | Disposition |
|---|---|---|
| `01-WINDOWS-ENVIRONMENT-PATH-AUDIT.md` | **Reusable with adaptation** | Phases 1-2 become the coverage checklist for Gaps 1-4. Phase 3 is retired as an instruction and retained as provenance. |
| `02-SHARED-CONFIGURATION-AUDIT.md` | **Reusable with adaptation** | Phase 1's scope/loading/precedence fields and Phase 3's intent-based duplication test are genuine additions the tooling cannot supply. They belong to Step 1 and Step 3 analysis in the consolidation plan, performed by an agent, not a script. Its A-G classification maps onto the four placement layers already in use. |
| `03-CODING-AGENT-BASELINE-INTEGRATION.md` | **Partly reusable, largely superseded** | Part A's dependency categories and requirement-level classification are reusable. Part E's fresh-session bootstrap checks are reusable and remain unautomatable. Parts B, C and D are superseded by `plans/AGENT-HUB-CONSOLIDATION.md` and blocked by the approval gate. |

## What this changes

Nothing is retired. The specs are not redundant with the tooling: they cover
classification, vendor verification and fresh-session activation that no script
here performs, and they identify four inventory detections the tooling is missing.

The `plans/` route already records the adaptation of these prompts into discovery
coverage checklists as open work; this document supplies the item-level detail
that item needed.

## Not verified

Neither the tooling nor the specs have been run against the live Windows machine.
Every "covered" row above states what the code collects, not that the collection
has been performed there. Windows PowerShell 5.1 remains unverified.
