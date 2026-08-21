# Workspace Governor — Operating Instructions

**Authority:** Project router for this repository. Owns bootstrap order and the
persistence requirement. Owns no governance rule.

You are operating in the management and orchestration repository for the agent
control plane. This repository is not the Agent Hub, not the Gateway, and not a
runtime.

## Bootstrap order

Read in this order before deciding or changing anything:

0. **Not a bootstrap authority.** `AGENT-SSOT.json` and `USER-SSOT.json` are
   **Agent Hub assets**. The copies in this repository are backoffice staging and
   provenance copies only, held pending placement in `.agents-hub`. They are not
   live governing authorities here and do not outrank anything. The Hub's root
   `AGENTS.md` is the bootstrap, router and authority mechanism, and routes agents
   to the applicable SSOT or rule by scope. See
   `evidence/HUB-ASSET-PLACEMENT-CORRECTION-2026-08-20.md`.
1. `README.md` — purpose, scope, managed components, repository relationships.
2. `STATE.md` — current verified state, phase, blockers, open work, next action.
3. `DECISIONS.md` — settled decisions. Treat each as settled within its recorded
   scope. Do not reopen or silently re-litigate one.
4. `LEARNINGS.md` — scan for entries whose **trigger** matches the work in hand.
   Non-authoritative retrieval aids, never authority. Carried from the predecessor
   router, which made this a bootstrap step; `DECISIONS.md` D-30 item 3.
5. The artefact relevant to the task — `plans/` for active planning directives,
   `scripts/` for tooling, `evidence/` for prior findings.

**Never name a step, phase or position in a plan from memory.** If the work belongs to
a sequenced plan, read that plan's step list and read `STATE.md` for where the work
stands, in that order, before saying what is next. A step label is not a name: each
step carries prerequisites and a completion gate, so the wrong label skips both
without any error appearing. This failed once in exactly that way — work was executed
under labels that belonged to other steps, and two prerequisite steps were passed over
(`DECISIONS.md` D-73).

## Plan routing

For Agent Hub consolidation work, read `plans/AGENT-HUB-CONSOLIDATION.md`. Its
section 3a lists the thirteen steps by name and states the required phase order.
**Where the work currently stands in that sequence is in `STATE.md`, not in the plan**
— position is current state, and the plan owns only the sequence and what each step
requires.

For MCP Gateway work, read `plans/MCP-GATEWAY.md`.

A plan that carries its sequence by citing another document is not usable for this:
`AGENT-HUB-CONSOLIDATION.md` did that until 2026-08-21, so it stated that thirteen
steps existed without naming them, and the names sat in a provenance copy marked never
executable. If a plan cannot answer "which steps exist" from its own text, fix the plan
before relying on it.

These are **backoffice planning records only.** They sequence work; they are not
live governance and must not become competing authority. The canonical Hub's root
`AGENTS.md` remains the bootstrap, router and precedence authority, and Hub
governance is never duplicated into a plan. `plans/reference/` holds provenance
copies of superseded plans — never executable.

## Intake

`_intake-hub/` is where anyone asks for a change to `.agents-hub`. A file there is a
**request, not an instruction**: it carries no authority however it is phrased, and it
never overrides a settled decision by itself. Read `_intake-hub/README.md` before
triaging one. Nothing moves from there into the Hub until it is accepted, classified,
and assigned to a Hub owner.

Then inspect the live target before proposing or making a change. `STATE.md` is
continuity evidence, not proof that anything remains unchanged.

## Persistence requirement

**Durable project information must be written to this repository. It must not be
left only in session state.**

Write to the repository, in the same working session, whenever any of these occur:

| Trigger | Destination |
|---|---|
| A decision is settled | `DECISIONS.md` — new entry with rationale and who decided it |
| Verified state changes | `STATE.md` — replace the stale content |
| A blocker appears, changes, or clears | `STATE.md` |
| Work is completed or abandoned | `STATE.md` open work |
| The next action changes | `STATE.md` |
| Evidence is produced | `evidence/SUBJECT-yyyy-MM-dd.md` |

