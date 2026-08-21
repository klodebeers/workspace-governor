# Step 2 -- provenance, sensitivity and external-source gates

**Date:** 2026-08-21
**Plan step:** 2 of the sequence in `plans/AGENT-HUB-CONSOLIDATION.md` section 3a.
**Why now:** Steps 7 and 8 were executed before this step, which is their stated
prerequisite. Content from an external source is already in the canonical Hub with no
provenance record. `DECISIONS.md` D-73 records the ordering error; this closes the gate
retrospectively rather than leaving it open.
**Form:** the step asks for one scoped report per distinct source. Four scoped sections
in one file, because each is short and the set is easier to read and re-check together
than as four files. No content is omitted by the choice.

**Scoping.** A source is in the required set if a downstream step consumed its content.
Four sources qualify or are commonly assumed to; `atrium_workspace`, `mcp-gateway` and
`KloWorkspaces` contributed nothing to the Hub and are out of scope.

---

## Source 1 -- `klodebeers/agents-hub-two` -- CLEARED

The only external source whose content is in the canonical Hub.

| Field | Finding | How established |
|---|---|---|
| Provenance | `klodebeers/agents-hub-two` at `0a222df`, a single commit titled "Initial Commit", authored `klodebeers <klodebeers@gmail.com>` 2026-08-19 | `git log` on the clone |
| Ownership | Owner `klodebeers`, a user account, id 246950610. The same account owns the canonical Hub and this backoffice | Authenticated repository lookup |
| Is it derived from anything? | **No.** `fork: false`, `forks_count: 0`, no upstream parent | Authenticated repository lookup |
| Rights and licence | **No `LICENSE`, `NOTICE` or copyright file exists.** With no fork parent and a single first-party commit, no third-party licence terms attach and there are no external rights to clear | Directory listing at the repository root; fork status above |
| Visibility | Private | Authenticated repository lookup |
| Access held | The session account holds `admin`, `maintain`, `push` | Authenticated repository lookup |
| Sensitivity | **No secret or credential value in any of the 27 files.** A case-insensitive scan for `api[_-]?key`, `secret`, `token`, `password`, `bearer`, `private[_-]key` returns two hits, both of which are *rule text about* secrets, not values: `AGENT-COORDINATOR-ORCHESTRATOR.escalation_rules` on MFA and secret-based flows, and `AGENT-IAM-ACCESS.rules.must_not_do` forbidding asking a human for credentials in chat | Content scan across all files |
| Runtime state | None. No logs, caches, sessions, discovery output or credentials. Recorded independently at reconciliation and re-confirmed | `evidence/AGENTS-HUB-TWO-RECONCILIATION-2026-08-20.md` |
| Personal data | None beyond the commit author's own name and email, which are ordinary git metadata for the account that owns every repository here |  |

**Decision: cleared for migration.** First-party content, same owner as the
destination, no fork parent, no licence terms to honour, no secrets, no runtime state.
The migration already performed under Steps 7 and 8 is retrospectively supported by
this evidence rather than by assumption.

**Limitations.** Rights are established from ownership and the absence of a fork
parent and licence file. No written assignment or contribution record exists, because
none is needed for first-party content by the owning account. If any of that content
turns out to have been copied from a third party into that initial commit, this
clearance does not cover it -- the commit is a single import with no history to inspect,
so provenance *within* the commit cannot be traced from the repository.

**Recheck trigger.** A new commit to `agents-hub-two`; the repository gaining a licence
file, a fork parent, or an additional contributor; or evidence that the initial commit
included third-party material.

**Affected classification rows.** All 27 rows in
`evidence/AGENTS-HUB-TWO-RECONCILIATION-2026-08-20.md`. None changes.

---

## Source 2 -- `design-systems\.remember` -- EXPLICITLY BLOCKED AND EXCLUDED

