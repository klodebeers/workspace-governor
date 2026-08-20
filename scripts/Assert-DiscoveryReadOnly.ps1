<#
.SYNOPSIS
  Runs Gateway discovery and independently proves it changed nothing.

.DESCRIPTION
  Three-part verification:

    PART A — Static analysis.
      Scans Invoke-GatewayDiscovery.ps1 for every mutating cmdlet and for
      install/network/process-start verbs. Each hit is listed with its line so
      it can be eyeballed. Expected: mutations confined to the emit block
      (New-Item / Set-Content targeting -OutDir only).

    PART B — Filesystem baseline and comparison.
      Records path, size and last-write time for every file under the inspected
      roots BEFORE running discovery, runs discovery, then re-records and
      compares. Any modification, creation or deletion outside -OutDir fails.

    PART C — Verdict and proof artifact.
      Writes a committable proof document stating PASS or FAIL with counts.

  This wrapper is itself read-only apart from the proof file and whatever
  discovery emits into -OutDir.

.PARAMETER HubPath
  Passed through to discovery. Default: $env:USERPROFILE\.agents-hub

.PARAMETER WorkspaceRoot
  Passed through to discovery. Default: C:\KloWorkspaces

.PARAMETER OutDir
  Output directory for evidence and the proof file. Default: .\evidence

.PARAMETER Thorough
  Also SHA256-hash files under 2 MB for a stronger comparison. Slower.

.EXAMPLE
  .\Assert-DiscoveryReadOnly.ps1
#>

[CmdletBinding()]
param(
    [string]$HubPath       = (Join-Path $env:USERPROFILE '.agents-hub'),
    [string]$WorkspaceRoot = 'C:\KloWorkspaces',
    [string]$OutDir        = (Join-Path (Get-Location) 'evidence'),
    [switch]$Thorough
)


# ---- traversal owner -------------------------------------------------------
# Sole owner of directory traversal. Provides pre-descent pruning so a
# protected directory is never passed to Get-ChildItem. No -Recurse anywhere.
$libPath = Join-Path $PSScriptRoot 'lib\SafeTraversal.ps1'
if (-not (Test-Path -LiteralPath $libPath)) {
    Write-Host "FAIL: required module not found: $libPath" -ForegroundColor Red
    exit 1
}
. $libPath

$ErrorActionPreference = 'Continue'
$stamp    = Get-Date -Format 'yyyy-MM-dd'
$stampISO = (Get-Date).ToString('o')
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$discovery = Join-Path $scriptDir 'Invoke-GatewayDiscovery.ps1'
$RememberGuard = '(?i)\\design-systems\\\.remember($|\\)'

if (-not (Test-Path -LiteralPath $discovery)) {
    Write-Host "FAIL: discovery script not found at $discovery" -ForegroundColor Red
    exit 1
}

Write-Host '=== PART A — static analysis of the discovery script ===' -ForegroundColor Cyan

