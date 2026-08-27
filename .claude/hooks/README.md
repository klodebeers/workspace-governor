# Enforcement carriers

**Authority:** none. This directory holds carriers, not rules. Every gate cites the
rule it enforces, and where a gate and its owning rule disagree, the rule governs and
the gate is the defect. `AGENTS.md` § Enforcement owns the three properties a gate
must have; this file owns **what is wired and what is proven.**

## Why this exists

`CLAUDE.md` imports `AGENTS.md`, so the rules are read. Being read is not being
enforced. `DECISIONS.md` C-03 and D-74 both say so: instruction placement enforces
nothing on its own, and a carrier -- a managed setting or a hook -- has to be chosen
per rule. Until 2026-08-21 no carrier existed in this repository.

## The architecture, and why it changed on day one

The first version put the content gates in a Claude Code `PreToolUse` hook that parsed
the shell command looking for `git commit`. An independent audit defeated it in eight
ways within minutes -- `git -C .`, `/usr/bin/git`, `sh -c '...'`, a variable holding
the command name, a repository alias, `commit-tree` + `update-ref`, `filter-branch`,
and a pathspec commit that the index-only diff never saw. Each produced **exit 0 with
empty output**. Two more findings were worse: one byte that UTF-8 could not decode
silently removed the secret scan and the encoding check, so a `.ps1` carrying the exact
cp1252 em dash `scripts/README.md` was written about passed cleanly.

A parser guessing what git will do cannot be the carrier. So:

| Layer | Where | What it owns |
|---|---|---|
| **git hooks** | `.githooks/pre-commit`, `.githooks/commit-msg` | The content invariants. Git runs them after deciding what the commit contains, for every invocation form. |
| **PreToolUse guard** | `.claude/hooks/gate_commit.py` | Only what a git hook cannot see: `--no-verify`, plumbing that writes history without hooks, force-pushes, and an uninstalled `core.hooksPath`. |
| **Stop gate** | `.claude/hooks/gate_persistence.py` | The persistence requirement at the end of a session. |
| **Prompt injection** | `.claude/hooks/inject_plan_position.py` | Puts the authoritative plan position into context every prompt. |
| **Delegation gate** | `.claude/hooks/gate_delegation.py` | Refuses a stop when the session claims an independent review, audit or adversarial check and no delegate ran. |
| **Performer injection** | `.claude/hooks/inject_delegation_check.py` | Puts the required-delegation criteria into context when a prompt is about review, audit or verification. |
| **Rule injection** | `.claude/hooks/inject_rules.py`, table in `.claude/hooks/rule-triggers.json` | Puts the section that owns a rule into context when a prompt is about the work that rule governs -- or, where the section exceeds the per-entry cap, a pointer saying to read it. Three of five entries are pointers today, so this carrier delivers rule *text* for a minority of them. Table-driven; holds no rule text of its own, and a check refuses a `why` field that quotes its section. |
| **Rule-trigger gate** | `wg_gates.check_rule_triggers`, checker in `scripts/Assert-RuleTriggerFidelity.py` | Refuses a commit that leaves any trigger-table entry pointing at a heading that no longer resolves. |

The two layers compose: the git hooks cannot be reached around except by the four cases
the guard refuses, and the guard refuses a commit while `core.hooksPath` is unset, so a
clone where nobody ran the setup step cannot commit at all rather than committing
ungated.

## Installation, and why it is enforced rather than documented

    git config core.hooksPath .githooks

One command, per clone. The guard treats a missing value as a blocking finding, because
a gate nobody installed reports no findings, which reads exactly like a clean result.

## What the git hooks refuse

1. **An entry line removed or rewritten in `DECISIONS.md`** -- it is append-only
   (`AGENTS.md` File ownership). A rewritten line counts, because it is a deletion.
   Prose and headings *outside* an entry are editable and pass with a note: the owning
   rule makes entries append-only, not the file's typography, and the first version
   refused a fix to the file's own title.
2. **A secret value in committed content** -- `AGENTS.md` Secrets. High-precision
   patterns only, and a `base64,` payload is excluded from the Google-key shape, which
   ordinary base64 otherwise matches.
3. **Non-ASCII in a `.ps1`** -- `scripts/README.md` section 1. Read as bytes, so an
   ANSI-encoded em dash is caught rather than crashing the check.
4. **An unbacked verification claim in the commit message** -- "by construction",
   "trivially true", "holds by definition", matched across line breaks because git
   joins several `-m` values with a blank line. This is a **proxy** for D-53, not a rule
   of its own: the phrase passes when the message names something re-runnable, which is
   what D-53 actually asks for. So a commit may describe or disclaim the phrase; only
   asserting it unbacked is refused.
5. **A Hub verification script failing**, when the commit touches `scripts/` or
   `evidence/`. The **committed** copy of each script runs, not the working-tree copy,
   which could otherwise be edited to make a failing check pass.

## What the delegation gate refuses, and what it cannot

It enforces `rules/VERIFICATION-RESOLUTION.md` § Performer selection: a claim that work
was independently reviewed, audited or adversarially checked requires an independent
performer in the record. The gate reads the transcript for a delegate spawn and refuses
the stop when the claim has none.

Three things it deliberately does not do. It does **not** judge whether delegation was
warranted -- that is judgement, and a gate has none. It does **not** refuse an honest
statement that you checked your own work; saying so plainly is what the rule asks for
when nothing was delegated, and the disclaimer forms are matched first for exactly that
reason. And it does **not** catch work that should have been delegated and was not: no
documented hook fires on that, so the gate catches the *claim*, not the omission. That
gap is real and is stated in the rule as well as here.

A claim it cannot check -- an unreadable or missing transcript -- **fails**, like every
other check that cannot run.

