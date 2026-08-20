<#
.SYNOPSIS
  Proves that protected directories are pruned BEFORE descent, not filtered
  out of recursive output afterwards.

.DESCRIPTION
  Three parts. All read-only.

    PART A — static invariant.
      Asserts that no script under scripts/ uses `Get-ChildItem -Recurse` in
      executable code, that the traversal path contains exactly one
      Get-ChildItem call (single-level, in lib/SafeTraversal.ps1), and that
      every traversing script dot-sources that module. If -Recurse is absent,
      traversal cannot pre-traverse a subtree before the prune decision.

    PART B — runtime proof from traversal data.
      Runs the real traversal against the Hub and asserts a positive property:
      no directory in visitedDirectories is the same as, or beneath, any
      directory in prunedForSafety. visitedDirectories records every directory
      actually passed to Get-ChildItem, so a traversed protected directory
      would appear there. This is stronger than checking that .remember is
      merely absent from the output.

    PART C — proof artifact for committing.

  Absence from output is NOT accepted as evidence here. Filtering after
  recursion produces identical output to pruning before descent; only the
  visited-directory record distinguishes them.

.PARAMETER HubPath
  Live Hub to traverse for Part B. Default: $env:USERPROFILE\.agents-hub

.PARAMETER OutDir
  Output directory. Default: .\evidence

.EXAMPLE
  .\scripts\Assert-RememberPruning.ps1
#>

[CmdletBinding()]
param(
    [string]$HubPath = (Join-Path $env:USERPROFILE '.agents-hub'),
    [string]$OutDir  = (Join-Path (Get-Location) 'evidence')
)

$ErrorActionPreference = 'Continue'
$stamp    = Get-Date -Format 'yyyy-MM-dd'
$stampISO = (Get-Date).ToString('o')
$scriptDir = $PSScriptRoot
$libPath = Join-Path $scriptDir 'lib\SafeTraversal.ps1'

if (-not (Test-Path -LiteralPath $libPath)) {
    Write-Host "FAIL: traversal module not found: $libPath" -ForegroundColor Red
    exit 1
}
. $libPath

function Remove-PsStringLiterals {
    <#
    .SYNOPSIS
      Removes string literals in one left-to-right pass.
    .DESCRIPTION
      Whichever quote character opens first wins, so a double-quoted string
      containing single quotes is handled correctly. A regex that strips
      single-quoted strings first would consume across the double-quoted
      boundary and corrupt the rest of the line — which silently breaks any
      check built on top of it.
    #>
    param([string]$Line)
    $sq = [char]39; $dq = [char]34; $bt = [char]96
    $sb = New-Object System.Text.StringBuilder
    $q = $null; $i = 0; $n = $Line.Length
    while ($i -lt $n) {
        $c = $Line[$i]
        if ($null -eq $q) {
            if ($c -eq $sq -or $c -eq $dq) { $q = $c; $i++; continue }
            if ($c -eq '#') { break }
            if ($c -eq $bt -and ($i + 1) -lt $n) { $i += 2; continue }
            [void]$sb.Append($c); $i++
        } else {
            if ($c -eq $bt -and $q -eq $dq -and ($i + 1) -lt $n) { $i += 2; continue }
            if ($c -eq $q) {
                if (($i + 1) -lt $n -and $Line[$i + 1] -eq $q) { $i += 2; continue }
                $q = $null; $i++; continue
            }
            $i++
        }
    }
    return $sb.ToString()
}

function Get-CodeLines {
    param([string]$Path)
    $out = @(); $inHelp = $false; $i = 0; $inHere = $false
    foreach ($l in (Get-Content -LiteralPath $Path)) {
        $i++
        $t = $l.Trim()
        if ($t -eq '@"' -or $t -eq "@'") { $inHere = $true; continue }
        if ($inHere) { if ($t -eq '"@' -or $t -eq "'@") { $inHere = $false }; continue }
        if ($t.StartsWith('<#')) { $inHelp = $true }
        if ($inHelp) { if ($l -match '#>') { $inHelp = $false }; continue }
        if ($t.StartsWith('#')) { continue }
        $stripped = Remove-PsStringLiterals -Line $l
        if ($stripped.Trim().Length -gt 0) { $out += [pscustomobject]@{ Line=$i; Text=$stripped } }
    }
    return $out
}

Write-Host '=== PART A — static invariant ===' -ForegroundColor Cyan

