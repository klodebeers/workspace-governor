# Step 2 -- first accepted artifact per domain

**Date:** 2026-08-21
**Revision:** 6. Revision 1 described the artifacts as first written; two reviews
reworked them before anything was committed. Revision 2 described the committed
state at `d1a8553`. Four further blind audits then found material defects in that
committed state, which were fixed at `df33f07`. A fifth, final audit found eight
more, closed at `1a91d32`. Earlier revisions are superseded in place: revision 1
never described committed content, and revisions 2 and 3 described content that has
since been corrected.
**Scope:** Create `agents/`, `orchestration/`, `registry/`, `templates/` and
`context/` in the canonical Hub, each with its first accepted artifact.
**Authorisation:** User, 2026-08-21: "proceed with Step 2".
**Source:** `agents-hub-two` @ `0a222df`. Classification carried from
`evidence/AGENTS-HUB-TWO-RECONCILIATION-2026-08-20.md` revision 2 and
`evidence/HUB-TARGET-TREE-AND-CLASSIFICATION-2026-08-21.md`.
**Base commit:** `c6c966b`. **Result commit:** `1a91d32` (first applied at
`d1a8553`, corrected at `df33f07` and `1a91d32`), verified on the live remote and by extracting `origin/main` and
re-running all three checks against the extraction.

## What "first accepted artifact" means here

The accepted taxonomy forbids empty or speculative directories: a directory is
created by its first real artifact. Step 2 therefore migrates **six artifacts**,
not the 27-file source package. The rest keep their recorded dispositions and
migrate later, against contracts this step establishes.

| Artifact | Directory | Disposition applied | Source |
|---|---|---|---|
| `registry/agent-registry.json` | `registry/` | **Adapt -- split.** Identity kept; routing, entry point, coordinator object and the second agent list superseded | `config/agent-registry.json` |
| `registry/agent-registry.schema.json` | `registry/` | **Adapt / rewrite.** The source schema did not describe its target | `schemas/agent-registry.schema.json` |
| `orchestration/routing.json` | `orchestration/` | **Fold.** Four routing declarations at three fidelities reduced to one owner | both coordinators, both dependency files, the registry |
| `agents/notion-formula-logic.json` | `agents/` | **Adapt.** Key-vocabulary normalisation; domain knowledge extracted | `agents/NOTION-FORMULA-LOGIC-AGENT.json` |
| `context/NOTION-FORMULA-V2.md` | `context/` | **Fold.** Quadruplicated domain knowledge consolidated | 4 files, 4 key names |
| `templates/verification-checklist.json` | `templates/` | **Keep** + rename, with one field default changed | `templates/verification-checklist-template.json` |

## Decisions taken inside the approved scope

Ordinary engineering decisions, made and proved here. Each traces to a recorded
finding.

**1. One entry point; domain selection is a step after entry.** The source
declared its entry point in eight locations that disagreed, and the only
machine-readable one named the Notion coordinator as the sole entry -- so a
general request reached the Notion domain, where the general coordinator's own
prompt then sent it to a registry with no routing rules for any of its six
specialists. `orchestration/routing.json` owns one domain-neutral entry point,
then domain selection, then routes.

Domain selection is **carried, not invented**: the source stated the step in prose
in `package-layout.json` notes, `docs/README.md` and
`prompts/general-coordinator.prompt.txt`. What is new is the machine-readable
condition and its placement after one entry point instead of before two. Revision
1 claimed the source had no such step; that was false and is corrected.

**2. The Notion coordinator is folded, and the fold is recorded on the entry that
absorbs it.** The reconciliation settled that it is the same orchestrator role
instantiated for a domain, not a distinct agent. The registry therefore holds
twelve identities, not thirteen, and the orchestrator's domain is `shared` -- one
orchestrator serving every domain after domain selection. Revision 1 held the fold
implicitly while its schema comment described a per-domain orchestrator model,
which left the `notion-operations` domain with no orchestrator to receive routed
work.

