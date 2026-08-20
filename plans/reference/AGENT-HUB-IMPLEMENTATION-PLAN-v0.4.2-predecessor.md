> **PROVENANCE COPY -- NOT AN ACTIVE DIRECTIVE.**
>
> Verbatim copy of `AGENT-HUB-IMPLEMENTATION-PLAN.md` v0.4.2 from
> `klodebeers/workspace-governor-agents-hub-one` at commit `24798d0`, the
> predecessor backoffice for the same Hub. Retained here so the carried-forward
> step sequence is available without depending on another repository.
>
> It is **not** live governance and **not** the active plan. The active plan is
> `plans/AGENT-HUB-CONSOLIDATION.md`, which carries this forward and records what
> changed. Paths, dates and status lines below are as written on 2026-08-17 and
> are not current. Do not execute from this file.

# Canonical Agent Hub Implementation Plan

**Plan owner:** `C:\KloWorkspaces\workspace-governor`  
**Implementation target:** `C:\Users\Chloe\.agents-hub`  
**Version:** 0.4.2  
**Status:** Execution-ready plan; implementation not started  
**Baseline date:** 2026-08-17  
**Authority:** Applicable live governance files remain authoritative; this plan sequences work and does not create governance

## 1. Purpose and execution boundary

This plan defines the controlled work required to finish the canonical Agent Hub as a lean, runtime-neutral source system for **Coding Agent Rules** and reusable agentic-system assets. Its shared contract governs autonomous coding agents that architect, execute, review, test, document, or orchestrate coding and agentic-system work. It does not generalize rejected Work-Agent role systems, mandatory team topologies, or project-management behavior into Coding Agent Rules.

This file is not permission to execute the work. During this planning change:

- do not edit, move, retire, activate, or migrate any Agent Hub item;
- do not change runtime-native instruction or configuration files;
- do not recreate `C:\KloWorkspaces\test4`, create another intake file, or plan implementation of the project-intake baseline;
- do not build the future dashboard-driven Workspace Orchestrator;
- do not infer runtime activation from source placement.

When execution is authorized, every step below is subject to the live authority and stop conditions then in force. A conflict stops only the affected work unless continuing elsewhere would conceal, worsen, or depend on it.

## 2. Authority and boundary map

| Layer | Owns | Does not own |
| --- | --- | --- |
| Workspace Governor | Hub architecture, placement, classification, change lifecycle, documentation construction, project state, research, and evidence | Canonical Global Governance, runtime-native settings, project requirements, or Workspace Orchestrator behavior |
| Canonical Agent Hub | Reusable cross-project authored source and the Global Governance contract | Runtime state, credentials, caches, sessions, logs, operational projects, or automatic activation |
| Runtime-native adapters and configuration | Discovery/loading, permissions, hooks, registrations, and runtime-specific enforcement | Shared-rule authorship or a competing governance contract |
| Individual projects | Project requirements, local specialization, implementation, tests, and continuity | Global reusable source merely because a project consumes it |
| Future Workspace Orchestrator | Dashboard-driven project management and agent coordination, if separately designed and authorized | The Workspace Governor's Hub-maintenance role or the Hub's canonical source ownership |

The sole governing owners for this plan are:

- `C:\Users\Chloe\.agents-hub\rules\AGENTS.md` — Global Governance scope, precedence, routing, and governance-owner eligibility;
- its four routed rule owners — responsibility, autonomy, context/orchestration, and verification;
- `C:\KloWorkspaces\workspace-governor\HUB-ARCHITECTURE.md` — what belongs where;
- `C:\KloWorkspaces\workspace-governor\HUB-MANAGEMENT.md` — how Hub changes, refactors, migrations, records, versions, and verification are performed;
- `C:\KloWorkspaces\workspace-governor\HUB-DOCUMENTATION.md` — construction of an authorized Hub document.

`README.md`, `CATALOG.md`, `STATE.md`, research, evidence, learnings, this plan, and version history are navigation, continuity, analysis, or execution records. They do not become parallel behavioral authorities.

## 3. Planning baseline

### 3.1 Established requirements

- The canonical Hub remains `C:\Users\Chloe\.agents-hub` unless a separate, verified root-relocation decision is authorized later.
- The governed workspace root is `C:\KloWorkspaces`; the Workspace Governor is `C:\KloWorkspaces\workspace-governor`.
- The Hub contract is Global Governance first and follows `Global -> Workspace -> Project -> Component` semantic authority.
- The core is runtime-neutral. Codex, Claude Code, and future runtime integration use thin adapters that reference shared source and do not duplicate or weaken it.
- Each governed issue and canonical artifact has one authoritative owner. Equivalent rules, semantic duplicates, partial overlaps, and narrower/broader restatements are folded into that owner.
- Agents own ordinary technical judgment and execution within granted authority. The user supplies business requirements, protected boundaries, validation expectations, and required outcomes; the user is not the default technical validator. Money-moving actions retain human approval.
- `ENGINEER-OWNERSHIP.md` is the common responsibility contract for executors, architects, reviewers, auditors, and other coding-agent roles whenever its routed conditions are encountered. Role names do not create copies of that contract.
- Agents are responsible for file hygiene, bootstrapping, tooling, context, workflow, delegation, continuity, verification, and correction within their authority.
- Subagents are optional bounded tools for independent parallel work or context isolation. They are not a mandatory hierarchy, council, staffing model, or substitute for the parent agent's intent, authority, integration, and final-verification responsibility.
- Durable project knowledge is project-owned and runtime-neutral: state/current-work checkpoints, decisions, research, evidence, and learnings remain available to any authorized runtime through project files. Runtime-private memory may assist retrieval but is never project authority or the sole continuity record.
- Retain material drafted outputs, accepted findings, qualifying prompts, reusable agent or subagent research, evidence, decisions, and checkpoints when needed to reproduce, audit, continue, or explain material work. Do not retain raw transcripts, caches, logs, hidden reasoning, transient tool output, routine drafts, unnecessary personal data, or semantic duplicates.
- Repository-specific branch, commit, pull-request, review, release, and rollback workflows belong in the applicable project, accepted reusable template, or skill layer. They are not Global Governance. Any genuine escalation condition routes only to `AUTONOMY-AND-PROTECTED-BOUNDARIES.md`.
- Candidate domains are created only with their first accepted artifact. Empty scaffolding is not evidence of acceptance.
- Before any material edit, preserve the accepted version and register it. Preserve original source throughout refactor and migration.
- Work follows the order: decide the target tree, refactor source and references, migrate only verified eligible source, then perform runtime integration and runtime-specific verification.
- A clean replacement is permitted when it is simpler and produces the same or a better verified outcome than editing or refactoring unsuitable material. It must still preserve accepted meaning, sole ownership, provenance, dependencies, references, recovery, and verification.
- The plan and its execution must not depend on `C:\KloWorkspace`, the legacy non-dot `C:\Users\Chloe\agents-hub`, runtime-private memory, attachments, or chat history. Consolidated current project records are the durable basis; legacy material may later be deleted.
- Runtime discovery, activation, and enforcement require separate fresh-session evidence.
- The project-intake baseline is already implemented and provides user and agent information at project creation. It is an input to future work, not an implementation item in this plan.