$scripts = @(Get-ChildItem -LiteralPath $scriptDir -Filter '*.ps1' -File -ErrorAction SilentlyContinue)
$libs    = @(Get-ChildItem -LiteralPath (Join-Path $scriptDir 'lib') -Filter '*.ps1' -File -ErrorAction SilentlyContinue)
$all     = @($scripts) + @($libs)

$recurseHits = @(); $gciSites = @(); $missingDotSource = @()
foreach ($f in $all) {
    foreach ($cl in (Get-CodeLines -Path $f.FullName)) {
        if ($cl.Text -match 'Get-ChildItem') {
            $gciSites += [pscustomobject]@{ File=$f.Name; Line=$cl.Line; Text=$cl.Text.Trim() }
            if ($cl.Text -match '-Recurse') {
                $recurseHits += [pscustomobject]@{ File=$f.Name; Line=$cl.Line; Text=$cl.Text.Trim() }
            }
        }
    }
}
# Traversal-path Get-ChildItem must live only in the module.
$traversalSites = @($gciSites | Where-Object { $_.File -eq 'SafeTraversal.ps1' })
$envSites       = @($gciSites | Where-Object { $_.Text -match 'Get-ChildItem\s+Env:' })
$otherSites     = @($gciSites | Where-Object { $_.File -ne 'SafeTraversal.ps1' -and $_.Text -notmatch 'Get-ChildItem\s+Env:' })

foreach ($f in $scripts) {
    $txt = Get-Content -LiteralPath $f.FullName -Raw
    if ($txt -match 'Get-SafeChildItems' -and $txt -notmatch 'SafeTraversal\.ps1') {
        $missingDotSource += $f.Name
    }
}

$modText = Get-Content -LiteralPath $libPath -Raw
$a1 = ($recurseHits.Count -eq 0)
$a2 = ($traversalSites.Count -eq 1)
$a3 = ($missingDotSource.Count -eq 0)
# A4 — reparse containment covers ALL items and is decided BEFORE the
# directory/file split. Proving the code merely exists is not enough: a
# container-gated test lets a file reparse point into items, where it is hashed.
$a4Exists   = ($modText -match 'Test-IsReparsePoint') -and
              ($modText -match '\[System\.IO\.FileAttributes\]::ReparsePoint') -and
              ($modText -match 'untraversedReparsePoints')
$a4NotGated = ($modText -notmatch 'Test-IsDirectoryReparsePoint')
$modLines = @(Get-Content -LiteralPath $libPath)
$idxLoop = -1; $idxReparse = -1; $idxSplit = -1
for ($k = 0; $k -lt $modLines.Count; $k++) {
    if ($idxLoop -lt 0 -and $modLines[$k] -match 'foreach \(\$c in \$children\)') { $idxLoop = $k; continue }
    if ($idxLoop -ge 0 -and $idxReparse -lt 0 -and $modLines[$k] -match 'Test-IsReparsePoint -Item \$c') { $idxReparse = $k }
    if ($idxLoop -ge 0 -and $idxSplit -lt 0 -and $modLines[$k] -match 'if \(\$c\.PSIsContainer\)') { $idxSplit = $k }
}
$a4Order = ($idxReparse -ge 0 -and $idxSplit -ge 0 -and $idxReparse -lt $idxSplit)
$a4 = $a4Exists -and $a4NotGated -and $a4Order
# A7 — the runtime test asserts no returned item is itself a reparse point.
$a7 = ($modText -match 'reparsePointsInItems') -and
      ($modText -match 'returned item is a reparse point')
# A5 — completeness is computed and can be INCOMPLETE.
$a5 = ($modText -match "completeness\s*=") -and ($modText -match 'INCOMPLETE') -and
      ($modText -match 'incompleteReasons')
# A6 — the inventory consumes completeness rather than ignoring it.
$invPath = Join-Path $scriptDir 'Invoke-HubInventory.ps1'
$a6 = $false
if (Test-Path -LiteralPath $invPath) {
    $invText = Get-Content -LiteralPath $invPath -Raw
    $a6 = ($invText -match 'completeness') -and ($invText -match 'INCOMPLETE')
}