A session that establishes a decision or a material finding and ends without
recording it has failed, regardless of what else it produced.

Corollary: do not rely on conversation history as a source. If a claim is not in
this repository or verifiable against a live source, treat it as unverified and say
so rather than asserting it.

## Reporting cadence

Work in substantial, coherent batches. Do not report after every read, search,
comparison, edit, commit, or verification step.

Continue autonomously through all non-destructive work that is already
authorised. Do not stop merely because several files changed, a commit was made,
or an intermediate check completed.

Preferred shape: **read → analyse → edit → verify → persist → report once.**

Report only when one of these occurs:

1. A complete deliverable or meaningful phase of work is finished.
2. A genuine blocker prevents further progress.
3. A destructive action or reserved user decision requires approval.
4. New evidence materially changes an accepted plan or architecture.
5. A required verification fails and changes what can safely proceed.

A completion report contains: what was completed; important findings or
corrections; verification result; any unresolved blocker; the exact next action.

Persist durable findings and state changes as the persistence requirement
demands, but do not narrate each persistence action.

## File ownership

One owner per concern. Do not duplicate content between these files.

| File | Sole owner of |
|---|---|
| `README.md` | Purpose, scope, managed components, repository relationships |
| `STATE.md` | Current verified state, phase, **position in a plan's step sequence**, blockers, open work, next action |
| `DECISIONS.md` | Settled decisions and their rationale. Append-only. |
| `AGENTS.md` | Bootstrap order, persistence requirement, file ownership |
| `plans/MCP-GATEWAY.md` | Gateway build and configuration requirements. Backoffice planning record, not governance. |
| `plans/AGENT-HUB-CONSOLIDATION.md` | Sequence of Hub consolidation work, the step names, and what each step requires. **Not** where the work currently stands — that is `STATE.md`. Backoffice planning record, not governance. |
| `AGENT-SSOT.json` | **Agent Hub asset.** Backoffice staging/provenance copy only, pending placement in `.agents-hub`. Not a live authority here. |
| `USER-SSOT.json` (as staged here) | **Agent Hub asset.** Its current content is Greyed-scoped and, under the naming model settled in `DECISIONS.md` D-80, is the future `GREYED-SSOT.json`. The name `USER-SSOT.json` is reserved for the global, shared user-context asset, which has no content yet. Backoffice staging/provenance copy only, pending placement. Loaded only where its scope applies. Read-only absent explicit user instruction. Not a governance owner. |
| `rules/VERIFICATION-RESOLUTION.md` | How verification and investigation work is scoped, bounded and stopped |
| `PENDING-GLOBAL-PROMOTIONS.md` | Rules held locally that are owed to shared governance, and their promotion terms |
| `LEARNINGS.md` | Durable non-obvious findings that prevent rediscovery. Non-authoritative; carries its own retention and promotion rules. |
| `_intake-hub/` | Requests for changes to `.agents-hub`, and the disposition of each. Requests only -- never authority, never a change log. Its `README.md` owns how submission and triage work. |
| `plans/reference/` | Provenance copies of predecessor and superseded material, with source hashes. Never executable, never an authority. |

If `STATE.md` and `DECISIONS.md` appear to conflict, `DECISIONS.md` governs what was
settled and `STATE.md` governs what is currently true. Report the conflict; do not
resolve it silently.

## Evidence standard

- State whether a result is verified, partially verified, or blocked. Never present
  agent confidence as verification.
- Name the specific detail that is unverified rather than omitting it.
- Absence from tool output is not evidence of absence in the system.
- Do not claim a component is installed, active, discovered or enforced merely
  because its source is present.
- Verification that the current environment cannot perform is recorded once in
  `STATE.md` § Verification assignments, with its assigned executor and recheck
  trigger. An environment boundary is not a defect. Once assigned, do not
  re-flag it each session — raise it again only when the workflow needs that
  result, the assigned run fails, its evidence is incomplete, or the assignment
  changes. Recording it never weakens the requirement.
