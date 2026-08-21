# Workspace Governor State

**Updated:** 2026-08-21
**Phase:** Hub consolidation — the plan's Steps 1, 2, 5, 7 and 8 are applied and
verified; Step 4 is satisfied by substitution. **Step 3's map exists and its gate is not
met.** Steps 2 and 3 were prerequisites for work already completed — see `DECISIONS.md`
D-73 for the label correction and the ordering cost. Step 2 closed 2026-08-21; an earlier
revision of this line still called it not done after the position table recorded it
closed.
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
incomplete where known gaps remain -- gaps are listed under Blockers below and in
the issue register. `README.md` owns the full relationship table. `DECISIONS.md` D-24
records the decision.

### Canonical Hub -- current verified state

`klodebeers/.agents-hub` at **`c8444cb`**, Step 1 restructuring applied and Step 2
first artifacts added, then corrected after four independent blind audits. Verified against the tree extracted from `origin/main`, not
only the working copy: both checks pass there. Fifteen tracked files:

```text
AGENTS.md                                     root bootstrap, router, precedence
CATALOG.md                                    inventory
README.md                                     navigation; bootstrap step 4 enters agent work
rules/ENGINEER-OWNERSHIP.md                   ownership, intake, decision resolution
rules/AUTONOMY-AND-PROTECTED-BOUNDARIES.md    autonomy, approval, boundaries
rules/CONTEXT-AND-ORCHESTRATION.md            context, delegation, continuity
rules/VERIFICATION-AND-EVIDENCE.md            done, testing, audit, evidence
registry/agent-registry.json                  12 agent identities, 1 with a definition
registry/agent-registry.schema.json           validates the registry; no runtime enforcement
orchestration/routing.json                    entry point, domain selection, 11 routes
agents/notion-formula-logic.json              first normalized agent definition
context/NOTION-FORMULA-V2.md                  Notion formulas 2.0 capability knowledge
templates/verification-checklist.json         pre-action checklist shape
references/AGENTS-MD-LIVE-AUDIT-2026-08-16.md retained dated audit
design-systems/placeholder.md                 EXCLUDED, Conflict, untouched
```

Not created, by decision: `policies/`, `prompts/`, `skills/`, `tools/`,
`runbooks/`, `adapters/` (renamed from `runtime-adapters/` by D-68), and every
unused branch of `context/`. There is no `global/` folder: the Hub is the global
layer (D-69). Each is created by its first accepted artifact.
Detail in `DECISIONS.md` D-37 and D-43 through D-53.

**Step 2 was reviewed twice, before and after commit.** The pre-commit round fixed
twenty findings. A second round then put four blind reviewers on the committed
state -- registry and schema, orchestration and routing, the agent/context/template
transformations, and scope compliance plus the verification tooling -- each given
the source, the approved scope and the result, and none given the implementer's
rationale. Their material findings were verified against source and fixed at
`df33f07`; three were rejected with reasons recorded in `DECISIONS.md` D-55.
Settled outcomes: D-54 through D-61. Detail:
`evidence/HUB-STEP-2-FIRST-ARTIFACTS-2026-08-21.md` revision 3.

The most serious finding was lost governance, not structure: consolidating the
formula material dropped three source obligations and softened their modality. The
obligations are recorded as owed in the issue register rather than left absorbed --
issue #22. D-61.

A **fifth blind audit** then ran on the corrected state and returned eight findings
that had to be resolved before the step could be declared complete: a fourth
softened obligation the earlier sweep missed, an unrecorded pre-routing obligation,
an unassigned deliverables duplication, remaining backoffice narrative in live
artifacts, this file's own stale header, three false-pass defects in the fidelity
script, a README claim the registry contradicts, and a missing disposition in the
remaining-migration ledger. All are closed at `1a91d32` and in these records.
D-62 through D-64.

