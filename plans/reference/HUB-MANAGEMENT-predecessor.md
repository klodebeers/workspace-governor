> **PROVENANCE COPY -- NOT AN ACTIVE DIRECTIVE.**
>
> Verbatim copy of `HUB-MANAGEMENT.md` from
> `klodebeers/workspace-governor-agents-hub-one` at commit `24798d0`, the
> predecessor backoffice for the same Hub. Retained here so carried-forward
> obligations do not depend on a repository declared a non-authoritative input.
>
> Source SHA-256: `a32586bdedaec153cbd9cc093ee5350345811c58de651643b553663b1c84ee06`
>
> **Not an authority.** It declares itself the owner of Hub architecture or
> lifecycle; that ownership does not transfer to the backoffice. Adaptations
> required by `DECISIONS.md` D-27 are recorded in
> `plans/AGENT-HUB-CONSOLIDATION.md` section 6.2.

# Agent Hub Management Standard

## Ownership

This file is the sole Workspace Governor owner for how `C:\Users\Chloe\.agents-hub` is inspected, classified, changed, promoted, refactored, migrated, reference-updated, and verified.

It consumes domain and placement decisions from `HUB-ARCHITECTURE.md` and must not redefine them. General responsibility, authority, autonomy, context, orchestration, and verification rules remain owned by the files routed through the canonical Hub `rules\AGENTS.md`.

When an authorized change creates or materially revises an Agent Hub document, `HUB-DOCUMENTATION.md` governs document construction only. This file retains ownership of the change lifecycle, record retention, version preservation, and verification sequence.

## Required change sequence

Use this sequence for every structural or canonical-content change:

