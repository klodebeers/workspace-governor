# Evidence -- PowerShell parse and execution verification

**Date:** 2026-08-20
**Subject:** `scripts/` PowerShell tooling
**Status:** Verified by execution under PowerShell 7.4.6 on Linux, against
synthetic fixtures. NOT verified under Windows PowerShell 5.1, and not against
the live Hub.

## Trigger

`Assert-RememberPruning.ps1` failed to parse on the operator's Windows machine
with a cascade of `Missing ')' in method call` and `Unexpected token` errors.

## Root cause -- encoding, not syntax

The sources contained 61 em dashes (U+2014). The files had no byte-order mark.
Windows PowerShell 5.1 reads a `.ps1` without a BOM using the system ANSI code
page, so the UTF-8 bytes `E2 80 94` were decoded as Windows-1252 `â€”`. The third
of those, `0x94`, is U+201D RIGHT DOUBLE QUOTATION MARK, which PowerShell accepts
as a **string delimiter**. Every affected string literal therefore terminated
early, which produced the parse cascade.

The scripts were never syntactically wrong. They were byte-wrong for the reader.

## Correction

All 61 em dashes replaced with `--`. All five `.ps1` files are now pure ASCII,
verified byte-wise: no byte above 0x7F remains. Pure ASCII decodes identically
under UTF-8 and any ANSI code page, so the defect class is removed rather than
suppressed. A BOM was considered and rejected: it would have preserved the
non-ASCII characters and left the file dependent on the BOM surviving every
future checkout, editor and copy.

## Method correction

A real PowerShell runtime was obtained (PowerShell 7.4.6, Linux x64) and used to
parse and execute the scripts. This should have been the first move. Three
successive hand-rolled static gates were built instead, none of which could
detect a parse error, because none of them was a PowerShell parser. This is the
failure mode `rules/VERIFICATION-RESOLUTION.md` describes: custom tooling built
before checking whether an existing capability was sufficient.

The static gate in `Assert-ScriptStructure.py` is retained but demoted. It
catches semantic defects that are valid PowerShell and therefore invisible to a
parser -- indexed assignment before construction, and case-insensitive
loop/container collisions. It is not a syntax gate.

## Verification performed

| Check | Method | Result |
|---|---|---|
| Parse, all 5 scripts | `[Parser]::ParseFile` | 0 errors (1293-5876 tokens each) |
| Non-ASCII bytes in `.ps1` | byte scan | 0 |
| PowerShell 7-only syntax (`??`, `?.`, ternary, `&&`/`\|\|`) | source scan | none present |
| `Assert-RememberPruning.ps1`, no Hub | executed | A1-A7 PASS; Part B skipped; VERDICT FAIL; exit 1 |
| `Assert-RememberPruning.ps1`, Hub with `.remember` + file and directory symlinks | executed | VERDICT PASS; exit 0; `.remember` pruned; both reparse points excluded; completeness COMPLETE |
| `.remember` contents leaked to output | grep for fixture secret | 0 occurrences in any emitted file |
| `Invoke-HubInventory.ps1`, COMPLETE path | executed | exit 0; comparison emitted |
| `Invoke-HubInventory.ps1`, INCOMPLETE path (depth cap exceeded) | executed | exit 2; incomplete reasons present in markdown; all 6 "Explicitly NOT verified" entries present |
| Structure gate | `Assert-ScriptStructure.py` | self-test PASS; 5 files, 0 findings |

The last two rows matter specifically: the INCOMPLETE path is where the
previously-fixed `$r`/`$R` collision caused silent evidence loss, and the
safety-pruned loop is where the `$p`/`$P` collision caused a hard failure. Both
now execute correctly under a real runtime.

## Still not verified

- **Windows PowerShell 5.1.** Parsing and execution were under PowerShell 7 on
  Linux. Pure-ASCII sources remove the encoding difference that caused this
  failure, and no 7-only syntax is present, but 5.1 has not run these scripts.
- **The live Hub.** All execution was against synthetic fixtures built for this
  test. Nothing here says anything about the real `.agents-hub` contents.
- Windows-specific behaviour: junction semantics, ACL-denied directories, and
  long-path handling were not exercised. Linux symlinks stood in for reparse
  points and were correctly excluded.
