# Step 3 -- semantic owner and dependency map

**Date:** 2026-08-21
**Plan step:** 3 of the sequence in `plans/AGENT-HUB-CONSOLIDATION.md` section 3a.
**Deliverable required:** an issue-to-owner matrix and an artifact-to-owner matrix,
with duplicate and overlap dispositions and unresolved gaps named.
**Gate required:** no included governed issue or artifact has two active owners.
**Gate result: NOT MET.** The map is produced; the gate cannot be closed by analysis.
Section 6 states exactly why and what would close it.

**Why this step ran after Steps 7 and 8, its dependents:** the labels used in this
project diverged from the plan's sequence. `DECISIONS.md` D-73.

## Method, and what was verified

The corpus was read in full at Hub commit `3e35f9d` (working tree clean, identical to
`origin/main`): the root `AGENTS.md`, all four `rules/` files, `README.md`,
`CATALOG.md`, and all six asset artifacts. In this repository: `AGENT-SSOT.json` in
full, `USER-SSOT.json` (the sections its own scope clause makes applicable),
`rules/VERIFICATION-RESOLUTION.md`, `PENDING-GLOBAL-PROMOTIONS.md` P-01 to P-04,
`evidence/GOVERNANCE-STRUCTURE-OBSERVATIONS-2026-08-20.md`, and the plan.

Comparison is by **obligation, not wording**. Two files stating one duty in different
words is a duplicate. Two files addressing genuinely different conditions is not.

Produced by a bounded independent analysis under `DECISIONS.md` D-60, then every
load-bearing claim re-checked against source before acceptance. Five checkable claims
were verified directly and all five held:

| Claim | Verification | Result |
|---|---|---|
| Method bounding -- simplest reliable method, stopping condition, complexity circuit breaker -- is absent from the Hub | `grep -ril` for each phrase across `AGENTS.md` and `rules/` | **Confirmed absent** |
| A source-selection standard is absent from the Hub | same | **Confirmed absent.** `ENGINEER-OWNERSHIP.md` matches only on "use current authoritative sources for drift-prone claims", which is a different obligation |
| The defect-class rule is absent from the Hub | same | **Confirmed absent** |
| "Presence is not activation" appears nowhere in `rules/` | `grep -ril` over `rules/` | **Confirmed.** It exists only in `AGENTS.md` § Locations, `README.md` and `CATALOG.md` -- navigation and boundary contexts, not the evidence owner |
| `P-03` recommends `AGENT-SSOT.json` as sole owner of verification scoping and of audience/format | direct read of `PENDING-GLOBAL-PROMOTIONS.md` lines 121-125 | **Confirmed**, and it is the reason the gate cannot close -- see section 6 |

Two defects the analysis found were fixed on confirmation rather than recorded for
later: the registry schema's only `$comment` described a constraint other than the one
it annotates, and this repository's `README.md` managed-components row still said
`.agents-hub` "does not yet exist" six lines above the paragraph declaring it
canonical. Both were mine.

## 1. Issue-to-owner matrix

Sixty-four distinct governed issues were identified across the corpus. Thirty-one have
more than one active statement. The matrix is grouped by intended owner; the full
per-issue table with every competing statement is retained in this record's working
analysis and summarised here by owner and by defect class, because the actionable unit
is the disposition, not the row.

