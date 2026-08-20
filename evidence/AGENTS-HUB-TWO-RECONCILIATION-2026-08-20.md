# Reconciliation -- `agents-hub-two` artifact by artifact

**Date:** 2026-08-20
**Revision:** 2. Revision 1 contained five material errors, corrected below and
listed in § Corrections. Revision 1 is superseded in place because it was issued
the same day and leaving its wrong findings standing would be worse than a
same-day revision. The dated-baseline supersession rule applies to inventories
with downstream consumers, not to a same-day correction of the authoring error.
**Source:** `agents-hub-two` @ `0a222df`, 27 files, 65,519 bytes. All 27 read.
**Method:** actual file content, field level. **Revision 2 additionally verified
every claim by direct re-read after an independent adversarial review.**
**Status:** Reconciliation analysis. **No source repository modified. Nothing
applied.** Approval required before restructuring (`plans/AGENT-HUB-CONSOLIDATION.md` § 6.7).

## Corrections to revision 1

Found by an independent adversarial subagent review, then verified by the parent
agent against source. All five are confirmed.

| # | Revision 1 claimed | Actually true | Cause |
|---|---|---|---|
| C1 | "Both coordinators carry the same key set" -- eight keys listed | Both carry **15** keys. Revision 1 never saw `escalation_rules`, `dependency_chain` or `meta` | **Authoring defect: my own key listing was truncated to the first 12 keys, and I then reasoned as though it were complete.** The same class of error as reporting a filtered result as a full one |
| C2 | "At field level it is four of four templates Notion-specific", correcting an earlier three-of-four | `templates/verification-checklist-template.json` is **domain-neutral**: `check_name`, `method`, `expected_result`, `pass_criteria`, `fail_criteria`, `human_review_required`, `notes`. The earlier three-of-four was right; revision 1 was a **regression** | Two contracts disagree on *synonyms* (`expected_result` vs `expected_output`), which I read as a domain field set |
| C3 | "`task-brief-template.json` matches the Notion task-brief contract" | It matches **`NOTION-COORDINATOR-ORCHESTRATOR.handoff_contract.required_fields`** -- all 10 fields, same order, plus 2 extras. It is the **handoff** artifact under a task-brief filename. No conforming task-brief template exists | **Classified from its filename**, in a document whose method line disclaims exactly that |
| C4 | The `decision_rules.must_not_do` boundary restatement described as a property of both coordinators | Only the **general** coordinator restates boundaries. The Notion coordinator's four items are schema, formula-migration, ambiguity and approval-authority rules -- three are legitimate domain specialisation | One file's content generalised to a class of blocks |
| C5 | Four duplicated governance blocks | **Five.** `escalation_rules` is present in both coordinators and is the most literal duplication in the repository | Consequence of C1 |

A sixth defect, in citation rather than finding: revision 1 named
`rules/ENGINEER-OWNERSHIP.md`, `rules/AUTONOMY-AND-PROTECTED-BOUNDARIES.md` and
`rules/VERIFICATION-AND-EVIDENCE.md` as bare paths. Locally, `rules/` holds only
`VERIFICATION-RESOLUTION.md`; those three live in the canonical Hub. Under this
repository's own evidence standard that was an unverified citation. Corrected
throughout to `.agents-hub/rules/...`.

## Summary of what this repository actually is

An **agent operating package** for two domains -- a general implementation domain
and a Notion operations domain -- each with a coordinator, a set of specialists,
a dependency/topology file, and shared output templates. It is not a governance
tree. Its 15 `agents/*.json` files are 13 agent definitions plus **2 files that
are not agents at all**.

## Finding 1 -- the entry point is declared three times, inconsistently

| Declaration | Value |
|---|---|
| `config/agent-registry.json` -> `entry_point` | Notion coordinator **only** |
| `package-layout.json` -> `entry_points` | **Both** coordinators |
| `prompts/notion-coordinator.prompt.txt` | Names an agent file as "the entry point"; the other three name no agent entry point |
| `schemas/agent-registry.schema.json` | A **fourth, machine-readable** declaration: `entry_point` typed as a single **string** and `coordinator` as a single **object** |

A general, non-Notion request entering through the registry's declared entry point
reaches the **Notion** coordinator. One owner is required: `orchestration/`.

