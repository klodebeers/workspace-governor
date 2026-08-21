# Enforcement gates -- independent audit and rebuild, 2026-08-21

**Status:** findings confirmed by reproduction, gates rebuilt, suite rebuilt. Two
verifications remain assigned to the operator's machine and are named as such.

**Method.** An independent adversarial audit was given the six gate files, the rules
they cite, and the vendor hooks reference, and told to construct bypasses rather than
report impressions. It worked in throwaway repositories and modified nothing. Its
findings were then reproduced here before any of them was accepted.

## Confirmed by reproduction

Each of these was re-run in this environment, not taken on the audit's word.

| Finding | Reproduction |
|---|---|
| `git -C . commit` defeats the gate entirely | `exit 0`, empty stderr, entry line rewritten and committed |
| One byte UTF-8 cannot decode removes the secret scan and the encoding check | `.ps1` containing the cp1252 em dash `0x97`: `exit 0`, empty stderr. A `ghp_` token sitting behind the same byte: `exit 0` |
| `-am` skips the message gate | claim committed verbatim; the append-only half fired while the message half did not |
| A later `--force-with-lease` disarms the push gate | `git push --force origin main && echo --force-with-lease` -> `exit 0` |
| The stop gate is inert in a linked worktree | dirty `STATE.md` in a worktree -> `exit 0`; the same file dirty in the main checkout -> `exit 2` |

The audit reported eight bypass forms; five were reproduced directly and the remaining
three (`sh -c`, a shell variable, a repository alias) follow from the same parser
defect and were confirmed against the rebuilt gates instead, where all five fail.

## The root cause, stated once

The carrier was wrong, not the checks. A `PreToolUse` hook receives the shell command
as text and has to guess what git will do with it. Guessing is defeated by any
indirection, and the index-only diff cannot see what a pathspec commit records. The
checks moved to `.githooks/`, where git runs them against the actual staged tree after
it has decided what the commit contains.

`git rev-parse` also had to stop being read as text: `subprocess` with `text=True`
raised on undecodable bytes, the bare `except` turned that into a non-zero return, and
every caller read non-zero as "nothing to check". One byte was enough to delete two
gates, and the byte in question is the one `scripts/README.md` section 1 exists to
prevent.

## After the rebuild

The five bypasses were re-run against the new gates:

    git -C . commit -am x                    -> refused
    /usr/bin/git commit -am x                -> refused
    sh -c "git commit -am x"                 -> refused
    git save -am x   (repository alias)      -> refused
    git commit -m x -- DECISIONS.md          -> refused

And the forms that evade a git hook are refused earlier, by the guard: `--no-verify`,
`-n`, `commit-tree`, `update-ref`, `filter-branch`, `fast-import`, `--force`, `-f`,
`--mirror`, a leading-plus refspec, and a `core.hooksPath` that is not installed.

## Findings accepted and fixed beyond the bypasses

- **A skip was a pass, invisibly.** `SKIPPED -- not a pass` went to stderr on exit 0,
  which the hooks reference routes to the debug log only. Every skip path now blocks.
- **Gate 5 had no test cases at all**, in either direction, while `README.md` and D-90
  claimed every gate was proven in both. Making it never block on failure left the
  suite at 31 of 31.
- **False blocks on clean input**, each now passing: a `base64,` data URI matching the
  Google-key shape; a correction to a non-entry line of `DECISIONS.md`; a commit
  message that *describes or disclaims* the banned phrase rather than asserting it.
- **The stop gate invented its own governed-file list**, omitting `AGENT-SSOT.json` and
  `USER-SSOT.json` which the `AGENTS.md` ownership table names, and its loop guard
  hashed status letters rather than content, so replacing a dirty file's contents
  entirely reused the marker and it stayed quiet.
- **The injector matched headings by substring**, so `## Current state and blockers`
  captured a request for `## Blockers` and the real section was never read; a clipped
  row could hide its own `~~closed~~` marker; and overall truncation dropped the tail,
  which is the next action.
- **`python3` on the operator's Windows machine.** The audit could not test it and said
  so; the concern is sound. The git hooks are now `sh` shims that try `python3`,
  `python`, then `py -3`, and refuse the commit if none is found.

## One finding rejected, with its ground

The audit reported that `AGENTS.md` § Enforcement asserts "five checker defects"
against its cited source, D-65, which says eight demonstrations and eleven regression
cases. **The count is correct and sourced:** `LEARNINGS.md` L-026 names exactly five
checker defects and lists each one. The defect was the **citation**. The paragraph now
cites L-026 for the five and D-65 for the both-directions rule. Read at the time, not
recalled -- `DECISIONS.md` D-87.

## Two claims of mine that the audit corrected

- "Hook registration is read at session start, so the session that wrote them could not
  have had them active" appeared in `README.md`, D-90 and `STATE.md`. The hooks
  reference says direct edits to settings files are normally picked up by a file
  watcher. **The boundary stands; the reason given for it was wrong**, and it was the
  reason the verification was deferred rather than attempted.
- "31 cases, every gate exercised in both directions" was asserted in four places
  within an hour of the gates existing. The suite did pass 31 of 31. The audit then
  mutated the source in 25 places and **ten mutations survived undetected**, including
  deleting every governed-path prefix from the stop gate and making the Hub check never
  block on failure. Passing is not proving.

## What replaced the claim

`python3 .claude/hooks/test_hooks.py` -- 87 cases, all passing. The content gates are
exercised through **real `git commit` calls**, so each case proves the gate as git
invokes it, including every bypass form above.

`python3 .claude/hooks/test_hooks.py --mutations` breaks each gate on purpose and
requires the suite to notice. Result: **18 mutations, 17 caught, one no-op control
correctly not flagged.**

The first mutation run left two survivors, and one was a real gap rather than a harness
artefact: every encoding case added a *new* file, so a mutation that read `HEAD` instead
of the index was invisible. A case that edits an already-committed `.ps1` now covers it,
in both directions -- a bad edit to a clean file is refused, and a repair to an
already-bad file passes. That is what the mutation mode is for: the gap was in the
cases, and only breaking the code found it.

## Still not verified, and assigned

1. That Claude Code fires the two `.claude/` hooks in a live session. Scripts driven
   with synthetic hook JSON test the scripts, not the wiring.
2. That a Python interpreter is reachable from Git's shell on the operator's Windows
   machine. Failing closed is the safe direction, and it is still unknown.

Both are in `STATE.md` § Verification assignments with an executor, a method and a
recheck trigger. Neither is reported as a pass.

## Known limits carried forward

`git stash` makes a dirty tree clean, so the stop gate permits the stop while the work
is unpersisted -- the exact failure it exists to catch, and nothing here detects it.
`commit-tree` plus `update-ref` still write history when run where the guard does not
see them. The guard's own detection is textual and best-effort, which is precisely why
the content gates are not in it.