| Intended owner | Issues owned | Of those, contested | Nature of the contest |
|---|---|---|---|
| `AGENTS.md` (root contract) | 19 | 12 | Mostly `README.md` and `CATALOG.md` restating scope and routing in their own words, plus one obligation stated twice inside `AGENTS.md` itself (runtime neutrality, § Canonical Assets and § Runtime Neutrality) |
| `rules/ENGINEER-OWNERSHIP.md` | 11 | 10 | Almost entirely `AGENT-SSOT.json`, which restates the ownership split, the non-transfer rule, intake, read-before-acting and communication substance |
| `rules/AUTONOMY-AND-PROTECTED-BOUNDARIES.md` | 8 | 6 | `AGENT-SSOT.json` § `execution_constraints` and § `secrets_and_privileged_actions`; one mutual restatement with `ENGINEER-OWNERSHIP.md` where each file states the duty and cites the other |
| `rules/CONTEXT-AND-ORCHESTRATION.md` | 8 | 3 | Internal: the current-work checkpoint and the handoff each carry a near-identical field list that differs in two fields, which reads as drift rather than design |
| `rules/VERIFICATION-AND-EVIDENCE.md` | 8 | 5 | `AGENT-SSOT.json` § `verification_and_audit` and this repository's `rules/VERIFICATION-RESOLUTION.md`. **Three of its issues have no Hub statement at all** -- see section 5 |
| The six asset artifacts | 10 | 5 | Two are the deliverables collision class; the rest are boundaries carried in `CATALOG.md` rather than in the artifact |

**The single largest cluster is `AGENT-SSOT.json`.** It restates obligations owned by
all four `rules/` files. Every one of its ten `verification_and_audit` rules restates
something stated elsewhere -- a higher count than
`GOVERNANCE-STRUCTURE-OBSERVATIONS-2026-08-20.md` Observation 3 recorded, which said
seven of ten.

## 2. Duplicate and overlap dispositions

Verbs: **FOLD** move the content into the owner and delete the copy. **ROUTE** replace
with a pointer naming the owner. **RETIRE** delete; the owner already states it.
**KEEP** genuinely different conditions, or legitimate specialisation. **BLOCKED**
needs a decision this analysis cannot make.

### 2.1 The `AGENT-SSOT.json` cluster -- BLOCKED on one question

| Section | Obligation status | Disposition if it is an asset | Disposition if it is an owner |
|---|---|---|---|
| `verification_and_audit`, 10 rules | All 10 restate something elsewhere. Rules 3, 5, 7 (simplest method, stopping condition, circuit breaker) duplicate only `VERIFICATION-RESOLUTION.md`, not the Hub | RETIRE, after folding the three unique sections of `VERIFICATION-RESOLUTION.md` into `rules/VERIFICATION-AND-EVIDENCE.md` | The Hub's verification owner is stripped of its routed condition, and `AGENTS.md` § Routing needs an edit no record plans |
| `escalation_and_ownership` | `agent_owns` 1-4, 7 and `agent_requests` 1-4 restate the rules; `agent_owns` 5-6 (translation, both directions) are unique | RETIRE the restatements; FOLD the non-transferable list as an enumeration under `ENGINEER-OWNERSHIP.md`, which reads better than the current prose | Splits a single routed condition across two owners |
| `technical_translation_and_audience` + `communication_and_format` | Audience-aware translation is **absent from the Hub**, verified. The rest restates `ENGINEER-OWNERSHIP.md` § Communication. One obligation appears twice inside the SSOT itself | FOLD the audience obligation into `ENGINEER-OWNERSHIP.md` § Communication as a section; RETIRE the rest | As above |
| `research_and_tooling` bullet 2 | Names a specific runtime tool | **Barred from shared governance either way** by `AGENTS.md` § Runtime Neutrality. Belongs to an adapter |

**Why this is blocked, precisely.** Three accepted records say `AGENT-SSOT.json` is a
Hub **asset**: `DECISIONS.md` D-25, plan delta D-d, and `AGENTS.md` § Canonical Assets
Outside This Contract, which states that assets "are not governance owners, they hold
no precedence tier". Two accepted records say it is the **owner** of verification
scoping, the ownership split, and communication: `PENDING-GLOBAL-PROMOTIONS.md` P-03
and plan § 6.4. Both readings are recorded; they cannot both hold.

`DECISIONS.md` D-09 already ruled the sibling file out on the same ground --
`USER-SSOT.json` "is data consumed by the governance owners, not an owner itself" and
"fails the governance-owner eligibility test". Nothing records why the agent file
would differ.

Precedence is not ownership. Observation 3 states this correctly: level-2 precedence
decides which statement wins in a conflict; it does not make the winner the owner of
the issue. P-03's table treats the two as the same thing.

