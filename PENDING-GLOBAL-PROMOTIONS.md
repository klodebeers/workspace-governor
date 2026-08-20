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
final canonical .agents-hub shared engineering/verification governance

Promotion trigger:
canonical .agents-hub structure and rule ownership are finalized
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
5. Update `STATE.md` so the promotion is no longer shown as pending.

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
final canonical .agents-hub root, alongside the root AGENTS.md contract

Promotion trigger:
canonical .agents-hub structure and rule ownership are finalized
```

It is placed at the repository **root**, not in `rules/`, because it is a root
behavior contract rather than a routed topic owner -- the same structural point
recorded as Observation 1 in
`evidence/GOVERNANCE-STRUCTURE-OBSERVATIONS-2026-08-20.md`.

`USER-SSOT.json` v1.3 is persisted alongside it at the repository root, so the
declared `load_order` is satisfiable. It is a **separate promotion item**: it
carries Greyed-specific business scope, so it belongs to workspace or company
governance, not to the runtime-neutral shared Hub. Do not promote it into
`.agents-hub` alongside the agent file. Its own `agent_rules.company_scope`
forbids widening it, and the Hub root contract requires shared governance to stay
runtime- and business-neutral.

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

Assessment against all five `agents-hub-one` rule owners found the great majority
of conflict classes already owned. Three gaps remain:

| Gap | Class | Currency | Recommended home |
|---|---|---|---|
| G-1 | Peer agent output conflict, outside any delegation hierarchy | Live | Section in `CONTEXT-AND-ORCHESTRATION.md` |
| G-2 | Contradiction between requirements or constraints at the **same** authority level | Plausible now. **Narrowed, not closed,** by `USER-SSOT.json` § `conflict_handling`: convert disputes into written rules and escalation ladders, and prioritise irreversible or money-moving issues and external deadlines. That supplies a business prioritisation principle, scoped to Greyed and to the user's own disputes. It does not establish a cross-agent owner for two contradicting instructions of equal standing. | Section in `AGENTS.md` § Normative Authority, routing to the SSOT principle for business prioritisation |
| G-3 | Stakeholder-goal conflict under multiple principals | Latent | Defer; record only |

`CONFLICT-RESOLUTION.md` is **not** recommended. Each gap is the missing branch
of a rule an existing owner already holds, and the hub root contract's Governance
Owner Creation Standard forbids a new owner where a focused section serves
cleanly.