**3. Divergent duplicate wording is chosen, not blended.** The five Notion routes
existed twice with different phrasing. The coordinator's copy is taken because
routing is the coordinator's role; the other is superseded, its wording preserved
in the reconciliation record rather than merged into a third phrasing neither
source states. The routes are **verified byte-identical to the
source** by `scripts/Assert-HubSourceFidelity.py`, which re-reads both sides on demand.
An earlier version of this paragraph said they were "generated from the source files, so
verbatim is true by construction". That claim is withdrawn: the generator was an
uncommitted inline script, so nothing could re-derive it, and a claim that cannot be
re-run is the failure D-53 exists to prevent. A committed verifier is the honest form.
The withdrawal is also recorded in the round-2 findings table below -- this paragraph
contradicted it until 2026-08-21.

**4. A reference to something that does not exist is `null` with a status, never a
path.** Eleven of twelve registry entries have no normalized definition; they
carry `definition: null` and `definition_status: pending`, and the schema enforces
the pairing in both directions. Writing the eventual paths would have manufactured
eleven dangling references -- the class `DECISIONS.md` D-39 exists to prevent.

**5. One agent-definition vocabulary; its schema is owed, not guessed.** The
source used two incompatible vocabularies for the same concepts and had no schema
for either. The migrated definition fixes the vocabulary. A schema written from one
migrated file would encode one shape as though it were thirteen, so it is required
before a second definition migrates and must be written against all thirteen
source shapes.

**6. `policies/` is not created for the registry schema.** The schema is
machine-verifiable, which is what `policies/` holds, but nothing enforces it in
any runtime, so placing it there would assert an enforcement boundary that does
not exist. It sits in `registry/`, which the accepted target tree already
specified as holding the registry plus its schema.

**7. New asset domains are indexed in `CATALOG.md`, not added to the root routing
table -- and `README.md` gained a bootstrap step.** The root routing table maps
governed conditions to governance owners, and the root contract states it "does
not govern ordinary non-governance artifacts or Hub domain placement". These six
artifacts are canonical source data. But the governance review established that
catalog presence alone leaves them **normatively unplaced**: `CATALOG.md` declares
itself non-authoritative and proving nothing, and the root contract tells an agent
to load only routed owners, so nothing instructed an agent to enter work through
the routing file. `README.md`, which owns bootstrap navigation, now has step 4:
enter agent work through `orchestration/routing.json` and resolve identity through
`registry/agent-registry.json`, neither being a governance owner and neither
granting permission. That closes the gap without touching precedence.

**8. `human_review_required` defaults to `null`, not `false`.** A canonical
template shipping `false` supplies a default answer to an approval question, and
approval is owned by `rules/AUTONOMY-AND-PROTECTED-BOUNDARIES.md`. `null` requires
whoever fills the checklist to answer it. This is the one field where the template
is no longer byte-identical to its source, and the reason is recorded.

## Adversarial review -- two rounds

### Round 1, before the first commit

Two reviews, one on fidelity to source and one on governance boundaries. Twenty
findings accepted and fixed, three rejected. Nothing from the pre-review draft
reached the repository. Four of the accepted findings were provenance claims wrong
in the same direction, overstating novelty: a domain-selection step called newly
authored when the source states it in prose in three files; an entry-point count of
three where eight locations declare it; a role sentence rewritten without marking
it; and a source `must` reclassified as not an instruction.

### Round 2, on the committed state at `d1a8553`

Four reviewers, each given the source package, the approved scope and the resulting
implementation, and each **denied the implementer's rationale** -- no access to this
file or to the Step 2 decision entries -- so no reviewer could be primed by it.
Boundaries were chosen from the actual change: registry and schema; orchestration and
routing; the agent, context and template transformations; and scope compliance plus
the verification tooling. Reviewers were instructed to report findings only and not
to implement an alternative architecture. Every finding was verified against source
or rule text before being accepted or rejected. Mechanism now settled as
`DECISIONS.md` D-60.

**Accepted and fixed:**

