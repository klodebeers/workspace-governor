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

## Core standard

> Choose the simplest reliable method that is proportionate to the risk and sufficient for the next decision. Prefer existing capabilities and perform checks in the environment containing the evidence. Escalate only when the current method cannot answer the question reliably. Stop once the required decision is adequately supported.

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