**This is an executable defect, not only a declaration inconsistency.**
`prompts/general-coordinator.prompt.txt` instructs the general coordinator to
"route work to the correct specialist using the workspace registry in
`./config/agent-registry.json`" -- a registry whose `routing_rules` contains a
`notion` key only. A general coordinator following its own prompt finds **no
routing rules for any of its six specialists**.

## Finding 2 -- routing logic exists in four places at three fidelities

| Location | Coverage | Fidelity |
|---|---|---|
| `AGENT-COORDINATOR-ORCHESTRATOR.routing_logic` | **6 routes plus 1 differently-shaped rule** | trigger + route_to + output, except `patterns[0]` ("Business request with unclear requirements") which has **no `route_to` and no `output`** and uses an `action` key -- a pre-routing clarification rule, not a route |
| `NOTION-COORDINATOR-ORCHESTRATOR.routing_logic` | 5 Notion routes | trigger + route_to + output |
| `NOTION-SYSTEM-DEPENDENCIES.routing_logic` | the **same 5** Notion routes | trigger + route_to + output, **differently worded** |
| `config/agent-registry.json` -> `routing_rules` | 5 Notion ids **only** | bare id list, no triggers |

The two Notion copies are the same five routes with different trigger phrasing and
slightly different declared outputs -- semantic duplicates, not textual ones. The
registry's `routing_rules` covers Notion only; the seven general agents sit in
`non_notion_agents` with **no routing rules at all**. Asymmetric and incomplete.

## Finding 3 -- template contracts disagree with the template files

Five template contracts are declared in **both** dependency files with **different
required fields**, and only four template files exist.

| Concept | File on disk | Verdict |
|---|---|---|
| verification checklist | `check_name`, `method`, `expected_result`, `pass_criteria`, `fail_criteria`, `human_review_required`, `notes` | **Domain-neutral.** Satisfies the Notion contract 6/6. The two contracts differ only in synonyms -- `expected_result`/`human_review_required` vs `expected_output`/`human_action_required`. The only unique field is `notes`, in neither contract |
| execution record | Notion field set | Notion-specific. **Missing the Notion contract's required `absolute_or_workspace_paths`** |
| technical spec | **Hybrid** | Carries `business_rules` and `risks`, which appear only in the **general** contract; missing Notion's required `related_databases` and `properties_affected`; has `properties_involved`, a third name. Plus `assumptions` and `expected_behavior`, in neither contract |
| task brief | Matches the **Notion coordinator's `handoff_contract.required_fields`** -- 10 fields, same order, plus `open_questions` and `dependencies` | **Misnamed.** It is the handoff artifact. It covers only 3 of 9 Notion task-brief fields and 2 of 8 general ones |
| handoff | **no file** | Declared **four** times with four different field sets: both dependency files' `handoff_template`, and `handoff_contract.required_fields` in **both** coordinators. A fifth variant exists as `handoff_format` in `AGENT-RESEARCH-DOCUMENTATION.json` |

**Corrected conclusion.** Three of four template files are Notion-specific; the
verification checklist is domain-neutral. One file is misnamed and is really the
handoff artifact, so **no conforming task-brief template exists**. Only the
verification checklist fully satisfies its own contract. The earlier
three-of-four figure in `evidence/HUB-RECONCILIATION-ASSESSMENT-2026-08-19.md`
was correct and is reinstated.

## Finding 4 -- topology and sequence duplicated

`system_model` (owner / coordinator / specialist_agents) and
`agent_creation_sequence` appear in both dependency files, same shape, different
domain. Both are orchestration concepts, not agent definitions.

## Finding 5 -- four governance concepts restated inside agent definitions

Semantic duplication of Hub-owned governance, found by comparing obligations
rather than wording. None of it may be carried into the Hub.

