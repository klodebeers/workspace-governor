> **PROVENANCE COPY -- NOT AN ACTIVE DIRECTIVE.**
>
> Verbatim copy of `HUB-ARCHITECTURE.md` from
> `klodebeers/workspace-governor-agents-hub-one` at commit `24798d0`, the
> predecessor backoffice for the same Hub. Retained here so carried-forward
> obligations do not depend on a repository declared a non-authoritative input.
>
> Source SHA-256: `651bc4efd1c23ba75a10136b7fa2d0af892acba9b6dec906d520030d22e2b0ce`
>
> **Not an authority.** It declares itself the owner of Hub architecture or
> lifecycle; that ownership does not transfer to the backoffice. Adaptations
> required by `DECISIONS.md` D-27 are recorded in
> `plans/AGENT-HUB-CONSOLIDATION.md` section 6.2.

# Agent Hub Architecture

## Ownership

This file is the sole Workspace Governor owner for the logical architecture of `C:\Users\Chloe\.agents-hub`: what canonical domains exist, where ordinary non-governance artifacts belong, and whether material is canonical authored source or project/runtime state.

It does not govern edit, refactor, migration, promotion, or verification procedure. Those belong to `HUB-MANAGEMENT.md`. It does not decide whether a new canonical governance owner may be created; that belongs only to the canonical Hub `rules\AGENTS.md`.

## Status of this taxonomy

No universal Agent Hub filesystem specification was found. The domains in this file are the local canonical taxonomy for `C:\Users\Chloe\.agents-hub`, derived from recurring concerns across current platforms and protocols. A domain name does not imply universal vendor support, runtime activation, or format compatibility.

## Four placement layers

Every artifact must be assigned to exactly one primary layer before placement:

1. **Canonical shared source** — reusable, cross-project authored material belongs in the Agent Hub under one owning domain.
2. **Project-local source** — project-specific requirements, instructions, workflows, tests, and continuity belong with that project.
3. **Runtime adapter or materialization** — runtime-specific loading files, settings, permissions, hooks, registrations, and installed representations belong in a thin adapter or the runtime's native configuration location.
4. **Runtime or operational state** — sessions, transcripts, caches, logs, checkpoints, queues, credentials, live connections, and generated state belong outside the Hub.

Global/shared and project-local answer **where an authored decision applies**. Source and runtime state answer **whether material is authoritative input or generated operational data**. These axes must not be collapsed.

## Root control files

- `rules\AGENTS.md` is the canonical governance router and precedence owner.
- `README.md` is human navigation and a concise explanation of the Hub boundary.
- `CATALOG.md` is the non-authoritative inventory and discovery index for Hub artifacts, their owners, paths, lifecycle status, dependencies, and runtime-materialization status. Canonical ownership remains with each artifact's owning source. The catalog does not route governed issues or define behavior; `rules\AGENTS.md` remains the governance router. It does not replace the active-work checkpoint in `STATE.md`.
- `STATE.md` is the mutable operational checkpoint. It records current work and evidence but never defines rules.

If a root control file is absent, its absence must be recorded and resolved through `HUB-MANAGEMENT.md`; another file must not silently take over its ownership.

## Established core domains