1. **Bootstrap authority** — load the canonical Hub contract and its routed owner before mutable state or local procedure.
2. **Inspect live state** — inventory the exact target, hidden files, relevant runtime adapters, indexes, manifests, references, and current continuity records.
3. **Find semantic ownership** — search for rules or artifacts with identical, equivalent, overlapping, narrower, or broader practical meaning.
4. **Classify every affected item** — assign `Keep`, `Move`, `Generalize`, `Specialize`, `Merge`, `Retire`, or `Conflict`, with evidence and destination.
5. **Reconcile the complete affected tree** — confirm domains, owners, dependencies, loading paths, and source-versus-state boundaries before any move or rewrite.
6. **Research drift-prone behavior** — use current authoritative vendor or protocol documentation for product-dependent claims. Separate documented behavior from local policy.
7. **Obtain independent pre-edit review** — a read-only reviewer must challenge authority, evidence, semantics, ownership, wording, and stop conditions before governance or architecture changes.
8. **Preserve the accepted version** — before a material edit, store an exact immutable snapshot under the corresponding `versions\project\` or `versions\hub\` path, verify its identity, and register it in `CHANGELOG.md`. The legacy root snapshot `versions\AGENTS.md-v0.1.0.md` remains valid and must not be renamed merely for consistency.
9. **Apply the smallest source-preserving change** — edit only the accepted owner and required adapters or indexes. When the artifact is an Agent Hub document, apply `HUB-DOCUMENTATION.md`. Never delete or overwrite the only verified source.
10. **Update dependencies atomically** — update routers, catalog entries, manifests, references, continuity, and source records affected by the same change.
11. **Verify actual state** — inspect the resulting files, references, boundaries, and behavior. Use a fresh runtime session before claiming discovery, activation, or enforcement.
12. **Correct and reverify** — correct each failed check and repeat the affected checks and their dependents.

Do not skip from inventory to editing. Do not preserve a known conflict merely to keep moving.

## Classification meanings

- `Keep` — correct owner, scope, location, and meaning; no material change.
- `Move` — meaning and scope are valid, but the owning location is wrong.
- `Generalize` — reusable core is extracted into the Hub while project or runtime-specific detail remains outside it.
- `Specialize` — a canonical core remains in the Hub while a thin project or runtime representation is created elsewhere.
- `Merge` — semantic duplicates or partial overlaps are folded into one authoritative owner; all other copies become references or are retired after verification.
- `Retire` — superseded or invalid material is removed from active discovery only after provenance, references, and recovery needs are satisfied.
- `Conflict` — two applicable authorities, decisions, or artifacts require incompatible outcomes. Stop the affected work, flag the conflict prominently, identify both sources and consequences, and resolve ownership before implementation.

Classification is controlled analysis, not permission to mutate. A classified item remains unchanged until the applicable review and change gate passes.

## Canonical decision and conflict route

When Hub management encounters an unresolved technical decision, a prior user answer, a repeated question, or a conflict between a prior answer and higher authority, load `ENGINEER-OWNERSHIP.md` through canonical `rules\AGENTS.md`. That canonical owner alone governs decision reuse and technical resolution and routes any genuine escalation condition to the canonical autonomy owner.

This management record may add only Hub-specific evidence: affected paths and classifications, conflicting source references, affected dependencies, current change stage, and the canonical resolution reference. It must not create a second decision or escalation rule.

## Project Records and Prompt Retention

Canonical `CONTEXT-AND-ORCHESTRATION.md` governs context, continuity, and delegation. Canonical `VERIFICATION-AND-EVIDENCE.md` governs what evidence is required and safe. `HUB-ARCHITECTURE.md` governs whether material is a canonical Hub artifact or project/runtime state.

This section begins only after material has been classified as a Workspace Governor project record. It governs only the retention and project-local placement of records produced while managing the Hub. It does not create a general evidence, context, or delegation rule; a reusable prompt library; or an Agent Hub domain.

Retain a project-owned record only when it materially affects a decision, implementation, verification, or the ability to continue the work without chat history:

- Place project-owned research, source analysis, and research synthesis in `research\`.
- Place audits, verification results, and material agent or subagent reports in `evidence\`.
- Leave a final deliverable in its authoritative owning location. Reference it from the applicable state or navigation record when needed for discovery or continuation; do not copy it into evidence merely to record its existence.
- Use `C:\KloWorkspaces\workspace-governor\prompts\` only for qualifying prompt records under the test below. Create that folder only with its first qualifying record.

Apply the canonical evidence exclusions for secrets, raw context dumps, and hidden reasoning. Additionally, do not retain transient tool output, intermediate drafts, logs, caches, complete transcripts, runtime prompt history, unnecessary personal data, or semantic duplicates.

Retain a project-authored agent or subagent prompt only when its safe prompt text is necessary to reproduce, audit, continue, or explain material work and no agent, skill, workflow, or template already owns that prompt. Do not retain system or developer instructions.

Each retained prompt record must identify:

- date and task;
- purpose;
- issuing authority;
- target role;
- scope and constraints;
- safe prompt text;
- distilled result or finding, with a reference to authoritative evidence or the deliverable when stored elsewhere;
- current status and any superseding record.

A retained prompt record is project evidence only. Its presence does not make it an instruction, reusable capability, canonical Hub artifact, runtime configuration, or proof of activation.

## Durable learning retention

Retain a learning in `LEARNINGS.md` only when completed work reveals a non-obvious finding that is likely to prevent repeated investigation, repeated failure, or an incorrect future classification. Do not record routine facts, transient status, raw tool output, or semantic duplicates.

`LEARNINGS.md` is project context, not authority. If a learning creates or changes required behavior, update the sole authoritative owner through this change sequence and replace the learning with a pointer or mark it superseded.

After the retention test passes, record one concise line using:

`L-nnn | Trigger: ... | Finding: ... | Consequence: ... | Owner or evidence: ...`

## Reusable capability promotion

When a reusable governance workflow is being developed, author and validate it as a focused skill first. Package it as a plugin only after the workflow is stable, verified, and requires installable distribution or connector bundling. Packaging must reference canonical skill source and must not create a second authoritative copy.

Source, package, installed, enabled, discovered, active, and verified remain separate states. Skill creation, plugin packaging, installation, runtime activation, and scheduled automation are separate controlled changes.

## Refactor and migration order

Structural work has three separate phases:

1. Decide and verify the complete target project tree.
2. Refactor source and references into that accepted tree.
3. Migrate only after the refactored source passes integrity and usability checks.

Preserve the original source throughout refactoring and migration. Do not treat a copied file, a catalog entry, or an ownership-marker README as proof of successful migration. Retire an old source only after destination integrity, reference correctness, fresh-use behavior, and a second recoverable copy or equivalent recovery path are verified.

## Promotion standard

Material becomes canonical only when:

- the architecture owner places it unambiguously;
- provenance and source rights are known;
- semantic duplication and overlap are resolved;
- the authoritative owner accepts responsibility for maintenance;
- required review and validation pass;
- the catalog and dependencies are updated;
- runtime compatibility claims are limited to what was actually tested.

Existing location, historical use, a planning document, a generated report, or runtime installation alone does not grant canonical status.

## Runtime-state vocabulary

Record these states separately:

- `source` — canonical authored material exists;
- `materialized` — a runtime-specific representation was produced;
- `installed` — the representation is present in a runtime-controlled location;
- `enabled` — runtime configuration permits its use;
- `discovered` — the runtime reports or demonstrates that it found the material;
- `active` — the material influenced the current execution;
- `verified` — defined acceptance evidence passed.

Never infer a later state from an earlier one.

## Hub-specific verification

In addition to the canonical `VERIFICATION-AND-EVIDENCE.md`, confirm:

- every governed issue and canonical artifact has one owner;
- routers and catalogs point to existing targets;
- no semantic duplicate or unresolved partial overlap remains;
- source, project, adapter, and runtime-state boundaries are preserved;
- no credential, transcript, cache, live session, or generated runtime state was promoted into the Hub;
- moved material has no stale inbound or outbound reference;
- candidate domains were not created empty;
- status and compatibility claims match the evidence;
- fresh-agent bootstrap reaches the canonical contract, correct project owner, and current checkpoint without chat history;
- fresh-runtime activation evidence exists for every activation claim.

## Stop conditions

Stop the affected change and report the exact blocker when:

- the canonical owner cannot be identified;
- two applicable sources conflict materially;
- a new canonical governance owner is required but its canonical creation standard is not yet accepted;
- provenance, credentials, sensitive state, or recovery safety is unresolved;
- a destructive action would be required;
- authoritative product documentation is missing for a material product-dependent claim;
- independent review is blocked or a material review finding remains unresolved;
- verification exposes a new semantic or ownership conflict.

Continue unrelated safe work only when it cannot conceal, worsen, or depend on the blocked issue.