| Block | Verdict | Existing owner |
|---|---|---|
| `escalation_rules` -- "Escalate to a human executor for any action that requires MFA, account ownership, bank payment, or secret-based flow" (general coordinator) | **CONFIRMED. The most literal duplication in the repository.** Missed in revision 1 | `.agents-hub/rules/AUTONOMY-AND-PROTECTED-BOUNDARIES.md`; `AGENT-SSOT.json` § `execution_constraints.cannot_do` |
| `ownership` | **OVERSTATED.** Only the `user:` line restates the authority split. The `agent:` line enumerates the coordinator's functional scope -- role definition, not governance -- and the two coordinators' blocks differ. Stripping the block wholesale destroys the role definition | `.agents-hub/rules/ENGINEER-OWNERSHIP.md`; `AGENT-SSOT.json` § `escalation_and_ownership` |
| `decision_rules.must_not_do` | **CONFIRMED for the general coordinator only.** Its items 1-2 restate boundaries. The Notion coordinator's four items are schema, formula-migration, ambiguity and approval-authority rules -- three are legitimate domain specialisation | as above |
| `decision_rules.must_do` | **CONFIRMED, missed in revision 1.** Carries two further restatements: "Keep the communicative style direct, structured, and action-oriented" and "Never present the coordinator as the business owner or decision-maker" | `AGENT-SSOT.json` § `communication_and_format`; ownership owners above |
| `communication_style` | **CONFIRMED.** Duplicates tone and the requirements-translation obligation | `AGENT-SSOT.json` § `communication_and_format`, § `requirements_translation_and_specification` |
| Response format -- Action / Status / Next | **CONFIRMED and understated in revision 1.** Restated in **six** places: both coordinators' `handoff_contract` (as `output_format` and `response_format`) and all four `prompts/*.prompt.txt` | `AGENT-SSOT.json` § `communication_and_format.response_format` |
| `verification_rules` | **CONFIRMED for the general coordinator.** The Notion coordinator's are domain instantiations -- "check the actual database behavior", "pass/fail evidence for formula, relation, view, automation fixes". Deleting those leaves the domain with no statement of what evidence counts | `.agents-hub/rules/VERIFICATION-AND-EVIDENCE.md`; `AGENT-SSOT.json` § `verification_and_audit` |
| Specialist boundary restatements | **Only two exist**, both missed in revision 1: `AGENT-PAYMENTS-BILLING.rules.must_not_do[0]` and `AGENT-IAM-ACCESS.rules.must_not_do[1]` | as above |

Revision 1's claim that `communication_style`'s absence from the Notion
coordinator evidenced incidental copying is **wrong**: the Notion coordinator
carries the same obligation in `decision_rules.must_do`. The asymmetry is key
placement, not content.

## Finding 6 -- the Notion coordinator is not a separate agent

Decided from content, as the directive requires.

Both coordinators carry **15 keys**, identical at top level except one swap --
`communication_style` on the general, `notion_formula_v2_guidance` on the Notion.
**Nested, they differ**: `handoff_contract.output_format` vs `.response_format`;
`meta.notes` vs `meta.note`; `dependency_chain` lists the four templates in the
general file and only agents in the Notion file. Routing shape is
trigger -> route_to -> output in both, **except** the general coordinator's
`patterns[0]`, which uses `action` and routes nowhere.

**Conclusion: one general orchestrator plus domain-specific orchestration
definitions.** The Notion coordinator is the same orchestrator role instantiated
for a domain, not a distinct agent. Its genuinely distinctive content -- Notion
formula v2 behavior, database-behavior verification -- is **domain knowledge**,
which belongs in `context/` or the domain orchestration definition, not in a
second coordinator identity.

Specialist separation is **preserved**. The five Notion and six general
specialists have materially different responsibilities, inputs and outputs; they
are not flattened.

**Cost of folding, not stated in revision 1.** The two
`handoff_contract.required_fields` sets share only **4 of 10** fields
(`task_name`, `specialist_agent`, `acceptance_criteria`, `verification_steps`),
and only the Notion one has a template file on disk. Folding requires choosing or
parameterising the handoff contract. The Notion coordinator also escalates to "the
relevant team or owner if the database change affects a critical workflow" -- a
third-party escalation target with no general-coordinator equivalent.

## Finding 6b -- the registry schema cannot express the model it validates

Missed in revision 1. Verified directly.