| Class | Finding | Verification |
|---|---|---|
| **Lost governance** | Consolidating the formula material dropped three source obligations and softened their modality: "the formula **must be validated after** the schema change"; "database schema and formulas **must be reviewed together** when migrating or repairing older logic"; and a coordinator-level `must_acknowledge` that any formula migration must validate actual behavior. None had a carrier | All three read directly from `NOTION-SCHEMA-RELATIONS-AGENT.json`, `NOTION-SYSTEM-DEPENDENCIES.json` and `NOTION-COORDINATOR-ORCHESTRATOR.json`. Confirmed. D-61; owed items recorded in `STATE.md` |
| **Invented content** | "distinct from schema structure" appears in no source block; a source "**may** affect" had been strengthened to an unconditional "behaves differently"; a legacy-migration statement had been generalised into a platform fact | Confirmed against source. Modality is now carried, and the file says so |
| **Narrowed scope** | The context file's consumer list named two specialists as though complete. Three further Notion specialists carry rules that depend on formula behavior | Confirmed by quotation from all three. Scope is now stated as a condition, not a list |
| **Non-verbatim claim** | The pre-routing condition had been reworded from "Business request with unclear requirements" while claimed as carried verbatim | Found by the new source-fidelity script, not by reading. Now exact |
| **Governance gap papered over** | The pre-routing entry claimed the source's intake obligation was "routed rather than restated" to `rules/ENGINEER-OWNERSHIP.md`. That owner governs *when to ask* and states no obligation to produce a decision brief or define required fields | Confirmed by reading the rule. The root contract requires surfacing a gap rather than inferring a parallel answer; the entry now surfaces it |
| **Backoffice state in live authority** | Flagged by all four reviewers. Narrative rationale, retirement arguments, a `deferred` progress ledger, and a **required** `definition_status` field that made migration progress a mandatory part of canonical data | Confirmed against the directive and against the Hub catalog's own sentence saying migration state lives in the backoffice. Removed; `definition: null` already carries the fact |
| **Derived and duplicated data** | `dependencies[].available` duplicated whether a path was null and would go stale silently. The agent definition carried `name`, `domain`, `role_class` and `canonical_status`, all registry-owned, while disclaiming ownership of them | Confirmed. Only the resolution key remains |
| **Unenforceable primary key** | The schema accepted duplicate ids, demonstrated by appending a copy of an entry. An id must resolve to exactly one entry | Reproduced. JSON Schema cannot express it, so the script now does, plus name uniqueness and folded-id collision |
| **Unresolvable folded id** | `notion-coordinator-orchestrator` appears twice in the source and resolved to nothing after the fold | Confirmed. Recorded in `folded_ids`; the schema permits it only on an orchestrator |
| **No way to retire an identity** | `canonical_status` admitted only two flavours of "accepted", so withdrawing an identity meant deleting its record | Confirmed. Now `accepted` / `retired` |
| **Root reachability** | `AGENTS.md` was unchanged, so an agent loading only the always-loaded root contract could not learn the asset domains exist. `README.md` alone left two entry surfaces with the discovery chain running the wrong way | Confirmed by reading `AGENTS.md`: no reference to `README.md` or `CATALOG.md`. A short section now names the asset domains and what weight they do not carry. The governance routing table is still four rule owners |
| **Untrue index claims** | The template's stated purpose, its field count (7, not the contract's 6), a retirement asserted in the Hub that exists in no Hub artifact, "output shapes" for a directory holding no output template, plural "definitions" for one file, and the undisclosed fact that 10 of 11 route destinations have no definition | Each checked against the artifact. All corrected |
| **Unrecorded decisions** | The synonym retirement and the third template identifier were recorded only in evidence and in the self-declared non-authoritative catalog, not in `DECISIONS.md` | Confirmed. D-58 |
| **Unsuperseded decision conflict** | Flat `agents/` and a domain-tagged registry contradict D-14, which required subdivision and a domain-keyed registry and argued flat would keep general agents second-class; D-12's template placement likewise | Confirmed by reading both. D-57 supersedes the structural halves and explains why the asymmetry is nonetheless resolved |
| **Unclassified content migrated** | `validated_references` was carried although the approved record left it unclassified | Confirmed. D-59 classifies it |
| **Tooling: PASS for checks that never ran** | Deleting `orchestration/routing.json` still produced "RESULT: PASS ... and cross-artifact checks all behaved as required", because the skip branch added nothing to the failure list | Reproduced by the auditor. A missing required artifact is now a refusal, and no success line names a check that did not run |
| **Tooling: false failure on correct content** | Negative-case fixtures were selected by `role_class`, so promoting the orchestrator to a migrated entry -- a state the schema permits -- made the harness report a defect in a correct registry | Reproduced. Fixtures are now selected by the property under test, and a missing fixture is a failure, not a crash |
| **Tooling: overstated coverage** | The reference check claimed "every backtick path token"; markdown link targets were uncovered, and its own out-of-scope counter was incremented twice per token, printing double | Both reproduced. Link targets now covered, the counter fixed -- it now agrees with the auditor's hand count of 13 -- and the docstring states the real limits, including that a token containing a space is treated as prose |
| **Tooling: an inverted check** | `$id` was resolved as a filesystem path. The correct absolute-URI form was skipped as uncheckable, and the defective relative form resolved cleanly -- rewarding the exact regression the schema rewrite removed | Reproduced. `$id` is now validated by URI semantics; an instance `$schema` may be a relative path and must resolve |
| **Tooling: no source-fidelity check at all** | Neither script read the source package, so every load-bearing claim of the migration was asserted in prose and verified by nobody. A commit message also claimed routes were "generated from the source files" with no committed generator | Confirmed. `scripts/Assert-HubSourceFidelity.py` is new and reads both sides. The generation claim is withdrawn: fidelity is now *verified* by a committed script, which is the honest form |
| **Tooling: no reverse coverage** | An unindexed artifact dropped into the tree passed both scripts, though catalog completeness is the Hub's discovery contract | Reproduced. The reference check now verifies that every artifact is indexed |
| **Record defect** | `STATE.md` carried the approval stop condition with nothing recording that approval had been given | Confirmed. Recorded, and see the rejection below |