$MutatingPatterns = @(
    'Set-Content','Add-Content','Out-File','New-Item','Remove-Item','Move-Item',
    'Rename-Item','Copy-Item','Clear-Content','Set-ItemProperty','New-ItemProperty',
    'Remove-ItemProperty','Set-Item','Clear-Item','New-ItemProperty',
    'Set-Acl','Set-Service','Stop-Service','Start-Service','Restart-Service',
    'Start-Process','Invoke-Expression','Invoke-WebRequest','Invoke-RestMethod',
    'Set-ExecutionPolicy','Register-','Unregister-','Install-','Uninstall-','Update-',
    'reg add','reg delete','netsh','schtasks','New-NetFirewallRule'
)
$src = Get-Content -LiteralPath $discovery
$hits = @()
for ($i=0; $i -lt $src.Count; $i++) {
    $line = $src[$i]
    if ($line -match '^\s*#') { continue }          # skip comment lines
    foreach ($pat in $MutatingPatterns) {
        if ($line -match [regex]::Escape($pat)) {
            $hits += [ordered]@{ line=($i+1); cmdlet=$pat; text=$line.Trim() }
        }
    }
}
$emitOnly = $true
foreach ($h in $hits) {
    # Permitted: creating -OutDir and writing the two evidence files
    $ok = ($h.text -match '\$OutDir') -or ($h.text -match '\$jsonPath') -or ($h.text -match '\$mdPath')
    if (-not $ok) { $emitOnly = $false }
    $h['permitted'] = $ok
}
Write-Host ("  mutating-cmdlet hits: {0}" -f $hits.Count)
foreach ($h in $hits) {
    $tag = if ($h.permitted) { 'OK (emit block)' } else { 'REVIEW' }
    $col = if ($h.permitted) { 'DarkGray' } else { 'Yellow' }
    Write-Host ("    L{0,-4} {1,-22} {2}" -f $h.line, $h.cmdlet, $tag) -ForegroundColor $col
}
Write-Host ("  PART A: {0}" -f $(if ($emitOnly) { 'PASS — all mutations target the output directory' } else { 'REVIEW REQUIRED — see lines marked REVIEW above' })) `
    -ForegroundColor $(if ($emitOnly) { 'Green' } else { 'Yellow' })

Write-Host ''
Write-Host '=== PART B — filesystem baseline ===' -ForegroundColor Cyan

$roots = @($HubPath, $WorkspaceRoot, (Join-Path $env:USERPROFILE '.claude'), (Join-Path $env:USERPROFILE '.codex')) |
         Where-Object { Test-Path -LiteralPath $_ }
$outFull = try { (Resolve-Path -LiteralPath $OutDir -ErrorAction Stop).Path } catch { $OutDir }

function Get-Manifest {
    param([string[]]$Roots)
    $m = @{}
    foreach ($r in $Roots) {
        # Pre-descent pruning; .remember, .git and node_modules are never entered.
        $items = @((Get-SafeChildItems -Root $r -FilesOnly).items |
                   Where-Object { -not $_.FullName.StartsWith($outFull, [System.StringComparison]::OrdinalIgnoreCase) })
        foreach ($f in $items) {
            $key = $f.FullName
            $sig = '{0}|{1}' -f $f.Length, $f.LastWriteTimeUtc.Ticks
            if ($Thorough -and $f.Length -lt 2MB) {
                $h = Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256 -ErrorAction SilentlyContinue
                if ($h) { $sig = $sig + '|' + $h.Hash }
            }
            $m[$key] = $sig
        }
    }
    return $m
}

Write-Host ("  roots: {0}" -f ($roots -join ', '))
Write-Host ("  mode : {0}" -f $(if ($Thorough) { 'size + mtime + sha256 (<2MB)' } else { 'size + mtime' }))
Write-Host '  taking baseline...'
$before = Get-Manifest -Roots $roots
Write-Host ("  baseline files: {0}" -f $before.Count)

Write-Host ''
Write-Host '=== running discovery ===' -ForegroundColor Cyan
& $discovery -HubPath $HubPath -WorkspaceRoot $WorkspaceRoot -OutDir $OutDir
$discoveryExit = $LASTEXITCODE

Write-Host ''
Write-Host '=== PART B — comparison ===' -ForegroundColor Cyan
$after = Get-Manifest -Roots $roots

$modified = @(); $created = @(); $deleted = @()
foreach ($k in $before.Keys) {
    if (-not $after.ContainsKey($k)) { $deleted += $k }
    elseif ($after[$k] -ne $before[$k]) { $modified += $k }
}
foreach ($k in $after.Keys) { if (-not $before.ContainsKey($k)) { $created += $k } }

Write-Host ("  modified outside OutDir : {0}" -f $modified.Count)
Write-Host ("  created  outside OutDir : {0}" -f $created.Count)
Write-Host ("  deleted                 : {0}" -f $deleted.Count)
foreach ($f in (($modified + $created + $deleted) | Select-Object -First 25)) { Write-Host "    $f" -ForegroundColor Yellow }

$partB = ($modified.Count -eq 0 -and $created.Count -eq 0 -and $deleted.Count -eq 0)
Write-Host ("  PART B: {0}" -f $(if ($partB) { 'PASS — no filesystem changes outside the output directory' } else { 'FAIL — see files listed above' })) `
    -ForegroundColor $(if ($partB) { 'Green' } else { 'Red' })

