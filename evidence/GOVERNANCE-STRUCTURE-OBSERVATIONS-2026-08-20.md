# Evidence -- governance structure observations for Hub consolidation

**Date:** 2026-08-20
**Sources inspected:** `/workspace/agents-hub-one` at ref `47c0187` (matches
`evidence/AGENTS-HUB-ONE-BASELINE-2026-08-19.json`); all five files in its
`rules/`; `AGENT-SSOT.json` v1.1 as supplied by the user 2026-08-20.
**Status:** Verified by direct file inspection. No source repository modified.

---

## Observation 1 -- `AGENTS.md` is misplaced inside `rules/`

**Verified.** `agents-hub-one` contains `rules/AGENTS.md` and **no root
`AGENTS.md`**. Directory listing of `rules/`:

```
AGENTS.md
AUTONOMY-AND-PROTECTED-BOUNDARIES.md
CONTEXT-AND-ORCHESTRATION.md
ENGINEER-OWNERSHIP.md
VERIFICATION-AND-EVIDENCE.md
```

`rules/AGENTS.md` is self-describing as the root contract. It owns "scope,
precedence, and routing", declares "This root file owns...", carries the
Normative Authority order and the routing table, and instructs "Read this file
first." A file that must be read before the routing table can be consulted
cannot live inside the directory the routing table addresses.

**Correction for the canonical Hub:** `AGENTS.md` at the Hub root;
`rules/` holds only routed topic owners. Placement only -- no content change.

**Not actioned.** `agents-hub-one` is unmodified, per the standing instruction
not to refactor the sources before the target tree is accepted.

**Consequence if not corrected:** the bootstrap contract becomes discoverable
only by entering the directory it governs, and a runtime adapter that exposes
`rules/*` as a rule set would expose the root contract as a peer topic rule,
flattening the precedence relationship the file itself defines.

---

## Observation 2 -- conflict-resolution coverage assessment

**Directive:** determine whether a distinct unresolved cross-agent
conflict-resolution obligation exists that is not already fully owned. Do not
create `CONFLICT-RESOLUTION.md`.

**Method note:** the assessment was directed at three files
(`AGENTS.md`, `ENGINEER-OWNERSHIP.md`,
`AUTONOMY-AND-PROTECTED-BOUNDARIES.md`). All **five** owners in the package were
read, because absence from three files is not absence from the package. Two of
the named-as-uncovered classes turned out to be owned by the two unnamed files.

### Coverage found

| Conflict class | Owner | Coverage |
|---|---|---|
| Two governance files govern one issue, or direct incompatible action | `AGENTS.md` -- governance conflict + Normative Authority | Complete. Explicit prohibition on blending or synthesizing. |
| Routed owner lacks the governing rule | `AGENTS.md` -- governance gap | Complete. |
| Instructions conflict **across authority levels** | `AGENTS.md` -- Normative Authority, 6 levels | Complete. |
| Authoritative sources, governing instructions, or observed system behavior materially disagree | `ENGINEER-OWNERSHIP.md` -- Technical Decision Resolution, activation condition 3 + 6-step process | Complete. Named activation condition with a defined resolution process. |
| New evidence or repeated failure undermines the chosen approach | `ENGINEER-OWNERSHIP.md` -- activation condition 4; reopening conditions | Complete. |
| Accepted decision conflicts with governing authority | `ENGINEER-OWNERSHIP.md` -- routes to Normative Authority | Complete. |
| Authority conflict, scope conflict, unmitigable material risk | `AUTONOMY-AND-PROTECTED-BOUNDARIES.md` -- protected boundaries + Escalation Contract | Complete. |
| Evidence inconsistent with accepted prior findings | `VERIFICATION-AND-EVIDENCE.md` -- topic audits check "consistency with accepted prior findings ... and unresolved conflicts" | Detection owned. Resolution routes to `ENGINEER-OWNERSHIP.md`. Adequate. |
| **Delegated** agent output conflicts with parent | `CONTEXT-AND-ORCHESTRATION.md` -- "Treat a child summary as a routing aid, not final proof; inspect decisive evidence before integration"; parent retains ownership | Complete for the parent/child case. |

### Genuine gaps