**This is a reserved decision.** It concerns a user-supplied artifact and which file
holds a governance concern -- both P-03 and Observation 3 give that as the reason they
stopped short. It is item **U-1** in section 6.

### 2.2 Dispositions that are not blocked

| Issue | Owner | Others | Reason |
|---|---|---|---|
| The Hub holds shared governance and canonical assets only | `AGENTS.md` § Locations | `README.md` and `CATALOG.md` → ROUTE | `README.md`'s exclusion list is **longer** than the owner's, which is broadening, not navigation |
| Presence does not activate | **`rules/VERIFICATION-AND-EVIDENCE.md`** as a new section, routed from `AGENTS.md` § Locations | `README.md`, `CATALOG.md` → ROUTE | It is an evidence rule. `AGENTS.md` § Routing sends "evidence requirements" to that owner, and § One Contract requires the owner to hold the complete rule. Today an agent routed there never meets it |
| Runtime neutrality | `AGENTS.md` § Runtime Neutrality | `AGENTS.md` § Canonical Assets last sentence → ROUTE internally; `AUTONOMY` closing ¶ → ROUTE | One obligation stated twice inside the owning file is still two statements |
| Record the resolved model; revalidate proportionately | `rules/VERIFICATION-AND-EVIDENCE.md` | `AGENTS.md` § Runtime Neutrality → ROUTE, keeping only "no 'latest model' name in durable governance" | Recording and revalidation are evidence duties; what durable governance text may contain is the root file's own |
| Escalation-request content, and limiting the request to the missing item | `rules/AUTONOMY-AND-PROTECTED-BOUNDARIES.md` | `ENGINEER-OWNERSHIP.md` ¶ after the table → ROUTE | Two files state one duty and each cites the other. The citation is permitted; the restatement is not. The routing table gives escalation content to `AUTONOMY` |
| Delegation never expands authority | `rules/CONTEXT-AND-ORCHESTRATION.md` § Delegation | `AUTONOMY` § Escalation Contract sentence → ROUTE | The routing table sends "delegation" there, and that file already enumerates the delegation contract. **Low confidence:** the counter-reading, that authority ceilings belong to the authority owner, is defensible. The routing table decides it |
| Checkpoint contents vs handoff contents | `rules/CONTEXT-AND-ORCHESTRATION.md` | Merge into one field set with two triggers | Same file, two near-identical lists differing in two fields. Internal duplication is still duplication |
| The condition→owner routing table | `AGENTS.md` § Routing | `CATALOG.md` "Sole responsibility" column → reduce to path and lifecycle status, or quote the routing conditions verbatim | `CATALOG.md` disclaims authority and paraphrases each owner's scope, and the paraphrase **already differs** from the routing table. Drift with no error surface |
| Governance-owner eligibility | `AGENTS.md` § Governance Owner Creation Standard | plan § 3's second source, `HUB-ARCHITECTURE.md` → RETIRE as a source | D-27 and plan delta D-j: that document "is not an authority". Naming it beside the Hub for one test reintroduces two sources for one rule |
| Precedence order | `AGENTS.md` § Normative Authority | `AGENT-SSOT.json` `meta.note` ("This file is authoritative for agent behavior") → FOLD into the Hub router at SSOT placement | An asset asserting its own precedence contradicts `AGENTS.md` § Canonical Assets. Live today |
| What an agent is responsible for | `agents/<id>.json` `responsibilities` | `registry` `responsibility` → **subordinate explicitly** in the registry's `authority.does_not_own`, exactly as D-64 did for routing | The identical collision class one artifact over. Ten of twelve identities have no definition, so the registry line is currently the only statement -- subordinate it, do not delete it |
| What an agent produces | `agents/<id>.json` `outputs` | `routing.json` `routes[].output` → retire per route as that agent's definition lands | D-64 settles precedence. For 10 of 11 routes the field is the only statement of the deliverable; deleting now would lose information |
| The verification-checklist boundary | `templates/verification-checklist.json` | Move the boundary and the `human_review_required: null` convention **into the artifact**; `CATALOG.md` → index only | `CATALOG.md` states that ownership remains with each artifact's owning source, then carries this artifact's entire boundary. A consumer opening the template alone cannot tell that `null` means "another owner answers this" |

