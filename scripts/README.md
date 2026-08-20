# Gateway discovery scripts

Read-only evidence collection for section 5 of the `mcp-gateway` directive.
These scripts collect evidence. They perform no analysis and change nothing.

## One command to run

From the repository root, in PowerShell on Windows:

```powershell
.\scripts\Assert-DiscoveryReadOnly.ps1
```

That wrapper runs discovery **and** proves it changed nothing. Do not run
`Invoke-GatewayDiscovery.ps1` on its own unless you do not need the proof.

Optional: add `-Thorough` for SHA256-based comparison (slower, stronger).
Override paths with `-HubPath`, `-WorkspaceRoot`, `-OutDir` if the defaults
are wrong.

## Output format

Three files, written only to `.\evidence\`:

| File | Purpose | Audience |
|---|---|---|
| `GATEWAY-DISCOVERY-<run date>.json` | Full structured findings, 14 sections | coding agent |
| `GATEWAY-DISCOVERY-<run date>.md` | Summary table, conflict check, non-verified list | human |
| `GATEWAY-DISCOVERY-<run date>-READONLY-PROOF.md` | PASS/FAIL that nothing changed | audit record |

Filenames carry the date the script runs, from `Get-Date`. They are not fixed.

All three are UTF-8 text, safe to commit. Naming follows the existing
`evidence/` convention (`SUBJECT-yyyy-MM-dd.md`).

Commit all three together — the proof is only meaningful alongside the
evidence it certifies.

## Coverage — the 14 evidence items

| # | Item |
|---|---|
| 1 | `.agents-hub` location and structure |
| 2 | Claude Code configuration and native controls |
| 3 | Codex configuration and native controls |
| 4 | Existing MCP configurations |
| 5 | PATH and environment entries relevant to coding agents |
| 6 | Installed and runtime dependencies relevant to the Gateway |
| 7 | Shared assets and tool registries |
| 8 | Scripts and APIs potentially relevant for exposure |
| 9 | Authentication and secrets mechanisms (names and locations only) |
| 10 | Audit and logging mechanisms |
| 11 | Duplicated governance locations |
| 12 | Runtime-native capabilities outside Gateway authority |
| 13 | Direct-access paths that could bypass Gateway governance |
| 14 | Repository and workspace paths relevant to the architecture |

## Traversal safety — pre-descent pruning

`lib/SafeTraversal.ps1` is the sole owner of directory traversal for every
script here. It exists because `Get-ChildItem -Recurse` **traverses** every
subtree before returning, so filtering its output with `Where-Object` is too
late — the protected directory has already been read. Filtering output and
pruning before descent produce identical output; only the record of visited
directories distinguishes them.

The module performs manual iterative traversal and decides whether to enter each
directory **before** entering it. A protected directory is identified while its
**parent** is listed, recorded as existing, and never passed to `Get-ChildItem`.

Invariant, enforced by `Assert-RememberPruning.ps1`:

| # | Assertion |
|---|---|
| A1 | No script under `scripts/` uses `Get-ChildItem -Recurse` in executable code |
| A2 | The traversal path contains exactly one `Get-ChildItem`, single-level, in the module |
| A3 | Every traversing script dot-sources the module |
| A4 | Reparse containment is attribute-based, covers files and directories, and is decided **before** the directory/file split (asserted by line order) |
| A5 | Completeness is computed and can be INCOMPLETE |
| A6 | The inventory consumes completeness rather than ignoring it |
| A7 | The runtime test rejects any reparse point inside returned `items` |

**The verdict is fail-closed.** `PASS` requires the Hub to exist, A1–A7 to pass,
the runtime pruning test to pass, **and** traversal completeness to be
`COMPLETE`. A skipped runtime proof is not a proof; the script exits 1 on FAIL.
If the supplied root is itself safety-pruned, nothing was inventoried, so the
result is INCOMPLETE rather than an empty success.

### Four pre-descent decisions, in order

1. **Safety-pruned by name** — `.remember`. Never entered. STATE.md B-2.
2. **Reparse point, by attribute, file *or* directory** — junctions, symlinks,
   mounts. Tested **before** the directory/file split, so a *file* link cannot
   reach the file branch, enter `items`, and be hashed (`Get-FileHash` follows
   links). Never entered, never returned, never hashed, whatever it is called. A
   name-based rule is defeated by an alias: a junction named anything can target
   `design-systems\.remember` or a path outside the Hub. Detection uses
   `[System.IO.FileAttributes]::ReparsePoint`, so the name is irrelevant.
   Attribute-read errors resolve to "treat as reparse point" — fail closed.
3. **Noise-pruned by name** — `.git`, `node_modules`. Never entered.
4. **Depth cap** — recorded as `depthLimited`, never silently dropped.

### Completeness fails closed

A reconciliation inventory that silently omits files is worse than none. The
traversal returns `completeness` = `COMPLETE` or `INCOMPLETE`. It is INCOMPLETE
if any of these occurred:

- the item cap was reached (`truncated`)
- a directory was not descended because of the depth cap (`depthLimited`)
- a directory could not be enumerated (`traversalFailures`)

`Invoke-HubInventory.ps1` consumes that value, prints it, writes it as a
top-level heading in the report, and **exits 2** when INCOMPLETE. It cannot
report success while part of the accessible tree was skipped.

Deliberate exclusions — safety-pruned, noise-pruned, reparse points — do not
make the accessible tree incomplete, but they are always listed and the
exhaustiveness claim is scoped to exclude their targets.

### Reported categories

```
Safety-pruned:        design-systems\.remember
Noise-pruned:         .git, node_modules
Not traversed:        reparse points, file and directory (junction/symlink/mount)
Traversal failures:   access or enumeration errors
Depth-limited:        directories not descended
Completeness:         COMPLETE | INCOMPLETE
```

### Proving it

```powershell
.\scripts\Assert-RememberPruning.ps1
```

Part A checks the static invariant. Part B runs the real traversal and asserts a
positive property: no directory in `visitedDirectories` is the same as, or
beneath, any excluded directory — safety-pruned **or** untraversed reparse point.
Since `visitedDirectories` records every directory actually passed to
`Get-ChildItem`, a traversed exclusion would appear there. Absence from output is
not accepted as proof.

The checker strips string literals in one left-to-right pass. Stripping
single-quoted strings first with a regex consumes across the boundary of a
double-quoted string that contains single quotes, which silently corrupts every
check built on top of it.

Emits `evidence\REMEMBER-PRUNING-PROOF-<run date>.md`.

## Safety contract

The discovery script:

- performs no writes anywhere except the files it emits into `-OutDir`
- never installs, modifies, deletes, moves, renames, reconfigures or repairs
- makes no network calls
- never emits a secret **value**; records names, locations and metadata only
- does not read or hash `design-systems\.remember` contents, per the
  unresolved provenance and sensitivity hold in Workspace Governor `STATE.md`;
  checks existence only; nothing inside is enumerated, counted, read, or hashed
- reports "not found" rather than failing when a path is absent
- executes none of the scripts it inventories

## How the proof works

`Assert-DiscoveryReadOnly.ps1` verifies in three parts:

- **Part A — static analysis.** Scans the discovery script for every mutating
  cmdlet plus install/network/process-start verbs, and lists each with its line
  number. Passes only if all mutations target `-OutDir`.
- **Part B — filesystem comparison.** Records path, size and last-write time
  for every file under the inspected roots before the run, re-records after,
  and compares. Any modification, creation or deletion outside `-OutDir` fails.
- **Part C — verdict.** Writes the proof document with PASS or FAIL and counts.

Known scope limits, stated in the proof itself: it covers the filesystem roots
listed, excluding `.git`, `node_modules`, `design-systems\.remember` and the
output directory. It does not monitor the registry, services, scheduled tasks
or network state — Part A establishes the script contains no cmdlet that
touches them. Reading a file updates last-*access* time; the comparison uses
last-*write* time and size, which reads do not alter.

## Pre-handoff gates

Run all three before handing anything here to the local operator. In this order.

### 1. Encoding -- ASCII only

Every `.ps1` in this repository must be **pure ASCII**. Windows PowerShell 5.1
reads a `.ps1` without a byte-order mark using the system ANSI code page, so a
UTF-8 em dash arrives as `â€”`; its third byte is U+201D, which PowerShell accepts
as a string delimiter, and every affected literal terminates early. That produced
a full parse cascade on the operator's machine. Pure ASCII decodes identically
under UTF-8 and any ANSI code page, which removes the class rather than relying
on a BOM surviving every checkout and editor.

```bash
! grep -rIPl '[^\x00-\x7F]' scripts --include='*.ps1' || echo "NON-ASCII FOUND"
```

### 2. Parse -- with a real PowerShell parser

```powershell
Get-ChildItem scripts,scripts/lib -Filter *.ps1 -File | ForEach-Object {
    $e = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile($_.FullName, [ref]$null, [ref]$e)
    '{0,-40} {1}' -f $_.Name, $(if ($e.Count) { "FAIL ($($e.Count))" } else { 'OK' })
    $e | ForEach-Object { "    L$($_.Extent.StartLineNumber): $($_.Message)" }
}
```

Use the parser, not a hand-rolled check. Three successive custom static gates
were built here before anyone tried an actual PowerShell parser, and none of them
could detect a parse error, because none of them was a parser. `pwsh` is
available for Linux as a self-contained tarball from the PowerShell releases page
and needs no install.

### 3. Semantics -- `Assert-ScriptStructure.py`

This is **not** a syntax gate; step 2 is. It catches defects that are valid
PowerShell and therefore invisible to a parser: indexed assignment before the
container is constructed, and case-insensitive loop/container collisions. Two
such defects reached committed code and broke the assigned commands.

Run it before every handoff:

```bash
python3 scripts/Assert-ScriptStructure.py --selftest
python3 scripts/Assert-ScriptStructure.py scripts/*.ps1 scripts/lib/*.ps1
```

| # | Check |
|---|---|
| S1 | Delimiter balance, over source with literals and comments blanked in a single pass |
| S2 | No indexed assignment `$X[...] =` before `$X` is bound in the same or an enclosing scope |
| S3 | No indexed assignment without a real container constructor before it in scope |
| S4 | No loop variable colliding case-insensitively with a container in the same or an enclosing scope |

S3 exists because existence is not enough. PowerShell variable names are
case-insensitive, so a file-scope `foreach ($r in ...)` binds the same variable
as a result object `$R`: the name exists while holding a value of the wrong
type, and the indexed write still fails. S4 flags that collision directly.

The tool is scope-aware — PowerShell opens a variable scope per function, not
per block — because a function-local `$r` otherwise masks a file-scope `$R`
defect. `--selftest` asserts the tool still fails on each defect it exists to
catch, including two cases that must **not** be flagged. A checker that only
ever passes proves nothing.

This is a static gate only. It does not verify behaviour, and it does not
replace or weaken the required local Windows runtime verification recorded in
`STATE.md` § Verification assignments.

## Verification status

These scripts have been **parsed and executed** under PowerShell 7.4.6 on Linux
against synthetic fixtures, including a Hub containing `.remember`, a file
symlink and a directory symlink, and both the COMPLETE and INCOMPLETE traversal
paths. Results, including exit codes and the leak check on `.remember`, are in
`evidence/POWERSHELL-EXECUTION-2026-08-20.md`.

Not verified: **Windows PowerShell 5.1** specifically, and the **live Hub**.
Pure-ASCII sources remove the encoding difference that broke 5.1, and no
PowerShell 7-only syntax is present, but 5.1 has not run these scripts. Windows
junction semantics, ACL-denied directories and long paths were not exercised;
Linux symlinks stood in for reparse points and were correctly excluded.

The scripts are read-only, so a failure cannot damage anything. If one errors,
send the error text.
