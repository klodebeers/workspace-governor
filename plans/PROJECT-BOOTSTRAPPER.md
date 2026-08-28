# Project Bootstrapper — design

**Status:** Design accepted in conversation 2026-08-27, not built.
**Owner of this file:** the bootstrapper's purpose, its input contract, its
output, and what it is forbidden to do. **Not** where the work stands — that is
`STATE.md`. Backoffice planning record, not governance.

## What it is

One persona. The first thing that runs in a project. It reads the intake the
dashboard produced, works out what this project needs, and **provisions the
environment** — enabling the subset of plugins and hooks this project actually
uses, and nothing else.

It **selects; it does not author.** It picks from a registry. Writing a skill or
a hook is a different job with a different owner. Keeping it a selector is what
keeps it small enough to be reliable.

## Why a provisioner and not a reader

An earlier version of this design had it return an orientation summary. That is
weaker, and the reason matters: a summary informs one agent, once, and is gone.
Provisioning changes what **every later session loads**, which is where the
reported drift actually comes from.

It also fixes the relevance problem the right way round. Relevance is decided
**once per project, at bootstrap**, from stated intent — not per prompt by
pattern matching, which is what the rule injector in this repository does and
which becomes wallpaper at scale.

## Input — the intake file, and the seam is already closed

Its input is `PROJECT-INTAKE.md`, written into the project folder by the Project
Intake Dashboard. The field list this design first guessed at is unnecessary: the
board already carries everything the bootstrapper needs, and more precisely than
the guess did.

**It reads Part 2, the agent-derived half — not Part 1.** Part 1 is the user's
own wording and is authoritative; Part 2 is the coding agent's analysis. The
board's working rule 6 keeps them separate, and the bootstrapper is a consumer of
the analysis, not an interpreter of the request.

| Intake section | What it decides |
|---|---|
| Part 2 § Project category and applicable technical disciplines | Which subagents and skills to enable |
| Part 2 § Environment, tools and dependencies | Which hooks are meaningful, and the dependency list it declares |
| Part 2 § Relevant repositories, files and interfaces | The scope it provisions |
| Part 2 § Security and data-handling requirements | Whether a gate is warranted, and which |
| Part 2 § Testing and evaluation strategy | Which verification skills earn their place, and which templates |
| Part 2 § Execution sequence | Which templates the project will need, and when |
| Part 1 § 6 — included, preserved or avoided | Constraints it must not provision against |
| Part 1 § 8 — decisions under human authority | What it must never auto-approve |
| Part 1 § Attachments | What arrived with the project |

## Precondition, read from the file itself

The frontmatter carries `agent_analysis_status`. While it is `pending`, Part 2 is
`_Pending._` and there is nothing to provision from. **The bootstrapper does not
run, and it does not improvise.**

It specifically does **not** fall back to inferring from `README`,
`package.json` or the tree. Discovery is the intake and discovery manager's job,
and that manager already exists. A bootstrapper that guesses when discovery is
incomplete produces an environment nobody can trace to a stated requirement --
which is the failure this whole design exists to avoid. It stops and names what
is pending.

The board's working rule 9 is the readiness gate and the bootstrapper inherits
it: it runs once intended outcome, starting point, scope, acceptance criteria,
approach, verification method and authority can each be stated with evidence.

## Idempotence key — `KLO-INTAKE-HASH` and `intake_version`

The file carries `<!-- KLO-INTAKE-HASH: ... -->` and an `intake_version`. The
bootstrapper records both in its provisioning record. On any later run:

- same hash and version -> **no-op**, reported as "already provisioned from
  intake v*N*";
- either changed -> re-provision, and report the delta against what the previous
  intake justified.

That is what makes "running it twice is a no-op" checkable rather than hopeful,
and it means a changed baseline cannot leave a stale environment behind it
silently.

## It never writes to the intake file

Working rules 6 and 7 settle this: agent-derived conclusions stay in Part 2, and
architecture, state, decisions and evidence belong in their own owner files. The
bootstrapper's output is `.claude/settings.json` and its own provisioning record.
It does not append to Part 2, and it does not touch Part 1 at all.

## What it does, in order

1. **Read the intake.** No intake and no fallback signal is a stop, reported —
   not a guess.
2. **Propose the environment.** The plugins, hooks, subagents and skills this
   project needs, each with the line from the intake that justifies it. Anything
   it cannot justify from the intake does not go in the list.
3. **Enable the subset**, and place the templates the intake justifies. Project
   scope only.
4. **Declare dependencies. Never install them.** It produces the list and the
   command. Running it is a separate, approved act.
5. **Verify it took**, and report what changed versus what was already correct.

Step 5 is the one that is always skipped, and skipping it is why an environment
that was never provisioned looks exactly like one that was.

## Templates — selected and placed, like everything else

It places the templates this project needs, from the Hub's `templates/`. Same
rule as the rest: **it selects; it does not author.** A template the Hub does not
carry is not invented here — it is proposed through `_intake-hub`, which is the
door for contributing one, and only then becomes available to place.

**Copied, not linked.** The intake dashboard's own requirement already allows
this — *"if symlinks are too difficult, copying the files is fine too"* — and on
this operator's machine copying is the correct choice, not the fallback: git on
Windows materialises a symlink as a text file containing its target path unless
`core.symlinks` is set, and it fails silently
(`evidence/ADAPTER-PATTERN-REFERENCE-2026-08-27.md`). A template that is silently
a one-line file naming another file is worse than no template.

**A copied template is a second copy, and that is correct here.** The one-owner
rule forbids copying a *rule*, because two copies of a rule can disagree about
what is required. A template exists to be filled in and to diverge — divergence
is its function. What must not be silent is the *other* divergence: the source
template changing after the copy was placed.

So each placed template carries a provenance stamp — which template, which
version, when placed. That is what distinguishes "filled in, as intended" from
"stale copy of something that has since changed", and without it the two are
indistinguishable, which is the failure shape this whole design keeps meeting.

**It does not fill them in.** Placing a template and completing it are different
jobs. It places the empty template and names it in the provisioning record.

## Two scopes, never blurred

| Action | Scope | Approval |
|---|---|---|
| `plugin marketplace add`, installing a plugin | Machine (`~/.claude`) | Asks first. It affects every project on the machine |
| Enabling an installed plugin, hooks, settings for this project | Project (`.claude/settings.json`) | Proceeds |

Conflating these is how a per-project decision becomes a machine-wide one.

## Hard requirement on writing `.claude/settings.json`

**Read, merge, validate, write. Never replace.** Back up first. Re-read after
writing and confirm the file still parses.

This is not defensive style. A settings file that fails to parse is dropped
**whole and in silence** — every other setting in it goes with it, including
`permissions.deny`, whose loss silently *widens* what later sessions may do.
This session produced a procedure that would have done exactly that, and it was
caught by an independent audit rather than by the author.

## Idempotent

It runs on new projects and again whenever a project changes. Running it twice
is a no-op that reports "already correct" rather than rewriting. An environment
it has already provisioned must be distinguishable from one it has not.

## Explicitly not its job

Authoring skills or hooks · installing dependencies · touching the intake file ·
governing anything. It configures an environment; it holds no rule.

## How it is proven

Run it on a project it has never seen, from an intake file. Then check by hand:
every enabled component traces to a line in the intake; nothing else is enabled;
`.claude/settings.json` still parses and its pre-existing keys survive; and a
second run reports no changes. A run that enables everything, or that cannot say
why a component is on, has failed even if the project works afterwards.