`schemas/agent-registry.schema.json` declares `required` and `properties` over six
keys only: `name`, `workspace_root`, `version`, `entry_point`, `coordinator`,
`specialists`. The live registry has **eight** keys. `non_notion_agents` and
`routing_rules` are **absent from `properties`**, and there is **no
`additionalProperties: false`**, so the seven general agents and every routing
rule pass through **unvalidated**. The schema validates only the Notion half.

It also types `coordinator` as a single object and `entry_point` as a single
string, so it **structurally forbids the two-coordinator model** the repository
implements. That is schema-level evidence *for* Finding 6 and *against*
`package-layout.json`'s two entry points.

Separately, `$id` is `"./schemas/agent-registry.schema.json"` -- a relative
reference. Draft 2020-12 requires an absolute URI, so the schema will not resolve
in a standard validator.

## Finding 6c -- two incompatible agent-definition shapes, and no schema for either

Missed in revision 1. The two coordinators use `core_responsibilities`,
`decision_rules{must_do,must_not_do}`, `handoff_contract`, `dependency_chain`. All
eleven specialists use `primary_responsibilities`, `rules{must_do,must_not_do}`,
`dependencies` -- the same concepts under different keys. `schemas/` covers agent
definitions **not at all**.

For a consolidation whose objective is one `agents/` folder with one owner per
concern, this is the real structural blocker.

## Finding 6d -- Notion formula knowledge is quadruplicated

Missed in revision 1, which mentioned it twice only in passing. The same domain
knowledge appears in four files under four different key names:
`NOTION-COORDINATOR-ORCHESTRATOR.notion_formula_v2_guidance`,
`NOTION-SYSTEM-DEPENDENCIES.notion_formula_v2_notes`,
`NOTION-FORMULA-LOGIC-AGENT.formula_2_0_notes`,
`NOTION-SCHEMA-RELATIONS-AGENT.notion_formula_v2_considerations`.

This is the largest genuine content duplication in the repository and the
strongest concrete argument for a `context/` extraction.

## Finding 6e -- template identifiers use two naming conventions

Agent files reference `"task-brief-template"` with hyphens; dependency files
declare and reference `"task_brief_template"` with underscores. Any consumer
resolving dependencies needs a mapping table.

## Finding 7 -- stale identity claim

`docs/README.md` calls the package "the canonical workspace" and states its root
"is the `.agents-hub` folder itself". `package-layout.json` sets
`"name": "agents-hub"` and notes that internal references are relative to
`.agents-hub`. Superseded by D-24 and D-26: `agents-hub-two` is source material
pending reconciliation, not an authority. Correcting the claim is reconciliation
work, not an open question.

## Per-artifact disposition

Record fields: purpose, canonical owner, disposition, overlaps, references, runtime implications.