| Field | Finding |
|---|---|
| What is known | It exists in the materialized Hub on the operator's machine. It is **not tracked in the repository**: the repository holds only `design-systems/placeholder.md`, a zero-byte file. Its content is described in prior records as runtime-like |
| What is not known | Everything else. Provenance, ownership, purpose, sensitivity, active dependencies, recovery need |
| Why it is not established | A standing stop condition forbids reading, hashing, moving or classifying it before a provenance and sensitivity review. That review has not happened, and this step does not perform it. **Nothing was inspected to write this section** |

**Decision: explicitly blocked and excluded.** The step's completion gate permits
exactly this outcome -- "either cleared with evidence or explicitly blocked and
excluded" -- provided no downstream action depends on it.

**Verified that nothing depends on it.** A search of the Hub for `design-systems`
returns two references, both instructing preservation: the `CATALOG.md` unclassified
row and the `README.md` source-areas line. No artifact, route, registry entry,
definition, template or context file references it. No step's output consumes it.

**Recheck trigger.** The provenance and sensitivity review being authorised, or any
downstream step coming to depend on it. Until then this section is the answer and is
not re-litigated.

**Affected classification row.** `design-systems\`, classified `Conflict`, unchanged.

---

## Source 3 -- `klodebeers/workspace-governor-agents-hub-one` -- CLEARED, backoffice only

The predecessor backoffice. Its material was carried into **this repository**
(`plans/reference/`, 18 provenance copies), **not** into the canonical Hub.

| Field | Finding |
|---|---|
| Ownership | `klodebeers`, private, `fork: false`, created 2026-08-19 |
| Rights and licence | No `LICENSE` or `NOTICE` file. Same account, no fork parent, so no third-party terms attach |
| Sensitivity | Not re-scanned here. The carried material is planning and evidence prose, and each of the 18 copies was verified by content hash at carry time |
| Hub exposure | **None.** Nothing from this source is in the canonical Hub. The three `tasks/` files carry a "SUPERSEDED, DO NOT EXECUTE" banner and are provenance only |

**Decision: cleared, and out of the Hub gate.** Recorded so the source is not mistaken
for an uncleared input to the Hub. **Limitation:** the sensitivity statement rests on
the carry-time verification, not a fresh scan.

**Recheck trigger.** Any proposal to promote material from this source into the Hub.

---

## Source 4 -- `agent-governance-toolkit` -- NOT ADOPTED, outside the required set

Provenance is already established: an unmodified MIT fork of a Microsoft project.
Adoption is recorded in `DECISIONS.md` under *Recorded as not decided* -- whether to
adopt, fork or ignore it is open.

**Decision: nothing to gate.** No content from it is in the Hub or in this repository,
and no downstream step consumes it, so it is outside this step's required set. It
enters the set if adoption is ever proposed, at which point the MIT terms -- attribution
and licence retention -- become live obligations to satisfy.

**Recheck trigger.** A proposal to adopt or vendor any part of it.

---

## Completion gate

The step's gate: *every item required by a downstream step is either cleared with
evidence or explicitly blocked and excluded; no downstream action depends on an
unresolved item.*

| Source | Outcome | Downstream dependency |
|---|---|---|
| `agents-hub-two` | Cleared with evidence | Content is in the Hub. Now supported |
| `design-systems\.remember` | Explicitly blocked and excluded | **None**, verified by search |
| Predecessor backoffice | Cleared; no Hub exposure | Backoffice only |
| `agent-governance-toolkit` | Not adopted; outside the set | None |

**Gate: PASS.** Each source is cleared or explicitly excluded, and the one excluded
source has no dependents.

## Not verified

- Provenance *inside* `agents-hub-two`'s single initial commit. A one-commit import has
  no history, so whether any of that content originated with a third party cannot be
  determined from the repository. Stated as a limitation, not treated as cleared.
- Anything about `.remember` beyond its existence and its absence from the repository.
- A fresh sensitivity scan of the predecessor material carried into `plans/reference/`.
