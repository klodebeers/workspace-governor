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

## Finding 1 -- the wiring named in D-75 cannot carry a rule. Partially verified.

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

**What is and is not verified here.** The quotation is from a prior research
file. `rules/VERIFICATION-RESOLUTION.md` § Authority selection excludes *"a prior
research file not re-verified"* as authority for vendor product behaviour, and no
re-verification against vendor documentation was performed, so this is
**partially verified** and an earlier revision of this heading wrongly said
"Verified." What *was* checked directly against the installed bundle, on
2026-08-27, is a narrower and harder fact: the `UserPromptSubmit` payload carries
`prompt`, never `user_prompt`. That is vendor behaviour read from implementation,
and it is what the hook fix rests on.

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
| **Total** | **258,918 (~64k tokens)** |

Self-correcting or superseding statements inside that set. The pattern is given
in full so the count can be re-run and falsified; an elided one cannot be:

    grep -ciE "supersed|corrected|correction|was wrong|no longer|stale|earlier revision|inverted|relitigat|carried-forward|until 2026" <file>

Counts:
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

## Procedure -- WITHDRAWN 2026-08-27, and why

`scripts/Probe-UserScopeHook.py` is **removed** along with it, recoverable from
git at `c2c11d5`. It is not fixed and kept, because the question no longer needs
an instrument and a bad one invites reuse: its `--selftest` never executed
`log_path()` and never called `main()`, so 8 of 11 injected defects passed it
green -- including a probe writing to the wrong filename, and a probe that never
records when invoked as a hook. Those are the two things the operator most needed
proven. Any argument other than the exact string `--selftest` also fell through
to the recording path, so a mistyped flag silently appended a real line and
poisoned both directions of the reading.

**Do not run the earlier version of this procedure.** It is preserved in git at
`c2c11d5`. Three defects, two of them found by an independent audit and one
dangerous:

1. **Its Step 2 could destroy the operator's whole configuration.** It printed a
   complete `settings.json` document with a prose caveat beside it saying to
   merge "if that file already has a `hooks` key". The caveat was under-scoped --
   pasting the document replaces the file whatever keys it has, taking `model`,
   `env`, `statusLine`, every other hook, and `permissions.allow` /
   `permissions.deny` with it. Losing `permissions.deny` silently **widens** what
   every later session on that machine may do. The CLI keeps no backup of
   `settings.json` to restore from.
2. **It could not produce a trustworthy negative.** Every failure mode of the
   probe is byte-identical to the result it measures: a JSON syntax error in the
   settings file drops the entire file with no warning to the operator
   (`f46` parses with reporting off and returns `settings: null`), and the probe
   swallows every write failure and exits 0 in silence. An empty log meant
   "user scope does not load", "you mistyped the JSON", "the interpreter is not
   on PATH", or "the log was not writable", with nothing to tell them apart.
3. **It sampled a variable the resolution code never reads.** See
   `evidence/HOOK-SCOPE-RESOLUTION-2026-08-27.md`: user settings are
   home-anchored and the execution path never consults the working directory.

## What answers the question instead -- read-only, nothing installed

`evidence/HOOK-SCOPE-RESOLUTION-2026-08-27.md` settles #43 from the
implementation. What remains is confirming this machine is not in one of the
states that gate the outcome. None of these writes anything.

1. **Version.** `claude --version`. The implementation reading is against 2.1.42;
   a materially different version needs re-reading, not assuming.
2. **What the CLI thinks is registered.** Run `/hooks` in a session. It labels
   every hook with its source -- *"User settings (~/.claude/settings.json)"*,
   *"Project settings"*, *"Plugin hooks"*. This reads out directly what the
   withdrawn trial tried to infer, and it distinguishes *not registered* from
   *registered but not firing*, which an empty log cannot.
3. **Is the user settings file even valid?** An invalid file is ignored whole and
   in silence:

       python -c "import json,os;json.load(open(os.path.expanduser('~/.claude/settings.json')));print('valid')"

4. **Four states that switch hooks off regardless of scope:**
   - managed settings at `C:\ProgramData\ClaudeCode\managed-settings.json`
     setting `allowManagedHooksOnly` -- blocks all user, project and local hooks;
   - `disableAllHooks` in **any** scope, including a project's own settings;
   - workspace trust not accepted for a directory (interactive sessions only);
   - `CLAUDE_CONFIG_DIR` set, or Cowork mode, either of which changes which file
     "user scope" even means.

**Reading the result.** `/hooks` lists the hook under *User settings* in a
directory whose project sets nothing: user scope reaches that session. It does
**not** license "user scope is the carrier" -- `disableAllHooks` at project scope
is a per-project kill switch, so the bypass-proof carrier is managed settings.
That is a separate question and a separate item.

This is an environment boundary, not a defect. It is recorded in `STATE.md`
§ Verification assignments with an executor.

## What was built here, and what it does not prove

`.claude/hooks/inject_rules.py` with `.claude/hooks/rule-triggers.json`
generalises the pattern the two existing injectors already establish: put the
governing text in context at the moment it applies. Each entry names an owning
file and an exact heading, read live when the trigger fires, so no second copy of
a rule exists to drift -- which the one-owner rule in `AGENTS.md` § File ownership
requires.

**That claim is now checked rather than asserted.** An independent reviewer found
that the table's `why` fields carried verbatim rule text -- up to 76 characters --
while six places in the same commit said the table held none, and that one of
those copies had already drifted, changing "the ownership table" to "this table"
and so altering the referent of the rule it quoted. The fields were rewritten to
say *when* an entry fires, and `Assert-RuleTriggerFidelity.py` now refuses any
`why` sharing 40 or more characters with the section it points at.

A section that does not fit the per-entry cap is injected as a **pointer**, never
as a prefix: a truncated prohibition arrives under an authoritative header and
reads as the whole rule. Three of five entries are pointers today. Measured
output is ~1.3--3.1 KB per prompt.

`scripts/Assert-RuleTriggerFidelity.py` refuses a table whose entries no longer
resolve, and `wg_gates.check_rule_triggers` makes that a commit refusal. It runs
unconditionally rather than diff-scoped, because the failure that matters --
rewording a heading in the owning file -- touches neither the table nor the hook.

**It is installed in `workspace-governor` only.** By Finding 3 that governs the
backoffice and nothing else. It is a proof of the mechanism, not fleet coverage.
Whether it can be promoted to user scope is exactly what the procedure above
decides.

## Results, and who produced them

| Check | Result | Performer |
|---|---|---|
| `test_hooks.py` | 144 cases, 0 failed | this session (author) |
| `test_hooks.py --mutations` | 29 rows, 26 caught, 0 behaved wrongly, at `1fc80dd` | this session (author) |
| `Assert-RuleTriggerFidelity.py --selftest` | 25 cases, both directions | this session (author) |
| Live table | 5 entries, every heading resolves exactly once | this session (author) |
| Review of the carrier code | 3 independent agents, rationale withheld per D-60 | **separate agents** |

The mutation figure is **not current**: it was produced against `3be99ca`, and the
carrier changed materially afterwards. A re-run against the current tree is owed
before any completion claim, and its absence is stated here rather than left to
be inferred.

**Performer.** Every check in the first four rows was authored and run in the
same session, and under `rules/VERIFICATION-RESOLUTION.md` § Performer selection
and `DECISIONS.md` D-94 a clean result from a self-authored check cannot carry a
completion claim. The review row is different: three separate agents examined the
carrier without this session's rationale, and their findings are recorded in
`DECISIONS.md` D-96. Nothing here is claimed as independently verified beyond
what that row covers.
