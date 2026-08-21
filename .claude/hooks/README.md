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

`python3 .claude/hooks/test_hooks.py` -- **87 cases, all passing** as of 2026-08-21.
The content gates are exercised through **real `git commit` calls** in throwaway
repositories, so a case proves the gate as git actually invokes it, including the eight
forms that defeated the first version.

`python3 .claude/hooks/test_hooks.py --mutations` additionally breaks each gate on
purpose and requires the suite to notice: **18 mutations, 17 caught, and the one that
survives is a no-op control that must not be flagged.** Two rounds were needed -- the
first run left two survivors, one of which was a real gap (every encoding case added a
new file, so reading `HEAD` instead of the index was undetectable) and is now covered by
a case that edits a file already committed. This exists because the first harness reported
31 of 31 passing while an audit found **10 mutations surviving undetected** -- among them
deleting every governed-path prefix from the stop gate, and making the Hub check never
block on failure. A suite that passes when the code is broken is not evidence, and
`31 of 31` was not the claim it looked like.

**Not verified, and not verifiable from the environment these were written in:**

- That Claude Code fires the two `.claude/` hooks in a live session. The scripts are
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
