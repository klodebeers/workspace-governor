# Workspace Governor Learnings

**Status:** Non-authoritative living record.
**Retention rule:** `plans/reference/HUB-MANAGEMENT-predecessor.md` § Durable
learning retention, carried forward. Retain an entry only when completed work
reveals a non-obvious finding likely to prevent repeated investigation, repeated
failure, or an incorrect future classification. Do not record routine facts,
transient status, raw tool output, or semantic duplicates.
**Promotion rule:** if a learning creates or changes required behaviour, the
authoritative owner is updated and the learning becomes a pointer. An entry here
never defines behaviour.

Format: `L-nnn | Trigger | Finding | Consequence | Owner or evidence`

## Carried from the predecessor backoffice

Verbatim in substance from `plans/reference/predecessor/LEARNINGS.md`. L-001 and
L-002 were already represented in this backoffice; L-003 to L-006 were dropped by
omission in the first predecessor review and are carried here.

- `L-001` | Trigger: evaluating Hub placement | Finding: canonical source placement does not establish runtime discovery, activation, adherence, or enforcement | Consequence: record and verify runtime states separately | Owner: `AGENTS.md` § Evidence standard; `evidence/RUNTIME-CONVENTIONS-2026-08-20.md`
- `L-002` | Trigger: reconciling similar rules | Finding: sentence comparison misses semantic duplicates and partial overlaps | Consequence: compare practical obligations, triggers, boundaries and outcomes, not wording | Owner: canonical Hub `rules/AGENTS.md`; `plans/reference/HUB-MANAGEMENT-predecessor.md`
- `L-003` | Trigger: drafting Agent Hub documents | Finding: human-oriented synonym replacement can weaken technical precision | Consequence: preserve agent-oriented standard terminology; put human explanation in a separate non-authoritative glossary | Owner: `plans/reference/HUB-DOCUMENTATION-predecessor.md`; `AGENT-SSOT.json` § `technical_translation_and_audience`
- `L-004` | Trigger: retaining a discovered lesson | Finding: a one-line learning is cheaper than repeating material investigation | Consequence: retain only qualified non-obvious findings, and promote normative outcomes to their sole owner | Owner: this file's retention and promotion rules above
- `L-005` | Trigger: evaluating repository-rule scaffolding | Finding: reusable scaffolding and generated repository rules have different owners | Consequence: an accepted reusable capability belongs in Hub `skills/`; generated rules stay with the governed repository | Owner: `plans/AGENT-HUB-CONSOLIDATION.md` G-02a; `plans/reference/predecessor/research-WORKSPACE-GOVERNANCE-CAPABILITY-REUSE-2026-08-16.md`
- `L-006` | Trigger: evaluating generator-owned markers | Finding: rerunning a generator can overwrite its delimited block | Consequence: never make a foreign generator-owned block authoritative Hub governance | Owner: `plans/AGENT-HUB-CONSOLIDATION.md` G-02a; `STATE.md` stop conditions

## Learned in this backoffice

- `L-007` | Trigger: committing a `.ps1` for a Windows operator | Finding: Windows PowerShell 5.1 reads a non-BOM file using the system ANSI code page, and the third byte of a UTF-8 em dash decodes to a character PowerShell accepts as a **string delimiter** | Consequence: keep `.ps1` sources pure ASCII; the failure presents as a cascade of unrelated syntax errors | Owner: `STATE.md` stop conditions; `evidence/POWERSHELL-EXECUTION-2026-08-20.md`
- `L-008` | Trigger: naming a loop variable in PowerShell | Finding: variable names are case-insensitive, so `foreach ($r in ...)` and a result object `$R` are one variable | Consequence: a loop silently destroys the container; use descriptive loop names. Detected by `scripts/Assert-ScriptStructure.py` check S4 | Owner: `DECISIONS.md` D-18; `evidence/SCRIPT-STRUCTURE-DEFECTS-2026-08-20.md`
- `L-009` | Trigger: reasoning from any tool output | Finding: a display limit, a filter, or a field-shaped query silently produces a partial result that reads as complete. This occurred three times in one session -- a `^[+-][^+-]` grep filter that dropped every matching line, a transcript search scoped to one message shape that found nothing and was reported as absence, and a key listing truncated to twelve entries that hid the most duplicated block | Consequence: before concluding absence, re-run with the simplest unfiltered method available -- plain `grep` over raw bytes, or an unlimited listing. Absence from tool output is not absence in the system | Owner: `AGENTS.md` § Evidence standard; `rules/VERIFICATION-RESOLUTION.md`
- `L-010` | Trigger: choosing a verification method | Finding: an environment capability assumed absent may be obtainable in minutes; "no PowerShell here" was accepted untested and three hand-rolled static gates were built on that premise, none of which could detect a parse error because none was a parser | Consequence: test for the real tool before building a substitute for it | Owner: `rules/VERIFICATION-RESOLUTION.md`; `DECISIONS.md` D-20
- `L-011` | Trigger: sizing the canonical root bootstrap file | Finding: the instruction budget is shared across the whole root-to-cwd chain, consumed root-first, and truncates mid-content with no signal to the model | Consequence: an oversized root file silently starves every nested one. Normative outcome promoted -- see owner | Owner: `DECISIONS.md` D-29; `evidence/RUNTIME-CONVENTIONS-2026-08-20.md`
- `L-012` | Trigger: vendoring the canonical Hub into a consumer repository | Finding: project-root discovery stops at the first `.git` and never walks past it, so a nested checkout becomes its own project root | Consequence: the consumer's own root instruction file stops loading entirely, silently. Use a symlink or adapter projection, not a nested repository | Owner: `DECISIONS.md` D-29; `evidence/RUNTIME-CONVENTIONS-2026-08-20.md`
- `L-013` | Trigger: correcting an entry in an append-only record | Finding: a correct finding does not license a non-compliant mechanism -- the fix for a wrong entry in an append-only file is an appended superseding entry, never an in-place edit | Consequence: restore the original verbatim and append the correction; verify by confirming the diff against the pre-edit commit contains no deletions | Owner: `DECISIONS.md` D-32; `AGENTS.md` § File ownership
