> **PROVENANCE COPY -- NOT AN ACTIVE DIRECTIVE.**
>
> Verbatim copy of `research/AGENTS-MD-RESEARCH-AND-LIVE-AUDIT-2026-08-16.md` from `klodebeers/workspace-governor-agents-hub-one`
> at commit `24798d0`, the predecessor backoffice for the same Hub.
>
> Source SHA-256: `0d53b0a38a2198d50db68323388fa54460720c550a4f4c5f582c739dfc86ec8e`
>
> Retained so no load-bearing information depends on a repository declared a
> non-authoritative input. **Not an authority.** Dispositions are recorded in
> `evidence/PREDECESSOR-BACKOFFICE-REVIEW-2026-08-20.md`.

# AGENTS.md Research and Live Audit

- **Date verified:** 2026-08-16
- **Scope:** Current official OpenAI guidance and the live Agent Hub/Codex instruction state
- **Mode:** Audit only; this reference records findings and does not itself govern agent behavior
- **Primary official sources:**
  - https://learn.chatgpt.com/docs/agent-configuration/agents-md
  - https://learn.chatgpt.com/docs/config-file/config-advanced
  - https://learn.chatgpt.com/docs/prompting

## Verdict

**Content architecture: PASS WITH FIXES.**  
**Operational activation: BLOCKED.**

The Hub's `AGENTS.md` is developing in the right direction, but the governance package is not currently connected to Codex correctly. Continuing to add rules without fixing activation and duplication would produce governance that looks complete but is not reliably applied.

## What Official OpenAI Guidance Establishes

Codex:

- Reads global guidance from `CODEX_HOME\AGENTS.md`, unless a non-empty `AGENTS.override.md` replaces it.
- Then walks from the project root toward the working directory, loading at most one instruction file per directory.
- Concatenates those instructions; files closer to the working directory appear later.
- Uses a default 32 KiB combined instruction limit.
- Rebuilds the instruction chain when a new run or session begins.
- Recommends concise rules that identify the behavior, safe path, and relevant exception.

For coding work, OpenAI recommends stating the desired behavior, relevant context, constraints, and how the result should be verified.

These are runtime facts. OpenAI does not prescribe this governance package's complete architecture or the "one authoritative owner" model; that is a local design decision intended to prevent ambiguity and context bloat.

## What an AGENTS.md Should Contain

For this autonomous coding-agent system, the root file should contain only durable, always-relevant instructions.

### 1. Scope

- What environments, agents, projects, and actions it governs.
- What it explicitly does not govern.

### 2. Authority and Precedence

- The applicable authority hierarchy.
- What lower governance may specialize.
- What happens when instructions conflict.

### 3. Problem Routing

- Recognizable encountered conditions.
- Exactly one authoritative owner for each condition.
- Explicit cross-file activation conditions.

### 4. Core Operating Responsibilities

- Who owns business decisions.
- Who owns technical decisions.
- What autonomous execution means.
- When escalation is permitted.

### 5. Safety Boundaries

- Protected actions and reserved human decisions.
- A reference to runtime enforcement rather than pretending prose provides enforcement.

### 6. Verification Responsibility

- Work is not complete merely because the agent believes it succeeded.
- The authoritative verification file or process.

### 7. Context and Continuity

- Where settled decisions and current state are stored.
- What must be loaded before asking questions again.

### 8. Runtime Boundary

- The file provides instructions and context.
- Permissions, sandboxes, hooks, credentials, and runtime settings belong in adapters or native configuration.

Project-specific `AGENTS.md` files should contain repository facts such as setup commands, build and test commands, architecture constraints, conventions, acceptance checks, and project-specific exceptions. Nested files should contain only genuinely local specialization.

Research history, logs, secrets, temporary state, long procedures, generated evidence, and duplicate rules should stay out of `AGENTS.md`.

## Assessment of the Hub Root