### 3.2 Verified current state reused from the accepted checkpoint

A lightweight 2026-08-17 drift check found no hash change in the 14 checkpointed Workspace Governor and Agent Hub files. The four remaining canonical rule-owner files have not been modified since before that checkpoint.

`evidence\LEGACY-GOVERNANCE-MATERIAL-CONSOLIDATION-2026-08-17.md` is the accepted non-authoritative consolidation record for legacy meaning, rejection boundaries, and remaining validation requirements. It is evidence for this plan, not a competing owner and not permission to reopen the legacy corpus.

- The five-file governance contract exists under `C:\Users\Chloe\.agents-hub\rules`.
- Hub root `README.md`, `CATALOG.md`, and `STATE.md` exist with navigation, inventory, and continuity roles.
- `runtime-adapters\codex\` and `runtime-adapters\claude-code\` exist but contain no accepted adapter and have no activation evidence.
- `references\AGENTS-MD-LIVE-AUDIT-2026-08-16.md` remains pending overlap reconciliation with Workspace Governor research.
- `governance-templates\workspace\`, `project\`, `component\`, and `delegation\` are empty historical scaffolding.
- `design-systems\.remember\` remains unclassified and untouched; its provenance and sensitivity are unresolved.
- Active Codex governance contains stale path references and overlaps Hub-owned responsibilities. This blocks Codex adapter activation and dependent work, not independent tree analysis.
- The Hub is canonical source but is not verified as runtime-active.

### 3.3 Narrow evidence discrepancy

`C:\KloWorkspaces\test4` was described as deleted, but a path-only drift check found the directory and five immediate intake-validation artifacts still present. This plan treats `test4` as excluded temporary validation material, does not use it as active project evidence, and does not authorize inspection, modification, deletion, recreation, or intake-baseline work. Its filesystem cleanup is outside this plan unless separately requested.

### 3.4 Unresolved conflicts and evidence gaps

| ID | Type | Issue | Blocks | Does not block |
| --- | --- | --- | --- | --- |
| C-01 | Conflict | Runtime-native Codex authority has stale critical paths and semantic overlap with Hub owners | Codex adapter design finalization, installation, activation, and Codex enforcement claims | Target-tree decision, unrelated Hub refactor, Claude Code adapter analysis |
| C-02 | Conflict | `design-systems\.remember\` provenance and sensitivity are unknown | Inspection beyond allowed metadata, classification, movement, promotion, or retirement of that area | Other Hub items |
| C-03 | Runtime precedence conflict | Claude Code's global-versus-project loading behavior can allow project instructions to take priority while semantic governance forbids lower layers from weakening Global Governance | Claude Code adapter finalization, installation, activation, and enforcement claims | Target-tree decision, runtime-neutral refactor, Codex conflict analysis |
| G-01 | Evidence gap | Hub reference audit overlaps project research; unique evidence and inbound references are not yet mapped | Merge/retirement of the Hub reference | Other domains |
| G-02 | Evidence gap | Third-party scaffolder provenance, license, and generated-output behavior are not accepted | Adoption or installation of that scaffolder | Local skill design after requirements are established |
| G-03 | Evidence gap | Runtime discovery, loading, precedence, permissions, hooks, activation, and enforcement behavior may drift | Adapter implementation and activation claims for the affected runtime | Runtime-neutral source work |
| G-04 | Decision gap | The future human glossary has no accepted artifact or final placement | Glossary creation or cataloging | Agent-oriented terminology and Hub completion without a glossary |
| G-05 | Artifact decision gap | No repository-specific coding-delivery workflow artifact has been accepted from the rejected legacy policy set | Promotion or creation of branch/commit/PR/review/release/rollback workflow source | Global Governance and unrelated Hub work |

No unresolved conflict authorizes a parallel rule. Record the blocker, route to the sole owner, and resume only the dependent work after resolution.

## 4. Target-tree decision baseline

The final target tree must be accepted in Step 1 before refactoring. The recommended end-state is:

```text
C:\Users\Chloe\.agents-hub\
|-- README.md
|-- CATALOG.md
|-- STATE.md
|-- rules\
|   |-- AGENTS.md
|   |-- ENGINEER-OWNERSHIP.md
|   |-- AUTONOMY-AND-PROTECTED-BOUNDARIES.md
|   |-- CONTEXT-AND-ORCHESTRATION.md
|   `-- VERIFICATION-AND-EVIDENCE.md
|-- runtime-adapters\
|   |-- codex\                 [accepted thin adapter only]
|   `-- claude-code\           [accepted thin adapter only]
|-- references\                [retained non-authoritative evidence only]
|-- agents\                    [conditional: first accepted artifact]
|-- skills\                    [conditional: first accepted artifact]
|-- tools\                     [conditional: first accepted artifact]
|-- orchestration\             [conditional: first accepted artifact]
|-- evaluations\               [conditional: first accepted artifact]
|-- templates\                 [conditional: first accepted artifact]
|-- packages\                  [conditional: first accepted artifact]
`-- archive\                   [conditional: first accepted retention need]
```

