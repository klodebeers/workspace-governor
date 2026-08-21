# Pending global-governance promotions

Rules held locally in `workspace-governor` that belong in shared governance once
the canonical owner exists. This file records the promotion obligation only; each
rule's content stays in its own file, which remains its sole owner.

---

## P-01 — Verification Resolution Rule

**Status:** Pending promotion.

```text
Current rule:
workspace-governor/rules/VERIFICATION-RESOLUTION.md

Current enforcement:
workspace-governor/AGENTS.md references the rule

Target:
canonical .agents-hub shared engineering/verification governance

Promotion trigger:
.agents-hub rule ownership is finalized (the repository is canonical now; ownership is not yet settled)
```

**Why it is pending rather than placed:** the canonical `.agents-hub` does not yet
exist. Per `DECISIONS.md` D-01, neither source repository is canonical; both are
inputs. There is therefore no shared rule owner to receive this rule, and the
local copy is a temporary binding, not its intended home.

### Terms of the obligation

- This is a **cross-agent standing rule**, not a `workspace-governor` policy. Its
  local placement is an interim measure.
- It **must be promoted** into the finalized canonical `.agents-hub` as soon as the
  appropriate shared rule owner is established.
- After promotion the full rule must have **one canonical owner**. No second copy
  of the rule body may persist as an authority.
- **Governed runtime adapters must expose or materialize the rule** as appropriate
  for each runtime, so governed agents are actually bound by it rather than
  merely having it committed somewhere.
- **Successful promotion must be verified before the temporary workspace copy is
  retired.** Retiring the local copy first would leave a period with no
  enforceable owner.

### On promotion

1. Verify the finalized `.agents-hub` contains the rule under its accepted
   canonical owner.
2. Verify the relevant runtime/adaptation paths make it available to governed
   agents.
3. Remove the temporary `workspace-governor` binding/reference if it is no longer
   required.
4. Archive the temporary `workspace-governor` rule and this promotion record with
   provenance. Do not hard-delete either.
5. Close the promotion's issue in the register with its outcome, and update `STATE.md`
   only if the promotion changes current state. Until 2026-08-21 this step named
   `STATE.md` § Open work, which no longer exists.

Steps 1 and 2 are the verification this rule itself governs: the sufficient
result is that the rule is present under its canonical owner and reachable by
governed agents. Nothing beyond that is required to close the promotion.

---

## P-02 -- `AGENT-SSOT.json`

**Status:** Pending promotion. Held at this repository root; belongs to shared
governance.

```text
Current artifact:
workspace-governor/AGENT-SSOT.json  (v1.1, user-supplied 2026-08-20)

Current enforcement:
workspace-governor/AGENTS.md bootstrap order item 0, ownership table, and
Standing rules

Target:
canonical .agents-hub root, alongside the root AGENTS.md contract

Promotion trigger:
.agents-hub rule ownership is finalized (the repository is canonical now; ownership is not yet settled)
```

It is placed at the repository **root**, not in `rules/`, because it is a root
behavior contract rather than a routed topic owner -- the same structural point
recorded as Observation 1 in
`evidence/GOVERNANCE-STRUCTURE-OBSERVATIONS-2026-08-20.md`.

`USER-SSOT.json` v1.3 is staged alongside it, so the declared `load_order` is
satisfiable.

**Corrected 2026-08-20.** An earlier revision of this record concluded that
`USER-SSOT.json` should stay in workspace or company governance rather than go to
the Hub, because it is Greyed-scoped. That reasoning was wrong: it confused
**scope** with **placement**. Both SSOT files are Agent Hub assets. Greyed scope
is a *loading condition* -- the file is loaded and applied only when Greyed
context is relevant -- not a reason to hold it in the backoffice. Both go to
`.agents-hub`; the Hub root `AGENTS.md` routes to each by scope.

### Terms

- Cross-agent behavior contract, not a `workspace-governor` policy.
- Must be promoted to the canonical Hub root once an owner exists.
- On promotion it must be the **single** owner of agent behavior, audience
  translation, communication format and verification scoping -- see P-03.
- Runtime adapters must expose it at session start, as the hub root contract
  already requires of the governance package.
- Promotion must be verified before the local copy is retired.

---

## P-03 -- Duplicate ownership to resolve at consolidation

**Status:** Open governance conflict. Surfaced, deliberately not resolved.

`AGENT-SSOT.json` overlaps two existing rule owners. Precedence is settled by
Normative Authority; ownership is not. Full analysis in
`evidence/GOVERNANCE-STRUCTURE-OBSERVATIONS-2026-08-20.md` § Observation 3.

