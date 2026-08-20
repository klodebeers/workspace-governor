> **PROVENANCE COPY -- NOT AN ACTIVE DIRECTIVE.**
>
> Verbatim copy of `research/GOVERNANCE-FILE-CREATION-GUIDE-2026-08-16.md` from `klodebeers/workspace-governor-agents-hub-one`
> at commit `24798d0`, the predecessor backoffice for the same Hub.
>
> Source SHA-256: `9783d68b8b879c444e0b678dd2c261badc0ec2f46c3c80e0da8e160e77b42928`
>
> Retained so no load-bearing information depends on a repository declared a
> non-authoritative input. **Not an authority.** Dispositions are recorded in
> `evidence/PREDECESSOR-BACKOFFICE-REVIEW-2026-08-20.md`.

# Governance File Creation Guide for the Workspace Governor

**Status:** Research and drafting reference; not an active governance rule  
**Owner:** Workspace Governor project  
**Applies to:** Future creation or revision of files intended for `C:\Users\Chloe\.agents-hub`  
**Verified:** 2026-08-16  
**Recheck trigger:** A supported runtime changes instruction discovery, precedence, context loading, file limits, skills behavior, or enforcement controls

## Purpose and authority boundary

This guide explains how the Workspace Governor should design clear, lean, maintainable governance files for autonomous coding agents. It is project-owned research. It does not itself govern the Agent Hub, create a new canonical rule owner, or prove that any file is loaded by a runtime.

Future rules may be derived from this guide only through the Workspace Governor's normal ownership, review, versioning, and verification process. Vendor facts below are separated from local recommendations so a preference is never presented as a platform requirement.

## Core conclusions

1. A governance file is an operational contract, not an essay. It must identify its purpose, scope, owner, trigger, required behavior, boundaries, evidence, and stop or escalation conditions.
2. One practical rule must have one authoritative owner. Routers point to that owner; they do not paraphrase it.
3. Exact wording matters most where a sentence changes authority, permissions, risk, routing, precedence, completion, or an external contract.
4. Instruction files provide model context. They are not deterministic enforcement. Use runtime permissions, hooks, tests, schemas, access controls, or other executable controls when behavior must be guaranteed.
5. There is no universal vendor word limit for most Markdown files. Limits vary by runtime, feature, file type, and loading path. Local word-count targets are therefore context-budget controls, not vendor hard limits.
6. A file that is not discovered, imported, routed, or deliberately read may have no effect. File presence is not proof of loading, activation, adherence, or enforcement.
7. Longer files consume more context and can reduce attention to individual rules. Before splitting a file, remove duplication, history, rationale, examples, and evidence that do not belong in the active contract.

## How agents read files

Agents do not read every file in a workspace automatically. Their behavior depends on the runtime and file type.

| Mechanism | What current documentation establishes | Design consequence |
| --- | --- | --- |
| Codex `AGENTS.md` chain | Codex builds a root-to-working-directory instruction chain. It stops adding files when the combined chain reaches `project_doc_max_bytes`, which defaults to 32 KiB. | Budget the whole chain, not only one file. Keep root instructions small enough to leave room for project and component instructions. |
| Codex skills | Startup context contains skill names, descriptions, and paths. The initial list uses at most 2% of context, or 8,000 characters when context is unknown. Descriptions may be shortened and some skills may be omitted when the list is large. Full instructions load when a skill is selected. | Make each skill description discriminating and concise. Do not assume every installed skill is visible in every run. |
| Claude Code `CLAUDE.md` | Files above the working directory load in full at launch; subdirectory files load when Claude reads files there. Claude recommends fewer than 200 lines per `CLAUDE.md`. Imports improve organization but still enter startup context. | Keep always-loaded instructions under 200 lines when possible. Use conditional rules or on-demand resources for narrow topics; imports do not solve context bloat. |
| Claude Code auto memory | Only the first 200 lines or 25 KB of `MEMORY.md`, whichever comes first, load at startup. Content beyond the threshold is not loaded then. | Keep the entry file as a compact index and route details to focused topic files. |
| GitHub Copilot | Custom-instruction support varies by feature. Copilot documentation warns that long files can cause rules to be overlooked; code review reads only the first 4,000 characters of each custom-instruction file, while a separate code-review guide recommends no more than about 1,000 lines. | Treat limits as feature-specific. Test the actual consumer and keep critical instructions near the beginning. Do not use the 1,000-line ceiling as a quality target. |
| Agent Skills | Metadata loads before the skill body. The specification recommends a `SKILL.md` body below 5,000 tokens and 500 lines, with longer material in focused referenced files loaded on demand. | Put trigger and purpose in metadata, the executable workflow in `SKILL.md`, and detailed reference material one link deep. |
| Ordinary Markdown | No reviewed vendor promises that arbitrary Markdown is automatically read. An agent may read it only when routed, prompted, or needed during exploration. | Every necessary reference needs a discoverable route that says when and why to read it. Verify the route with a fresh agent. |