### 2.3 Domain instantiation versus restatement -- the reusable test

The question of whether an agent definition's domain rules duplicate
`rules/VERIFICATION-AND-EVIDENCE.md` is settled by a test taken from the artifact's own
boundary statement:

> **Strip the domain nouns. If a sentence already in a `rules/` file remains, it is a
> restatement. If the sentence becomes false or vacuous, it is an instantiation.**

Applied to the one migrated definition: **6 of 8 rules are legitimate instantiation, 2
are restatement.** The two are "Document any assumptions about output types or object
behavior" (which reduces to an obligation `ENGINEER-OWNERSHIP.md` already holds) and
"Do not hide formula assumptions in the final output" (which reduces to § Communication).
The clearest legitimate instantiation is "Verify formula output against actual database
data, not just syntax" -- stated generally it would not tell a formula agent what to
open.

**This test is the template for the remaining eleven migrations, and belongs in the
agent-definition schema work** so it is applied once rather than eleven times. The ratio
will be far worse there: `STATE.md` already records that 16 of the source package's 22
agent rule entries touch a concern a Hub rule owns.

## 3. Artifact-to-owner and dependency map

| Artifact | Owns | Depends on | Depended on by | Boundary matches content? |
|---|---|---|---|---|
| `registry/agent-registry.json` | Identity and classification of 12 agents | its schema; 1 definition; 4 named rule owners | `routing.json` (12 ids), the definition, `CATALOG.md`, `README.md`, 3 scripts | **Mostly.** One overrun: `responsibility` × 12 states what each agent is *for*, the definition's territory |
| `registry/agent-registry.schema.json` | Structural validity, and what validation cannot express | the instance; the enforcing script | the instance's `$schema`; `CATALOG.md` | **No.** Field descriptions carry settled decisions and their rationale, which is `DECISIONS.md` content in a live asset. Also holds one governed constraint stated nowhere else: a folded id requires an orchestrator |
| `orchestration/routing.json` | Entry point, pre-routing, domain selection, 11 routes | 12 registry ids; 3 rule owners; `context/`; definitions | `README.md` bootstrap 4, `CATALOG.md`, 1 script. **Nothing machine-consumes it** -- no adapter exists | **Yes -- the best-matched artifact.** Six boundary entries, each naming an owner; one states a precedence rule, which is D-64 working as intended; its surfaced governance gap performs the root contract's duty rather than inventing an answer |
| `agents/notion-formula-logic.json` | One specialist's purpose, inputs, outputs, domain rules | `context/NOTION-FORMULA-V2.md` **with a stated reason to read it** -- the corpus's only compliant instance of the no-blind-references rule; the checklist template; two `null` templates | registry `definition`, one route, `CATALOG.md` | **Yes**, apart from the two restatements in 2.3 |
| `context/NOTION-FORMULA-V2.md` | Formulas 2.0 platform behavior and its consequences | two named rule owners; four vendor URLs, explicitly not re-verified | the definition's `context[0]`, `CATALOG.md` | **Partly.** Three header paragraphs restate the class-wide asset rule instead of routing to it. Its § Scope claims an audience no router delivers |
| `templates/verification-checklist.json` | The instance shape for recording how a change will be validated | **nothing -- 9 lines, no references, no boundary** | the definition; `CATALOG.md`, which supplies its entire boundary; one route's declared output, an **undeclared** dependency since that agent has no definition | **No declared boundary exists in the artifact** |

**The pattern that works, and should be extended:** naming the owning file inside an
`authority.does_not_own` entry. Five of six artifacts declare a boundary; four of those
five are accurate; and the approval question -- whether an action may proceed and
whether a human must approve it -- is correctly routed by all four artifacts that touch
it. That is the corpus's best-executed control.