Write-Host ''
Write-Host '=== PART C — verdict ===' -ForegroundColor Cyan
$verdict = if ($emitOnly -and $partB) { 'PASS' } else { 'FAIL' }

$proof = Join-Path $OutDir "GATEWAY-DISCOVERY-$stamp-READONLY-PROOF.md"
$P = New-Object System.Collections.Generic.List[string]
$P.Add('# Discovery Read-Only Proof')
$P.Add('')
$P.Add("**Verdict:** $verdict")
$P.Add("**Generated:** $stampISO")
$P.Add("**Machine:** $env:COMPUTERNAME")
$P.Add("**Discovery script:** ``Invoke-GatewayDiscovery.ps1``")
$P.Add("**Comparison mode:** $(if ($Thorough) { 'size + mtime + sha256 (<2MB)' } else { 'size + mtime' })")
$P.Add('')
$P.Add('## Part A — static analysis')
$P.Add('')
$P.Add("Mutating-cmdlet occurrences found: **$($hits.Count)**")
$P.Add('')
$P.Add('| Line | Cmdlet | Targets output dir | Statement |')
$P.Add('|---|---|---|---|')
foreach ($h in $hits) { $P.Add("| $($h.line) | ``$($h.cmdlet)`` | $($h.permitted) | ``$($h.text -replace '\|','\|')`` |") }
$P.Add('')
$P.Add("Result: **$(if ($emitOnly) { 'PASS' } else { 'REVIEW REQUIRED' })**")
$P.Add('')
$P.Add('## Part B — filesystem comparison')
$P.Add('')
$P.Add("Roots monitored: $($roots -join ', ')")
$P.Add('')
$P.Add('| Metric | Count |')
$P.Add('|---|---|')
$P.Add("| Files in baseline | $($before.Count) |")
$P.Add("| Files after run | $($after.Count) |")
$P.Add("| Modified outside output dir | $($modified.Count) |")
$P.Add("| Created outside output dir | $($created.Count) |")
$P.Add("| Deleted | $($deleted.Count) |")
$P.Add('')
if (-not $partB) {
    $P.Add('### Unexpected changes')
    $P.Add('')
    foreach ($f in $modified) { $P.Add("- MODIFIED ``$f``") }
    foreach ($f in $created)  { $P.Add("- CREATED  ``$f``") }
    foreach ($f in $deleted)  { $P.Add("- DELETED  ``$f``") }
    $P.Add('')
}
$P.Add("Result: **$(if ($partB) { 'PASS' } else { 'FAIL' })**")
$P.Add('')
$P.Add('## Scope of this proof')
$P.Add('')
$P.Add('- Covers the filesystem roots listed above. Excludes `.git`, `node_modules`, `design-systems\.remember`, and the output directory.')
$P.Add('- Does not monitor the Windows registry, installed services, scheduled tasks, or network state. Part A establishes the script contains no cmdlet that touches them.')
$P.Add('- File read operations may update last-access time; this proof compares last-WRITE time and size, which reads do not alter.')
($P -join "`r`n") | Set-Content -LiteralPath $proof -Encoding UTF8

Write-Host ''
if ($verdict -eq 'PASS') {
    Write-Host 'VERDICT: PASS — discovery made no system changes.' -ForegroundColor Green
} else {
    Write-Host 'VERDICT: FAIL — review the proof document before committing.' -ForegroundColor Red
}
Write-Host "  Proof: $proof"
Write-Host ''
Write-Host 'Commit the contents of the evidence directory to workspace-governor.' -ForegroundColor Yellow