**Step 2 authorisation.** The stop condition below requires approval before applying
canonical restructuring or modifying live Hub governance. It was given by the user on
2026-08-21 ("proceed with Step 2"), and again for the correction round ("fix
confirmed defects within the approved Step-2 boundary"). Recorded here because a
blind reviewer correctly found the stop condition standing with nothing beside it
recording that the gate had been opened.

Three verification scripts hold the Step 2 claims, all re-runnable and each proven
against injected defects: `scripts/Test-HubRegistrySchema.py` (32 assertions),
`scripts/Assert-HubSourceFidelity.py` (21 assertions, the only one that reads the
source package), `scripts/Assert-ReferenceIntegrity.py` (58 tokens, plus URI
semantics and catalog coverage). The audits demonstrated blind spots and false
passes in all three; all are closed, and the eleven defect trees they built are
retained as regression cases. The reference check
refuses to run outside the Hub, where it produced 1022 false positives.

**The local folder is kept up to date by routine.** The operator pulls in GitHub
Desktop, so it tracks the repository without a per-commit handoff (D-70, D-71, D-72). It was last
independently verified equal at `1a91d32` -- a fast-forward from `c6c966b` whose
diffstat matched the repository exactly, which also proves the clone carried no
divergent local commits. D-41's no-drift principle stands; only the reporting
changed.

### Conflict C-05 -- closed 2026-08-21

Two blind reviewers independently found that the flat `agents/` and the
domain-tagged registry contradict D-14, which required a subdivided `agents/` and a
domain-keyed registry, and D-12's owner-local template placement. Neither was marked
superseded. Closed by `DECISIONS.md` D-57: the accepted taxonomy governs, D-14's
diagnosis of the source asymmetry stands, and its prescribed structure does not.

### Conflict C-04 -- closed 2026-08-21

Resolved by the taxonomy owner with a single agent-agnostic definition, which
replaces both conflicting records. The earlier gloss "scoped operating context, not
knowledge or authorization" is superseded; the Step-1 target tree's assignment of
domain knowledge to `context/` stands.

`context/` owns scoped knowledge and supporting operating context -- domain
concepts, architecture, terminology, rationale, constraints, reference material, and
detail that would bloat the root instruction files. It owns no governance,
permissions, approvals, protected boundaries, behavioral obligations, verification
authority or instruction precedence. A file is not mandatory because it sits there;
it is loaded only when routed by the bootstrap, the orchestration layer, an agent
definition, or a runtime adapter.

`context/NOTION-FORMULA-V2.md` is confirmed correctly placed: it carries supporting
Notion domain knowledge, absorbs no governance obligation, and grants no authority.

Full definition, with the scope, runtime and backoffice separations:
`plans/AGENT-HUB-CONSOLIDATION.md` section 6.2a. `DECISIONS.md` D-66. The
capability-versus-implementation rule that now shapes context substructure is
section 6.2b and D-67.

### Step 1 gate -- satisfied

Both required results are in, from the operator's machine, committed at `12f93e6`:

| Script | Required | Returned |
|---|---|---|
| `Assert-RememberPruning.ps1` | `Proof verdict: PASS` | **PASS**, fail-closed. A1-A7 PASS. 12 directories visited, 1 safety-pruned, 0 violations |
| `Invoke-HubInventory.ps1` | `Completeness: COMPLETE` | **COMPLETE**. 9 live files, 0 only-in-live, 0 content differs |

Step 1 is therefore complete: the target tree and item classification are in
`evidence/HUB-TARGET-TREE-AND-CLASSIFICATION-2026-08-21.md`. **Applying it needs
approval** per `plans/AGENT-HUB-CONSOLIDATION.md` § 6.7.

**Intake exists.** `_intake-hub/` is the single door for change requests to
`.agents-hub`, created 2026-08-21 (`DECISIONS.md` D-81). It holds requests and their
dispositions, and no authority. Empty of submissions today; its `README.md` and
`SUBMISSION-TEMPLATE.md` are the whole folder.

## Position in the plan sequence

`plans/AGENT-HUB-CONSOLIDATION.md` section 3a owns the sequence and what each step
requires. This table owns where the work stands. It is here, not in the plan, because
position is current state; two copies would drift.

| Plan step | State | Notes |
|---|---|---|
| 0 -- bootstrap and drift check | Done informally | No dated drift-check record produced. Low consequence: the baseline was re-inspected repeatedly in practice |
| 1 -- accept target tree and classify | **Done** | D-35. All 46 inputs classified |
| 2 -- provenance, sensitivity, external-source gates | **Done 2026-08-21** | Gate PASS. `agents-hub-two` cleared with evidence; `.remember` explicitly blocked and excluded with nothing depending on it, verified by search; predecessor backoffice cleared with no Hub exposure; `agent-governance-toolkit` outside the set. `evidence/PROVENANCE-AND-SENSITIVITY-GATES-2026-08-21.md` |
| 3 -- semantic owner and dependency map | **Map produced; gate NOT met** | 64 issues, 31 contested, 25 dispositions settled, 6 blocked. `evidence/AGENT-HUB-SEMANTIC-OWNERSHIP-MAP-2026-08-21.md`; D-77. **U-1 is a reserved user decision and gates about a third of the dispositions** |
| 4 -- version preservation and rollback | **Satisfied by substitution** | Git is the mechanism, D-28 |
| 5 -- refactor runtime-neutral core and root controls | **Done** | The root `AGENTS.md` move, retiring the Hub `STATE.md` and the placeholders, and the later `AGENTS.md` edits. Recorded at the time under the labels "Step 1" and "Step 2" |
| 6 -- consolidate references and evidence | Partly done, partly deferred | D-15 settled the disposition; execution edits another repository |
| 7 -- refactor structural domains, accept reusable artifacts | **Done** | `registry/`, `orchestration/`, `agents/`, `context/`, `templates/` with their first artifacts. Recorded at the time as "Step 2" |
| 8 -- migrate accepted external source | **Done** | The `agents-hub-two` content in those artifacts. Also recorded as "Step 2" |
| 9 -- thin runtime adapters | Not started | `adapters/` per D-68. Requires Step 3 |
| 10 -- routes, registries, references, atomically | Partly done | The `CATALOG.md` and `README.md` updates that accompanied Step 7 |
| 11 -- fresh-agent bootstrap and runtime-activation verification | Assigned, not executed | The one open verification assignment |
| 12 -- final audit and completion declaration | Not started | Not before Step 3 |

**The label collision, for anyone reading older records.** "Step 2" was used in this
project to mean *create each new domain with its first accepted artifact*, which is the
plan's Step 7 and Step 8. The plan's own Step 2 was never done. The executed work is
verified and stands; the labels were wrong. `DECISIONS.md` D-73.

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

### Keeping the local Hub folder up to date -- ROUTINE

| Field | Value |
|---|---|
| Status | **ROUTINE.** There are two copies of the Hub: the GitHub repository, and the folder `C:\Users\Chloe\.agents-hub` on the operator's PC. Only the repository can be changed from a cloud session; the folder catches up when the operator pulls in GitHub Desktop, which they do as a matter of course. So it is not reported or requested per commit (D-70, D-71, plainly restated in D-72). D-41's no-drift principle is unchanged; what changed is that it is carried by routine rather than by a reminder. Last independently verified equal at `1a91d32`: a fast-forward from `c6c966b` whose diffstat matched the repository exactly |
| Requirement | D-33: the repository and `C:\Users\Chloe\.agents-hub` are one logical Hub and must not drift |
| Why no remote action can do it | The path is on the operator's Windows machine, unreachable from a cloud session (blocker B-5). No cloud-side change can move it |
| Assigned executor | Klo, on the local Windows machine |
| Method | The operator pulls in **GitHub Desktop**. Mechanism settled as git, not hand-copying, per D-41; a desktop client is git, so nothing about D-41 changes. Do not hand back terminal commands for this |
| Verification | `git rev-parse HEAD` must return `c8444cb`, and `git status --short` print nothing. **Corrected 2026-08-21:** this row required `3e35f9d` while the Hub had advanced two commits past it, so an operator following it against a correctly synced clone would have reported drift that did not exist. Found by the migration audit. Previous round, done: the reported HEAD was `1a91d32846fe298f1d18cdffe4219129b2f0f5f0`, an exact match. The operator's `git pull` transcript shows a **fast-forward** `c6c966b..1a91d32`, which is stronger evidence than the SHA alone: a fast-forward is only possible if the local clone carried no divergent commits, so nothing had been committed locally and lost. Its diffstat -- 9 files, 583 insertions, 3 deletions, 6 created -- matches `git diff --stat c6c966b..1a91d32` in the repository exactly. The `git status` half was not reported; a dirty tree there would be local drift rather than a materialization failure, and would show up as a mismatch at the next pull. Tree afterwards, this round: no file added or removed. `AGENTS.md`, `CATALOG.md`, `README.md`, `agents/notion-formula-logic.json` and `context/NOTION-FORMULA-V2.md` are modified; `context/NOTION-FORMULA-V2.md` stays at that path. `design-systems/` unchanged |
| Known wrinkle | The local clone's `origin` may still carry the pre-rename URL `.../agents-hub-one`. It resolves through GitHub's redirect, so `git pull` works; `git remote set-url origin https://github.com/klodebeers/.agents-hub` re-points it when convenient. A repository rename never renames a clone or rewrites its remote |
| Recheck trigger | Raise it only when a specific task needs the folder to be current -- the fresh-session bootstrap test is the clear case, since a new agent reads these files off that disk and an old copy would give a wrong answer -- or when something shows the two have actually diverged |

### Enforcement carriers -- two assignments, both on the operator's machine

**What is proven here.** `.claude/hooks/` and `.githooks/` hold the carriers and a
115-case suite. The content gates are exercised through **real `git commit` calls** in
throwaway repositories, so each case proves the gate as git actually invokes it --
including the eight invocation forms that defeated the first version of these gates the
same day (`evidence/HOOK-GATES-AUDIT-2026-08-21.md`). `--mutations` additionally breaks
each gate on purpose and requires the suite to notice -- 24 mutations, 22 caught, two
no-op controls correctly not flagged. This exists because the first harness reported 31 of
31 passing while ten deliberate breakages survived it undetected.

**Assignment 1: do the two `.claude/` hooks fire in a live session?**
*Executor:* the local operator, in a fresh session opened in this repository.
*Method:* submit any prompt and confirm the position block appears; then attempt a
commit that rewrites a line of `DECISIONS.md` and confirm it is refused.
*Recheck trigger:* any change to `.claude/settings.json`, and any Claude Code version
change touching hook configuration.
**Correction 2026-08-21:** the earlier version of this assignment said the reason it
could not be verified here was that "hook registration is read at session start". That
reason was wrong -- the hooks reference says direct edits to settings files are normally
picked up by a file watcher. The boundary stands, its stated reason did not, and it was
the reason the verification was deferred rather than attempted.

**Assignment 2: is a Python interpreter reachable from Git's shell on Windows?**
*Executor:* the local operator.
*Method:* in the repository, run `git config core.hooksPath .githooks`, then attempt a
commit that rewrites a `DECISIONS.md` entry line. A refusal naming the append-only rule
proves the interpreter search works; a refusal naming "no Python interpreter found"
means the gates are failing closed and Python needs to be on PATH.
*Why it is assigned rather than assumed:* every `scripts/` record shows that machine
running Windows PowerShell 5.1, and `python3` is frequently not the name on PATH under
Git for Windows. The shims try `python3`, `python`, then `py -3` and refuse the commit
if none is found, so the failure direction is safe -- but whether the gates run at all
there is unknown until this is done.

### Fresh-agent bootstrap and runtime activation

| Field | Value |
|---|---|
| Status | PENDING, **unassigned until now** |
| Requirement | v0.4.2 Step 11, completion criterion 18, and predecessor learning L-001 all require fresh-agent bootstrap and per-runtime activation evidence |
| Why no script can do it | Activation is a property of a new session, not of the filesystem. `Collect-LocalEvidence.ps1` collects configuration presence, which is explicitly **not** evidence of discovery, loading or enforcement |
| Assigned executor | Klo, in a fresh session of each runtime |
| Method | Start a new Claude Code session and a new Codex session in a governed directory. In each, ask the agent to state which instruction files it loaded and from where, without being told the answer. Record the reply verbatim |
| Verification | The reply names the canonical Hub route. Silence, a guess, or a different file is a negative result and must be recorded as such. **Run it where work actually happens, not inside `.agents-hub`** -- nobody opens a session there, so a test run there would answer a question no one asks. The real question is whether a fresh session, started where the operator and the agent actually work, reaches the Hub's contract at all. Note when interpreting the result: Claude Code reads only `CLAUDE.md`, never `AGENTS.md`, so its answer depends on the local wiring (issue #9); Codex reads `AGENTS.md` natively. `evidence/RUNTIME-CONVENTIONS-2026-08-20.md` addendum |
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

**Moved out of this file 2026-08-21.** Open items live in the issue register:
`github.com/klodebeers/workspace-governor/issues`, one issue per item, each carrying
its dependencies and the condition under which it closes. This file holds no copy of
that list -- `AGENTS.md` § Issue register and § File ownership.

Thirty-five issues were filed, covering every open item that stood in this section plus
eleven that had no register at all. The item-by-item mapping, the merges, and what the
migration does **not** verify are in
`evidence/OPEN-WORK-MIGRATION-2026-08-21.md`. The prior list, including the closed
items struck through in it, is in git at `b39a097`; nothing was deleted to make the
mapping true.

**Reserved for the user:** issue #1 (is `AGENT-SSOT.json` a governance owner or an
asset) and issue #8 item 2 (approval to modify live Hub governance) -- these two gate
other work. Issue #21 (where exact domain implementation lives per owner) and issue #35
(the Workspace Orchestrator material) are also the user's to answer but **gate nothing
today**; an earlier revision of this line said they gated other work, which contradicted
both issues' own bodies.