**G-1 -- Peer agent output conflict. Live now.**
Two agents with no parent/child relationship reach contradictory technical
conclusions about the same system. `CONTEXT-AND-ORCHESTRATION.md` resolves this
only inside a delegation hierarchy, by parent authority. No owner governs
reconciliation between peers, where no agent holds authority over the other and
neither output is "the child summary". This is not hypothetical in this
architecture: Claude Code, ChatGPT/Codex and a Raycast-mediated layer all
operate over the same repositories.

**G-2 -- Same-level requirement or constraint contradiction. Plausible now.**
Normative Authority resolves conflicts *between* levels. Two requirements at the
*same* level -- two explicit current user instructions, or two business rules in
one specification -- have no precedence tiebreak. `ENGINEER-OWNERSHIP.md` intake
requires flagging conflicts immediately, which is a detection duty, not a
resolution process; and the prohibition on blending is scoped to governance
files, not to requirements. An agent facing "must be exhaustive" against "must
ship today" has no owned route. That exact tension occurred in this project.

**G-3 -- Stakeholder-goal conflict. Latent.**
No file references multiple stakeholders. `ENGINEER-OWNERSHIP.md` assumes a
single "user or accountable business authority". Low relevance under a single
principal; real for multi-stakeholder governed work.

### Recommendation

**Do not create `CONFLICT-RESOLUTION.md`.** All three gaps are narrow, and
`AGENTS.md` § Governance Owner Creation Standard condition 6 requires that a
separate owner not be created where a focused section in an existing owner serves
cleanly. It does here:

- **G-1** -> a section in `CONTEXT-AND-ORCHESTRATION.md`, which already owns
  delegation, continuity and multi-agent flow.
- **G-2** -> a section in `AGENTS.md` § Normative Authority, which already owns
  precedence and already prohibits blending; the same-level case is the missing
  branch of a rule it owns.
- **G-3** -> defer. Record only. Creating a rule for a class with no current
  instance would violate condition 1 (a distinct issue requiring a durable
  normative answer).

A single new owner spanning all three would cut across three existing owners'
concerns and reintroduce the duplication the package is built to prevent.

---

## Observation 3 -- duplicate ownership introduced by `AGENT-SSOT.json`

**Surfaced, not resolved.** Per `rules/AGENTS.md`: two files appearing to govern
the same issue is a governance conflict; surface the competing sources and do not
blend or synthesize.

| Concern | Owner A | Owner B | Assessment |
|---|---|---|---|
| Verification scoping, stopping condition, proportionality, complexity circuit breaker | `AGENT-SSOT.json` § `verification_and_audit` | `rules/VERIFICATION-RESOLUTION.md` (this repo, created 2026-08-20 per D-19) | **Substantial duplication.** Seven of the ten `verification_and_audit` rules restate the six numbered steps and the proportionality, stopping-condition and circuit-breaker safeguards. Same obligations, two owners, created one day apart. |
| Ownership split; what must not be transferred to the user | `AGENT-SSOT.json` § `escalation_and_ownership` | `rules/ENGINEER-OWNERSHIP.md` (hub-one) | Overlapping. The SSOT is more specific on environment and tooling ownership; the rule is more specific on intake and technical decision resolution. |
| Communication substance and format | `AGENT-SSOT.json` § `technical_translation_and_audience`, `communication_and_format` | `rules/ENGINEER-OWNERSHIP.md` § Communication | Partial overlap. The SSOT adds the audience dimension, which the rule lacks entirely. |

By `rules/AGENTS.md` § Normative Authority, an explicit current user instruction
(level 2) outranks the global contract package (level 3), so `AGENT-SSOT.json`
governs where they differ. That resolves *precedence*. It does not resolve
*ownership*: two files still state the same obligation, which is the condition
the package exists to prevent.

**Recommended resolution at consolidation, not applied now:** `AGENT-SSOT.json`
becomes the single owner of agent behavior, communication audience and
verification scoping. `rules/VERIFICATION-RESOLUTION.md` is either retired into
it or demoted to a routed detail file that adds no obligation the SSOT already
states. `rules/ENGINEER-OWNERSHIP.md` retains intake and technical decision
resolution and drops the overlapping ownership and communication clauses.

Not applied because `rules/VERIFICATION-RESOLUTION.md` and its promotion record
were created on explicit user direction on 2026-08-19/20, and retiring them is a
governance decision about the user's own artifact, not an ordinary engineering
correction.
