# Step 2 -- first accepted artifact per domain

**Date:** 2026-08-21
**Revision:** 2. Revision 1 described the artifacts as first written. Two
independent adversarial reviews then found sixteen fidelity findings and thirteen
governance findings; the artifacts were reworked before anything was committed, so
revision 1 never described committed content. Revision 1 is superseded in place.
**Scope:** Create `agents/`, `orchestration/`, `registry/`, `templates/` and
`context/` in the canonical Hub, each with its first accepted artifact.
**Authorisation:** User, 2026-08-21: "proceed with Step 2".
**Source:** `agents-hub-two` @ `0a222df`. Classification carried from
`evidence/AGENTS-HUB-TWO-RECONCILIATION-2026-08-20.md` revision 2 and
`evidence/HUB-TARGET-TREE-AND-CLASSIFICATION-2026-08-21.md`.
**Base commit:** `c6c966b`. **Result commit:** `d1a8553`, verified on the live
remote and by extracting `origin/main` and re-running both checks against the
extraction.

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
source states. The routes are now **generated from the source files** by the
build step that wrote the artifact, so "verbatim" is true by construction rather
than by assertion.

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

## Adversarial review -- findings accepted and rejected

Two independent reviews ran before commit: one on fidelity to the source, one on
governance boundaries. Every finding was verified against source or rule text
before being accepted or rejected. Both reviews were read-only.

### Accepted and fixed

| # | Finding | Verification |
|---|---|---|
| 1 | `authored_additions` claimed the source had no domain-selection step | False. `package-layout.json` notes[1], `docs/README.md` § Canonical entry points and § Typical usage step 2, and `prompts/general-coordinator.prompt.txt` all state it. Read directly |
| 2 | Entry point "declared three times" undercounts | Eight locations, including `meta.notes` and `meta.note` in the two coordinators and `docs/README.md`, none of which revision 1 listed. All read directly. The count is now replaced by the enumerated list |
| 3 | The registry claimed a per-domain orchestrator model while holding one orchestrator, in the `general` domain | Confirmed. `notion-operations` had no orchestrator. Fixed by `domain: "shared"` plus an explicit `folded_from` record |
| 4 | `agents[0].responsibility` was an unmarked new sentence, and asserted ownership of a handoff contract the same migration declares unmigrated | Confirmed against `config/agent-registry.json non_notion_agents[0].role`. Now shorter, no handoff claim, and marked with `responsibility_source` |
| 5 | `name` silently shortened from "General Coordinator / Orchestrator" | Confirmed. Correct under the fold, but unrecorded. Now recorded |
| 6 | `workspace_root` dropped with no supersession record | Confirmed: the source has eight top-level keys and only four were accounted for. Now listed |
| 7 | `docs/README.md` unaccounted for while the routing file claimed exhaustive supersession | Confirmed. Added |
| 8 | The orchestrator was omitted from the context file's consumer list, and the source's `must_acknowledge` modality was lost | Confirmed: the block's key is literally `must_acknowledge`, placed on the coordinator. Orchestrator restored as a consumer, obligation stated as the source's |
| 9 | "its own failure modes" appears in no source block, and a source `must` was reclassified as "not an instruction" | Confirmed. Reworded to attribute the statement to the source with its force intact |
| 10 | A context bullet came from the agent's `rules`, not the four formula blocks, and duplicated a verification obligation | Confirmed. That bullet is removed: what counts as evidence is owned by `rules/VERIFICATION-AND-EVIDENCE.md` |
| 11 | `validated_references` narrowed from subsystem scope to formula scope, unrecorded | Confirmed. The narrowing is now stated in the file, and all four URLs retained |
| 12 | `meta.created` silently dropped; `purpose` reworded | Confirmed. Both restored from source |
| 13 | "validated against 8 negative cases" had no artifact anyone could re-run | Confirmed -- agent confidence stated as verification. Now `scripts/Test-HubRegistrySchema.py` |
| 14 | `not_yet_migrated` under-enumerated the deferred dependency-file content | Confirmed. `shared_dependencies`, `specialist_agents` and `planning_model.initial_assessment` added |
| 15 | `pre_routing` restated the intake obligation more broadly than its owner | Confirmed. `rules/ENGINEER-OWNERSHIP.md` bounds asking to "when a missing decision would materially change the outcome, exceed granted authority, or require user or business judgment"; the carried text made a decision brief the default for any unclear request. The entry now records only the routing consequence and names the owner |
| 16 | Migration narrative, retirement arguments and progress ledgers written into live artifacts | Confirmed against the directive: management, migration and consolidation-progress state do not belong in the live Hub, and § 6.8 requires no backoffice history in live authority. Reduced to short provenance identifiers in all six artifacts; narrative lives here |
| 17 | `CATALOG.md` asserted session verification results as durable status, without the "runtime activation unverified" qualifier every other row carries, and made three claims untrue of the artifacts | Confirmed. Rewritten |
| 18 | The `$schema` field was outside the reference sweep's scope, so "0 dangling" did not cover it | Confirmed -- the same defect class as D-39: a check whose scope was assumed. The sweep now covers `$schema` and `$id`, with URL and URN exemptions |
| 19 | `context/` self-described as "Domain knowledge only" while the taxonomy says `context/` is "not knowledge or authorization" | Confirmed as a real contradiction. Reframed as operating context. **The underlying conflict is not resolved by that reframing** -- see § Open conflict |
| 20 | Everything was uncommitted while the catalog described it as active canonical source | Confirmed at the time. Committed at `d1a8553` |

