# Runtime delegation and messaging mechanics -- 2026-08-21

**Status:** vendor mechanics extracted from primary sources; the project-facing
conclusions are marked as such. Nothing here is verified against a live runtime, and
several items are explicitly recorded as not documented rather than absent.

**Why it was gathered.** The delegation practice keeps being forgotten. A rule is owed
saying when work must be handed to a delegate rather than done inline, and it will be
given a carrier rather than left as advice. These are its inputs. Issue #42 holds the
rule.

**Sources read**, by three independent researchers, each fetching the pages rather than
recalling them: `code.claude.com/docs/en/agents`, `/sub-agents`, `/agent-view`,
`/agent-teams`, `/cross-session-messaging`, plus `/hooks`, `/settings`, `/errors`,
`/tools-reference` and `/sessions` where a mechanic depended on them.

**A version caveat that binds anything written against this.** The agent-teams page
describes behaviour "as of v2.1.178" and cites changes at eight later versions;
cross-session messaging requires v2.1.224+ (v2.1.234+ on native Windows), and
`notify_when_idle` requires v2.1.236+ **in both sessions**. A rule keyed to these
mechanics is keyed to a moving surface.

## 1. What the docs decide about when to delegate

Documented, and quotable:

- Subagents: "the task produces verbose output you don't need in your main context";
  "you want to enforce specific tool restrictions or permissions"; "the work is
  self-contained and can return a summary".
- Main conversation: "the task needs frequent back-and-forth"; "multiple phases share
  significant context"; "a quick, targeted change"; "latency matters".
- Teams: research and review where delegates "share and challenge each other's
  findings", separate modules, competing debugging hypotheses, cross-layer work. Not
  teams: "for sequential tasks, same-file edits, or work with many dependencies, a
  single session or subagents are more effective."
- Sizing: 3-5 delegates; "three focused teammates often outperform five scattered ones."
- Cross-session messaging: for a peer that is **already running** and needs something
  mid-task. The page routes every other multi-session need elsewhere -- resume, teams,
  agent view, Remote Control, channels.

**Not documented on any page read: when a single piece of work must be delegated to one
subagent rather than done inline.** That threshold is this project's to write, and it is
the part that keeps being skipped.

**And the vendor's rationale is not this project's rationale.** Every documented
criterion is about context economy or capability restriction. None is about correctness
or independence. A rule mandating delegation for review or verification goes beyond the
documented rationale -- legitimately, but it cannot cite these pages as its basis.

## 2. What delegation costs

Fresh context, totally: a subagent "doesn't see your conversation history, the skills
you've already invoked, or the files Claude has already read." The parent's only channel
is the delegation prompt. What returns is the final report and nothing else.

What is lost across the boundary: output style, auto memory, the parent's context-window
size, and -- documented explicitly -- the tool pool, because "the same definition can
resolve to different tools in the foreground and the background."

Caps: 20 concurrently running subagents by default, then `Concurrent subagent limit
reached` with an instruction not to retry; three layers of nesting; `maxTurns`. Teams
have no hard cap, and token use "scales with the number of active teammates" -- the
agent-view page quantifies the same thing as "ten agents in parallel uses quota roughly
ten times as fast as one."

**No wall-clock timeout for a subagent is documented on the pages read.**

## 3. Independence -- what is supported and what is inference

Supported: a fresh isolated context window, no inherited conversation history, its own
system prompt, a separate prompt cache, and "input isolation" as the vendor's own phrase
for what a fork deliberately drops.

**Inference, not their claim:** that this isolation yields independent judgment, or that
a delegate is a check on the parent. The mechanism supports it; the docs never say it.

**A counter-pressure worth keeping.** Every custom subagent loads the full CLAUDE.md
hierarchy, so a delegate is **not** independent of this repository's governance -- it
arrives carrying it. Independence is from the parent's conversation, not its rules.

Two limits bound what a parent may do to a delegate: no message from any agent counts as
the user's approval for a pending permission prompt, and no agent message can change a
subagent's permission settings, `CLAUDE.md`, or configuration.

## 4. A message cannot carry an obligation

Four documented limits on an inbound cross-session message: it cannot approve anything;
it cannot change configuration; a slash command in its text "arrives as plain text" and
is never executed; and permission prompts still fire. The receiving Claude is told the
message "came from another session, not from you."

**So work can be reported across a session boundary and never delegated across one.** An
obligation must come from somewhere the recipient already answers to. This agrees with
`rules/CONTEXT-AND-ORCHESTRATION.md`, which places the duty on the parent and calls a
child summary "a routing aid, not final proof".