### What “ignored because it is too long” can actually mean

Use precise language. Depending on the runtime, a long file may be:

- excluded because a combined startup cap was reached;
- truncated at a documented line, byte, or character boundary;
- represented only by a preview or description until selected;
- loaded in full but given less reliable attention;
- never loaded because no routing or discovery mechanism selected it.

Do not claim that a runtime “ignores long files” without identifying which mechanism applies.

## Local size recommendations

These are Workspace Governor drafting defaults, not vendor limits. Count UTF-8 bytes and lines as well as words because vendors often measure bytes, characters, lines, or tokens rather than words. Exceed a target only when the extra content is necessary, the loading path is known, and verification shows acceptable behavior.

| File role | Local target | Action when the target is exceeded |
| --- | --- | --- |
| Always-loaded root or global router | At most 1,200 words, 150 lines, and 12 KiB | Remove duplication and explanatory material first. Do not exceed 200 lines without a recorded justification and fresh-load test. |
| Scoped governance owner | At most 2,000 words, 250 lines, and 20 KiB | Split only if separate issues have separate triggers and owners; otherwise tighten the same file. |
| Runtime adapter | At most 500 words, 80 lines, and 6 KiB | Keep only runtime-specific discovery, configuration, or compatibility details. Route shared meaning to the neutral owner. |
| Agent or subagent definition | At most 1,200 words, 150 lines, and 12 KiB | Remove background the agent can inspect. Preserve role, scope, inputs, constraints, deliverable, evidence, and stop conditions. |
| `SKILL.md` | Prefer at most 2,500 words and 300 lines; never cross the specification's 500-line recommendation without a strong reason | Move detailed domain reference and large examples to focused files, one link deep. Keep the complete workflow in the main file. |
| Router, catalog, README, or state index | At most 1,000 words, 150 lines, and 10 KiB | Convert detail to one-line routes. Remove closed history and stale entries from live state. |
| Research or technical reference | Prefer at most 4,000 words, 400 lines, and 32 KiB per focused topic | Add a concise conclusion and contents list. Split by independently retrievable topic, not arbitrary length. |
| Audit or verification record | At most 2,500 words for the decision-bearing summary | Store only necessary evidence and links. Keep bulky raw output outside active instructions and retain it only when required. |
| Retained prompt record | At most 1,500 words | Preserve only the safe, material prompt and its result linkage; never duplicate system or runtime-owned prompts. |

These targets apply across file types as reasonable creation limits. They do not imply that every file should be close to its maximum. The shortest complete file is preferable.

## When a new file is justified

Create a new file only when all of these are true:

1. It has one durable purpose that cannot be expressed as a short section or route in an existing owner.
2. Its activation condition can be stated clearly: an agent can determine when to read it and when not to read it.
3. It has one authoritative owner and does not duplicate or partially restate another owner's practical rule.
4. Its expected audience, scope, and lifecycle differ materially from the existing file.
5. Its location and inbound route are known before creation.
6. Creating it reduces context or ownership ambiguity rather than merely moving text around.
7. Its first accepted content exists; do not create empty future scaffolding.