The current Hub root at `C:\Users\Chloe\.agents-hub\rules\AGENTS.md` correctly includes:

- Scope and canonical locations.
- A one-contract model.
- One authoritative owner per governed issue.
- Governance-gap and conflict handling.
- Normative authority.
- Condition-based routing.
- Runtime neutrality.
- An explicit warning that source placement does not activate governance.

Its size is approximately 4.5 KB, which is appropriately compact.

The complex-technical-problem route is now correct:

> Classification and resolution of difficult or materially unresolved technical problems -> `ENGINEER-OWNERSHIP.md`

The other files become relevant only when distinct secondary conditions appear.

## Critical Live-State Problems

### 1. The Hub Governance Is Not Active in Codex

`C:\Users\Chloe\.agents-hub\rules\AGENTS.md` is outside the active Codex home and current project instruction chain.

The trusted-project entry in `C:\Users\Chloe\.codex\config.toml` does not automatically load governance from that directory. Trust and instruction discovery are different mechanisms.

No live Codex runtime adapter was found. Therefore, the Hub rules are currently canonical source material, not proven active instructions.

### 2. The Active Global File Contains Incorrect Paths

The actually discovered global file is:

`C:\Users\Chloe\.codex\AGENTS.md`

But it repeatedly refers to:

- `C:\Users\ByteBoss\.codex`
- `C:\Users\ByteBoss\.agents-hub`
- `C:\Workspace`

Those locations do not exist. The live locations are:

- `C:\Users\Chloe\.codex`
- `C:\Users\Chloe\.agents-hub`
- `C:\KloWorkspaces`

This is an active governance conflict and must be corrected before relying on those instructions.

### 3. Required Hub Navigation Files Are Missing

The active global file requires:

- `C:\Users\ByteBoss\.agents-hub\README.md`
- `C:\Users\ByteBoss\.agents-hub\CATALOG.md`

Those paths do not exist, and equivalent files were also absent from `C:\Users\Chloe\.agents-hub` at the time of verification.

Agents are therefore instructed to read sources they cannot access.

### 4. The Active Global File Duplicates Hub Responsibilities

The approximately 20 KB global Codex file contains its own rules for:

- execution ownership;
- autonomy;
- delegation;
- context;
- verification;
- escalation;
- continuity.

Those overlap the new Hub files. Connecting the Hub without reconciling this duplication would violate the one-owner requirement.

### 5. Context-Budget Risk

No explicit `project_doc_max_bytes` setting was found, so the documented default applies. The active global file already consumes approximately 20 KB before project instructions are added.

Copying the entire Hub package into it would create unnecessary context pressure and possible truncation. The Codex adapter must remain thin.

## Correct Next Sequence

1. Audit every rule in the active `.codex\AGENTS.md` against the Hub using:
   - Keep
   - Move
   - Generalize
   - Specialize
   - Merge
   - Retire
   - Conflict
2. Make the Hub the canonical owner of shared behavioral rules.
3. Reduce `.codex\AGENTS.md` to a thin Codex adapter containing:
   - the mandatory Hub bootstrap route;
   - Codex-specific discovery and configuration behavior;
   - Codex-specific permissions, tools, hooks, and review controls;
   - no duplicated shared governance.
4. Repair all `ByteBoss`, `C:\Workspace`, and missing-file references.
5. Create the missing Hub navigation/catalog layer only after its exact ownership is defined.
6. Verify with a fresh Codex session:
   - which instruction sources were loaded;
   - whether the Hub root was actually read;
   - whether an encountered condition selects the correct sole owner;
   - whether the agent avoids loading unrelated governance;
   - whether conflicts are surfaced instead of synthesized.

## Evidence Status

- Official OpenAI documentation was opened and verified on 2026-08-16.
- The live Hub and Codex instruction/configuration paths were inspected directly.
- No governance file was changed as part of the research audit.
- This file is a reference record, not behavioral authority.