Write-Host ("  A1 no -Recurse in executable code        : {0} ({1} hits)" -f $(if($a1){'PASS'}else{'FAIL'}), $recurseHits.Count) -ForegroundColor $(if($a1){'Green'}else{'Red'})
Write-Host ("  A2 exactly one traversal Get-ChildItem   : {0} ({1} in module)" -f $(if($a2){'PASS'}else{'FAIL'}), $traversalSites.Count) -ForegroundColor $(if($a2){'Green'}else{'Red'})
Write-Host ("  A3 traversing scripts dot-source module  : {0}" -f $(if($a3){'PASS'}else{'FAIL'})) -ForegroundColor $(if($a3){'Green'}else{'Red'})
Write-Host ("  A4 reparse containment covers files+dirs, pre-split: {0}" -f $(if($a4){'PASS'}else{'FAIL'})) -ForegroundColor $(if($a4){'Green'}else{'Red'})
Write-Host ("     exists={0} notContainerGated={1} decidedBeforeSplit={2} (reparse L{3} < split L{4})" -f $a4Exists,$a4NotGated,$a4Order,($idxReparse+1),($idxSplit+1)) -ForegroundColor DarkGray
Write-Host ("  A5 completeness computed, can be INCOMPLETE: {0}" -f $(if($a5){'PASS'}else{'FAIL'})) -ForegroundColor $(if($a5){'Green'}else{'Red'})
Write-Host ("  A6 inventory consumes completeness        : {0}" -f $(if($a6){'PASS'}else{'FAIL'})) -ForegroundColor $(if($a6){'Green'}else{'Red'})
Write-Host ("  A7 runtime test rejects reparse in items  : {0}" -f $(if($a7){'PASS'}else{'FAIL'})) -ForegroundColor $(if($a7){'Green'}else{'Red'})
foreach ($h in $recurseHits) { Write-Host ("    -Recurse at {0}:{1}" -f $h.File,$h.Line) -ForegroundColor Red }
Write-Host ("  Env: provider reads (not filesystem)     : {0}" -f $envSites.Count) -ForegroundColor DarkGray
Write-Host ("  other single-level filesystem reads      : {0}" -f $otherSites.Count) -ForegroundColor DarkGray
foreach ($s in $otherSites) { Write-Host ("    {0}:{1}" -f $s.File,$s.Line) -ForegroundColor DarkGray }

Write-Host ''
Write-Host '=== PART B — runtime proof ===' -ForegroundColor Cyan

$hubResolved = $HubPath
try { $hubResolved = (Resolve-Path -LiteralPath $HubPath -ErrorAction Stop).Path } catch { }
$hubExists = Test-Path -LiteralPath $hubResolved
Write-Host ("  hub          : {0} (exists: {1})" -f $hubResolved, $hubExists)

$b1 = $null; $trav = $null; $proof = $null; $rememberSeen = $false
if ($hubExists) {
    $trav = Get-SafeChildItems -Root $hubResolved
    $proof = Test-SafePruning -Traversal $trav
    $rememberSeen = @($trav.prunedForSafety | Where-Object { $_ -match '(?i)\.remember$' }).Count -gt 0
    $b1 = $proof.pass
    Write-Host ("  directories visited (passed to Get-ChildItem) : {0}" -f $proof.visitedDirectoryCount)
    Write-Host ("  safety-pruned directories                     : {0}" -f $proof.prunedForSafetyCount)
    foreach ($pruned in $trav.prunedForSafety) { Write-Host ("    pruned: {0}" -f $pruned) -ForegroundColor Yellow }
    Write-Host ("  .remember present and pruned                  : {0}" -f $rememberSeen)
    Write-Host ("  reparse points not traversed                  : {0}" -f $proof.reparsePointCount)
    foreach ($rp in $trav.untraversedReparsePoints) { Write-Host ("    reparse: {0}" -f $rp.path) -ForegroundColor Yellow }
    Write-Host ("  noise-pruned                                  : {0}" -f $proof.prunedForNoiseCount)
    Write-Host ("  traversal failures                            : {0}" -f $proof.traversalFailureCount)
    Write-Host ("  depth-limited                                 : {0}" -f $proof.depthLimitedCount)
    Write-Host ("  reparse points inside returned items          : {0}" -f $proof.reparsePointsInItems) -ForegroundColor $(if($proof.reparsePointsInItems -eq 0){'Green'}else{'Red'})
    Write-Host ("  completeness                                  : {0}" -f $proof.completeness) -ForegroundColor $(if($proof.completeness -eq 'COMPLETE'){'Green'}else{'Red'})
    Write-Host ("  B1 no visited dir at/beneath a pruned dir     : {0} ({1} violations)" -f $(if($b1){'PASS'}else{'FAIL'}), @($proof.violations).Count) -ForegroundColor $(if($b1){'Green'}else{'Red'})
    foreach ($v in $proof.violations) { Write-Host ("    $v") -ForegroundColor Red }
} else {
    Write-Host '  SKIPPED: live Hub not found. Part B requires the Hub. Part A still applies.' -ForegroundColor Yellow
}

