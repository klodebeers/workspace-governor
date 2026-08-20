# Reconciliation -- `agents-hub-two` artifact by artifact

**Date:** 2026-08-20
**Source:** `agents-hub-two` @ `0a222df`, 27 files, 65 KB. All 27 read.
**Method:** actual file content, field level. No artifact classified from its
filename. Every JSON parsed.
**Status:** Reconciliation analysis. **No source repository modified. Nothing
applied.** Approval required before restructuring (`plans/AGENT-HUB-CONSOLIDATION.md` § 6.7).
**Blocked portion:** none. This input required no live-Hub evidence, so it
proceeded while B-6 remains open.

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
| `prompts/*.prompt.txt` | Each prompt hardcodes its own entry path |

A general, non-Notion request entering through the registry's declared entry point
reaches the **Notion** coordinator. This is a live inconsistency in the source, not
an artifact of consolidation. One owner is required: `orchestration/`.

## Finding 2 -- routing logic exists in four places at three fidelities

| Location | Coverage | Fidelity |
|---|---|---|
| `AGENT-COORDINATOR-ORCHESTRATOR.routing_logic` | 7 general routes | trigger + route_to + output |
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

| Concept | `AGENT-SYSTEM-DEPENDENCIES` declares | `NOTION-SYSTEM-DEPENDENCIES` declares | File on disk |
|---|---|---|---|
| verification checklist | `expected_output`, `human_action_required` | `expected_result`, `human_review_required` | matches **Notion** |
| execution record | `objective`, `files_changed`, `commands_run`, `environment_assumptions`, `result`, `failure_modes` | `issue_summary`, `database_names`, `changes_made`, `formula_or_property_details`, `risks_and_follow_ups` | matches **Notion** |
| technical spec | `proposed_solution`, `data_requirements`, `system_dependencies`, `acceptance_criteria`, `risks` | `database_scope`, `related_databases`, `properties_affected`, `relation_paths`, `formula_logic`, `view_requirements`, `automation_rules` | matches **Notion** |
| task brief | `goal`, `context`, `constraints`, `required_data`, `dependencies`, `success_criteria`, `owner` | `issue_or_goal`, `database_name`, `expected_behavior`, `current_behavior`, `user_approval_points` | matches **Notion** |
| handoff | declared | declared | **no file exists** |

So: **all four template files carry the Notion field set, the general variants are
declared but unimplemented, and the handoff template is declared twice and exists
nowhere.** This corrects the earlier statement in
`evidence/HUB-RECONCILIATION-ASSESSMENT-2026-08-19.md` that three of four
templates are Notion-specific -- at field level it is four of four.

## Finding 4 -- topology and sequence duplicated

`system_model` (owner / coordinator / specialist_agents) and
`agent_creation_sequence` appear in both dependency files, same shape, different
domain. Both are orchestration concepts, not agent definitions.

## Finding 5 -- four governance concepts restated inside agent definitions

Semantic duplication of Hub-owned governance, found by comparing obligations
rather than wording. None of it may be carried into the Hub.

| Block | Restates | Existing owner |
|---|---|---|
| `ownership` -- user is business owner and decision-maker; agent does implementation | the ownership split | `rules/ENGINEER-OWNERSHIP.md`; `AGENT-SSOT.json` § `escalation_and_ownership` |
| `decision_rules.must_not_do` -- no budget or vendor approval without the user; no financial execution, contracts, or MFA-privileged actions | protected boundaries | `rules/AUTONOMY-AND-PROTECTED-BOUNDARIES.md`; `AGENT-SSOT.json` § `execution_constraints` |
| `communication_style` -- direct, action-oriented, precise; translate a rough request into implementation-ready language | tone, format, and requirements translation | `AGENT-SSOT.json` § `communication_and_format`, § `requirements_translation_and_specification` |
| `verification_rules` -- verify before implementing, require verification criteria, name human steps, mark blocked with the missing item | verification and evidence | `rules/VERIFICATION-AND-EVIDENCE.md`; `AGENT-SSOT.json` § `verification_and_audit` |

`communication_style` is present in the general coordinator and **absent** from the
Notion coordinator -- an asymmetry with no stated reason, and further evidence that
these blocks are incidental copies rather than owned content.

## Finding 6 -- the Notion coordinator is not a separate agent

Decided from content, as the directive requires.

Both coordinators carry the **same key set** -- `ownership`,
`core_responsibilities`, `decision_rules`, `routing_logic`, `required_inputs`,
`required_artifacts`, `handoff_contract`, `verification_rules` -- differing only
in domain vocabulary and two domain extras (`notion_formula_v2_guidance` on one,
`communication_style` on the other). The routing structure is identical:
trigger -> route_to -> output.

**Conclusion: one general orchestrator plus domain-specific orchestration
definitions.** The Notion coordinator is the same orchestrator role instantiated
for a domain, not a distinct agent. Its genuinely distinctive content -- Notion
formula v2 behavior, database-behavior verification -- is **domain knowledge**,
which belongs in `context/` or the domain orchestration definition, not in a
second coordinator identity.

Specialist separation is **preserved**. The five Notion and six general
specialists have materially different responsibilities, inputs and outputs; they
are not flattened.

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
| `agents/AGENT-{AUTOMATION-BUILDER, IAM-ACCESS, INTEGRATION, PAYMENTS-BILLING, REPORTING-DASHBOARD, RESEARCH-DOCUMENTATION}.json` (6) | General specialist definitions | `agents/` | **Keep**, minus any Finding 5 duplication |
| `agents/NOTION-{AUTOMATION, DATA-QUALITY-TROUBLESHOOTING, FORMULA-LOGIC, SCHEMA-RELATIONS, VIEWS-DASHBOARD}-AGENT.json` (5) | Notion specialist definitions | `agents/` | **Keep**, minus Finding 5 duplication |
| `config/agent-registry.json` | Identity + classification + partial routing + entry point | `registry/` for identity; routing and entry point to `orchestration/` | **Adapt** -- split |
| `schemas/agent-registry.schema.json` | Machine-verifiable registry structure | `registry/`, or `policies/` if enforced | **Move** -- owner decided in Step 3 |
| `templates/{task-brief, technical-spec, verification-checklist, execution-record}-template.json` (4) | Output templates, Notion field sets | `templates/` | **Adapt** -- reconcile against the two declared contracts; decide whether general variants are needed or the declaration is retired |
| `prompts/{general,notion}-{coordinator,specialist}.prompt.txt` (4) | Runtime bootstrap prompts naming relative paths and entry points | `prompts/` **only if** canonical and reusable | **Adapt** -- each hardcodes `./package-layout.json` and `./agents/...`; all break on restructure |
| `package-layout.json` | Package/distribution layout, second entry-point declaration | none -- `packages/` is not in the accepted taxonomy | **Retire for execution; provenance only** |
| `docs/README.md` | Navigation + stale canonical claim | `README.md` | **Adapt** -- keep navigation, drop the identity claim |

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
2. Decide the owner of `agent-registry.schema.json`: `registry/` as structure, or
   `policies/` if it is actually enforced. Requires knowing whether anything
   validates against it.
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