**The two systematic failures:** rationale and decision content leaking into live
artifacts, and a boundary carried by `CATALOG.md` for the one artifact that declares
none.

## 4. Dependency defect worth stating on its own

The only accepted agent definition **cannot be executed as written.** Two of its four
declared template dependencies are `null`, because the handoff and task-brief contract
is declared five times in the source with five different field sets and has no file.
`STATE.md` open work 26 and 29c record why. Its `outputs` include "Verification
checklist", whose template exists, alongside deliverables whose templates do not.

## 5. Gaps -- governed conditions no file answers

Each is assigned to an existing owner as a section. **No new rule file is proposed, and
no rule text is written here** -- `AGENTS.md` § Governance Owner Creation Standard
condition 6 forbids a separate owner where a focused section serves, which is the same
reasoning P-04 used to refuse a conflict-resolution file.

| # | Gap | Currency | Absorbing owner |
|---|---|---|---|
| G-1 | Two peer agents' outputs conflict, outside any delegation hierarchy | **Live.** Multiple agents operate on these repositories, and this analysis was itself produced beside others | `rules/CONTEXT-AND-ORCHESTRATION.md`. **Note:** nothing in the corpus defines "peer". The only structure that can ground it is `role_class` plus the entry-point orchestrator -- and the schema permits multiple orchestrators, so "route to the orchestrator" is not itself a tiebreak |
| G-2 | Two requirements at the same authority level contradict each other | **Plausible now**; an instance is already recorded | `AGENTS.md` § Normative Authority. It owns precedence and already carries the detection half; the tiebreak is the missing branch. `USER-SSOT.json § conflict_handling` has a principle to route to, but is Greyed-scoped and addresses the user's disputes |
| G-3 | Stakeholder-goal conflict under multiple principals | Latent -- one principal today | `rules/ENGINEER-OWNERSHIP.md` § Authority and Responsibility Contract. **Name the owner now, write the rule later:** naming it costs nothing and pre-empts a future new-rule-file proposal |
| G-4 | Where a surfaced governance gap goes -- the destination, the minimum record, the lifecycle | **Live.** Two instances exist right now, and the only register is this project's `STATE.md`, so a gap found by an agent working elsewhere has nowhere to go | `AGENTS.md` § One Contract, which creates the duty. A gap must be recordable by an agent that has loaded only the root contract |
| G-5 | Presence is not activation, as a rule an agent routed to the evidence owner meets | Live and load-bearing | `rules/VERIFICATION-AND-EVIDENCE.md` § Verification Standard |
| G-6 | Bounding a verification: simplest reliable method, stopping condition, complexity circuit breaker | Live. D-20 records the pattern recurring | `rules/VERIFICATION-AND-EVIDENCE.md`. The Hub's verification owner currently tells an agent to verify without telling it when to stop |
| G-7 | Which source is authoritative for a question class | Live. Two real failures of exactly this kind are recorded in `STATE.md` | `rules/VERIFICATION-AND-EVIDENCE.md`. Depth is proportionate to risk; source is not, and nothing in the Hub says so |
| G-8 | A domain is selected but no trigger matches | Live for 11 routes | `orchestration/routing.json` for the default; intake already correctly routed |
| G-9 | The pre-routing obligation: define required fields and produce a decision brief before technical work | Live; already surfaced in the tree and recorded as owed | `rules/ENGINEER-OWNERSHIP.md` § Intake |
| G-10 | **A Hub asset's data contradicts a Hub rule.** Assets have no precedence tier, so the six-level order cannot be applied to an asset-versus-rule conflict | Live the moment a definition's domain rule reads against a rule obligation -- which 2.3 shows is one clause away, and which the unmigrated definitions will multiply | `AGENTS.md` § Canonical Assets. **This is the structural hole behind D-64, which solved one instance rather than the class** -- the thing the defect-class rule exists to prevent |
| G-11 | "Checkpoint" names two different objects: the continuity checkpoint and the verification checkpoint | Live. The routing table distinguishes them; neither rule file does | Qualify the noun in each rule file. Not a new section: a collision that makes one rule misapplicable |
| G-12 | No accepted evidence-record shape | Live | `templates/` absorbs it; the field list stays with `rules/VERIFICATION-AND-EVIDENCE.md`. **Reconcile the two competing field lists first**, or the template canonicalises one by accident |
| G-13 | Nobody owns what "an authorized model" means, or who authorizes | Latent now, live at Step 9 | `AGENTS.md` § Runtime Neutrality, which creates the obligation and delegates it to a layer that does not exist |

