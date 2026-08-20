> **PROVENANCE COPY -- NOT AN ACTIVE DIRECTIVE.**
>
> Verbatim copy of `research/AGENT-HUB-STRUCTURE-RESEARCH-2026-08-16.md` from `klodebeers/workspace-governor-agents-hub-one`
> at commit `24798d0`, the predecessor backoffice for the same Hub.
>
> Source SHA-256: `c4c251531f720553c7b6fb48a5881af1db710096b9953ad2ad74ad9f2ce43076`
>
> Retained so no load-bearing information depends on a repository declared a
> non-authoritative input. **Not an authority.** Dispositions are recorded in
> `evidence/PREDECESSOR-BACKOFFICE-REVIEW-2026-08-20.md`.

# Agent Hub Structure Research

**Verified:** 2026-08-16  
**Scope:** Current structures and separation principles relevant to a runtime-neutral canonical Agent Hub  
**Authority:** Evidence and rationale only; not behavioral authority

## Conclusion

No current primary source reviewed defines a universal filesystem specification called an **Agent Hub**. The reliable cross-platform result is a set of recurring logical concerns, not one vendor-neutral directory tree.

The local architecture therefore adopts a small canonical source taxonomy and keeps project-specific source, runtime-specific adapters, and runtime-written state separate. Vendor-native layouts are evidence for separation and capabilities; they are not copied wholesale.

## Source-supported recurring concerns

The following concerns are directly described by one or more current sources, although names, formats, discovery rules, and scope differ by runtime:

- persistent instructions and governance context;
- reusable skills;
- specialized agent definitions;
- tools and external integrations, including MCP;
- orchestration and handoffs;
- state, memory, results, and checkpoints;
- deterministic permissions, hooks, or guardrails;
- packages, plugins, manifests, and distribution;
- discovery metadata and catalogs;
- evaluations and verification.

These are logical categories only. A source describing one category does not establish universal file compatibility or runtime support.

## Global, project, source, and state separation

Claude Code's official directory reference explicitly distinguishes personal/global configuration from project-shared configuration and separately identifies application data written during runtime. OpenAI and GitHub documentation likewise use scoped project instructions and separate extension/configuration mechanisms.

Locally adopted inference:

- canonical cross-project authored source belongs in the Agent Hub;
- project-specific authored source belongs with the project;
- runtime-specific loading and enforcement belong in thin adapters or native runtime configuration;
- runtime-written data belongs outside canonical source.

This is a cross-source architectural inference, not a vendor-defined Hub standard.

## Locally adopted Hub taxonomy and rationale

The following names are local organizational decisions documented authoritatively in `..\HUB-ARCHITECTURE.md`:

- established: `rules`, `runtime-adapters`, `references`;
- candidate on first accepted artifact: `agents`, `skills`, `tools`, `orchestration`, `evaluations`, `templates`, `packages`, `archive`.

Rationale:

- each domain has a distinct retrieval and maintenance responsibility;
- source ownership remains singular;
- runtime-native representations can be derived without becoming duplicate owners;
- generated state and operational work remain outside the Hub;
- lazy creation prevents empty scaffolding and context bloat.

The taxonomy is not an industry standard. It is the Workspace Governor's local synthesis of source-supported concerns and repository-management needs.

## Primary sources

### OpenAI