Do not create a new file solely because an existing file is long. First remove semantic duplicates, move dated evidence out of active rules, shorten examples, archive superseded history, and distinguish active state from permanent policy.

## Drafting process

### 1. Define the governance problem

Write one sentence for each item before drafting:

- issue being governed;
- affected actors and systems;
- authoritative owner;
- activation trigger;
- intended outcome;
- protected boundary;
- evidence of compliance;
- stop, conflict, or escalation outcome.

If any item is unknown, research or inspect it before writing a rule.

### 2. Separate content classes

Classify every proposed paragraph as one of these:

- **Normative rule:** required, prohibited, recommended, or permitted behavior.
- **Procedure:** ordered steps for applying a rule.
- **Definition:** a term whose ambiguity would change behavior.
- **Route:** where to find the sole owner of another issue.
- **Rationale:** why a rule exists; informative only.
- **Example:** a non-authoritative illustration unless explicitly declared a test case.
- **Evidence or state:** dated facts that may change and do not define authority.

Do not mix these classes in one sentence. Put volatile facts, research history, and audit evidence outside always-loaded rules.

### 3. Draft the smallest complete contract

State the outcome first. Use active voice and name the actor: “The Workspace Governor records…” instead of “A record should be made…”. Use one main idea per sentence and short sections with descriptive headings.

An operational rule should normally identify:

- **Trigger:** the observable condition that activates it.
- **Actor:** who performs the action or owns the decision.
- **Action:** what must, must not, should, or may happen.
- **Object and scope:** the exact files, systems, or decisions affected.
- **Boundary:** what remains outside the rule.
- **Evidence:** what proves the action occurred correctly.
- **Failure route:** what happens if the rule cannot be followed or authorities conflict.

### 4. Reconcile semantics before editing

Search for identical, equivalent, broader, narrower, and partially overlapping meaning. If another owner already governs the issue, improve that owner or add a route; do not create a second answer.

Test terms that commonly hide ambiguity: `material`, `safe`, `appropriate`, `reasonable`, `critical`, `complex`, `destructive`, `sensitive`, `verified`, `done`, and `when needed`. Define the term, give a decision test, or route to the file that owns it.

### 5. Add only useful examples

Use examples when they clarify a boundary, counter a recurring misinterpretation, or provide an acceptance case. Include both a positive and an edge case when the distinction matters. Label examples as non-normative unless they are formal test fixtures.

### 6. Review, version, and test

For a material governance change:

1. preserve the prior accepted version according to project versioning rules;
2. perform an independent ambiguity and conflict review before editing the canonical owner;
3. update every affected route and reference with the change;
4. inspect the actual diff after editing;
5. test with a fresh agent that receives no hidden chat context;
6. verify discovery, correct owner selection, behavior, stop conditions, and evidence;
7. record the change reason and verification result.

## Why exact language matters

Exact wording materially reduces operational risk in these areas:

- **Authority and responsibility:** identifies who decides, who implements, who validates, and who may approve exceptions.
- **Autonomy and approval:** prevents both unnecessary questions and unauthorized action.
- **Precedence and conflict:** prevents an agent from choosing arbitrarily between incompatible instructions.
- **Safety and recovery:** defines protected data, destructive effects, reversibility, and required recovery evidence.
- **Credentials, privacy, legal, and financial boundaries:** prevents a technical agent from assuming business or fiduciary authority.
- **External effects:** identifies when local work becomes a message, deployment, purchase, production change, or other outward action.
- **Interoperability:** keeps schemas, APIs, paths, states, and version contracts consistent.
- **Completion:** distinguishes “file exists” from loaded, active, tested, and verified.