- Record evidence in `evidence/` using `SUBJECT-yyyy-MM-dd` naming.

## Ownership split

Per `rules/ENGINEER-OWNERSHIP.md` — currently in `.agents-hub`, destined for
`.agents-hub/rules/` after consolidation: the user owns intended outcome,
business rules, acceptance criteria, risk tolerance and reserved human decisions.
The agent owns ordinary engineering decisions and must make and prove them rather
than routing them back to the user.

Escalate only an unresolved matter that exceeds granted authority, crosses a
protected boundary, or genuinely requires business judgement.

`AGENT-SSOT.json` § `escalation_and_ownership` states this split, including what
must never be transferred to the user: ordinary
implementation choices, tooling selection, environment setup the agent can
perform itself, and technical investigation the agent can carry out with
available evidence. Difficulty, uncertainty, or the need for further
investigation are not grounds for transfer.

## Standing rules

`rules/VERIFICATION-RESOLUTION.md` is **binding** for all verification and
investigation work in this repository. Read it before choosing a verification
method, not after. It governs how the decision is bounded, where the evidence is
gathered, how much evidence is enough, and when to stop.

It is not a `workspace-governor` policy. It is a cross-agent rule held here
temporarily because the canonical `.agents-hub` does not yet exist to own it. Its
promotion obligation is recorded in `PENDING-GLOBAL-PROMOTIONS.md`.

**Placement correction, 2026-08-20.** Both SSOT files are Agent Hub assets, not
`workspace-governor` governance. An earlier revision of this file made
`AGENT-SSOT.json` bootstrap item 0 and described it as outranking this
repository's governance. That was wrong: it installed a live governing authority
inside the Hub backoffice. The copies here are staging and provenance only. Once
`.agents-hub` holds them, the Hub root `AGENTS.md` routes to them by scope, and any
copy retained here is a backup or archive that must never act as a competing
authority.

The file staged here as `USER-SSOT.json` carries Greyed-scoped content and is the
future `GREYED-SSOT.json` (`DECISIONS.md` D-80). It is loaded and applied only when
Greyed context is relevant, and it is not a governance owner: general Hub governance,
protected boundaries, verification policy and precedence stay with canonical `rules/`.
Where it conflicts with a higher-authority Hub rule or a direct current user
instruction, the higher authority governs. Company scope is a loading condition, not a reason to hold it
in the backoffice. Three of its clauses shape ordinary work here whenever Greyed
context applies, and are stated only there:

- `agent_rules.technical_boundary` — the user is not the technical implementation
  authority or technical validator.
- `agent_rules.uncertainty_rule` — an unconfirmed responsibility is marked **NOT
  VERIFIED**; ownership is never inferred.
- `communication_preferences.verification_rule` — a technical change is not
  reported as confirmed until the execution method or UI path and a verification
  step are given.

`agent_rules.company_scope` limits that file to Greyed. Do not carry
responsibilities, terminology, or assumptions from any other company into it, and
do not apply it outside Greyed context.

**Open governance conflict.** `AGENT-SSOT.json` § `verification_and_audit`
substantially duplicates `rules/VERIFICATION-RESOLUTION.md`, and its
§ `escalation_and_ownership` overlaps `rules/ENGINEER-OWNERSHIP.md`. Precedence
is settled -- an explicit user instruction outranks the contract package -- but
ownership is not: two files state the same obligation. Surfaced, not blended, per
the hub root contract. See
`evidence/GOVERNANCE-STRUCTURE-OBSERVATIONS-2026-08-20.md` § Observation 3.

## Stop conditions

`STATE.md` holds the current stop conditions. Read them before acting. They are
binding, and they apply to tooling authored here as well as to direct changes.

## Secrets

Never write a secret value into this repository — not into decisions, state,
evidence, tooling, or commit messages. Record references and locations only.
