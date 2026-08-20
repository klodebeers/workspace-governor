> **PROVENANCE COPY -- NOT AN ACTIVE DIRECTIVE.**
>
> Verbatim copy of `HUB-DOCUMENTATION.md` from
> `klodebeers/workspace-governor-agents-hub-one` at commit `24798d0`, the
> predecessor backoffice for the same Hub. Retained here so carried-forward
> obligations do not depend on a repository declared a non-authoritative input.
>
> Source SHA-256: `1f1aba880f7b89b243da6f277abe1b5ab967995bedc20fd9c181f210cf0c17b0`
>
> **Not an authority.** It declares itself the owner of Hub architecture or
> lifecycle; that ownership does not transfer to the backoffice. Adaptations
> required by `DECISIONS.md` D-27 are recorded in
> `plans/AGENT-HUB-CONSOLIDATION.md` section 6.2.

# Agent Hub Documentation Construction Standard

**Version:** 0.1.1  
**Authority:** Workspace Governor project rule  
**Owner:** Construction of authorized Agent Hub documents

## Scope and activation

Load this file only after `HUB-ARCHITECTURE.md` determines an artifact's placement and `HUB-MANAGEMENT.md` opens an authorized change that creates or materially revises an Agent Hub document.

This file governs document construction. It does not:

- authorize a change;
- decide placement or create a domain;
- decide whether a new canonical governance owner is eligible;
- govern the general change lifecycle, record retention, or version preservation;
- own the substantive rule written into another authoritative file.

The canonical governance-owner creation standard is owned only by `C:\Users\Chloe\.agents-hub\rules\AGENTS.md`. The Hub change lifecycle and preservation procedure are owned only by `HUB-MANAGEMENT.md`.

## Primary audience and terminology

Agent Hub governance and operational documents are written primarily for execution by agents and maintained by agents acting within authority.

- Preserve precise, standard technical terminology.
- Do not replace established terms with softer or less exact wording for human readability.
- Use one stable term for one concept across owners, routes, evidence, and adapters.
- Define a term only when ambiguity would change behavior; otherwise use the established technical meaning.
- Prefer compact operational structure over explanatory prose.
- Keep rationale and human-oriented explanation outside authoritative rules unless needed to prevent misapplication.

A human glossary is a separate, non-authoritative aid. It may explain canonical terms but must never redefine them. `HUB-ARCHITECTURE.md` determines its final placement.

## Content-class separation

Classify each proposed block before drafting:

| Class | Correct function |
| --- | --- |
| Rule | Mandatory, prohibited, recommended, or permitted behavior owned by one authority |
| Architecture | Domain, placement, source, and boundary decisions |
| Procedure | Ordered application of an established rule or architecture decision |
| State | Current mutable checkpoint; never authority |
| Evidence | Dated proof, result, or audit record |
| Research | Sources, findings, limitations, and local inference |
| Learning | Non-authoritative project record governed by `HUB-MANAGEMENT.md`; not content for an Agent Hub rule |
| Glossary | Non-authoritative explanation of canonical terms |
| Runtime adapter | Runtime-native discovery, translation, configuration, or enforcement without duplicate core rules |

Do not mix mutable state, evidence, research history, or glossary explanation into a normative rule.

## Construction pattern

Use only the elements the document requires. For an operational requirement, make the following explicit where applicable:

1. **Trigger** — the observable condition that activates the requirement.
2. **Actor** — the agent, owner, or authority responsible.
3. **Action** — the required, prohibited, recommended, or permitted behavior.
4. **Object and scope** — the exact artifacts, systems, or decisions affected.
5. **Boundary** — what the requirement does not govern.
6. **Evidence** — the observable proof of correct application.
7. **Failure route** — the sole owner and stop condition when the requirement cannot be applied.

Use active voice, imperative language, descriptive headings, short paragraphs, bullets, and tables when they reduce ambiguity. Examples are non-normative unless explicitly identified as acceptance tests or fixtures.

## Semantic reconciliation and size

Before drafting, search the complete affected scope for identical, equivalent, broader, narrower, and partially overlapping practical meaning. Improve the existing owner or add a route when an owner already exists. Do not create a second answer.

Keep always-loaded files lean. Move detailed procedures, dated evidence, research, examples, and history to their proper owners. File length or a fixed file count never justifies fragmentation by itself; ownership and activation must justify every file.

Use the conservative file-type targets in `research\GOVERNANCE-FILE-CREATION-GUIDE-2026-08-16.md` as review heuristics, not universal vendor limits or permission to omit required content.

## Vendor-dependent content

Before writing a product-dependent claim, inspect current primary vendor documentation. Record the vendor fact, local inference, verification date, volatility, and recheck trigger in research. Keep runtime-native syntax and behavior in adapters or native configuration; do not generalize it into the runtime-neutral core.

Instruction-file presence is not evidence of discovery, activation, adherence, or deterministic enforcement. Verify each claimed runtime state separately.

## Authoring completion gate

An Agent Hub document passes construction review only when:

- its purpose, scope, exclusions, audience, and owner are explicit;
- its trigger and required behavior are observable;
- terminology is precise and stable;
- no semantic duplicate, partial overlap, or competing owner remains;
- routes point to existing authoritative targets without paraphrasing them;
- examples, evidence, research, learnings, glossary content, and runtime controls remain in their proper layers;
- the required pre-edit snapshot and changelog entry exist under `HUB-MANAGEMENT.md`;
- every affected route, catalog entry, state record, and reference is updated;
- the actual edited file and diff are inspected;
- discovery or behavior changes receive a fresh-agent or fresh-runtime test appropriate to the claim.

Correct every failed check and reverify the affected checks before completion.