Conditional domains are absent until created with an accepted artifact. `governance-templates\` is not retained merely to reserve a concept. `design-systems\` is not shown as accepted target architecture because C-02 prevents its classification; preserve it in place and visibly mark it excluded until resolved.

### 4.1 Current item classification ledger

These are the required starting classifications for Step 1. `Conflict` entries cannot be silently converted; other entries may change only if new evidence invalidates a premise and the decision record explains why.

| Current item | Class | Authoritative owner | Intended disposition |
| --- | --- | --- | --- |
| `README.md` | Keep | Hub root navigation role defined by Architecture | Retain as concise boundary/bootstrap navigation; update only for accepted routes |
| `CATALOG.md` | Keep | Hub catalog role defined by Architecture | Retain as non-authoritative source inventory; update atomically with accepted artifacts/status |
| `STATE.md` | Keep | Hub continuity role defined by Architecture/Management | Retain as concise mutable checkpoint; never convert to rules |
| `rules\AGENTS.md` | Keep | Itself | Retain as root Global Governance router, precedence owner, and governance-owner eligibility owner |
| `rules\ENGINEER-OWNERSHIP.md` | Keep | Itself via root router | Retain as sole responsibility/intake/technical-decision owner |
| `rules\AUTONOMY-AND-PROTECTED-BOUNDARIES.md` | Keep | Itself via root router | Retain as sole autonomy/approval/protected-boundary owner |
| `rules\CONTEXT-AND-ORCHESTRATION.md` | Keep | Itself via root router | Retain as sole context/long-work/delegation/continuity owner |
| `rules\VERIFICATION-AND-EVIDENCE.md` | Keep | Itself via root router | Retain as sole done/testing/audit/evidence/correction owner |
| `runtime-adapters\` | Keep | Architecture for placement; Management for lifecycle | Retain as the adapter boundary; no shared rules placed here |
| `runtime-adapters\codex\` | Specialize | Canonical rules remain source owners; adapter owns only Codex translation/loading | Add only after C-01 and current official-product evidence are resolved; verify native activation separately |
| `runtime-adapters\claude-code\` | Specialize | Canonical rules remain source owners; adapter owns only Claude Code translation/loading | Add only after current official-product evidence and native-surface inspection; verify separately |
| `references\` | Keep | Architecture | Retain only non-authoritative, provenance-tracked reference material with a distinct maintenance need |
| `references\AGENTS-MD-LIVE-AUDIT-2026-08-16.md` | Merge | Workspace Governor evidence/research owner, subject to Architecture placement | Preserve unique evidence in one project-owned record, update references, then retire the overlapping active Hub copy only after verification |
| `governance-templates\` | Retire | Architecture | Remove empty historical scaffolding from active tree only after path/reference check and version evidence; use `templates\` later only with a first accepted artifact |
| `governance-templates\workspace\` | Retire | Architecture | Same gate; empty directory creates no accepted workspace-template owner |
| `governance-templates\project\` | Retire | Architecture | Same gate; project-intake baseline does not justify recreating or populating it |
| `governance-templates\component\` | Retire | Architecture | Same gate; no accepted component template exists |
| `governance-templates\delegation\` | Retire | Architecture | Same gate; delegation governance remains in its canonical rule owner and reusable prompt/template source requires a separate accepted artifact |
| `design-systems\` | Conflict | Architecture after provenance/sensitivity resolution | Preserve in place and exclude from accepted tree decisions until C-02 is resolved |
| `design-systems\.remember\` | Conflict | Architecture after provenance/sensitivity resolution | Do not inspect deeply, move, generalize, merge, retire, or activate until C-02 is resolved |

No current item requires `Generalize` at baseline. Apply `Generalize` only when later inventory finds project/runtime-specific material containing a reusable core. Apply `Move` to a current item only if evidence shows valid canonical meaning in the wrong domain. Apply `Merge` whenever equivalent practical meaning or partial overlap is found; do not keep a second active owner as a “backup.”

## 5. Execution controls common to every step

Before modifying an affected path:

1. Load live `rules\AGENTS.md` and only the routed canonical owner needed for the encountered issue.
2. Load the relevant Workspace Governor owner: Architecture for placement, Management for lifecycle, Documentation for Hub document construction.
3. Confirm that the step's prerequisites and earlier completion gates remain valid.
4. Reinspect only paths and conclusions affected by material drift.
5. Preserve exact pre-edit versions of every materially changed existing file under the matching `versions\project\` or `versions\hub\` path; hash-verify and register each snapshot.
6. Apply the smallest source-preserving change and update dependencies atomically.
7. Record evidence under Workspace Governor `evidence\`; store research under `research\`; retain prompts only if they pass the existing Management test.
8. Verify actual state, correct failures, and rerun affected checks.
9. Use the consolidation record and current owners; do not reopen or create a dependency on legacy folders, runtime-private memory, attachments, or chat history.
10. Choose between focused editing and a clean replacement by the least complex safe path. A replacement must pass the same ownership, provenance, dependency, reference, recovery, and verification gates.

Never expose secrets in evidence. Never treat a catalog entry, copied file, adapter source, installed file, enabled setting, discovered instruction, active behavior, and verified behavior as the same state.

## 6. Executable implementation sequence

### Step 0 — Execution bootstrap and checkpoint validation

- **Prerequisites:** Explicit authorization to begin implementation; this plan accepted; live project and Hub accessible.
- **Affected paths:** Read-only inspection of the plan, live authority owners, `README.md`, `CATALOG.md`, non-authoritative `STATE.md`, the plan-verification and legacy-consolidation evidence records, the affected paths named by the next step, and checkpoint evidence.
- **Authoritative owner:** Hub root router for governance; Workspace Governor Management for change lifecycle.
- **Intended result:** An execution session starts from current authority and reuses the verified checkpoint without repeating unaffected work.
- **Actions:** Confirm path identity and hashes/timestamps for the accepted baseline; identify material drift; reinspect only changed items and dependent conclusions; use the consolidation record for accepted legacy meaning and rejection boundaries; create a compact, non-authoritative execution checkpoint in project `STATE.md` only when implementation actually starts.
- **Prohibited changes:** No Hub edit, adapter edit, migration, target-tree mutation, full conversation recovery, wholesale research rerun, legacy-corpus reopening, dependency on runtime-private memory/attachments/chat history, or recreation/use of `test4`.
- **Dependencies:** None.
- **Verification method:** Compare the declared baseline files and affected paths; confirm all authority targets exist and routes resolve.
- **Evidence:** Dated drift-check record with compared paths, identities, differences, and affected conclusions.
- **Completion gate:** Baseline is either confirmed unchanged or all changed inputs and dependent plan assumptions are explicitly reconciled.

### Step 1 — Accept the final target tree and complete classification

- **Prerequisites:** Step 0 complete; C-02 remains isolated; no destructive action.
- **Affected paths:** Entire Hub path inventory at name/type/size/identity level; deep content only where authorized; `HUB-ARCHITECTURE.md`; Hub `CATALOG.md`; Workspace Governor `STATE.md` and evidence.
- **Authoritative owner:** `HUB-ARCHITECTURE.md` for domains/placement; `HUB-MANAGEMENT.md` for classification procedure.
- **Intended result:** One accepted final tree and an item-by-item disposition for every live Hub item, including hidden items, without changing the tree.
- **Actions:** Inventory live items; start from Section 4.1; add every newly observed item; assign exactly one of `Keep`, `Move`, `Generalize`, `Specialize`, `Merge`, `Retire`, or `Conflict`; record destination, owner, dependencies, provenance status, and reason; identify conditional domains without creating them; accept the target-tree decision through the applicable authority.
- **Prohibited changes:** No move, rename, deletion, directory creation, content rewrite, adapter creation, or deep inspection of C-02 material.
- **Dependencies:** Step 0.
- **Verification method:** Reconcile classification rows to the live inventory one-for-one; validate every destination against Architecture; check no item or hidden path is omitted or multiply classified.
- **Evidence:** `evidence\AGENT-HUB-TARGET-TREE-DECISION-<date>.md` containing inventory identity, complete ledger, accepted tree, conflicts, and approval status.
- **Completion gate:** Every live item is classified; every non-conflict destination has one owner; the final tree is accepted; conflicts are isolated with exact blocked dependents.

### Step 2 — Resolve provenance, sensitivity, and external-source gates

- **Prerequisites:** Step 1 complete; authority exists to inspect each scoped source; protected-data handling is defined.
- **Affected paths:** Only conflict/evidence-gap paths authorized for review, including `design-systems\.remember`, candidate third-party scaffolder source, relevant manifests/licenses, and any cataloged external-live source.
- **Authoritative owner:** Architecture for placement; Management for promotion; canonical autonomy owner for protected boundaries; canonical evidence owner for safe proof.
- **Intended result:** Each scoped unknown becomes a supported classification or remains a documented isolated conflict.
- **Actions:** Establish provenance, ownership, rights/license, sensitivity, purpose, active dependencies, and recovery needs; inspect content only after the applicable protection gate passes; classify results; reject or quarantine unsafe/unowned material outside active discovery without destroying the sole source.
- **Prohibited changes:** No copying sensitive/runtime state into the Hub; no adoption based only on popularity or installed presence; no overwrite, deletion, or forced inspection of protected material.
- **Dependencies:** Step 1; C-02 for `.remember`; G-02 for third-party adoption.
- **Verification method:** Trace each classification to source evidence and confirm exclusions contain no secrets or unnecessary personal data.
- **Evidence:** One scoped provenance/sensitivity report per distinct source, with decision, limitations, recheck trigger, and affected classification row.
- **Completion gate:** Every item required by a downstream step is either cleared with evidence or explicitly blocked and excluded; no downstream action depends on an unresolved item.

### Step 3 — Establish the semantic owner and dependency map

- **Prerequisites:** Steps 1–2 complete for all included items; canonical rule-owner eligibility standard loaded.
- **Affected paths:** All included canonical documents/artifacts; project-local research/evidence used for comparison; runtime-native instructions only as conflict evidence.
- **Authoritative owner:** `rules\AGENTS.md` for governance-owner eligibility/routing; Architecture for ordinary artifact ownership; Management for reconciliation lifecycle.
- **Intended result:** Every governed issue and reusable artifact has one authoritative owner, one inbound route, and no competing practical answer.
- **Actions:** Compare identical, equivalent, overlapping, narrower, and broader meanings; create an issue-to-owner matrix and artifact-to-owner/dependency matrix; select the accepted owner; decide `Merge`, reference-only, or `Retire` treatment for duplicates; identify gaps without inventing rules; route distinct issues rather than duplicating answers; confirm that executor, architect, reviewer, auditor, and other coding-agent role conditions reach `ENGINEER-OWNERSHIP.md`; confirm every escalation condition routes only to the canonical autonomy owner; reject generic Work-Agent and mandatory-role-hierarchy material.
- **Prohibited changes:** No new governance owner based on file size or topic count; no blended conflicting rule; no non-owner paraphrase; no role-specific copy of the engineering responsibility contract; no escalation rule outside `AUTONOMY-AND-PROTECTED-BOUNDARIES.md`; no conversion of research, state, examples, history, or runtime-private memory into authority.
- **Dependencies:** Steps 1–2.
- **Verification method:** Search the affected corpus by concepts and obligations, not filenames alone; confirm every normative statement maps to one owner and every cross-file link points only to a distinct governed issue.
- **Evidence:** `evidence\AGENT-HUB-SEMANTIC-OWNERSHIP-MAP-<date>.md` with duplicate/overlap dispositions and unresolved gaps.
- **Completion gate:** No included governed issue or artifact has two active owners; each gap/conflict is explicit; downstream edit instructions name the accepted owner and dependent routes.

### Step 4 — Prepare version preservation and rollback manifests

- **Prerequisites:** Steps 1–3 complete; exact edit set accepted; no unresolved semantic issue in that edit set.
- **Affected paths:** Every existing file to be materially changed; Workspace Governor `versions\project\`, `versions\hub\`, `CHANGELOG.md`, and evidence.
- **Authoritative owner:** `HUB-MANAGEMENT.md`.
- **Intended result:** The complete pre-change state can be restored without relying on chat history or an unverified copy.
- **Actions:** Assign version identifiers; copy exact accepted pre-edit files into matching immutable version paths; compute and compare hashes/lengths; record source/destination identity; define phase-level rollback order and recovery checkpoints; preserve directory listings for structural changes.
- **Prohibited changes:** No edit before its snapshot verifies; no overwrite of an existing version; no renaming of the legacy `versions\AGENTS.md-v0.1.0.md`; no deletion of the only verified source.
- **Dependencies:** Steps 1–3; repeats before each later material edit set.
- **Verification method:** Hash source against preserved version; confirm snapshot paths and changelog registration; test that the rollback manifest references existing artifacts.
- **Evidence:** Version files, changelog entries, and `evidence\AGENT-HUB-ROLLBACK-MANIFEST-<date>.md`.
- **Completion gate:** Every planned material edit has a verified pre-edit snapshot and a deterministic rollback instruction.

### Step 5 — Refactor the runtime-neutral core and root controls

- **Prerequisites:** Steps 1–4 complete for the core edit set; independent pre-edit review accepted for governance/architecture changes.
- **Affected paths:** Accepted Hub root controls, `rules\`, and only the routes/indexes directly affected; Workspace Governor authority files only if the accepted tree decision materially changes architecture or lifecycle.
- **Authoritative owner:** Each rule owner for its content; root router for routes; Architecture for placement; Documentation for Hub document construction; Management for edit lifecycle.
- **Intended result:** A coherent runtime-neutral core with precise ownership, concise bootstrap, correct navigation, and no semantic duplication.
- **Actions:** Edit only accepted owners or create a clean replacement when the accepted classification shows replacement is simpler and equally or more verifiable; fold duplicates and partial overlaps into their owner; replace removed restatements with a narrow route only when a distinct issue transition is needed; keep root bootstrap small; keep business authority, governance responsibility, and agent technical judgment distinct; preserve common Engineer Ownership routing across coding-agent roles; keep examples in the owning file only when needed to disambiguate execution; update navigation and catalog status.
- **Prohibited changes:** No runtime syntax or model identifiers in the shared contract; no lowering of protected boundaries; no transfer of ordinary technical validation to the user; no generic Work-Agent behavior or mandatory agent hierarchy; no repository-specific delivery mechanics in Global Governance; no escalation owner outside the canonical autonomy file; no fixed file-count rule; no empty governance owner; no architecture expansion unrelated to accepted artifacts.
- **Dependencies:** Steps 1–4.
- **Verification method:** Diff against accepted wording; rerun semantic-owner checks; validate all routes and file existence; check agent-oriented terminology, authority hierarchy, and protected boundaries; obtain distinct post-edit verification.
- **Evidence:** Reviewed diffs, owner map update, post-edit verification report, exact versions, and changelog entries.
- **Completion gate:** The core contract and root controls match accepted owners/tree, all routes resolve, no duplicate obligation remains, and post-edit verification passes.

### Step 6 — Consolidate references and evidence without losing unique findings

- **Prerequisites:** Steps 1, 3, and 4 complete for G-01; unique-content and inbound-reference map available.
- **Affected paths:** `references\AGENTS-MD-LIVE-AUDIT-2026-08-16.md`; relevant Workspace Governor `research\`, `evidence\`, `README.md`, `STATE.md`, version, and changelog records; Hub `CATALOG.md`.
- **Authoritative owner:** Architecture for project-versus-Hub placement; Management for project records, merge, retirement, and references.
- **Intended result:** One project-owned evidence/research record retains all material unique findings; the Hub does not carry a semantically overlapping active copy without a distinct need.
- **Actions:** Map unique and overlapping content; merge only unique evidence into its correct project record; preserve citations, dates, limitations, and source identity; update all inbound/outbound links; preserve the Hub source version; remove the redundant reference from active Hub discovery only after destination integrity and reference verification.
- **Prohibited changes:** No loss of unique evidence; no rewriting dated observations as current facts; no copying the final deliverable into evidence; no raw transcript or duplicate report retention.
- **Dependencies:** Steps 1, 3, and 4; G-01 resolved.
- **Verification method:** Content-accounting checklist, link search, hash/version checks, and catalog/navigation validation.
- **Evidence:** Merge matrix and verification report showing where every unique finding and reference went.
- **Completion gate:** Unique evidence is preserved once, stale links are zero, the active catalog is accurate, and recovery remains possible.

### Step 7 — Refactor structural domains and accept reusable artifacts

- **Prerequisites:** Accepted final tree; Steps 2–5 complete for included content; artifact creation test passes for every new artifact/domain.
- **Affected paths:** `governance-templates\`; conditional `agents\`, `skills\`, `tools\`, `orchestration\`, `evaluations\`, `templates\`, `packages\`, or `archive\`; their owner-local manifests; Hub `CATALOG.md`; project evidence/versions/state.
- **Authoritative owner:** `HUB-ARCHITECTURE.md` for domains/artifacts; `HUB-MANAGEMENT.md` for refactor/promotion; canonical rule owner remains authoritative for any behavior a capability applies.
- **Intended result:** The physical tree matches accepted domains, contains no empty speculative scaffolding, and admits reusable assets only with known provenance, owner, lifecycle, dependencies, compatibility, and tests.
- **Actions:** Retire empty `governance-templates\` after reference/version gates; create a candidate domain only with its first accepted artifact; keep generated project rules in the target project; place any accepted branch, commit, pull-request, review, release, or rollback workflow in its applicable project, independently reusable template, or focused skill; keep artifact-specific assets/scripts/tests with their owner; retain material drafted outputs and reusable agent research in the owning project records when the retention test passes; keep delegation support optional and bounded; author and validate a focused Workspace Governor skill before considering a distribution plugin; use clean replacement when it is the simpler verified path; register source and compatibility states precisely.
- **Prohibited changes:** No empty candidate domain; no promotion of the rejected legacy policy set as Global Governance; no mandatory subagent hierarchy or council; no foreign generator-owned block as Hub authority; no installed plugin/cache/runtime state in canonical source; no plugin packaging before the workflow is stable and needs distribution; no scheduled automation in this step; no new intake baseline; no dependence on legacy files remaining available.
- **Dependencies:** Steps 1–5; Step 2 for third-party material.
- **Verification method:** Tree-to-architecture comparison; artifact creation-test checklist; provenance/license/test review; catalog and manifest validation; no-empty-domain scan.
- **Evidence:** Per-artifact acceptance record, structural diff, tests, catalog update, and post-edit verification.
- **Completion gate:** Every active domain contains an accepted artifact, every artifact meets the minimum record, no unapproved scaffolding remains, and the refactored tree passes integrity/usability checks.

### Step 8 — Migrate accepted external source into the canonical Hub

- **Prerequisites:** Refactored Hub passes Step 7; an external source is explicitly accepted for migration; source rights, owner, destination, and rollback are known.
- **Affected paths:** Only a currently cataloged and accepted external-live source and its accepted canonical Hub destination; all referencing projects/adapters/indexes; versions, evidence, and changelog. Legacy paths named only in the consolidation record are not migration inputs.
- **Authoritative owner:** Architecture for destination; Management for migration; the accepted artifact owner for content.
- **Intended result:** Eligible reusable source is transferred into its canonical owner without data loss, authority duplication, or premature retirement of the old source.
- **Actions:** Inventory and hash the source; copy source-preservingly to a staged destination; validate content and usability; update references and ownership markers; test consumers; keep the old source intact until destination integrity, reference correctness, fresh-use behavior, and a second recovery path pass; then separately authorize old-source retirement if required.
- **Prohibited changes:** No relocation of `C:\Users\Chloe\.agents-hub` itself; no migration of individual project workspaces; no `/MOVE`, purge, mirror-delete, or sole-source overwrite; no promotion of credentials, logs, sessions, caches, runtime-private memory, or operational state; no reopening or dependence on consolidated legacy material; no claim that copied means migrated.
- **Dependencies:** Steps 1–7 and an accepted source. If no eligible source exists, record “no migration required” with evidence rather than inventing one.
- **Verification method:** Source/destination file inventory, hashes where applicable, reference scan, artifact tests, fresh-use test, and second-recovery-path check.
- **Evidence:** `evidence\AGENT-HUB-MIGRATION-<artifact>-<date>.md`, integrity manifest, updated catalog/links, and retirement decision if any.
- **Completion gate:** Every accepted migration has destination integrity, one authoritative source, correct references, verified usability, and recovery; or the phase records that no accepted migration candidate exists.

### Step 9 — Reconcile and implement thin runtime adapters

- **Prerequisites:** Runtime-neutral core stable; Steps 1–8 complete or explicitly `NOT APPLICABLE` with evidence; current official vendor documentation and live runtime-native surfaces inspected; C-01 resolved before Codex work; C-03 resolved before Claude Code adapter activation.
- **Affected paths:** Hub `runtime-adapters\codex\` and `runtime-adapters\claude-code\`; the minimum runtime-native authority/configuration locations required for loading; Hub catalog/state; Workspace Governor research/evidence/versions/changelog.
- **Authoritative owner:** Canonical Hub rules for shared behavior; runtime adapter for translation/loading only; runtime-native authority for native configuration; Management for lifecycle.
- **Intended result:** Each supported runtime can discover the shared contract through a minimal, traceable adapter without creating another owner.
- **Actions:** Revalidate discovery, loading, scope, precedence, imports, permissions, hooks, configuration, context limits, and enforcement behavior from current primary vendor documentation; resolve stale paths and overlapping Codex rules through their rightful owner; resolve the Claude Code global-versus-project precedence constraint with a supported design that does not claim semantic precedence the runtime cannot demonstrate; specify adapter inputs/outputs and native location; implement the smallest adapter; link rather than restate shared rules where supported; record materialized/installed/enabled/discovered/active/verified separately; update catalog and routes.
- **Prohibited changes:** No assumption that instruction files are deterministic enforcement; no assumption that file-system placement implies loading; no shared-rule duplication; no runtime-specific syntax in core; no Codex activation while C-01 remains; no Claude Code activation while C-03 remains; no cross-runtime claim based on one runtime's test; no use of legacy files or runtime-private memory as adapter authority.
- **Dependencies:** Steps 1–8; C-01 for Codex; C-03 for Claude Code; G-03 for each runtime.
- **Verification method:** Static adapter comparison to canonical source; native configuration inspection; clean fresh-session discovery, loading, and precedence probes; permission, hook, and enforcement tests supported by the runtime; Claude global-versus-project conflict and negative tests; behavior probes for routed owners; negative tests showing an adapter adds no competing rule.
- **Evidence:** Current source-linked vendor research, adapter manifest, native-path diff/version, per-state status record, and runtime-specific test report.
- **Completion gate:** Each claimed supported runtime independently reaches and applies the intended canonical source in a fresh session; C-01 and C-03 are resolved for their respective adapters; documented discovery, loading, precedence, permissions, hooks, and enforcement claims pass their runtime-specific tests; all stale critical paths are resolved; and no adapter duplicates shared governance.

### Step 10 — Update routes, registries, continuity, and references atomically

- **Prerequisites:** The corresponding source change, refactor, migration, or adapter change is ready for the same edit set.
- **Affected paths:** Hub `README.md`, `CATALOG.md`, `STATE.md`, owner-local manifests; Workspace Governor `README.md`, `STATE.md`, `LEARNINGS.md` only when retention test passes, `CHANGELOG.md`, versions, research/evidence; runtime routes affected by adapter work.
- **Authoritative owner:** The source owner for meaning; Architecture for catalog schema/placement; Management for lifecycle/records; canonical context owner for continuity behavior.
- **Intended result:** Every consumer and authorized runtime can find the current owner, durable project knowledge, and status without stale paths, chat-only knowledge, or runtime-private memory dependence.
- **Actions:** Update moved/merged/retired paths and dependencies in the same change; remove stale inbound/outbound links; distinguish current source, materialization, installation, enablement, discovery, activity, and verification; maintain project-owned state/current-work checkpoints, decisions, research, evidence, and learnings in their proper owners; replace stale state rather than append a transcript; record only durable non-obvious learnings; register all snapshots.
- **Prohibited changes:** No catalog as behavioral authority; no `STATE.md`, decision record, research, evidence, learning, or runtime-private memory as a competing rule; no semantic duplicate in navigation; no history deletion; no automatic creation of `prompts\`; no storing hidden prompts/reasoning, raw transcripts, caches, logs, or transient tool output.
- **Dependencies:** Runs atomically with Steps 5–9 whenever their references change.
- **Verification method:** Full path/reference scan of affected scopes, broken-link check, owner/status consistency check, changelog-to-version reconciliation, and state freshness review.
- **Evidence:** Reference-update matrix and post-change verification report.
- **Completion gate:** Zero stale affected routes, every catalog item exists and has the correct status/owner, versions are registered, and a fresh session can find the current checkpoint.

### Step 11 — Fresh-agent bootstrap and runtime-activation verification

- **Prerequisites:** Refactor/reference changes complete; at least one adapter ready for activation testing; acceptance prompts/tests defined without relying on hidden chat history.
- **Affected paths:** Read-only test of Hub, Workspace Governor, one controlled test project created only if separately authorized, and the runtime-native adapter/configuration under test; project evidence for results.
- **Authoritative owner:** Canonical context owner for bootstrap/continuity; canonical verification owner for proof; adapters only for runtime mechanics.
- **Intended result:** A fresh coding agent can identify who it is, where it is, where it works, what is expected, its responsibilities, what the Hub is, which single owner governs the encountered issue, and the current checkpoint; each claimed runtime demonstrates actual activation separately.
- **Actions:** Start clean sessions with no conversation history or required runtime-private memory; test Hub-first bootstrap and project-local specialization; test executor, architect, reviewer/auditor, and orchestrating coding-agent scenarios to prove role-neutral routing to `ENGINEER-OWNERSHIP.md`; present routine, complex-technical, protected-boundary, repeated-question, conflicting-authority, long-project, optional bounded-delegation, and verification scenarios; resume a project using only its project-owned state, decisions, research, evidence, and learnings; confirm the correct single owner is loaded and all escalation conditions reach only the autonomy owner; verify source through `verified` states independently; test that unclaimed runtimes/statuses remain unclaimed.
- **Prohibited changes:** No use or recreation of `test4`; no generic Work-Agent acceptance scenario or mandatory subagent hierarchy; no treating the user as technical validator; no runtime-private memory as project authority; no passing result based only on file presence or agent self-report; no reuse of a session already carrying the rules; no conflation of adherence with hard enforcement.
- **Dependencies:** Steps 5–10; Step 9 for runtime activation.
- **Verification method:** Reproducible fresh-session protocol, observed paths/context, behavior outputs, negative controls, and independent post-edit verifier review.
- **Evidence:** `evidence\FRESH-AGENT-BOOTSTRAP-<date>.md` plus one activation report per runtime with environment/version, resolved files, tests, results, limitations, and recheck trigger.
- **Completion gate:** Bootstrap passes without hidden chat knowledge; each claimed runtime passes its own discovery/precedence/activation tests; failures are corrected and affected tests rerun.

### Step 12 — Final audit, rollback readiness, and completion declaration

- **Prerequisites:** All applicable prior gates complete; conflicts resolved or explicitly excluded without a completion dependency; no failed check outstanding.
- **Affected paths:** Entire accepted Hub tree; affected runtime adapters/native routes; Workspace Governor authority, plan, state, catalog, versions, changelog, research, and evidence.
- **Authoritative owner:** Canonical verification owner for done/evidence; Management for Hub-specific final checks; Architecture for final tree.
- **Intended result:** A defensible declaration that the Hub is complete for its accepted scope, with known limitations and working recovery.
- **Actions:** Audit target tree, classifications, semantic owners, references, domain creation tests, provenance, context boundaries, runtime statuses, version history, and evidence; confirm no accepted artifact depends on legacy files, attachments, chat history, or runtime-private memory authority; confirm rejected Work-Agent rules and runtime-state-in-Hub designs are absent; compare implementation against every requirement and plan gate; rehearse rollback from manifests without destructive execution; correct failures and rerun affected checks; update Hub and project state to the verified result.
- **Prohibited changes:** No completion claim with unresolved dependent conflict, stale critical path, missing owner, semantic duplicate, empty candidate domain, unverified adapter, broken recovery path, legacy-source dependency, runtime-private-memory authority, rejected legacy behavior, or undocumented material deviation.
- **Dependencies:** All applicable Steps 0–11.
- **Verification method:** Requirement traceability matrix, final tree inventory, semantic-duplicate scan, link/path validation, evidence completeness check, fresh-agent/runtime results, and recovery-manifest inspection.
- **Evidence:** `evidence\AGENT-HUB-FINAL-AUDIT-<date>.md`, final traceability matrix, final inventory/hashes as proportionate, and updated state/changelog.
- **Completion gate:** Every criterion in Section 8 is `PASS`, `NOT APPLICABLE` with reason, or an explicitly accepted limitation that does not contradict the declared completion scope.

## 7. Rollback and recovery strategy

Rollback is phase-scoped. Reverse only the smallest failed edit set and its dependent routes.

| Failure point | Recovery action | Required proof before resuming |
| --- | --- | --- |
| Classification/tree decision is wrong before edits | Amend the decision record; no filesystem rollback needed | Reconciled complete ledger and reaccepted tree |
| Core document edit fails verification | Restore exact pre-edit version; restore dependent routes/catalog/state from the same edit set | Hash match to preserved versions and successful affected checks |
| Reference merge loses or misroutes evidence | Restore the Hub source and prior project records; rebuild unique-content map | All unique findings accounted for once and all links valid |
| Structural refactor breaks discovery | Restore original paths and matching routers/indexes; do not remove destination evidence | Fresh bootstrap reaches original owners and inventory matches rollback manifest |
| Migration copy or consumer test fails | Keep original source authoritative; remove destination from active discovery without destroying evidence | Source integrity, catalog correction, and consumer recovery verified |
| Runtime adapter conflicts or fails | Disable/remove adapter from active native routing, restore native versions, keep canonical Hub source unchanged | Clean runtime session returns to prior verified behavior and no stale route remains |
| Final audit fails | Reopen only failed step and dependents; do not declare completion | Corrected artifacts and rerun evidence pass |

The original source is not retired until the destination has verified integrity/usability and a second recoverable copy or equivalent recovery path. Any destructive retirement requires separate authority at the time of action.

## 8. Final completion criteria

The canonical Agent Hub is complete for the accepted scope only when all applicable statements are true:

1. The accepted physical tree matches `HUB-ARCHITECTURE.md`; every live item is classified and every `Conflict` affecting completion is resolved.
2. Every governed issue and canonical artifact has one authoritative owner, one unambiguous route, and no active semantic duplicate or unresolved partial overlap.
3. The five-file Global Governance contract remains runtime-neutral, precise, internally consistent, and complete for its routed responsibilities.
4. The shared contract governs coding-agent roles rather than generic Work Agents; executors, architects, reviewers/auditors, and other coding-agent roles reach `ENGINEER-OWNERSHIP.md` whenever its routed conditions occur, without role-specific duplicates.
5. Business authority, governance responsibility, and agent technical judgment remain distinct; ordinary technical validation is not transferred to the user, and escalation is owned only by `AUTONOMY-AND-PROTECTED-BOUNDARIES.md`.
6. Subagents remain optional bounded context-isolation or parallel-work tools; no mandatory hierarchy or council is required.
7. Root bootstrap, catalog, non-authoritative state, owner-local manifests, and references point to existing current sources and do not claim authority they do not own.
8. Durable project knowledge is project-owned and cross-runtime through state/current-work checkpoints, decisions, research, evidence, and learnings; runtime-private memory is optional retrieval only and never authority.
9. Material drafted outputs and reusable agent research that pass retention are preserved once; raw transcripts, caches, logs, hidden reasoning, transient tool output, and semantic duplicates are absent.
10. Repository-specific branch, commit, pull-request, review, release, and rollback workflows reside only in their accepted project, template, or skill layer—not Global Governance.
11. No candidate domain is empty; every accepted artifact has purpose, provenance, owner, lifecycle, dependencies, compatibility, verification date, and recheck trigger.
12. No credential, secret, session, transcript, cache, log, live connection, runtime-private memory database, generated runtime state, or ordinary project artifact has been promoted into canonical shared source.
13. Every material change has an exact registered pre-edit version, auditable history, and a tested or inspectable rollback path.
14. Target-tree acceptance preceded refactoring; refactoring preceded migration; migration completed or was evidenced `NOT APPLICABLE` before runtime integration and verification; every migration preserved the original until integrity, references, fresh use, and recovery passed.
15. All affected routes, registries, catalogs, manifests, continuity records, and runtime-native references are current; stale critical paths are zero.
16. Thin adapters contain only runtime-specific loading/translation/enforcement mechanics and do not duplicate, redefine, or weaken shared rules.
17. Runtime states are reported separately and accurately. Current vendor evidence covers discovery, loading, precedence, permissions, hooks, and enforcement; C-01 and C-03 are resolved before their respective adapter activation claims.
18. A fresh coding agent, without chat history or required runtime-private memory, can bootstrap to the correct contract, select the sole owner for an encountered issue, locate non-authoritative current state and other project-owned knowledge, and act within authority.
19. No accepted source or verification depends on `C:\KloWorkspace`, the legacy non-dot Hub, attachments, chat history, or runtime-private memory; rejected Work-Agent rules and runtime-state-in-Hub designs are absent.
20. The final audit and every affected re-verification pass; evidence is sufficient, safe, linked, and stored in its correct project layer.
21. The Workspace Governor, Hub, runtime adapters, individual projects, project-intake baseline, and future Workspace Orchestrator remain separate in ownership and function.

## 9. Implementation outputs and records

Execution should produce only records justified by the existing governance:

- accepted target-tree/classification evidence;
- semantic ownership/dependency map;
- material decisions and accepted drafted outputs in their authoritative project locations;
- retained reusable agent or subagent research when the project retention test passes;
- exact version snapshots and changelog registrations;
- scoped provenance/sensitivity reports where required;
- refactor, merge, migration, adapter, bootstrap, runtime-activation, rollback, and final-audit evidence as applicable;
- concise updates to project and Hub `STATE.md` at material phase transitions;
- catalog/manifest/reference updates tied to actual accepted source changes;
- one-line durable learnings only when the Management retention test passes.

Do not create reports merely to mirror this list. Combine evidence when one record can prove multiple related gates without obscuring ownership, and do not copy final deliverables into evidence.

## 10. Immediate next action after plan acceptance

When implementation is separately authorized, execute **Step 0 only**, then proceed to **Step 1: Accept the final target tree and complete classification**. Preserve the order `target-tree decision -> refactoring -> migration -> runtime integration and verification`. Do not begin a later phase before the preceding phase's completion gate passes or is explicitly evidenced `NOT APPLICABLE` where the plan permits that result.
