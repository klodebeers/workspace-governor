# Project Bootstrapper — design

**Status:** Design, revised 2026-08-27 against the actual intake board. Not built.
**Owner of this file:** the bootstrapper's purpose, where it sits in the sequence,
its input contract, its output, and what it is forbidden to do. **Not** where the
work stands — that is `STATE.md`. Backoffice planning record, not governance.

## Where it sits — corrected

It is **not** the first thing that runs. An earlier revision of this file said it
was, and that was wrong in a way that mattered: it would have had the bootstrapper
provisioning from a file that is empty at the moment it is written.

    ①  Intake board  →  writes the folder
    ②  /kickoff      →  discovery fills INTAKE-ANALYSIS.md
    ③  Bootstrapper  →  provisions from the completed analysis   ← here

The board writes `INTAKE-ANALYSIS.md` with all fourteen sections set to
`_Pending._`. Nothing can be justified from it until `/kickoff` has run. The
bootstrapper is the third step, not the first.

## What the board already does — do not rebuild it

Verified by reading `ProjectIntake.html`. On Save it writes, and **never
overwrites** an existing one of:

| Artifact | Note |
|---|---|
| `PROJECT-INTAKE.md` | The user's words. Versioned; prior version archived to `.history/` |
| `INTAKE-ANALYSIS.md` | Agent-owned, fourteen `_Pending._` sections |
| `AGENTS.md`, `CLAUDE.md` | Runtime-neutral rules, and the Claude loader |
| `.claude/settings.json` | Deny rule + PreToolUse hook |
| `.claude/hooks/protect-intake.mjs` | Baseline write protection |
| `.claude/commands/kickoff.md` | The discovery command |
| `attachments/` | Copies. Originals untouched |

It also refuses to write into a folder whose `PROJECT-INTAKE.md` names a
different project, and no-ops when the baseline hash is unchanged.

**So the baseline environment already exists.** What the board cannot do is the
*per-project* part: at Save time nothing is known yet, so every project gets the
same settings, the same hook and the same command. Selecting the subset a
particular project needs is the only gap, and it is the bootstrapper's whole job.

## Input — `INTAKE-ANALYSIS.md`

Not `PROJECT-INTAKE.md`. The board separates them into two files, and the
baseline is explicitly read-only to agents. The bootstrapper consumes the
analysis and reads the baseline only for its two constraint sections.

| Source | What it decides |
|---|---|
| Analysis § Project category and applicable technical disciplines | Which subagents and skills to enable |
| Analysis § Environment, tools and dependencies | Which hooks are meaningful, and the dependency list it declares |
| Analysis § Relevant repositories, files and interfaces | The scope it provisions |
| Analysis § Security and data-handling requirements | Whether a gate is warranted, and which |
| Analysis § Testing and evaluation strategy | Which verification skills and templates earn their place |
| Analysis § Execution sequence | Which templates the project will need, and when |
| Analysis § Conflicts detected | **Any entry here stops provisioning** |
| Baseline § 6 — included, preserved or avoided | Constraints it must not provision against |
| Baseline § 8 — decisions under human authority | What it must never auto-approve |

## Precondition — measured, not declared

The frontmatter fields do not answer this. `agent_analysis_status: pending` is
written by the board and **never updated by anything**; the analysis file's own
`status: pending-discovery` is likewise never updated. Trusting either would mean
trusting a flag nothing sets.

**Count instead**, exactly as the board's own analysis viewer already does:
sections are `## ` headings, incomplete ones still read `_Pending._`.

- Any section still `_Pending._` → **stop**, and name which ones.
- § Conflicts detected is non-empty → **stop**. The board's working rule 5 puts
  conflicts before affected work, and provisioning is affected work.
- § Execution-readiness statement complete → proceed.

It does **not** fall back to inferring from `README`, `package.json` or the tree.
Discovery is `/kickoff`'s job. A bootstrapper that guesses when discovery is
incomplete produces an environment nobody can trace to a stated requirement,
which is the failure this design exists to prevent.

## Idempotence key — `KLO-INTAKE-HASH` and `intake_version`

