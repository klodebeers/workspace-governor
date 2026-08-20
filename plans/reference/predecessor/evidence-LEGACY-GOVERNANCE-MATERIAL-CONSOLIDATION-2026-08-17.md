> **PROVENANCE COPY -- NOT AN ACTIVE DIRECTIVE.**
>
> Verbatim copy of `evidence/LEGACY-GOVERNANCE-MATERIAL-CONSOLIDATION-2026-08-17.md` from `klodebeers/workspace-governor-agents-hub-one`
> at commit `24798d0`, the predecessor backoffice for the same Hub.
>
> Source SHA-256: `5a7975b1e1ee155e85f8de5d7a809ee347c2fc50cf3a18e9b6a177e0b823b1d8`
>
> Retained so no load-bearing information depends on a repository declared a
> non-authoritative input. **Not an authority.** Dispositions are recorded in
> `evidence/PREDECESSOR-BACKOFFICE-REVIEW-2026-08-20.md`.

# Legacy Governance Material Consolidation

**Date:** 2026-08-17  
**Status:** Non-authoritative decision and disposition evidence  
**Scope:** Agent-governance files, folders, research, and runtime records supplied during the Workspace Governor review

## Purpose and cleanup boundary

This record preserves the accepted meaning of the supplied material without preserving every old implementation. It does not create another governance authority.

- Retain `C:\KloWorkspaces\workspace-governor` as the project record and control workspace.
- Retain `C:\Users\Chloe\.agents-hub` as the canonical Agent Hub target until an accepted, verified migration changes that location.
- Do not confuse the canonical dot-folder with the legacy non-dot folder `C:\Users\Chloe\agents-hub`.
- Preserve unrelated project material outside the Agent Hub cleanup scope.
- Material marked **Discard** below is rejected as active governance. Physical deletion remains a separate controlled cleanup action after any protected unrelated content and required recovery copy are confirmed.

## Consolidated decisions