| Artifact | Actual purpose | Canonical owner | Disposition |
|---|---|---|---|
| `agents/AGENT-COORDINATOR-ORCHESTRATOR.json` | General orchestrator: routing + 4 governance blocks | `orchestration/` for routing; governance blocks removed | **Adapt** -- split; strip Finding 5 blocks |
| `agents/NOTION-COORDINATOR-ORCHESTRATOR.json` | Notion orchestrator, same role | `orchestration/` domain definition | **Fold** into the general orchestrator + domain definition |
| `agents/AGENT-SYSTEM-DEPENDENCIES.json` | Topology, template contracts, creation sequence. **Not an agent** | `orchestration/` (topology, sequence); `templates/` (contracts) | **Move** + **Fold** |
| `agents/NOTION-SYSTEM-DEPENDENCIES.json` | Same, plus 4th routing copy, `validated_references`, `planning_model`, formula notes | `orchestration/`; formula notes to `context/` | **Move** + **Fold** |
| `agents/AGENT-{AUTOMATION-BUILDER, IAM-ACCESS, INTEGRATION, PAYMENTS-BILLING, REPORTING-DASHBOARD, RESEARCH-DOCUMENTATION}.json` (6) | General specialist definitions | `agents/` | **Adapt.** No specialist carries the coordinator governance blocks, so that work is zero here. The real work is key-vocabulary normalisation (Finding 6c), removing two boundary restatements (PAYMENTS-BILLING, IAM-ACCESS), and relocating `AGENT-RESEARCH-DOCUMENTATION.handoff_format` -- an output contract living inside an agent definition, which is `templates/` content |
| `agents/NOTION-{AUTOMATION, DATA-QUALITY-TROUBLESHOOTING, FORMULA-LOGIC, SCHEMA-RELATIONS, VIEWS-DASHBOARD}-AGENT.json` (5) | Notion specialist definitions | `agents/` | **Adapt.** Key-vocabulary normalisation, plus extracting the formula blocks per Finding 6d |
| `config/agent-registry.json` | Identity + classification + partial routing + entry point | `registry/` for identity; routing and entry point to `orchestration/` | **Adapt** -- split |
| `schemas/agent-registry.schema.json` | Declares itself the registry schema but omits two of the registry's eight keys, forbids the two-coordinator model, and has a non-resolving relative `$id` | `registry/`, or `policies/` if enforced | **Adapt / rewrite.** It does not describe its target. Ownership is the secondary question |
| `templates/verification-checklist-template.json` | Domain-neutral verification checklist | `templates/` | **Keep.** Retire the general contract's synonym fields rather than building a needless "general variant" |
| `templates/task-brief-template.json` | The Notion **handoff** artifact under a task-brief filename | `templates/` | **Adapt + rename.** Reconcile against the four handoff declarations, and record that no conforming task-brief template exists |
| `templates/{technical-spec, execution-record}-template.json` | Output templates; technical-spec is a hybrid, execution-record is missing a required field | `templates/` | **Adapt** -- reconcile against the declared contracts |
| `prompts/{general,notion}-{coordinator,specialist}.prompt.txt` (4) | Runtime bootstrap prompts naming relative paths and entry points | `prompts/` **only if** canonical and reusable | **Adapt** -- each hardcodes `./package-layout.json` and `./agents/...`; all break on restructure |
| `package-layout.json` | Package/distribution layout, second entry-point declaration | none -- `packages/` is not in the accepted taxonomy | **Retire for execution; provenance only.** Note the dependency: **all four prompts instruct reading it first**, so retiring it requires updating every prompt |
| `docs/README.md` | Navigation, stale canonical claim, **and runtime bootstrap** | `README.md` | **Adapt.** Keep navigation; drop the identity claim; and note that `## Typical usage` and `## Example prompt` duplicate `prompts/general-coordinator.prompt.txt` -- bootstrap content, not navigation. A second stale claim: it describes `./schemas/` as holding "validation schemas for generated config and templates", but no template schema exists |

## Runtime implications

- **Every internal reference is relative to a package root of `.`** -- `./agents/`,
  `./config/`, `./package-layout.json`. Restructuring into the Hub taxonomy breaks
  all of them. The four prompt files are the most fragile: they instruct an agent
  to read `./package-layout.json` first, a file classified as provenance-only.
- **The registry doubles as a routing table.** Splitting identity into `registry/`
  and routing into `orchestration/` means any consumer reading
  `config/agent-registry.json` for routing must be updated.
- **No runtime state is present.** No logs, caches, sessions, credentials or
  discovery output. Nothing in this repository violates the runtime-state boundary.
- **No secrets found.** No credential-shaped values in any of the 27 files.

## Open items for Step 1 and Step 3

1. Decide whether the declared general template variants are built or the
   declaration is retired. Do not silently keep contracts with no artifact.
2. Rewrite `agent-registry.schema.json` before deciding its owner. It omits two of
   its target's eight keys, forbids the two-coordinator model, and has a
   non-resolving `$id`. Also determine whether anything validates against it at
   all -- if nothing does, it is aspirational, not enforcement.
2b. Author a schema for agent definitions. There is none, and two incompatible
   shapes are in use (Finding 6c).
3. Decide whether the four prompts are canonical reusable prompts or runtime
   bootstrap belonging to `runtime-adapters/`. Their content is loading
   instructions, which suggests adapter, not `prompts/`.
4. Reconcile `validated_references` and `planning_model` in
   `NOTION-SYSTEM-DEPENDENCIES.json` -- not yet classified; they may be domain
   context or stale planning state.

## Not verified

Whether any runtime currently loads this package. Presence of a coordinator,
registry or prompt file is not evidence of discovery or activation -- predecessor
learning L-001 and the same rule in `rules/VERIFICATION-AND-EVIDENCE.md`.
