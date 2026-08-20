> **PROVENANCE COPY -- NOT AN ACTIVE DIRECTIVE.**
>
> Verbatim copy of `research/WORKSPACE-GOVERNANCE-CAPABILITY-REUSE-2026-08-16.md` from `klodebeers/workspace-governor-agents-hub-one`
> at commit `24798d0`, the predecessor backoffice for the same Hub.
>
> Source SHA-256: `b60ba8a6bf1e2c7c3344583d4fad6d03a9a6dc7ab23ef128d144a9d52e06cedc`
>
> Retained so no load-bearing information depends on a repository declared a
> non-authoritative input. **Not an authority.** Dispositions are recorded in
> `evidence/PREDECESSOR-BACKOFFICE-REVIEW-2026-08-20.md`.

# Workspace Governance Capability Reuse Research

**Verified:** 2026-08-16  
**Authority:** Research and disposition only; not behavioral authority  
**Scope:** Existing skills, plugins, and scaffolding patterns relevant to Workspace Governor work

## Conclusion

The current workflow should be authored and tested as a focused skill before plugin packaging. No reviewed component is a complete replacement for the Workspace Governor. Several components contain useful patterns that may be reused after provenance, licensing, output, and ownership review.

OpenAI currently defines skills as the authoring format for reusable workflows and plugins as the installable distribution unit for sharing skills or bundling them with connectors. Skills use progressive disclosure: metadata is available for discovery and the full `SKILL.md` loads when selected. This supports a focused skill during workflow development and later plugin packaging when stable distribution is required.

Primary source: [OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills).

## Reviewed component dispositions

| Component | Retained use | Excluded or unresolved |
| --- | --- | --- |
| `agent-governance-discovery` | Read-only discovery of instruction surfaces and separation of shared source from runtime-native state | Not a Hub maintainer, migrator, or activation mechanism |
| `workspace-doc-auditor` | Content-grounded file audit, overlap detection, and conflict detection | Does not own authority, placement, migration, versioning, reference updates, or continuing state; therefore not the complete Governor |
| `optimize-agents-md` | Compact transformation examples, verification-oriented rule patterns, and redundancy review | Its fixed approximate 2.5k-token target and assumption that learnings belong in every `AGENTS.md` are not adopted as universal rules |
| `scaffold-rules` | Shared `AGENTS.md` plus thin `CLAUDE.md` import pattern; repeatable generated sections for target repositories | The `PLAITED-RULES` block is generator-owned and overwritten on rerun. The third-party implementation is not adopted, installed, or authorized as canonical Hub governance pending provenance and output review |
| `constraint-placement-strategy` | Abstract sequence: classify the concern, identify one owner, choose placement, distinguish source from projection, record rationale | Its database-specific assumptions are excluded. `HUB-ARCHITECTURE.md` remains the sole Hub placement owner |
| `plugin-creator` | Candidate packaging mechanism after the workflow is stable and tested | Plugin creation is deferred; it does not replace skill authoring |

## Adopted placement logic

- An accepted reusable repository-governance scaffolder belongs in the Agent Hub `skills\` domain.
- Rules generated for a particular coding environment belong in that target repository.
- Stable distributable packaging may later belong in `packages\` and must reference, not duplicate, canonical skill source.
- Runtime-specific loaders, settings, hooks, and permissions remain thin runtime adapters or native runtime configuration.
- Scheduled audits are separate runtime-specific automation and remain deferred.

These are local architecture decisions. Product documentation establishes loading and packaging behavior; it does not prescribe this Hub taxonomy.

## Activation and adoption limits

Inspection, local availability, catalog presence, or source placement does not prove that a component is accepted, installed, enabled, discovered, active, or verified. Each state requires separate evidence. No skill, plugin, repository, scheduled task, or third-party generator was installed or activated by this research.

## Recheck triggers

Recheck current primary documentation and component provenance before:

- creating the Workspace Governor skill;
- adopting or forking a third-party scaffold;
- packaging a plugin;
- creating runtime adapters;
- scheduling recurring audits;
- making compatibility or activation claims.