| Concern | Competing owners | Recommended resolution |
|---|---|---|
| Verification scoping, stopping condition, proportionality, circuit breaker | `AGENT-SSOT.json` § `verification_and_audit` vs `rules/VERIFICATION-RESOLUTION.md` | SSOT becomes sole owner; the rule file is retired into it or demoted to a routed detail file adding no duplicate obligation. |
| Ownership split; non-transferable decisions | `AGENT-SSOT.json` § `escalation_and_ownership` vs `rules/ENGINEER-OWNERSHIP.md` | SSOT owns the split; the rule retains intake and technical decision resolution. |
| Communication substance and audience | `AGENT-SSOT.json` § `technical_translation_and_audience` vs `rules/ENGINEER-OWNERSHIP.md` § Communication | SSOT owns audience and format; remove the overlapping clause from the rule. |

Not resolved now because `rules/VERIFICATION-RESOLUTION.md` and P-01 were created
on explicit user direction, and retiring them is a governance decision about the
user's artifact rather than an ordinary engineering correction.

---

## P-04 -- Conflict-resolution coverage gaps

**Status:** Recorded as governance gaps. No new rule file created, as directed.

Assessment against all five `.agents-hub` rule owners -- inspected while the
repository was named `agents-hub-one` -- found the great majority
of conflict classes already owned. Three gaps remain:

| Gap | Class | Currency | Recommended home |
|---|---|---|---|
| G-1 | Peer agent output conflict, outside any delegation hierarchy | Live | Section in `CONTEXT-AND-ORCHESTRATION.md` |
| G-2 | Contradiction between requirements or constraints at the **same** authority level | Plausible now. **Narrowed, not closed,** by the Greyed-scoped user-context SSOT (staged as `USER-SSOT.json`, becoming `GREYED-SSOT.json` per D-80) § `conflict_handling`: convert disputes into written rules and escalation ladders, and prioritise irreversible or money-moving issues and external deadlines. That supplies a business prioritisation principle, scoped to Greyed and to the user's own disputes, and D-80 confirms a scoped SSOT is never a general governance owner. It does not establish a cross-agent owner for two contradicting instructions of equal standing. | Section in `AGENTS.md` § Normative Authority, routing to the SSOT principle for business prioritisation |
| G-3 | Stakeholder-goal conflict under multiple principals | Latent | **Name the owner now, write the rule later** -- `rules/ENGINEER-OWNERSHIP.md` § Authority and Responsibility Contract. Naming it costs nothing and pre-empts a future new-rule-file proposal. Reconciled 2026-08-21: this row said "Defer; record only" while issue #7 assigned an owner, so one gap carried two dispositions |

`CONFLICT-RESOLUTION.md` is **not** recommended. Each gap is the missing branch
of a rule an existing owner already holds, and the hub root contract's Governance
Owner Creation Standard forbids a new owner where a focused section serves
cleanly.

## Register note, 2026-08-21

Every promotion here also has an issue: P-01 and P-03 are issue #17, P-02 is issue #15,
P-04's gaps are rows in issue #7. **The issue is the item; this file holds the promotion
terms.** The migration audit found two defects that this note closes -- step 5 of P-01's
on-promotion list pointed at a register that no longer exists, and P-04 gave G-3 a
disposition that contradicted issue #7's.

P-02 was absent from `evidence/OPEN-WORK-MIGRATION-2026-08-21.md` in both directions --
neither mapped nor listed as newly filed. Its destination, the canonical `.agents-hub`
root alongside the root `AGENTS.md` contract, and its terms -- runtime adapters must
expose it at session start, and promotion is verified before the local copy is retired --
were carried by no issue until issue #15 was corrected.

## P-01 addendum, 2026-08-21 -- Performer selection

`rules/VERIFICATION-RESOLUTION.md` gained a § Performer selection: when verification,
review or audit work must be performed by an agent other than the author, what
delegation never does, and the reporting standard for a claim of independent review. It
is part of P-01 and promotes with it, under the same terms.

**Why it matters that this one is cross-agent rather than local.** The rule exists
because an agent reviewing its own work has already reached the conclusion under review.
That is a property of agents, not of this repository, and every agent the Hub routes has
it. Holding the rule here means an agent that loads only the Hub root contract cannot
reach it -- which is the same defect as G-6 and G-7 in issue #6, in a new instance.

Its two carriers are `workspace-governor`-local because of how the runtime works, not
by choice: hooks live in a `.claude/` directory, and the Hub is not a directory anyone opens
a session in. On promotion, the rule moves and the carriers stay -- which means the
promoted rule is read-only-enforced in every other repository until each one carries its
own. Say so at promotion rather than implying the gate travels with the text.