## What the rule-trigger gate refuses, and why it is not diff-scoped

`.claude/hooks/rule-triggers.json` names, per entry, an owning file and an **exact**
heading. `inject_rules.py` reads that section live when the entry's trigger matches, so
no copy of a rule lives in the table -- the one-owner rule in `AGENTS.md` § File
ownership would forbid one, and a copy drifts with no error.

That design moves the failure rather than removing it. The way an entry breaks is that
someone **rewords the heading in the owning file**. The table is untouched, this gate's
own file is untouched, and from then on the hook injects `RULE NOT READ` where the rule
used to be. A table of NOT READ notices reads exactly like a table that is working.

So the check runs on every commit rather than only when the table is staged, and a
finding blocks. Headings are matched exactly after normalisation, never by substring:
substring matching is a defect this repository has already paid for, when `section()`
in `inject_plan_position.py` captured `## Current state and blockers` for a request for
`## Blockers` and read the wrong section silently.

Three things it deliberately does **not** do:

- **It does not judge whether a trigger is well chosen.** An entry that never fires and
  an entry that fires on everything both pass. Wallpaper is not a resolvable-heading
  problem.
- **It does not make injection enforcement.** Injection is advisory -- it puts a rule in
  front of a decision and cannot refuse. Adding an entry enforces nothing
  (`DECISIONS.md` C-03, D-74).
- **It does not reach outside this repository.** Project hooks fire only for sessions
  whose working directory is this project, so this governs the backoffice and nothing
  else. Whether a user-scope carrier can govern every session is unverified and has a
  procedure: `evidence/USER-SCOPE-HOOK-CARRIER-2026-08-27.md`.


## What it means that a check cannot run

`LEARNINGS.md` L-026: "A check that cannot run must fail, never skip." Earlier these
paths printed `SKIPPED -- not a pass` to stderr on exit 0 -- which the hooks reference
sends to the debug log and nowhere else, so a skip was operationally a pass, invisibly.

Now every one of them blocks: an unreadable diff, an unreachable Hub clone on a commit
touching `scripts/` or `evidence/`, a missing message file, and a machine with no Python
interpreter. The git hooks are `sh` shims that try `python3`, then `python`, then
`py -3`, and **refuse the commit** if none is found, because the operator's machine is
Windows and `python3` is frequently not the name on PATH there.

## Verification status

`python3 .claude/hooks/test_hooks.py` -- **151 cases, all passing** as of 2026-08-27.
The content gates are exercised through **real `git commit` calls** in throwaway
repositories, so a case proves the gate as git actually invokes it, including the eight
forms that defeated the first version.

`python3 .claude/hooks/test_hooks.py --mutations` additionally breaks each gate on
purpose and requires the suite to notice: **36 mutations, 33 caught, 0 behaving
wrongly, at `f6d081a`** -- the three survivors are controls that must survive,
each carrying, in the row itself, the reason no case can discriminate it.

The harness mutates `scripts/` as well as `.claude/hooks/`, and the suite runs
`Assert-RuleTriggerFidelity.py --selftest` (27 cases) as a case of its own. Both
were added because an independent auditor built nine mutation rows for fixes
living in the checker and **all nine survived**: the harness could not reach the
file they were in, and nothing automated ran the selftest that covered them. A
check proven only by a command a human remembers to type is proven for as long
as they remember.

**Read this before trusting a number here.** It took seven runs to get one that
measured anything, and the failures are more instructive than the total:

- **Run 1** reported 27 of 27 caught while the suite crashed on a path bug in
  every one. A crash exits non-zero, and the harness reads non-zero as "caught".
  Only the two no-op controls, which must survive and were flagged, exposed it.
- **Runs 4 and 6** each reported a **stale** row. Retargeting the first showed
  the mutation then survived the whole suite: the case meant to cover it deleted
  a file from disk and from the index together, so the guard was never
  exercised. A stale row tests nothing while still counting in the total, which
  is the same false-clean shape as a check that cannot run -- so the harness
  reports stale as WRONG, and that is what caught both.
- Twice while wiring the checker in, the environment defect was reintroduced:
  a relative import that broke under `WG_HOOKS_DIR`, then an unconditional
  override that hid the missing-injector case. **Run the unmutated control in
  both layouts** -- real repo and harness copy -- before believing any run.

**Not verified, and not verifiable from the environment these were written in:**

- That Claude Code fires the `.claude/` hooks in a live session. The scripts are
  driven directly with synthetic hook JSON, which tests the scripts and not the wiring.
  An earlier version of this file gave the reason as "hook registration is read at
  session start" -- **that reason was wrong**: the hooks reference says direct edits to
  settings files are normally picked up by a file watcher. The boundary stands, the
  stated reason did not.
- That a Python interpreter is reachable from Git's shell on the operator's Windows
  machine. If it is not, the shims refuse commits, which is the safe direction but is
  still a thing to find out on that machine rather than here.

Both are recorded in `STATE.md` § Verification assignments with an executor and a
method. A skipped verification is never reported as a pass.

## Known limits, stated rather than glossed

- **`git stash` defeats the stop gate.** A stash makes the tree clean, so the gate
  permits the stop while the work is unpersisted -- the exact failure it exists to
  catch. Nothing here detects it.
- **`commit-tree` + `update-ref` still write history** if run outside a session where
  the guard sees them.
- **The guard's detection is textual** and therefore best-effort. That is why the
  content gates are not in it: an unrecognised command still meets the git hooks.
- **No gate judges intent.** These catch classes, not wrongness.

## Changing a gate

Run the suite, then run it with `--mutations`. A change not covered by a case in both
directions is not finished: add the case first, watch it fail, then make it pass. If a
mutation of your new code survives the suite, the case you added is decorative.
