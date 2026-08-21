# Enforcement hooks

**Authority:** none. This directory holds enforcement *carriers*, not rules. Every
rule enforced here is owned elsewhere and cited at the point of enforcement. If a
hook and its owning rule disagree, the rule governs and the hook is the defect.

## Why this exists

`CLAUDE.md` imports `AGENTS.md`, so the rules are read. Being read is not being
enforced. `DECISIONS.md` C-03 and D-74 both say so directly: instruction placement
enforces nothing on its own, and an enforcement carrier -- a managed setting or a
hook -- must be chosen per rule.

Until 2026-08-21 no carrier existed. Three failure classes recurred in spite of being
written down, and all three are mechanically detectable:

| Failure | Recorded as | Now caught by |
|---|---|---|
| A step named from memory, under a label belonging to another step | D-73, D-74 | `inject_plan_position.py` |
| A fidelity claim in a commit with no committed check behind it | D-53, D-88 | `gate_commit.py` |
| A session ending with a durable finding unwritten | `AGENTS.md` persistence requirement | `gate_persistence.py` |

## What is wired

`.claude/settings.json`:

| Event | Script | Effect |
|---|---|---|
| `UserPromptSubmit` | `inject_plan_position.py` | Reads `STATE.md` and puts the position table, blockers and next action into context. Never blocks. |
| `PreToolUse` on `Bash` | `gate_commit.py` | Exit 2 blocks the command. Gates `git commit` and `git push`. |
| `Stop` | `gate_persistence.py` | Exit 2 refuses the stop while governed files are uncommitted. Raises one dirty set once. |

## What `gate_commit.py` refuses

1. **A deletion in `DECISIONS.md`.** It is append-only. A rewritten line counts as a
   deletion, because it is one. Supersede an entry with a new entry.
2. **A secret value in staged content.** High-precision patterns only -- private key
   blocks and known credential prefixes. Prose *about* secrets passes, deliberately: a
   gate that fires on this repository's own governance text would train its reader to
   ignore it.
3. **Non-ASCII in a `.ps1`.** Windows PowerShell 5.1 reads a non-BOM source as ANSI,
   and one U+2014 becomes a string delimiter (`scripts/README.md` section 1).
4. **An unperformed-verification claim in the commit message** -- "by construction",
   "trivially true", "holds by definition". The gate does not judge whether the claim
   is true. It refuses the *class*, because this project has committed one (D-88).
5. **A plain force-push.** `--force-with-lease` passes.

## What it deliberately does not do

- **It has no bypass switch.** A gate with an escape hatch is a suggestion.
- **It never counts a skip as a pass.** Where a check cannot run -- an untokenisable
  command, a missing message file, no Hub clone -- it prints `SKIPPED -- not a pass`
  and says so on stderr. Reporting a skipped check as a pass is a defect this project
  has already committed once (D-65).
- **It does not judge intent.** It catches classes, not wrongness. A true claim
  phrased as "by construction" is blocked; that is the correct trade, because the
  phrasing is what made the false one invisible.

## Hub verification scripts

When a commit touches `scripts/` or `evidence/`, the gate runs
`scripts/Assert-ReferenceIntegrity.py` and `scripts/Test-HubRegistrySchema.py`
against the Hub clone. The clone path is `$WG_HUB_CLONE`, default
`/workspace/agents-hub-one`. A failure blocks. **An absent clone is reported as
`SKIPPED`, and the commit proceeds** -- a `workspace-governor` commit is not itself a
claim about the Hub tree. Do not turn a skip into a verification claim in the commit
message; gate 4 exists partly for that.

## Verification status

`python3 .claude/hooks/test_hooks.py` -- 31 cases, all passing as of 2026-08-21.
Every gate is exercised in **both** directions: it must block its defect and pass
clean input, per D-65. Cases include a rewritten line, a deleted line, a pure append,
`-am` with nothing staged, a token value, prose about tokens, the gate's own source
(its patterns must not match themselves), non-ASCII in a `.ps1` and in a `.md`, both
claim phrasings, five push forms, a non-Bash tool, an unbalanced quote, a clean tree,
a dirty tree, the same dirty set twice, an ungoverned file, another repository
entirely, and a `STATE.md` with no position section.

**Not verified, and it cannot be verified from here:** that Claude Code actually
fires these hooks in a live session. That needs a session opened in this repository
on the local machine. It is recorded as a `STATE.md` verification assignment with an
executor. The scripts are proven; the wiring is not. An environment boundary is not a
defect, and recording it does not weaken the requirement.

## Changing a hook

Run the harness. A hook change that is not covered by a case in both directions is
not finished -- add the case first, watch it fail, then make it pass.