# ---------------------------------------------------------------------------
# FAIL-CLOSED VERDICT. PASS requires ALL of:
#   - the Hub exists (a skipped runtime proof is not a proof)
#   - every static assertion A1-A7 passes
#   - the runtime pruning test passes
#   - traversal completeness is COMPLETE
# Absence of evidence is never PASS.
# ---------------------------------------------------------------------------
$staticOk    = ($a1 -and $a2 -and $a3 -and $a4 -and $a5 -and $a6 -and $a7)
$runtimeOk   = ($hubExists -and ($b1 -eq $true))
$completeOk  = ($hubExists -and $null -ne $proof -and $proof.completeness -eq 'COMPLETE')
$verdict     = if ($staticOk -and $runtimeOk -and $completeOk) { 'PASS' } else { 'FAIL' }

$failReasons = @()
if (-not $staticOk)   { $failReasons += 'one or more static assertions A1-A7 failed' }
if (-not $hubExists)  { $failReasons += 'live Hub not found at the resolved path; runtime proof could not run' }
elseif ($b1 -ne $true) { $failReasons += 'runtime pruning test failed' }
if ($hubExists -and $null -ne $proof -and $proof.completeness -ne 'COMPLETE') {
    $failReasons += "traversal completeness is $($proof.completeness)"
}
if ($hubExists -and -not $rememberSeen) {
    $failReasons += 'advisory: no .remember directory was present to prune (not a failure by itself)'
}