**Rejected, with reasons** -- settled in `DECISIONS.md` D-55 so they are not reopened:
that Step 2 lacked approval (it was given in session; the reviewer was blind to
that by design, and the real defect was the missing record); that a negative scope
disclaimer restates a routed rule (it denies answering a question rather than
answering it, and the taxonomy requires the boundary); and that a statement about
platform causality is sequencing content owned by `orchestration/` (it is a domain
fact; the imperative form was removed so it cannot read as a rule).

Also rejected in round 1 and still settled, per D-51: that the verification
checklist is a narrowed copy of the evidence record, and that domain instantiations
inside a specialist definition are duplication.

**One finding accepted as a condition rather than a reversal.** The approved
reconciliation states that folding the coordinators "requires choosing or
parameterising the handoff contract". The fold was applied and the contract
deferred, so no consumer can resolve a handoff today. The fold's identity half is
sound and stays; the unpaid prerequisite is recorded as `STATE.md` open work 29c and
blocks further agent migration.

### Round 3, the final audit, on the corrected state at `df33f07`

One reviewer, same blind conditions, asked plainly whether the step could be
declared complete. Answer: not yet, with eight findings. All eight verified and
closed at `1a91d32`.

| Finding | Verification | Resolution |
|---|---|---|
| A **fourth** formula `must` was softened into an attribution, with nothing recording whether it was met. Its three siblings were recorded as owed | Confirmed against `NOTION-SYSTEM-DEPENDENCIES.json implications[0]`, and confirmed absent from every approved record. The earlier sweep found three of four | Stated as the obligation it is, with how it is met. D-62 |
| The pre-routing obligation is genuinely unowned -- the reviewer independently confirmed the gap claim against the rule -- but was recorded only inside the governed artifact | Confirmed by reading `rules/ENGINEER-OWNERSHIP.md`: it governs when to ask and states neither the required-fields nor the decision-brief obligation | Recorded in `STATE.md` open work as well. D-63 |
| A route's `output` and a definition's `outputs` state the same agent's deliverables differently, with no owner and no record; it would replicate across ten remaining migrations | Confirmed: 3 items versus 5, not a subset, both carried from source | The definition governs; the relationship is stated in the routing file. D-64 |
| Backoffice narrative remained in six named locations, including a schema description arguing with its predecessor and a migration-progress sentence in the catalog beside the sentence denying it holds migration state | Each read directly. The reviewer fairly noted that lineage is authorised and argument is not, which is the line D-52 drew | Trimmed to lineage. The surfaced gap stays, stating the gap rather than narrating the source |
| `STATE.md`'s own header said 2026-08-19 and "reconciliation assessment in progress" while its body recorded Steps 1 and 2 applied | Confirmed. The file that owns current state carried a stale header, and its own text says to replace stale content | Corrected |
| **Three false passes in the fidelity script.** It passed a tree with the whole consequences section deleted; it exempted a falsified name whenever a responsibility marker was present; and reverting the one required divergence passed while the check count silently dropped from 19 to 18 | All three reproduced by the reviewer with commands and output | Implications are now checked individually; a name needs its own marker; an exemption **requires** its divergence. D-65 |
| `README.md` asserted the registry was a canonical source for "where work goes" while the registry disclaims routing | Confirmed by reading both | Routing owns where work goes; the registry owns who the agents are |
| `docs/README.md`'s recorded **Adapt** disposition was absent from the remaining-migration ledger, in the change that edited its target | Confirmed. It also carries two further uncarried source obligations about workspace-relative paths | Added to `STATE.md` item 29 |