| What was clarified | Accepted interpretation | Sole authoritative owner | Old material to discard | Still required |
| --- | --- | --- | --- | --- |
| The Hub is for autonomous coding agents, not generic Work Agents. | Agents may architect, execute, review, test, document, and orchestrate coding and agentic-system work. Role names do not replace the common engineering responsibility contract. | Hub `rules\AGENTS.md` for scope and routing; `rules\ENGINEER-OWNERSHIP.md` for responsibility. | Old Work-Agent role systems, mandatory team topologies, and behavior that makes every agent act like a project-management worker. | Complete the implementation plan and verify fresh-agent routing.
| Business authority, governance responsibility, and technical judgment are separate. | The user owns outcomes, business rules, validation expectations, protected business boundaries, and reserved human decisions. Governance owns universal boundaries. Agents own ordinary technical judgment and proof. The user is a non-coder where relevant, not “non-technical.” | `rules\ENGINEER-OWNERSHIP.md`; protected decisions route to `rules\AUTONOMY-AND-PROTECTED-BOUNDARIES.md`. | Language that treats the user as technically incapable or makes the user validate ordinary implementation decisions. | Preserve this split in project intake and fresh-agent tests.
| Complex implementation is not itself an escalation trigger. | Resolve difficult but established work autonomously. Run Technical Decision Resolution only for materially unresolved choices; escalate only the remaining authority, protected-boundary, or human/business decision. | `rules\ENGINEER-OWNERSHIP.md`; escalation contract in `rules\AUTONOMY-AND-PROTECTED-BOUNDARIES.md`. | Fixed role ladders, arbitrary 24-hour escalation triggers, and automatic escalation merely because work is complex. | Verify lower governance does not create competing escalation rules.
| Subagents were requested to protect the primary agent’s context. | Use bounded subagents when independent work materially improves context isolation or elapsed time. This is not a mandatory “battalion” or fixed hierarchy. The parent retains intent, integration, authority, and final verification. | `rules\CONTEXT-AND-ORCHESTRATION.md`. | Mandatory multi-agent staffing, permanent councils, and claims that solo execution is inherently a failure. | Implement and test reusable delegation support only if the target-tree decision accepts it.
| Retention concerns drafted outputs and reusable agent research that otherwise disappear in long chats. | Retain material outputs, accepted findings, qualifying prompts, reusable subagent research, evidence, decisions, and checkpoints when needed to reproduce, audit, continue, or explain material work. Do not retain raw context merely because effort was spent. | Global retention boundary: `rules\CONTEXT-AND-ORCHESTRATION.md` and `rules\VERIFICATION-AND-EVIDENCE.md`; Workspace Governor placement: `HUB-MANAGEMENT.md`. | Raw transcripts, transient tool output, routine drafts, caches, logs, hidden reasoning, semantic duplicates, and unneeded personal data. | Apply the retention test during implementation and verify references to retained artifacts.
| Project memory must be shared across runtimes. | Durable project knowledge belongs to the project: concise `STATE.md` or current-work checkpoint, decisions, research, evidence, and learnings. Claude or Codex private memory may aid retrieval but must not be the sole canonical project record. | Global continuity contract: `rules\CONTEXT-AND-ORCHESTRATION.md`; project-specific record owners remain in each project. | A memory database, handoff cache, traces, logs, or live runtime state inside the canonical Hub; runtime-private memory presented as project authority. | Decide whether the project-intake baseline needs a runtime-neutral continuity template and verify both runtimes can resume from it.
| `STATE.md` is a new living record, not a rule file. | State records the current checkpoint, settled decisions, verification status, blockers, and exact next step. It routes to authority and never replaces it. | Each project’s `STATE.md`; Workspace Governor state behavior is routed by its `AGENTS.md`. | Old state files after unique current facts and unrelated project facts are safely routed. | Keep state concise and test fresh-session continuation.
| Executors and architects share the engineering contract. | An executor loads Engineer Ownership for implementation and completion responsibility. An architect loads it for architecture tradeoffs and material technical decisions. | Hub `rules\AGENTS.md` routes both conditions to `rules\ENGINEER-OWNERSHIP.md`. | Role-specific copies of the same responsibility rules. | Runtime adapters and fresh-session tests must prove that the route is actually loaded.
| The six supplied policy files are coding-delivery workflows, not the complete Coding Agent Rules. | Branch, commit, PR, review, release, and rollback mechanics belong in repository or project governance, templates, or skills when applicable. Escalation remains globally owned by the canonical autonomy owner. | General verification: `rules\VERIFICATION-AND-EVIDENCE.md`; Hub placement/change: `HUB-ARCHITECTURE.md` and `HUB-MANAGEMENT.md`; repository-specific owner to be created only when justified. | The supplied policies as universal rules, including hard-coded API Agent/Architect/Auditor roles, GitHub labels, fixed SLAs, import gates, phase gates, and fixed branch categories. | Design runtime-neutral or repository-appropriate coding-delivery workflows; validate Git-host-specific behavior before adoption.
| A clean replacement may be easier than refactoring existing material. | Choose the least complex safe path that produces the same or a better verified outcome. Create a clean replacement when that is faster and clearer than editing or refactoring, provided accepted meaning, sole ownership, provenance, dependencies, reference updates, recovery, and verification are preserved. Speed does not weaken accuracy or completion gates. | Workspace Governor `HUB-MANAGEMENT.md` for Hub change method; ordinary technical approach remains the agent’s judgment under `rules\ENGINEER-OWNERSHIP.md`. | Unnecessary refactoring performed only to preserve an unsuitable structure; destructive replacement that loses unique accepted content or recovery. | Apply this choice during implementation-plan execution and verify the resulting artifact rather than the amount of editing performed.
| Precise terminology is for agents first. | Preserve exact technical language. Human explanation may live in a non-authoritative glossary and must not weaken canonical meaning. | Workspace Governor `HUB-DOCUMENTATION.md`; substantive behavior remains with its canonical owner. | Softened terminology that changes technical meaning and duplicated human-oriented paraphrases inside canonical rules. | Classify and create a glossary only if the implementation plan reaches that accepted artifact.
| Runtime-neutral source and runtime-native behavior are different layers. | Shared rules are authored once. Thin adapters handle discovery, configuration, permissions, hooks, and other runtime-native behavior without redefining the core. Instruction files provide context; placement alone does not prove activation or enforcement. | Hub `rules\AGENTS.md` for the shared contract; each thin runtime adapter for runtime-native integration. | Claude-specific directory names or Codex-specific configuration generalized into the neutral Hub tree. | Revalidate Codex and Claude Code behavior from current official documentation, implement adapters, and run fresh-runtime activation tests.
| Global and project layers coexist, but runtime precedence can conflict with semantic governance. | Claude Code’s current documentation distinguishes global and project `.claude` locations and states that project instructions take priority when they conflict. The Hub’s semantic contract does not permit lower governance to weaken Global Governance; a naive global importer is therefore insufficient. | Semantic precedence: Hub `rules\AGENTS.md`; runtime behavior: Claude Code adapter, supported by project research. | Any adapter design that assumes file placement alone preserves Hub precedence. | Resolve and test the Claude precedence constraint before adapter activation. Official source: <https://code.claude.com/docs/en/claude-directory#ce-global-settings> (verified 2026-08-17).