- [AGENTS.md configuration](https://learn.chatgpt.com/docs/agent-configuration/agents-md) — global and project instruction discovery, root-to-working-directory precedence, and instruction-size constraints.
- [Build skills](https://learn.chatgpt.com/docs/build-skills) — focused skill directories with `SKILL.md` and optional owned resources; progressive disclosure.
- [Build plugins](https://learn.chatgpt.com/docs/build-plugins) — packaging skills and MCP integrations for distribution.
- [Define agents](https://developers.openai.com/api/docs/guides/agents/define-agents) — agent composition from model, instructions, tools, guardrails, handoffs, and output contracts.
- [Orchestration](https://developers.openai.com/api/docs/guides/agents/orchestration) — multi-agent coordination and handoffs.
- [Agent evaluations](https://developers.openai.com/api/docs/guides/agent-evals) — evaluation as a separate lifecycle concern.

### Runtime-specific evidence used only for general separation logic

- [Claude Code directory](https://code.claude.com/docs/en/claude-directory) — explicit personal/global versus project scope; authored configuration versus runtime-written application data.
- [Claude Code features overview](https://code.claude.com/docs/en/features-overview) — separate instructions, skills, subagents, agent teams, MCP, hooks, and plugins.
- [Claude Code memory and instructions](https://code.claude.com/docs/en/memory) — instruction loading and project/global context; instruction files provide context rather than deterministic enforcement.
- [Claude Code plugins](https://code.claude.com/docs/en/plugins) — runtime-native package composition.

The runtime-specific file and folder names in these sources were not adopted into the canonical taxonomy.

### Cross-platform specifications and official references

- [GitHub Copilot customization reference](https://docs.github.com/en/copilot/reference/customization-cheat-sheet) — distinct instructions, prompt files, agents, skills, hooks, and MCP configuration.
- [Agent Skills specification](https://agentskills.io/specification) — adopted skill-directory format; it does not define an entire Hub.
- [Model Context Protocol architecture](https://modelcontextprotocol.io/specification/2026-07-28/architecture) — host/client/server separation and server-exposed tools, resources, and prompts.
- [Agent2Agent specification](https://a2a-protocol.org/latest/specification/) — protocol-specific agent discovery metadata; not a universal local-agent format.
- [NIST AI RMF resources](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) — governance, inventory, monitoring, and lifecycle concerns.

## Claim classification

| Decision or claim | Classification | Basis |
|---|---|---|
| No universal Agent Hub filesystem was found | Inference from compared sources | Each source defines its own surfaces; none claims a universal Hub tree |
| Separate shared/global and project-local authored source | Directly described and locally generalized | Runtime documentation describes scopes; local architecture generalizes the separation |
| Separate authored source from runtime-written state | Directly described and locally generalized | Runtime docs distinguish authored config from application data |
| Use focused skill directories with owned resources | Direct when Agent Skills format is adopted | Agent Skills and current runtime documentation |
| Keep MCP auth, connections, and running state outside canonical source | Local control supported by protocol separation and security practice | MCP architecture plus local source/state boundary |
| Use candidate domain names in `HUB-ARCHITECTURE.md` | Local organizational decision | Workspace Governor taxonomy |
| Create domains only with a first accepted artifact | Local anti-bloat control | User requirement and repository-maintenance rationale |
| Catalog state does not prove runtime activation | Cross-source inference | Source presence, runtime discovery, and execution are distinct mechanisms |

## Supplied-document disposition

The eight user-supplied reports were read completely and used as secondary input. They are not treated as current primary authority.

### Retained themes

- one authoritative owner and semantic deduplication;
- lean always-loaded context and progressive detail;
- separation of guidance from deterministic controls;
- source versus runtime configuration/state separation;
- agent responsibility for engineering workflow, context, tooling, and verification;
- explicit authority and escalation boundaries.

### Rejected or held pending primary evidence

- claims of universal instruction-file support or universal loading behavior;
- exact benchmark or productivity percentages without inspectable primary studies;
- mandatory unique identity or separate service accounts for every agent;
- blanket regulatory conclusions or deadlines;
- collection of full hidden reasoning traces;
- mandatory directory counts or a fixed fifteen-domain Hub;
- vendor-specific role or folder names presented as universal architecture.

### Files reviewed

- `The Enterprise Runtime Governance Blueprint: From Passive Policy to Machine-Spe…`
- `AI Coding Agent Governance and Configuration: A 2026 Strategic Briefing Executi…`
- `AI Agent Safety: From Text Generation to Real-World Action 1. Defining the "Age…`
- `The Shift to Passive Context: How Modern AI Agents "Know" What to Do 1. The "Ma…`
- `Technical Standard: Operational Policy for Autonomous AI Coding Environments 1.…`
- `Strategic Framework: Enterprise Agentic Governance & Integration Roadmap (2026)…`
- `The Engineer Ownership Handbook: Mastering the High-Agency Implementation Minds…`
- `Guidance vs. Guardrails: Mastering AI Workflow Enforcement In the orchestration…`

The original attachments remain the source copies. This research file records only the accepted or rejected themes and does not duplicate their full contents.

## Volatility and recheck triggers

Recheck the relevant official sources before a product-dependent implementation when:

- an involved runtime or protocol has materially changed;
- a loading, precedence, discovery, packaging, hook, permission, or activation claim will govern behavior;
- an adapter or materialization is created or updated;
- the last verification is no longer reasonably current for the decision's risk;
- observed runtime behavior conflicts with this record.