**Further tooling defects the audit demonstrated, all closed:** two source governance
blocks the approved record names were missing from the leak list and markdown was
never scanned; ten of the fourteen real references in the new artifacts went
unexamined because only two JSON keys were read; a governance document was accepted
as a resolved schema declaration because the file existed; the reference check would
have failed the next legitimate edit naming `runtime-adapters\`,
`governance-templates\` or `STATE.md`; an orphan definition file, a retired identity
still used as a route destination, and a domain carrying routes that domain selection
cannot select all passed; and nothing enforced the one invariant all three checks
exist to protect -- that these artifacts grant no permission. A fabricated
`"permission": "The orchestrator may approve its own structural changes."` passed
every check.

**One finding confirmed authorised rather than fixed.** The reviewer flagged that the
template's recorded disposition is `Keep` while a rename and a value change were
applied, and said it could not verify authorisation from the decision window it was
given. Both are authorised: D-50 for the value, D-58 for the identifier convention.
The reviewer named the limit correctly rather than assuming.

## The surfaced conflict, resolved

Two accepted records disagreed about whether domain knowledge may live in
`context/`: the taxonomy's gloss said "scoped operating context, **not knowledge or
authorization**", and the accepted Step-1 target tree assigned
`context/ domain knowledge, e.g. the quadruplicated formula notes`. The artifact
created here was exactly the case they disagreed about. Surfaced rather than
resolved silently, and escalated to the taxonomy owner.

**Resolved by the taxonomy owner, 2026-08-21.** `context/` owns scoped knowledge and
supporting operating context, and owns no governance, permissions, approvals,
boundaries, behavioral obligations, verification authority or precedence. The gloss
is superseded; the target tree stands. `context/NOTION-FORMULA-V2.md` is confirmed
correctly placed on the ground the reframing had already established: it carries
supporting domain knowledge, absorbs no obligation, and grants no authority.

Two additions came with the resolution and are wider than this step: a file is not
mandatory merely because it sits under `context/` -- it loads only when routed; and
general reusable capability knowledge belongs in global machine-level context while
exact domain implementation belongs in domain or project context.
`plans/AGENT-HUB-CONSOLIDATION.md` sections 6.2a and 6.2b; `DECISIONS.md` D-66 and
D-67.

### What the resolution changed after Step 2 closed

Applied at `c384c60`, on top of the completed step:

- The three places in the Hub that carried the superseded phrase "scoped operating
  context" now carry the canonical wording. That phrase came from the definition the
  resolution replaced, so leaving it would have kept the resolved conflict alive in
  the Hub's own text.
- Two clauses from the resolution were missing from the Hub and are now readable
  there: a file under `context/` is not mandatory because it exists, and a runtime
  adapter may load or expose an artifact but must not redefine what it owns.
- `NOTION-FORMULA-V2.md` was moved to `context/global/services/notion/` and then
  **moved back**. The owner corrected the model: there is no `global/` folder, because
  the Hub is itself the global layer. The file sits at `context/NOTION-FORMULA-V2.md`,
  where the owner had confirmed it one message earlier. Recorded as an error of mine,
  not a design change: a sample tree is not authority to relocate an accepted
  artifact. `DECISIONS.md` D-69, `LEARNINGS.md` L-033.
- No empty branches were scaffolded. Every other directory in the accepted global
  shape arrives with its first accepted artifact.
- The adapter domain's accepted name is now `adapters/`, superseding
  `runtime-adapters/`. Surfaced as a supersession, not applied silently: two accepted
  records and two earlier decisions use the old name. Nothing is built, so it is a
  rename of an unbuilt domain, and the catalog states the accepted names.

## Verification performed

Three scripts, all re-runnable from this repository, all run against the tree
extracted from `origin/main` rather than only against a working copy, and each
proven against injected defects in both directions.

| Script | Assertions | Result | Proven by |
|---|---|---|---|
| `scripts/Test-HubRegistrySchema.py` | 32 | PASS | Duplicate id, a definition contradicting its entry, an orphan definition file, a retired identity used as a route destination, a domain unreachable from domain selection, a permission-shaped key, a schema declaration resolving to a non-schema, a missing routing artifact, and a corrupted `entry_point` domain each produce exit 1 |
| `scripts/Assert-HubSourceFidelity.py` | 21 | PASS | A reworded route output, a softened agent rule, a falsified agent name, a changed template field, a **reverted** required divergence, a deleted implications section, an injected source governance block, a removed citation and a removed platform capability each produce a FAIL |
| `scripts/Assert-ReferenceIntegrity.py` | 58 tokens, plus URI semantics and catalog coverage | PASS, 0 dangling | A dangling backtick path, a dangling markdown link target, a broken cross-owner pointer inside an authority block, a relative `$id`, a schema declaration to a non-schema, and an unindexed artifact are each detected; the documented-as-absent tokens are correctly not flagged |

Eleven defect trees built from the fifth audit's own demonstrations are retained as
regression cases; each produces a non-zero exit from at least one check, and the
clean tree passes all three.

What the fidelity script checks, which nothing checked before: all 11 routes
byte-identical to source in source order; the pre-routing condition exact; every
source routing destination present; the five carried agent-definition fields
identical; every registry identity string either the source string or marked as
authored; every source agent id resolving as a live id or a recorded fold; the
template field set unchanged and every value unchanged except one recorded
exemption; every source citation and every named platform capability still present;
the four source keys named in provenance; and no source governance block --
`escalation_rules`, `communication_style`, `decision_rules`, `handoff_contract`,
`core_responsibilities`, `dependency_chain` -- present in any Hub artifact.

`design-systems/` untouched throughout: zero lines in every staged diff, blob hash
unchanged.

### The reference checker needed four model corrections and two bug fixes

Each produced a false positive that would have damaged correct content. Recorded
because the checker is now durable tooling.

1. **A token that asserts its own absence is not a broken reference.**
   `CATALOG.md` names `policies\`, `prompts\`, `skills\`, `tools\` and `runbooks\`
   in the sentence stating they are intentionally absent. Now documented
   exceptions, with the reason, beside the existing `design-systems\.remember\`.
2. **Reference resolution is scoped to one repository.** The context file cites
   paths inside `agents-hub-two`. Cross-repository prefixes are now out of scope,
   the same treatment absolute Windows paths already had, and the cited paths carry
   the repository name so scope is explicit in the token.
3. **A URN or URL in a path-valued JSON field is not a path.** The Markdown side
   already exempted them; the JSON walker did not, so the schema's own `$id` and
   meta-schema URL were reported as dangling.
4. **But exempting them was the wrong fix for `$id`.** `$id` is a URI, not a path,
   and it must be *absolute*. Exempting it meant the correct form was never checked
   and a relative `$id` -- the predecessor schema's defect -- resolved as a path and
   passed. It is now validated by URI semantics. An instance `$schema` is the
   opposite case: a relative path there is legitimate and must resolve.

Two outright bugs, both found by audit rather than by use: the out-of-scope counter
was incremented twice per token, so the printed coverage figure was exactly double;
and a capability check used case-sensitive patterns, so `Multi-line`, `Type-aware`
and `Dot notation` read as absent from a file that stated all three. A third,
found while writing this: a shell `grep '[^\x00-\x7F]'` used to check for non-ASCII
matched every line, because GNU grep does not interpret `\x` escapes without `-P`.
Each is the same lesson in a new place -- a check is not evidence until the check
itself is checked.

A fourth correction came from misusing the checker rather than from its model.
Pointed at this backoffice it reported **1022 dangling references**, essentially
all false: bare filenames in prose, git refs such as `origin/main`, `owner/repo`
names, and paths inside other repositories. The check is calibrated for a
self-contained governance tree, and a run like that is worse than no run because
1022 findings look like a result. The script now refuses to run outside the Hub
rather than relying on the operator to remember its scope. A backoffice profile
does not exist.

It also crashed on the first backoffice JSON file it read, because that evidence
carries a UTF-8 BOM (`DECISIONS.md` D-36) and a strict `utf-8` read rejects it. It
now reads `utf-8-sig` and reports an unparseable file as a failure rather than
skipping it: an unreadable file is an uncovered file, not a passing one.

One real defect was found while sweeping: `CATALOG.md`'s closing line routed
placement decisions to `C:\KloWorkspaces\workspace-governor\HUB-ARCHITECTURE.md`,
which does not exist here. The only copy is
`plans/reference/HUB-ARCHITECTURE-predecessor.md`, never an authority (D-j). The
line now routes to `plans/AGENT-HUB-CONSOLIDATION.md`.

## What Step 2 does not do

- **No second agent definition.** Eleven identities are accepted with no
  definition; the agent-definition schema gates the next one.
- **No topology or sequence artifact**, no `shared_dependencies` or
  `specialist_agents` maps, no `planning_model`. Recorded as deferred in the
  routing file.
- **No handoff template.** Declared five times with five different field sets and
  having no file. Reconciling it needs the contract decided.
- **No evidence-record template.** Gap surfaced by the review; the source's
  `execution_record_template` is the candidate.
- **No `policies/`, `prompts/`, `skills/`, `tools/` or `runbooks/`.**
- **No prompt migration.** The four source prompts hardcode `./package-layout.json`
  and `./agents/...` and also carry role definition, operational rules and an
  output-format block that overlaps `rules/ENGINEER-OWNERSHIP.md` § Communication.
  Adapter material; they wait for Step 9. Revision 1 described them as loading
  instructions only, which understates their content.
- **`design-systems/` untouched.** Still `Conflict`, still preserved.

- **No carrier for three source obligations.** Recorded as owed in `STATE.md` open
  work 29a, with their intended owners named. A record is not a carrier; the record
  exists so the carrier is not forgotten. `DECISIONS.md` D-61.
- **No handoff contract**, and the fold's stated prerequisite for it is unpaid.
  Open work 29c; it blocks further agent migration.
- **No answer for a domain-selected request that matches no trigger.** The gap is
  inherited from the source and is now stated in the owning file rather than left to
  be discovered at use. Open work 29e.

## Not verified

- **Runtime discovery.** No runtime is known to read any of these files. Presence
  is not discovery, loading, activation or enforcement. The fresh-session bootstrap
  assignment is now broader: it should establish whether a new session finds the
  root contract, and whether `README.md` step 4 actually leads an agent into the
  routing file.
- **Whether anything validates the registry in a runtime.** The schema is proved
  correct against its instance by a script run here. Nothing runs it
  automatically.
- **The cited Notion documentation URLs.** Carried as cited; not fetched.
- **Semantic fitness of the migrated content.** Fidelity to the source is
  verified. Whether the source's triggers and specialist boundaries are *good* is
  a separate question this step does not answer.