## Supplied-source disposition

### Discard as active governance after this record and existing project evidence are verified

- `C:\KloWorkspace\Workspace Configurations\_superseded-originals\agent-agnostic-global-config-brief.md`
- `C:\KloWorkspace\Workspace Configurations\_superseded-originals\machine-folder-structure.md`
- `C:\KloWorkspace\Workspace Configurations\CLAUDE-DIRECTORY-GUIDE.md` after runtime claims needed by adapters are revalidated and retained in project research
- `C:\KloWorkspace\_EXTRACT-agents-hub-from-STATE.md`
- `C:\KloWorkspace\AGENT-AUTONOMY.md`
- `C:\KloWorkspace\CODING-AGENT-DECISIONS-FOR-CODEX.md` after every accepted or unresolved item is confirmed in current owners, state, this record, or the implementation plan
- `C:\KloWorkspace\CODING-AGENT-QUESTIONS.md` after every unresolved item is confirmed in current state or the implementation plan
- `C:\KloWorkspace\engineer-ownership-handbook.md`
- `C:\KloWorkspace\ONBOARDING.md`
- `C:\KloWorkspace\STATE.md` after unique unrelated project state is separated
- `C:\Users\Chloe\.claude\projects\c--KloWorkspace\memory\MEMORY.md` as governance authority; preserve any unique unrelated project facts before deletion
- The four historical files under `C:\Users\Chloe\agents-hub\rules\agent-memory*.md`
- The six historical files under `C:\Users\Chloe\agents-hub\policies\`
- Generated or pasted research reports after their material supported findings and source provenance are retained in Workspace Governor `research\` or `evidence\`; generated reports are not vendor authority

The concepts accepted above survive through their authoritative owners or pending implementation requirements. The old files themselves do not remain active merely because a concept was useful.

### Preserve outside Agent Hub governance cleanup

- `C:\KloWorkspace\Workspace Configurations\drafts\navigate-gemini-notebook\` — separate capability draft, not Agent Hub governance; retain or manage with its owning project.
- `C:\KloWorkspace\PMA-WORKSPACE-SPEC.md` — separate Project Manager Assistant material; retain or move only under that project’s authority.
- A currently applicable runtime-specific `SUBAGENT-PROMPT-STANDARD.md` — keep in the owning runtime configuration unless separately superseded; do not copy it into the runtime-neutral Hub.
- Any other unrelated project files discovered during cleanup.

## Remaining implementation and validation

1. Execute the accepted implementation plan beginning with its checkpoint and complete target-tree classification; this record does not execute the plan.
2. Reinspect every proposed deletion target for unique unrelated project content and required recovery evidence before deletion.
3. Finish semantic deduplication so each governed issue has one owner and all other copies are retired or routed.
4. Design project-level coding-delivery workflow artifacts from requirements, not by promoting the six old policies wholesale.
5. Establish the runtime-neutral project-continuity pattern used by both Codex and Claude Code.
6. Revalidate current Codex and Claude Code discovery, precedence, instruction loading, limits, permissions, hooks, and enforcement behavior from primary vendor documentation.
7. Resolve the Claude global-versus-project precedence constraint and the active Codex governance conflict before adapter activation.
8. Implement thin adapters and pass fresh-agent bootstrap, fresh-runtime activation, adherence, and enforcement tests before claiming completion.

## Conclusion

The supplied material has served as historical evidence and design input. Accepted meaning is retained through current authoritative owners, this consolidation record, existing Workspace Governor research/evidence, and the implementation plan. Rejected implementations and semantic duplicates do not need to survive as active files.