### Rejected, with reasons

| Finding | Why rejected |
|---|---|
| The verification checklist template is a narrowed parallel answer to `rules/VERIFICATION-AND-EVIDENCE.md` § Proportionate Evidence Record | Two different artifacts. The rule's § Proportionate Evidence Record governs what an **evidence record** contains after a change; the template is a **pre-action checklist**, which the same rule's § Verification Standard asks for: "Define the evidence needed in proportion to risk before acting." No duplication. It did surface a real gap: no accepted evidence-record template exists, and the source's `execution_record_template` is the candidate. Recorded as open work, not fixed here. `CATALOG.md` now states the distinction so the checklist is not mistaken for the record |
| The migrated agent's `rules.must_do` / `must_not_do` restate verification, assumption-recording and communication obligations owned by `rules/` | These are **domain instantiations**, which the reconciliation settled as legitimate and required: "Deleting those leaves the domain with no statement of what evidence counts." "Verify formula output against actual database data, not just syntax" states what evidence counts *for formulas*; the general obligation stays with its owner. Reopening this would reverse a settled finding without new evidence. The definition now names the boundary explicitly in its `authority` block |
| "Validated after the schema change, not before" is sequencing content belonging in `orchestration/` | The taxonomy's "sequencing" concerns ordering of agents and steps, not a statement about platform causality. This is a domain fact: a formula that depends on a retyped property behaves differently after the change. Reworded to remove the imperative form so it cannot be read as a rule |

## Open conflict -- surfaced, not resolved

The accepted taxonomy says `context/` holds "scoped operating context, **not
knowledge or authorization**". The accepted Step-1 target tree says
`context/ domain knowledge, e.g. the quadruplicated formula notes`. Those two
accepted records disagree about whether domain knowledge may live in `context/`,
and the artifact created here is exactly the case they disagree about.

The file has been reframed as operating context -- platform behavior needed to plan
and check work correctly -- and the authorization half is unambiguously satisfied:
it states that it grants nothing. That reframing makes the artifact defensible
under either reading. It does **not** settle which reading governs, and the
question returns the moment a second context artifact is proposed. Surfaced per
the hub root contract rather than resolved silently. The taxonomy owner decides.

## Verification performed

Both checks are scripts in this repository, so the results are reproducible rather
than asserted. Both were re-run against the tree extracted from `origin/main`, not
only against the working copy.

`python3 scripts/Test-HubRegistrySchema.py <hub>`

| Case | Required | Result |
|---|---|---|
| Schema is valid draft 2020-12 | valid | PASS |
| Live instance validates | 0 errors | PASS |
| Pending entry naming a definition | rejected | PASS |
| Migrated entry with null definition | rejected | PASS |
| Unknown top-level key -- the predecessor schema's real defect | rejected | PASS |
| Unknown key inside an agent entry | rejected | PASS |
| Non-kebab id | rejected | PASS |
| `role_class` outside the classification | rejected | PASS |
| Missing `provenance` | rejected | PASS |
| Empty `agents` array | rejected | PASS |
| A second orchestrator entry -- the model the predecessor schema forbade | **accepted** | PASS |
| Every `route_to` resolves to a registry id | 0 unresolved | PASS |
| Every route domain exists in the registry | 0 unknown | PASS |
| No registry specialist is unroutable | empty | PASS |
| `entry_point` resolves to a registry id | true | PASS |

`python3 scripts/Assert-ReferenceIntegrity.py <hub>`

| Check | Result |
|---|---|
| Every backtick path in every live Markdown file, plus every `$schema`, `$id`, `definition` and `path` field in every JSON file | **46 tokens checked, 0 dangling** |
| Fabricated references detected before restore | 3 of 3 Markdown/JSON cases, then 0 after restore |
| `design-systems/` untouched | 0 lines in the staged diff; blob hash unchanged |

Route fidelity is not in either script: the routes are built from the source files
at authoring time, so a divergence is impossible rather than untested.

### The reference checker needed three model corrections

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