NIST's AI Risk Management Framework likewise emphasizes documented, differentiated roles and responsibilities for human-AI configurations. Precise governance is how technical autonomy can coexist with accountable human authority.

## Situations where exact phrasing is less critical

Precision can be lighter in:

- brainstorming and option generation;
- informal progress updates;
- research hypotheses that are clearly marked unconfirmed;
- narrative rationale that does not create a rule;
- early drafts that are visibly non-authoritative;
- illustrative examples that are clearly subordinate to the rule.

“Less critical” does not mean misleading is acceptable. Mark drafts, assumptions, and non-authoritative material clearly so an agent cannot mistake them for binding instructions.

## Best practices for precise language

### Use a controlled requirement vocabulary

If a governance package adopts the BCP 14 vocabulary, declare it once and use uppercase `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` with their defined meanings. RFC 2119 advises using imperatives carefully and sparingly; RFC 8174 clarifies that the special meanings apply only to uppercase terms when the convention is declared.

Uppercase is not inherently better than lowercase. It is useful only as a declared requirement-level notation. Use normal sentence case for headings, explanations, and ordinary prose. Avoid `shall` unless a legal or contractual drafting standard specifically requires it.

### Make requirements observable

Prefer:

> Before overwriting the only verified copy, the agent must stop and identify the exact target, recovery path, and required approval.

Avoid:

> Be careful with important files.

Prefer:

> When two applicable authorities require incompatible outcomes, stop only the affected work, cite both sources, state the operational consequence, and route the conflict to the named owner.

Avoid:

> Resolve conflicts appropriately.

### Calibrate triggers

A good trigger is based on observable consequences rather than a narrow list of tools or a broad feeling such as “this seems complex.” It should:

- catch materially equivalent cases;
- exclude routine reversible choices;
- name the consequence or authority boundary;
- provide a decision test for borderline cases;
- say what to do when uncertainty remains.

For example, “any technical question” is too broad, while “database deletion commands” is too narrow. A better trigger is: “an action may irreversibly remove valuable data, overwrite the only verified copy, or make recovery uncertain.”

### Keep one answer per issue

A router should say:

> This file governs Hub placement. For unresolved technical decisions, read `ENGINEER-OWNERSHIP.md`, the sole owner of that process.

It should not summarize the other file's decision process. A summary can drift and become a conflicting second rule.

### Separate guidance from enforcement

Use prose for judgment, responsibility, routing, and expected behavior. Use deterministic controls for requirements that cannot depend on model adherence—for example permissions, hooks, protected branches, schemas, tests, and access controls. Record which layer owns each control.

## Potential risks of vague or over-relaxed wording

- agents repeatedly ask questions the user has already answered because authority and decision reuse are unclear;
- agents act beyond scope because “use your judgment” lacks an outer boundary;
- routine work stalls because “ask before risky work” activates too broadly;
- incompatible rules are silently chosen instead of loudly flagged;
- destructive or external actions are treated like reversible local edits;
- technical validation is incorrectly transferred to a non-technical user;
- a router becomes a second rule owner through paraphrase;
- examples, old state, or research notes are mistaken for current authority;
- runtime-specific behavior leaks into the neutral core;
- a long startup file crowds out task context or places critical rules after a truncation boundary;
- an import reorganizes text but does not reduce loaded context;
- a file is assumed active merely because it exists in the Hub;
- absolute words such as `always` and `never` create impossible or unsafe behavior because exceptions were not modeled.

## Recommended governance-file structure

Use only the sections the file needs, in this order:

1. **Title and status** — authority class, owner, version, last review, and runtime status if relevant.
2. **Purpose** — the one problem this file owns.
3. **Scope and exclusions** — where and when it applies; what it does not govern.
4. **Definitions** — only terms whose ambiguity changes behavior.
5. **Activation triggers** — observable conditions for loading or applying the file.
6. **Responsibilities and authority** — who decides, acts, verifies, and approves.
7. **Rules or procedure** — short, imperative, ordered where sequence matters.
8. **Conflict and escalation route** — sole owner, required evidence, and stop boundary.
9. **Verification and completion** — observable acceptance criteria.
10. **Dependencies and routes** — direct links to other owners without duplicated rules.
11. **Examples** — optional, explicitly informative or identified as tests.
12. **Version history** — concise change and reason, or a route to the authoritative history.

