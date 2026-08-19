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

function Get-CodeLines {
    param([string]$Path)
    $out = @(); $inHelp = $false; $i = 0
    foreach ($l in (Get-Content -LiteralPath $Path)) {
        $i++
        if ($l.Trim().StartsWith('<#')) { $inHelp = $true; continue }
        if ($inHelp) { if ($l -match '#>') { $inHelp = $false }; continue }
        if ($l.Trim().StartsWith('#')) { continue }
        # Strip string literals BEFORE matching, so prose inside quotes is not
        # mistaken for a call. Without this, the proof text describing
        # "Get-ChildItem -Recurse" would register as a violation.
        $stripped = $l
        $stripped = [regex]::Replace($stripped, "'(?:[^']|'')*'", '')
        $stripped = [regex]::Replace($stripped, '"(?:[^"]|"")*"', '')
        $stripped = ($stripped -replace '#.*$','')
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

$a1 = ($recurseHits.Count -eq 0)
$a2 = ($traversalSites.Count -eq 1)
$a3 = ($missingDotSource.Count -eq 0)

Write-Host ("  A1 no -Recurse in executable code        : {0} ({1} hits)" -f $(if($a1){'PASS'}else{'FAIL'}), $recurseHits.Count) -ForegroundColor $(if($a1){'Green'}else{'Red'})
Write-Host ("  A2 exactly one traversal Get-ChildItem   : {0} ({1} in module)" -f $(if($a2){'PASS'}else{'FAIL'}), $traversalSites.Count) -ForegroundColor $(if($a2){'Green'}else{'Red'})
Write-Host ("  A3 traversing scripts dot-source module  : {0}" -f $(if($a3){'PASS'}else{'FAIL'})) -ForegroundColor $(if($a3){'Green'}else{'Red'})
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
    foreach ($p in $trav.prunedForSafety) { Write-Host ("    pruned: {0}" -f $p) -ForegroundColor Yellow }
    Write-Host ("  .remember present and pruned                  : {0}" -f $rememberSeen)
    Write-Host ("  B1 no visited dir at/beneath a pruned dir     : {0} ({1} violations)" -f $(if($b1){'PASS'}else{'FAIL'}), @($proof.violations).Count) -ForegroundColor $(if($b1){'Green'}else{'Red'})
    foreach ($v in $proof.violations) { Write-Host ("    $v") -ForegroundColor Red }
} else {
    Write-Host '  SKIPPED: live Hub not found. Part B requires the Hub. Part A still applies.' -ForegroundColor Yellow
}

$verdict = if ($a1 -and $a2 -and $a3 -and ($null -eq $b1 -or $b1)) { 'PASS' } else { 'FAIL' }
if ($hubExists -and -not $rememberSeen) { $verdict = "$verdict (advisory: no .remember directory found to prune)" }

Write-Host ''
Write-Host '=== PART C — proof artifact ===' -ForegroundColor Cyan
if (-not (Test-Path -LiteralPath $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }
$proofPath = Join-Path $OutDir "REMEMBER-PRUNING-PROOF-$stamp.md"

$P = New-Object System.Collections.Generic.List[string]
$P.Add('# Pre-Descent Pruning Proof')
$P.Add('')
$P.Add("**Verdict:** $verdict")
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
$P.Add('')
$P.Add('Without `-Recurse`, a subtree cannot be traversed before the prune decision is made.')
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
    $P.Add("| Violations | $(@($proof.violations).Count) |")
    $P.Add('')
    if (@($trav.prunedForSafety).Count -gt 0) {
        $P.Add('### Pruned, never entered'); $P.Add('')
        foreach ($p in $trav.prunedForSafety) { $P.Add("- ``$p``") }
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
$P.Add('- Neither part inspects anything inside a pruned directory. Existence is')
$P.Add('  established while listing the parent.')
($P -join "`r`n") | Set-Content -LiteralPath $proofPath -Encoding UTF8

Write-Host ''
if ($verdict -like 'PASS*') { Write-Host "VERDICT: $verdict" -ForegroundColor Green }
else { Write-Host "VERDICT: $verdict" -ForegroundColor Red }
Write-Host "  Proof: $proofPath"