The transport also supplies no handoff shape: plain text only, no schema, no validation.
Issue #13's five competing field sets are not arbitrated by anything external.

**Five documented paths where a message is silently not acted on:** refused inbound (and
"a refusing session shows no visible change"); held inbound, which is the *default* when
the receiver bypasses permission prompts and the sender does not; an unanswered hold
dropped after `dialogExpiry`, five minutes by default; duplicate and loop suppression,
which "drops identical repeats arriving within a short window"; and held-store overflow
past 100. Sender-side notice is conditional on being "an interactive session on this
machine". A successful send is not evidence that work was handed over.

## 5. The trap that inverts an orchestration flow

With `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, a subagent that Claude **names** launches
as a teammate instead. A subagent's result returns to the caller; a teammate's idle
notification "doesn't carry the teammate's output". The docs state the consequence: "an
orchestration flow that waits on subagent results can stall."

Settings precedence puts **managed settings last**, so an organisation can enable teams
from a layer this repository does not control, and the page warns that "teams can form
even when you didn't ask for one". A delegation rule written as "hand it over and use
what comes back" fails there, and the failure looks like a delegate that finished
successfully and said nothing.

## 6. Carriers available for a delegation rule

| Mechanism | What it can enforce |
|---|---|
| `PreToolUse` hook, exit 2 | Blocks a tool call. Hooks from settings files "also run before every tool a subagent uses", so a gate reaches inside delegates. **Matcher support for `Agent`/`Task`/`SendMessage` by name is not documented** and must be proven before it is relied on |
| `SubagentStart` / `SubagentStop` | Matcher input is the agent type name, so which delegate ran is observable |
| `TaskCreated` / `TaskCompleted` / `TeammateIdle`, exit 2 | Refuse creation, refuse completion, or send a teammate back to work |
| `permissions.deny: ["Agent(name)"]` | Refuses a delegate type outright. **Denying `SendMessage` also removes messaging to subagents and teammates** -- one tool serves both |
| Managed settings | The only tier nothing local overrides |
| Subagent definition `tools` / `model` | The one documented way to constrain what a delegate may do; a teammate honours both |

**The structural gap.** Every documented hook fires on something happening -- a tool
used, a delegate started, a delegate stopped. **Nothing fires on work being done inline
that should have been delegated.** There is no negative trigger, so a carrier has to be
built inside-out: catch the *claim* of independent review with no delegate in the
transcript, rather than the omission itself.

## 7. What this changes for artifacts already in the Hub

Recorded here because it bears on #10, #36 and #19, and because the researcher checked
the live tree rather than reasoning from the schema:

- A Claude Code subagent definition is **Markdown with YAML frontmatter**; `name` and
  `description` are the only required fields. The Hub's accepted definition is JSON and
  the schema pins `\.json$`. **Inference:** a `.json` file in an `agents/` directory has
  no frontmatter, so it meets the documented skip rule for a file with no `name` -- and
  that skip is "without reporting it in the session".
- `description` means "when Claude should delegate to this subagent". The Hub has no such
  field; the delegation condition lives in `orchestration/routing.json`'s `trigger`
  strings, and **the vendor router reads only the request, the `description`, and current
  context**. So `routing.json` has no documented path into runtime selection.
- Every runtime capability field -- `tools`, `permissionMode`, `model`, `hooks`,
  `mcpServers`, `effort` -- is barred from Hub governance by § Runtime Neutrality and
  § Canonical Assets. **A vendor-format definition therefore cannot be a Hub canonical
  asset.** It is an adapter artifact, and the adapter has no named owner: that is U-4,
  now #36, which this makes load-bearing rather than latent.
- `context[]` paths are loaded by nothing. The documented preload channels are `skills:`
  and the CLAUDE.md hierarchy. A bare path becomes an instruction to `Read`, if something
  puts it in the body. That is #38.
- Team identity is disjoint from the registry: team names are session-derived, teammate
  names are lead-chosen at spawn, and `.claude/teams/teams.json` in a project "is not
  recognized as configuration". A Hub-authored team topology would be inert.

## 8. Not verified

- No live runtime was exercised. Every mechanic here is documentation, not observation.
- Whether unknown frontmatter keys survive into an emitted definition is not documented,
  and needs an empirical check this environment cannot perform.
- The cross-session size cap is stated as about a million characters on one page and
  100MB on another. Not reconcilable from the pages read; the smaller figure binds.
- Message ordering is not documented.
- `isolatePeerMachines` did not appear in the settings reference fetch; it is documented
  only on the cross-session page.
