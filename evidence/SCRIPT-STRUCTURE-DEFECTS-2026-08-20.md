# Evidence — case-insensitive variable collisions in the PowerShell tooling

**Date:** 2026-08-20
**Subject:** `scripts/` PowerShell tooling, as committed at `068dfa4`
**Status:** Verified by static analysis. Runtime behaviour not verified — no
PowerShell in this environment.
**Method:** `scripts/Assert-ScriptStructure.py`, run against `068dfa4` and
against the corrected tree.

## Finding

PowerShell variable names are case-insensitive. `$r` and `$R` are one variable.
A file-scope `foreach ($r in ...)` therefore overwrites a result object named
`$R`, silently and with a value of the wrong type.

Four scripts carried this collision. Two of the four were live defects in
scripts already handed to the local operator.

| File (at `068dfa4`) | Line | Collision | Effect |
|---|---|---|---|
| `Assert-RememberPruning.ps1` | 315 | `foreach ($p in $trav.prunedForSafety)` vs `$P` (report list, L245) | **Breaks.** First iteration rebinds `$P` to a string; the `$P.Add(...)` in the loop's own body then throws. The block runs whenever a directory was safety-pruned — the normal case when `.remember` is present. The verdict lines and the `Set-Content` that writes the proof are never reached. |
| `Invoke-HubInventory.ps1` | 245 | `foreach ($r in $trav.incompleteReasons)` vs `$R` (result object, L165) | **Silent evidence loss.** JSON is already written at L228, so the JSON survives. But L353 `foreach ($u in $R.unverified)` then reads a string: `$R.unverified` is `$null` and the loop emits nothing. The unverified list disappears from the markdown exactly when the inventory is INCOMPLETE — when it matters most. |
| `Invoke-GatewayDiscovery.ps1` | 279 | `foreach ($r in $scanRoots)` vs `$R` (result object, L341) | Latent. Contributed to the `00_hubState` ordering defect below. |
| `Assert-DiscoveryReadOnly.ps1` | 88 | `foreach ($p in $MutatingPatterns)` vs `$P` (report list, L173) | Latent — the loop precedes the container. |

`Assert-RememberPruning.ps1` and `Invoke-HubInventory.ps1` are the two commands
recorded as assigned for local execution. Both were affected. The
`Assert-RememberPruning.ps1` defect is a certain failure, not a possibility.

## Correction to the recorded mechanism of the `00_hubState` defect

The ordering defect in `Invoke-GatewayDiscovery.ps1` (`$R['00_hubState']`
assigned before `$R` was constructed) was described as indexing an
uninitialised variable. That is not what happened. `$R` was not empty: the
file-scope `foreach ($r in $scanRoots)` at L279 had already bound the name to a
scan-root path. The indexed assignment therefore failed against a `String`, and
the section was then discarded when `$R` was rebuilt.

The defect, its severity and the fix are unchanged. Only the mechanism is
corrected, and it is the reason a plain "is it initialised" check does not
detect this class.

## Why static checks had not caught it

Three successive gate designs failed on this class:

1. **Delimiter balance alone.** Cannot see ordering or naming at all.
2. **Existence check** (`is $X bound before its first indexed write`). Passes
   the defective file, because a leaked loop binding does bind the name.
3. **Case-folded, scope-blind existence check.** Passes for a second reason: a
   function-local `$r` inside `Get-PathFact` masked the file-scope `$R` defect.

The gate that detects the class requires a **container constructor** — `@{}`,
`[ordered]@{}`, `@()`, `New-Object`, `::new()` — before the first indexed write,
and is **scope-aware**, since PowerShell opens a variable scope per function
rather than per block.

## Verification performed

| Check | Result |
|---|---|
| `Assert-ScriptStructure.py --selftest` | PASS — 5 cases, including 2 that must not be flagged |
| Same tool against `068dfa4` sources | FAIL — 7 findings across 4 files, listed above |
| Same tool against corrected tree | PASS — 5 files, 0 findings |
| Single traversal `Get-ChildItem`, single-level | Unchanged: `lib/SafeTraversal.ps1:155` |
| `-Recurse` in executable code | None |
| `.remember` accessed by `Test-Path` only | Unchanged |
| A1–A7 assertions present | All 7 present |

## Not verified

Runtime behaviour of any script. This environment has no PowerShell. The
required local Windows runtime verification is unchanged and still pending; see
`STATE.md` § Verification assignments. Static analysis establishes that the
collisions are gone from the source. It does not establish that the scripts run.