- `rules\` — the collective governance contract, with one authoritative owner for each governed issue and one root router.
- `runtime-adapters\` — the minimum runtime-specific loading or translation layer needed to connect canonical source to a supported runtime. Adapters must not become duplicate rule owners.
- `references\` — non-authoritative research, explanations, audits, and source material retained for evidence or future work.

## Candidate artifact domains

These domains are approved architectural destinations but must not be created empty. Create one only when its first accepted artifact satisfies the creation test below.

- `agents\` — reusable authored source for agent roles, capabilities, instructions, and associated discovery metadata. Prefer a runtime-neutral core where supported runtimes permit one; record runtime-specific representations and compatibility explicitly. Protocol-specific discovery cards belong here only for agents actually exposed through that protocol and do not become universal agent definitions.
- `skills\` — reusable skills authored under the current Agent Skills specification when that format is adopted. Each such skill is one directory containing required `SKILL.md` and only the scripts, references, and assets it owns. Record the runtimes and surfaces that actually validated it; specification conformance alone does not prove discovery or execution.
- `tools\` — reusable capability contracts and authored source, including MCP server source and its tools, resources, and prompts where applicable. Authentication material, live connections, native registrations, and running server state remain outside the Hub.
- `orchestration\` — reusable workflow, coordination, delegation, and handoff definitions. Live tasks, run queues, checkpoints, transcripts, and actual handoff records remain project or runtime state.
- `evaluations\` — shared or cross-artifact test cases, validators, rubrics, fixtures, and compatibility checks. Artifact-specific evaluations remain with their owning artifact when separation would weaken maintenance or retrieval. Evaluation run output remains outside the Hub.
- `templates\` — independently reusable or cross-domain scaffolds. A template specific to one agent, skill, tool, package, or workflow remains with that owner.
- `packages\` — distribution definitions, manifests, and intentionally promoted release bundles whose primary purpose is packaging one or more canonical artifacts. A package references source in the owning domains and must not duplicate it. Build output, installed plugins, marketplaces, and plugin caches remain outside the Hub.
- `archive\` — retired canonical source or supersession evidence that must remain directly accessible and is not adequately preserved by normal version history. Create it only when such an accepted artifact exists. It is not a destination for raw runtime state, unclassified dumps, caches, or material retained merely to avoid deciding its ownership.

## Domains not created by default

Do not create separate top-level domains merely because a runtime or historical plan uses them:

- `policies\` when the material is governance owned by `rules\`;
- `prompts\` when the prompt belongs to an agent, skill, workflow, or template;
- `apps\`, `connectors\`, or `plugins\` when canonical source belongs to `tools\` or distribution belongs to `packages\`;
- generic `docs\` when root navigation or owner-local documentation is sufficient;
- top-level `assets\`, `scripts\`, or `data\` when the material belongs with one artifact;
- `memory\`, `logs\`, `cache\`, `sessions\`, or other runtime-state directories.

Existing folders are not approved merely because they already exist. `governance-templates\` and `design-systems\` require classification under `HUB-MANAGEMENT.md` before promotion, relocation, or retirement.

## Repository-rule scaffolding and glossary placement

A reusable capability for creating or maintaining repository-level agent rules belongs in `skills\` when it passes the ordinary artifact creation test. Rules generated for one repository remain project-local source in that repository. A generator-owned block, including a block delimited by `PLAITED-RULES` markers, remains owned by that generator and must not become the authoritative owner of canonical Hub governance.

If a stable skill is later packaged for distribution, its package belongs in `packages\` and references the canonical skill source. Packaging must not create a second copy of the skill or its rules.

A human glossary, if created, is non-authoritative. It may explain canonical terminology but must never redefine it or be cataloged as canonical governance. Its final project-local or `references\` placement must be classified here from its actual purpose and audience; it must not be placed in `rules\`.

## Ordinary artifact and domain creation test

An ordinary non-governance artifact may be accepted only when all are true:

1. A real reusable artifact exists; the request is not speculative scaffolding.
2. Its scope is canonical shared source rather than project-local or runtime state.
3. No existing artifact owns the same practical responsibility, including semantic duplicates and partial overlaps.
4. It has a distinct retrieval and maintenance need that cannot be served cleanly by an existing owner.
5. Its owning domain is unambiguous under this file.
6. Its provenance, purpose, status, dependencies, compatibility, and verification requirements can be registered in `CATALOG.md` or an owner-local manifest referenced by the catalog.
7. Its runtime-specific representations can remain thin and traceable to the canonical source.

If the owning domain does not yet exist, create the domain and its first accepted artifact in the same controlled change. Never create an empty domain in anticipation of possible future content.

## Minimum artifact record

Every canonical artifact must have one stable name or identifier and a discoverable record containing:

- purpose and scope;
- authoritative owner and canonical path;
- provenance and source status;
- lifecycle status;
- dependencies and references;
- known runtime representations and their distinct materialized, installed, enabled, discovered, active, and verified states;
- last verification date and recheck trigger.

Catalog registration is evidence of source ownership and discovery only. It is never proof that a runtime loaded or enforced the artifact.