## 6. The gate, and what blocks it

**Gate: no included governed issue or artifact has two active owners. NOT MET.**

Applying the section 2.2 dispositions would collapse most of the 31 contested issues to
one statement each. Six questions cannot be answered from the corpus, and the first
gates roughly a third of the dispositions.

| # | Blocked question | What would settle it |
|---|---|---|
| **U-1** | **Is `AGENT-SSOT.json` a governance owner, or an asset consumed by owners?** | An explicit user instruction. **Partial evidence added 2026-08-21:** D-80 states that verification policy is owned by canonical `rules/`. If that is general rather than scoped to the user-context files, U-1's first row is settled and P-03's recommendation inverts. Read strictly, the sentence is about what the scoped SSOTs do not own, so it is evidence and not a ruling. It concerns the user's own artifact and which file holds a governance concern. If asset: P-03's three rows invert, and the SSOT sections retire into the rule owners. If owner: `AGENTS.md` § Canonical Assets and § Routing both need edits no record currently plans, and the Hub's verification owner loses its routed condition |
| U-2 | Does `registry.responsibility` belong to the registry or the definition? | Whether a consumer must learn what an agent is for without loading its definition. Settle it in the agent-definition schema work |
| U-3 | Who owns output tone and format -- `AGENT-SSOT.json` or the scoped user-context SSOT? | **Half settled 2026-08-21 by `DECISIONS.md` D-80:** a scoped SSOT may hold preferences and agent-facing interpretation rules *for its own scope* and is not the owner of a general format contract, so the Greyed preferences are scoped content rather than a competing general owner, and D-08's assignment was correct within Greyed and never general. What remains is whether `AGENT-SSOT.json` owns the general contract -- which is U-1 |
| U-4 | Which file is the "Workspace Governor architecture owner" that the Hub root routes non-governance placement to? | Either name the path in `AGENTS.md`, or move the placement standard into a Hub-side owner. The Hub root currently delegates a live decision to a plan that declares itself not live governance |
| U-5 | Is the context file's self-declared audience a legitimate loading condition? | Either add the inbound routes when the other Notion definitions migrate, or delete the self-asserted scope. `AGENTS.md` § Canonical Assets lists four routing sources and a context file is not one of them |
| U-6 | May a live asset carry consolidation reasoning at all? | Plan § 6.8 suggests not, and the fifth Step-2 audit already removed such narrative once. Two instances remain: the schema's field descriptions and one context bullet |

## 7. Not verified

- The full 64-row issue table was produced by the bounded analysis; **five load-bearing
  claims were re-verified against source and all held**, and two produced immediate
  fixes. The remaining rows are consistent with the corpus as read but were not
  individually re-derived. Any disposition acted on should be re-checked against its
  own source at execution time, which the plan's Step 5 verification method requires
  anyway.
- Whether applying the section 2.2 dispositions closes the gate for the issues they
  cover. That is Step 5 work -- editing governance owners -- and needs approval under
  plan § 6.7. Nothing was edited here beyond the two confirmed defects.
- `GOVERNANCE-STRUCTURE-OBSERVATIONS-2026-08-20.md` cites `rules/AGENTS.md` throughout.
  That path no longer exists; the root move landed at `80dff05`. The evidence file is
  correctly dated and is not rewritten, but any disposition executed from it must
  repoint to the root `AGENTS.md`.
