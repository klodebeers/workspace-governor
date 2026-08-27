# User-scope hook carrier -- what Step 9 has to deliver

**Date:** 2026-08-27
**Status:** Finding 1 verified from committed evidence. Finding 2 verified by
demonstration in this repository. Finding 3 **NOT VERIFIED** -- it names a
verification that only the operator's machine can perform, and the procedure is
below.

## Why this was written

Reported symptom, 2026-08-27: agents across the fleet are drifting -- reading
superseded plans, citing step labels that belong to other steps, not following
plain instructions. The question asked was whether more governance would fix it.

## Finding 1 -- the wiring named in D-75 cannot carry a rule. Verified.

`DECISIONS.md` D-75 names the runtime wiring files as `.claude/CLAUDE.md` and
`.codex/AGENTS.md`. `evidence/RUNTIME-CONVENTIONS-2026-08-20.md` classifies every
Claude Code mechanism as enforceable or advisory, and puts both of those in the
second class:

> **Enforced:** `permissions.allow` / `permissions.deny`, managed-only keys,
> **hooks**, sandbox flags.
> **Advisory or startup-only:** model selection, output style, and **all
> `CLAUDE.md` content**.

So Step 9 as specified delivers discovery and nothing enforceable. That is not a
defect in the wiring -- it is the wiring doing what an instruction file does.
`DECISIONS.md` C-03 already records the general form and remains open.

**Consequence.** Drift is advisory content losing to context pressure. A carrier
that is itself advisory cannot fix it. Two instruction files is the wrong
deliverable for Step 9, and completing Step 9 exactly as written would leave the
reported symptom untouched.

## Finding 2 -- the load is the mechanism of the drift. Verified.

Measured against `110a9e3`, the bootstrap `AGENTS.md` mandates before any work:

| File | Bytes |
|---|---|
| `DECISIONS.md` | 125,865 |
| `plans/AGENT-HUB-CONSOLIDATION.md` | 45,429 |
| `STATE.md` | 40,877 |
| `LEARNINGS.md` | 23,322 |
| `AGENTS.md` + `README.md` | 23,425 |
| **Total** | **258,929 (~64k tokens)** |

Self-correcting or superseding statements inside that set, counted by pattern
(`supersed|corrected|was wrong|no longer|stale|earlier revision|inverted|...`):
`DECISIONS.md` 62, `plans/AGENT-HUB-CONSOLIDATION.md` 28, `STATE.md` 25,
`LEARNINGS.md` 6 -- **121 total**.

An agent that must compress 259 KB to act retains the narrative, not the current
rule. D-73 is that failure already recorded: work executed under step labels
belonging to other steps, with no error appearing anywhere. Old records still say
"Step 2" for work that is the plan's Steps 5, 7 and 8, so an agent reading history
faithfully lands on the wrong step.

The Hub root contract is not implicated: `.agents-hub/AGENTS.md` is 7,213 bytes,
22% of the 32 KiB budget.

## Finding 3 -- the carrier that would reach every session is NOT VERIFIED here.

Project hooks in `.claude/settings.json` fire only for sessions whose working
directory is that project. They therefore cannot govern work in
`C:\KloWorkspaces\<project>`, and cannot govern a session opened inside
`.agents-hub` itself. Building more of them in `workspace-governor` governs only
the backoffice.

The candidate carrier is a **user-scope** `~/.claude/settings.json` carrying the
same hooks: directory-independent, and in the enforceable class per Finding 1.

**This is not in our verified record.** The runtime-conventions table lists
`./.claude/settings.json` and `./.claude/settings.local.json` only. It records
user scope for *skills* (`~/.claude/skills/`) but says nothing about settings.
Absence from that table is not evidence either way -- it was not the question that
evidence set out to answer. Nothing should be built on user-scope hooks until the
procedure below has run.

**Codex has no equivalent.** It is `AGENTS.md`-native and advisory-only. Claude
Code can be given trigger-dispatch; Codex cannot, by this mechanism. Any design
that assumes fleet-wide uniformity will fail silently on the Codex side.

## Procedure -- settle Finding 3 on the operator's machine

Both directions, per `DECISIONS.md` D-65. A run that only shows the trace
appearing proves nothing: the trace must also be absent when the hook is removed,
or something else is writing it.

1. Create `~/.claude/hooks/trace_probe.py`. It appends one line -- an ISO
   timestamp and the session's working directory -- to `~/.claude/hook-trace.log`,
   prints nothing, and exits 0.
2. Register it as a `UserPromptSubmit` hook in `~/.claude/settings.json` only.
   Do not put it in any project's settings.
3. Note the log's current line count, or that it does not exist.
4. **Positive direction.** Open a fresh session in each of three directories and
   submit one prompt in each:
   - a governed workspace project under `C:\KloWorkspaces`
   - `~/.agents-hub`
   - a directory that is not a git repository at all
5. Record the log. Expected if user scope loads: three new lines, one per
   directory, each naming that directory.
6. **Negative direction.** Remove the hook from `~/.claude/settings.json`. Open a
   fresh session in the same governed workspace project, submit one prompt.
7. Record the log. Expected: **no new line.** A new line here means the trace has
   a second source and step 5 proved nothing.
8. Record both directions in `evidence/`, including a partial or negative result.
   A hook that fires in two of three directories is a finding, not a retry.

**Reading the result.** All three fire and the negative direction is clean: user
scope is the carrier, and the injector set moves there. Any directory misses:
user scope is not sufficient alone, and coverage has to be per-project or per
managed-settings, which is a materially different design and a different Step 9.

This is an environment boundary, not a defect. It is recorded in `STATE.md`
§ Verification assignments with an executor.

## What was built here, and what it does not prove

`.claude/hooks/inject_rules.py` with `.claude/hooks/rule-triggers.json`
generalises the pattern the two existing injectors already establish: put the
governing text in context at the moment it applies. The table holds **no rule
text** -- each entry names an owning file and an exact heading, read live when the
trigger fires -- so no second copy of a rule exists to drift, which the one-owner
rule in `AGENTS.md` § File ownership requires.

Injected size is 1.7--3.3 KB per prompt against the 259 KB bootstrap.

`scripts/Assert-RuleTriggerFidelity.py` refuses a table whose entries no longer
resolve, and `wg_gates.check_rule_triggers` makes that a commit refusal. It runs
unconditionally rather than diff-scoped, because the failure that matters --
rewording a heading in the owning file -- touches neither the table nor the hook.

**It is installed in `workspace-governor` only.** By Finding 3 that governs the
backoffice and nothing else. It is a proof of the mechanism, not fleet coverage.
Whether it can be promoted to user scope is exactly what the procedure above
decides.

**Performer.** Every check named here was authored and run in the same session.
Under `rules/VERIFICATION-RESOLUTION.md` § Performer selection and `DECISIONS.md`
D-94, a clean result from a self-authored check cannot carry a completion claim.
The demonstrations below are recorded as demonstrations; no claim of independent
verification is made for them.