Both live in `PROJECT-INTAKE.md`. The bootstrapper records them in its
provisioning record. On a later run: same pair → **no-op**, reported as "already
provisioned from intake v*N*". Either changed → re-provision and report the delta
against what the previous intake justified.

That makes "running it twice is safe" checkable rather than hopeful, and it means
a changed baseline cannot leave a stale environment behind it silently.

## What it does, in order

1. **Read the analysis.** Incomplete, or conflicts present → stop and name them.
2. **Propose the environment** — every plugin, hook, subagent, skill and template
   with the line from the analysis that justifies it. Anything it cannot justify
   does not go in the list.
3. **Enable the subset and place the templates.** Project scope.
4. **Declare dependencies. Never install them.** The list and the command;
   running it is a separate, approved act.
5. **Verify it took**, and report what changed versus what was already correct.

Step 5 is the one that gets skipped, and skipping it is why an environment that
was never provisioned looks exactly like one that was.

## Templates

Selected from the Hub's `templates/`, on the same rule as everything else: **it
selects, it does not author.** A template the Hub does not carry is proposed
through `_inbox` and only then becomes available to place.

**Copied, not linked.** The board already copies attachments for the same reason,
and here copying is correct rather than a fallback: git on Windows materialises a
symlink as a text file containing its target path unless `core.symlinks` is set,
silently.

**A copied template is a second copy, and that is correct.** The one-owner rule
forbids copying a *rule*, because two copies can disagree about what is required.
A template exists to diverge — that is its function. What must not be silent is
the *other* divergence: the source template changing after the copy was placed.
So each placed template carries a provenance stamp — which template, which
version, when placed. Without it, "filled in as intended" and "stale copy of
something that has since changed" are indistinguishable.

It places them empty. Filling one in is a different job.

## Two scopes, never blurred

| Action | Scope | Approval |
|---|---|---|
| `plugin marketplace add`, installing a plugin | Machine (`~/.claude`) | **Asks first.** Affects every project on the machine |
| Enabling an installed plugin, hooks, settings, templates for this project | Project (`.claude/`) | Proceeds |

## Hard requirement on `.claude/settings.json`

**Read, merge, validate, write. Never replace.** Back up first; re-read after
writing and confirm it still parses.

The board already wrote a settings file here, so the bootstrapper is always
editing an existing one — this is the normal case, not the edge case. A settings
file that fails to parse is dropped **whole and in silence**, taking
`permissions.deny` with it, which silently *widens* what later sessions may do.

## Known defect in the environment it inherits

The board's generated `.claude/settings.json` gives its PreToolUse hook
`"command": "node"` with a separate `"args"` array. **There is no `args` field in
the hook schema** — `command` is the whole shell string — so Claude Code runs bare
`node`, which reads the hook payload from stdin as JavaScript and exits 1 on a
syntax error. Verified against CLI 2.1.42 and by execution.

Consequence: the `permissions.deny` rule works, and nothing else does. `Write`,
`MultiEdit` and `NotebookEdit` are not in the deny list, and Bash access to the
baseline is not blocked at all — while the generated `AGENTS.md` tells every agent
that both file tools and shell commands are covered.

Fix, in the board's `HOOK_SETTINGS`:

    "command": "node \"${CLAUDE_PROJECT_DIR}/.claude/hooks/protect-intake.mjs\""

Drop `args`. Add `Write(PROJECT-INTAKE.md)` and `MultiEdit(PROJECT-INTAKE.md)` to
the deny list so layer one covers what the matcher intends. **This is a board fix,
not a bootstrapper one**, and it is noted here because the bootstrapper would
otherwise inherit a guard that does not fire and report an environment as
provisioned. It is tracked as issue #45, which owns the close condition and the
question of what happens to folders the board has already provisioned.

## Explicitly not its job

Authoring skills, hooks or templates · installing dependencies · writing to
either intake file · governing anything. It configures an environment; it holds
no rule.

## How it is proven

Run it on a project it has never seen, from a completed analysis. Then check by
hand: every enabled component traces to a line in the analysis; nothing else is
enabled; `.claude/settings.json` still parses and its pre-existing keys survive;
and a second run reports no changes. A run that enables everything, or that
cannot say why a component is on, has failed even if the project works
afterwards.