Write-Host ''
Write-Host '=== PART C — proof artifact ===' -ForegroundColor Cyan
if (-not (Test-Path -LiteralPath $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }
$proofPath = Join-Path $OutDir "REMEMBER-PRUNING-PROOF-$stamp.md"

$P = New-Object System.Collections.Generic.List[string]
$P.Add('# Pre-Descent Pruning Proof')
$P.Add('')
$P.Add("**Verdict:** $verdict")
$P.Add('')
$P.Add('Verdict is fail-closed. PASS requires the Hub to exist, A1-A7 to pass, the')
$P.Add('runtime pruning test to pass, and traversal completeness to be COMPLETE. A')
$P.Add('skipped runtime proof is not a proof.')
if (@($failReasons).Count -gt 0) {
    $P.Add('')
    $P.Add('Reasons:')
    $P.Add('')
    foreach ($fr in $failReasons) { $P.Add("- $fr") }
}
$P.Add("**Generated:** $stampISO")
$P.Add("**Machine:** $env:COMPUTERNAME")
$P.Add('**Claim under test:** protected directories are pruned before descent, not filtered out of recursive output afterwards.')
$P.Add('')
$P.Add('Filtering after recursion and pruning before descent produce identical')
$P.Add('output. Absence of `.remember` from a report therefore proves nothing. This')
$P.Add('proof rests on the record of directories actually passed to `Get-ChildItem`.')
$P.Add('')
$P.Add('## Part A — static invariant')
$P.Add('')
$P.Add('| # | Assertion | Result |')
$P.Add('|---|---|---|')
$P.Add("| A1 | No ``Get-ChildItem -Recurse`` in executable code | $(if($a1){'PASS'}else{'FAIL'}) — $($recurseHits.Count) hits |")
$P.Add("| A2 | Exactly one traversal ``Get-ChildItem``, single-level, in ``lib/SafeTraversal.ps1`` | $(if($a2){'PASS'}else{'FAIL'}) — $($traversalSites.Count) found |")
$P.Add("| A3 | Every traversing script dot-sources the module | $(if($a3){'PASS'}else{'FAIL'}) |")
$P.Add("| A4 | Reparse-point containment present and attribute-based | $(if($a4){'PASS'}else{'FAIL'}) |")
$P.Add("| A5 | Completeness computed and can be INCOMPLETE | $(if($a5){'PASS'}else{'FAIL'}) |")
$P.Add("| A6 | Inventory consumes completeness rather than ignoring it | $(if($a6){'PASS'}else{'FAIL'}) |")
$P.Add("| A7 | Runtime test rejects any reparse point inside returned items | $(if($a7){'PASS'}else{'FAIL'}) |")
$P.Add('')
$P.Add('Without `-Recurse`, a subtree cannot be traversed before the prune decision is made.')
$P.Add('')
$P.Add('A4 matters twice over. A name-based prune list is defeated by an alias: a')
$P.Add('junction named anything can target a protected directory or a location outside')
$P.Add('the Hub, so detection is by file attribute. And the test must run BEFORE the')
$P.Add('directory/file split — a container-gated test lets a FILE reparse point reach')
$P.Add('the file branch, enter `items`, and be hashed, and `Get-FileHash` follows the')
$P.Add('link. A4 asserts the call site precedes the split by line order:')
$P.Add("reparse at line $($idxReparse+1), split at line $($idxSplit+1).")
$P.Add('')
if ($recurseHits.Count -gt 0) {
    $P.Add('### -Recurse violations'); $P.Add('')
    foreach ($h in $recurseHits) { $P.Add("- ``$($h.File):$($h.Line)`` — ``$($h.Text)``") }
    $P.Add('')
}
$P.Add('## Part B — runtime proof')
$P.Add('')
if ($hubExists) {
    $P.Add("Hub traversed: ``$hubResolved``")
    $P.Add('')
    $P.Add('| Metric | Value |')
    $P.Add('|---|---|')
    $P.Add("| Directories passed to ``Get-ChildItem`` | $($proof.visitedDirectoryCount) |")
    $P.Add("| Safety-pruned directories | $($proof.prunedForSafetyCount) |")
    $P.Add("| ``.remember`` found and pruned | $rememberSeen |")
    $P.Add("| Items returned | $($proof.itemCount) |")
    $P.Add("| Reparse points not traversed | $($proof.reparsePointCount) |")
    $P.Add("| Noise-pruned | $($proof.prunedForNoiseCount) |")
    $P.Add("| Traversal failures | $($proof.traversalFailureCount) |")
    $P.Add("| Depth-limited | $($proof.depthLimitedCount) |")
    $P.Add("| Reparse points inside returned items | $($proof.reparsePointsInItems) |")
    $P.Add("| **Completeness** | **$($proof.completeness)** |")
    $P.Add("| Violations | $(@($proof.violations).Count) |")
    $P.Add('')
    if (@($trav.prunedForSafety).Count -gt 0) {
        $P.Add('### Safety-pruned, never entered'); $P.Add('')
        foreach ($pruned in $trav.prunedForSafety) { $P.Add("- ``$pruned``") }
        $P.Add('')
    }
    if (@($trav.untraversedReparsePoints).Count -gt 0) {
        $P.Add('### Not traversed — directory reparse points'); $P.Add('')
        foreach ($rp in $trav.untraversedReparsePoints) { $P.Add("- ``$($rp.path)`` — $($rp.note)") }
        $P.Add('')
    }
    if (@($trav.traversalFailures).Count -gt 0) {
        $P.Add('### Traversal failures'); $P.Add('')
        foreach ($tf in $trav.traversalFailures) { $P.Add("- ``$($tf.path)`` — $($tf.reason)") }
        $P.Add('')
    }
    if (@($trav.depthLimited).Count -gt 0) {
        $P.Add('### Depth-limited'); $P.Add('')
        foreach ($dl in $trav.depthLimited) { $P.Add("- ``$($dl.path)`` — $($dl.note)") }
        $P.Add('')
    }
    $P.Add("**B1 — no visited directory is at or beneath a pruned directory: $(if($b1){'PASS'}else{'FAIL'})**")
    $P.Add('')
    if (@($proof.violations).Count -gt 0) {
        foreach ($v in $proof.violations) { $P.Add("- $v") }
        $P.Add('')
    }
    $P.Add('### Directories actually visited')
    $P.Add('')
    foreach ($v in $trav.visitedDirectories) { $P.Add("- ``$v``") }
} else {
    $P.Add('Part B skipped: no live Hub at the resolved path. Part A still holds.')
}
$P.Add('')
$P.Add('## Scope')
$P.Add('')
$P.Add('- Part A is a source-level invariant and holds regardless of filesystem state.')
$P.Add('- Part B reflects one traversal of one machine at the stated time.')
$P.Add('- Neither part inspects anything inside a pruned directory or a reparse point.')
$P.Add('  Existence is established while listing the parent.')
$P.Add('- Reparse-point targets are outside the read boundary and are not inventoried.')
$P.Add('  No exhaustiveness claim covers them.')
($P -join "`r`n") | Set-Content -LiteralPath $proofPath -Encoding UTF8

Write-Host ''
if ($verdict -eq 'PASS') {
    Write-Host 'VERDICT: PASS' -ForegroundColor Green
} else {
    Write-Host 'VERDICT: FAIL' -ForegroundColor Red
    foreach ($fr in $failReasons) { Write-Host "  - $fr" -ForegroundColor Red }
}
Write-Host "  Proof: $proofPath"
if ($verdict -ne 'PASS') { exit 1 }