Do not force every file into this full template. A thin router or adapter may need only purpose, scope, routes, and verification notes.

## Creation and review checklist

- [ ] The file has one durable purpose and one authoritative owner.
- [ ] The title, status, scope, exclusions, and audience are explicit.
- [ ] The trigger is observable, neither universal nor tool-list narrow.
- [ ] The actor and action are named in active voice.
- [ ] Mandatory, recommended, and optional behavior are distinguishable.
- [ ] Ambiguous terms have a definition, decision test, or sole-owner route.
- [ ] Equivalent and partially overlapping rules were folded into one owner.
- [ ] Routers link without paraphrasing another owner's rule.
- [ ] Normative rules are separate from rationale, examples, evidence, and current state.
- [ ] Vendor facts are sourced and separated from local policy.
- [ ] The file's discovery and loading mechanism is known; presence alone is not treated as activation.
- [ ] Word, line, byte, character, and token considerations were checked as applicable.
- [ ] Critical content appears before any known truncation boundary.
- [ ] Deterministic requirements have executable controls where needed.
- [ ] Prior accepted versions and change reasons are preserved as required.
- [ ] A fresh agent can find the file, identify when it applies, follow it, and prove completion without hidden chat history.

## Sources and evidence notes

Only current official or standards-body sources were used for the operative findings above.

- [OpenAI — Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) — discovery order and the default 32 KiB combined instruction-chain cap.
- [OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills) — progressive disclosure and the startup skill-list budget.
- [OpenAI — Model guidance](https://developers.openai.com/api/docs/guides/latest-model) — lean prompts, one statement per rule, explicit autonomy boundaries, and outcome-focused task specification.
- [Claude Code — How Claude remembers your project](https://code.claude.com/docs/en/memory) — loading behavior, the under-200-line `CLAUDE.md` target, imports, and the `MEMORY.md` startup limits.
- [Claude Code — Debug your configuration](https://code.claude.com/docs/en/debug-your-config) — adherence risks from vague, conflicting, or long instructions.
- [GitHub Copilot — Using custom instructions for code review](https://docs.github.com/en/copilot/tutorials/customize-code-review) — concise, structured instructions; long-file degradation; and the approximately 1,000-line feature guidance.
- [GitHub Copilot — About customizing Copilot responses](https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/prompting/response-customization) — short self-contained rules and the code-review-specific first-4,000-character limit.
- [GitHub Copilot CLI — Managing context](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/context-management) — fixed context windows and large-output preview behavior.
- [Agent Skills specification](https://agentskills.io/specification) — metadata constraints, whole-file loading, progressive disclosure, and recommended `SKILL.md` size.
- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) — documented and differentiated roles, accountability, monitoring, and risk governance.
- [Digital.gov — Principles of plain language](https://digital.gov/guides/plain-language/principles) and [Writing for understanding](https://digital.gov/guides/plain-language/writing) — audience-aware organization, active voice, short sections, and explicit actors.
- [RFC 2119](https://www.rfc-editor.org/info/rfc2119/) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html) — controlled requirement terms and capitalization semantics.

### Limitations

- Vendor behavior changes. Recheck official documentation before creating or revising runtime-dependent governance.
- GitHub limits are feature-specific and must not be generalized to Codex, Claude Code, or every Copilot interface.
- NIST AI RMF 1.0 is under revision; this guide uses only its stable general principle that roles and responsibilities should be documented and differentiated.
- Local word-count targets are conservative design choices for this project. They require validation against actual runtime behavior and may be adjusted by a later approved project rule.