## Next action

**Propose the edit set that applies Step 3's settled dispositions.** It is the one
thing on the critical path that needs no decision from the user first: list exactly which
files change and which recorded disposition each edit executes, excluding everything
issue #1 blocks. The gate is written per edit set -- "no **included** governed issue or
artifact has two active owners" -- so a set that excludes the blocked cluster satisfies
the prerequisite. Issue #8 holds the assessment.

**This work has no clean step number, and that is a defect in the plan, not a fact about
the work.** The position table above records Steps 5, 7 and 8 as **Done**, while plan
§ 10 is titled "What Step 5 needs before it starts" -- so the plan asserts both. Those
steps are done *for their first pass*; applying Step 3's dispositions is a second
refactoring pass the plan does not model. Naming it "Step 5" would take a completion gate
that has already been passed and reuse it, which is the exact failure D-73 records. The
work is therefore named by what it does. The plan defect is filed rather than resolved
here, because the plan owns its own sequence.

Then, in order: **approval** to modify live Hub governance for that set (user, issue
#8), and a **blind pre-edit review** of it before any edit lands (D-60 -- reviewers
get source, approved scope and result, and are denied the implementer's rationale).

**What is waiting on the user, and what each unblocks:**

- **Issue #1, U-1.** Enlarges the Step 5 edit set to include the `AGENT-SSOT.json`
  cluster, and settles issue #17's ownership question. It does **not** block Step 5.
- **Issue #8, approval.** The actual gate on Step 5. Nothing in the plan's refactoring
  phase proceeds without it.
- **Issue #21.** Where exact domain implementation lives per owner. Nothing is blocked
  by it today -- no domain implementation content is in the Hub.
- **Issue #35.** The Workspace Orchestrator material. **Its only basis is a statement
  made in session, and nothing in this repository records it** -- every one of the
  eleven repository mentions of Workspace Orchestrator describes a future project
  explicitly out of scope. Treated as unverified, per the rule against relying on
  conversation history. If material does arrive it comes from outside the classified
  input set and needs classifying rather than slotting in.

**Ready and not blocked by any of the above:** issue #12, the fresh-agent bootstrap
test -- the one open verification assignment, needing the local machine.

**Not to be started before Step 3 has an accepted owner map:** the plan's Step 9
(adapters) and Step 12 (final audit).

## Stop conditions

- Do not read, hash, move, or classify `design-systems/.remember` before its provenance and sensitivity review.
- Do not activate a Codex adapter while B-3 is unresolved.
- Do not fold existing Hub rules before the target tree and ownership map are accepted.
- Do not reopen the 46-section directive structure (`DECISIONS.md` D-04).
- Do not run the discovery tooling in `scripts/` until it is revised **and** Hub consolidation is complete (`DECISIONS.md` D-05, D-06). The revision is done -- semantics verified across the full report and the `00_hubState` ordering defect fixed -- so what remains binding is the consolidation half and the unexecuted local Windows runtime test under Verification assignments. Until 2026-08-21 this condition cited "open work item 2", which the issue-register migration made unlocatable.
- Do not adopt `agent-governance-toolkit` without provenance, licence, and generated-output review.
- Do not adopt the third-party **rules scaffolder** without provenance, licence and generated-output review. Its generator-owned block is overwritten on rerun and must never own Hub governance. This is a **different artifact** from the `agent-governance-toolkit` fork; both stop conditions apply independently.
- Do not migrate before refactoring passes source-preserving verification. Carried from the predecessor; it survived only implicitly inside the step ordering.
- Do not delete any predecessor or legacy material before reinspecting each proposed target for unique unrelated content and required recovery evidence. Carried from `evidence/LEGACY-GOVERNANCE-MATERIAL-CONSOLIDATION-2026-08-17.md`, where roughly 20 files are marked discard-as-active-governance and **none has been deleted**.
- Do not commit a `.ps1` under `scripts/` containing any byte above 0x7F. Windows PowerShell 5.1 reads non-BOM sources as ANSI, and U+2014 becomes a string delimiter.
- Do not apply canonical restructuring, or modify live Hub governance, runtime configuration, code, manifests or lockfiles, without approval. The current task is reconciliation, not implementation (`plans/AGENT-HUB-CONSOLIDATION.md` § 6.7).
- Do not create a Technical Translation rule file or carry `rules/VERIFICATION-RESOLUTION.md` into the Hub. Both concerns already have owners (`plans/AGENT-HUB-CONSOLIDATION.md` § 6.4).
- Do not treat `AGENT-SSOT.json` or the scoped user-context SSOTs in this repository as live governing authorities. They are Agent Hub assets; the copies here are backoffice staging and provenance. Under D-80 no scoped SSOT is a general governance owner. The Hub root `AGENTS.md` is the bootstrap and routing authority. Do not restate their content here either.
- Do not choose a verification method before reading `rules/VERIFICATION-RESOLUTION.md`. It is binding, and it bounds the method, the stopping condition, and when new tooling is justified.
- Do not hand any script under `scripts/` to the local operator until
  `python3 scripts/Assert-ScriptStructure.py --selftest` and the same tool run
  over `scripts/*.ps1 scripts/lib/*.ps1` both pass. This gate is static only; it
  does not satisfy the PowerShell runtime verification recorded above.

Reinspect live sources before acting. This record is continuity evidence, not proof that anything remains unchanged.
x
