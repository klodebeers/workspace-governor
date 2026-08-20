# Verification Resolution Rule

For each technical verification or investigation task:

1. Define the decision the evidence must support.
2. Identify where the authoritative evidence exists.
3. Use the simplest reliable method available in that environment.
4. Establish what result is sufficient to close the question.
5. Stop when the decision is adequately supported.
6. Escalate only when:
   - the result is insufficient or ambiguous;
   - the consequence of being wrong requires stronger evidence;
   - the current method cannot answer the question reliably; or
   - the task's recurrence, scale, audit requirements, or risk justifies additional tooling.

## Required safeguards

- **Locality:** Perform checks where the evidence exists. Prefer a capable local agent or runtime over remote proxy machinery or unnecessary transfer of technical investigation to a human. Human involvement is appropriate when access, authorization, physical interaction, privacy, accountability, or a genuine user decision requires it.

- **Proportionality:** Match verification effort to the consequence of being wrong. Low-risk and reversible decisions require less evidence than destructive, security-sensitive, production, migration, or compliance-sensitive decisions.

- **Stopping condition:** Before beginning substantial verification, identify what result would be sufficient to make the next decision. Do not continue gathering evidence after that condition is met.

- **Simplicity:** Prefer existing operating-system, runtime, Git, filesystem, and application capabilities. Create custom scripts, frameworks, proof systems, or reusable tooling only when their additional time, maintenance, failure modes, and verification burden are justified.

- **Complexity circuit breaker:** If validating the verification method itself becomes a substantial task, stop expanding the mechanism and reconsider whether the original question can be answered more directly.

## Authority selection

Verification has two independent dimensions. **Depth is proportionate to risk.
Source is not.** A low-risk question still has exactly one correct authority, and
a cheap check against the wrong source is not a cheap check -- it is a wrong
answer obtained quickly.

Step 2 above requires identifying where the authoritative evidence exists. This
section names it for recurring classes, so the choice is not re-derived, and
re-derived wrongly, each time. Neither this rule nor `AGENT-SSOT.json`
§ `verification_and_audit` previously named a source; this section adds only that.

| Question | Authoritative source | **Not** authoritative for this question |
|---|---|---|
| Does a repository exist; what is it named now | Authenticated repository listing or API for the owning account | A local clone's remote URL; a record in this repository; an unauthenticated `ls-remote`, which fails on credentials rather than absence; **the old name resolving, because a rename leaves a redirect** |
| What a repository contains at a ref | The remote at that ref | A local working tree, which may be stale, dirty, or on another branch |
| Did a change reach the remote | `git fetch` then compare against `origin/<branch>` | Local `HEAD`, or a push command's exit status alone |
| State of the operator's machine -- installed tools, PATH, configuration presence | That machine, via read-only collection | This repository's records; any cloud environment |
| Did a runtime discover, load, or enforce an instruction | A fresh session of that runtime, asked without being told the answer | File presence, configuration presence, or source placement. None of these is evidence of activation |
| Vendor product behaviour -- limits, precedence, discovery paths | Current official vendor documentation, or implementation source at a pinned commit, recorded with its date | Memory; third-party summaries; a prior research file not re-verified |
| Status of work assigned to someone else | The live system where that work lands | The assignment record here. It states what was true when written |
| What was decided | `DECISIONS.md` | `STATE.md`, which states what is currently true, not what was settled |
| Whether text is present or absent in a file or transcript | The simplest unfiltered read -- plain search over raw content | Any filtered, limited, or shape-scoped query. A partial result reads exactly like a complete one |

Where a class is absent from this table, apply step 2 and add the class once
resolved.

## Defect class

A confirmed defect is treated as an **instance of a class**, never as a lone fact.
When one is confirmed, inspect that class across the scope the same change
affected, fix every confirmed instance already inside the approved change, verify
the class, and stop.

Do not wait to be told about sibling instances. Whoever reports the first defect is
not the enumerator of the rest.

Stop before: work outside the approved change, an area classified `Conflict`, or
anything requiring a decision that has not been made. Report those; do not fold
them in.

Two failure modes make a class sweep worse than useless, and both occurred here:

- **A subset reported as the class.** Checking one direction of a change and
  reporting the class as clear. A rename has two directions -- references *to* the
  moved file and references *from* it -- and a deletion has its own. Verify each
  direction that the change created.
- **A check that is not itself verified.** A sweep is only as good as its check.
  Confirm the check finds a known instance and does not flag a known-good one
  before trusting its result. An over-broad check invites "fixing" correct
  references; an over-narrow one certifies a subset as complete.

Where a known instance is a legitimate exception, record it in the check with its
reason. A check that always reports a known false failure stops being read.

## Core standard

> Choose the simplest reliable method that is proportionate to the risk and sufficient for the next decision, **against the source that actually holds the answer**. Prefer existing capabilities and perform checks in the environment containing the evidence. Escalate only when the current method cannot answer the question reliably. Stop once the required decision is adequately supported.

## Anti-patterns

Do not:

- equate maximum rigor with good engineering;
- create tooling before checking whether an existing capability is sufficient;
- continue verification after the decision is already supported;
- transfer technical investigation to a human when a capable agent or runtime can perform it;
- create a second verification system merely to prove the first without reconsidering the original task;
- treat complexity, token use, elapsed effort, or additional tooling as evidence of quality.

Unnecessary complexity, unnecessary human intervention, and verification effort disproportionate to the decision are engineering defects. This rule is not permission to under-verify high-risk work.

## Scope

Applies prospectively to `workspace-governor`, `.agents-hub`, MCP Gateway work,
runtime adapters, and future governed projects.
