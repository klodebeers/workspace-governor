<#
.SYNOPSIS
  Read-only inventory of the live local .agents-hub, compared against the
  committed GitHub baseline for agents-hub (captured while named agents-hub-one).

.DESCRIPTION
  Answers one question: what exists in the live local Hub that is absent,
  different, or only a placeholder in GitHub agents-hub?

  No network access and no clone required. The GitHub side is read from
  evidence\AGENTS-HUB-ONE-BASELINE-<date>.json, which was generated from a
  verified clone and committed to this repository.

  SAFETY CONTRACT. This script:
    - performs NO writes anywhere except the files it emits into -OutDir
    - never installs, modifies, deletes, moves, renames, reconfigures or repairs
    - makes NO network calls
    - never emits file contents; only paths, sizes, hashes and classifications
    - does not read, hash, enumerate, or count anything inside
      'design-systems\.remember'. Checks EXISTENCE ONLY, per the unresolved
      provenance and sensitivity hold in workspace-governor STATE.md (B-2)
    - resolves the Hub path from the environment; nothing is hardcoded

  Content is never emitted, so secrets cannot leak through this report. Only
  path, size, and SHA256 are recorded.

.PARAMETER HubPath
  Live Hub location. Default: $env:USERPROFILE\.agents-hub
  The resolved path is recorded in the output so the evidence states exactly
  what was inspected.

.PARAMETER BaselinePath
  Committed GitHub baseline JSON. Default: newest
  evidence\AGENTS-HUB-ONE-BASELINE-*.json in this repository.

.PARAMETER OutDir
  Output directory. Default: .\evidence

.EXAMPLE
  .\scripts\Invoke-HubInventory.ps1
#>

[CmdletBinding()]
param(
    [string]$HubPath      = (Join-Path $env:USERPROFILE '.agents-hub'),
    [string]$BaselinePath = '',
    [string]$OutDir       = (Join-Path (Get-Location) 'evidence')
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
$RememberRel = 'design-systems\.remember'

Write-Host '=== Live Hub Inventory (read-only, no network) ===' -ForegroundColor Cyan

# ---- resolve baseline ------------------------------------------------------
if ([string]::IsNullOrWhiteSpace($BaselinePath)) {
    $cand = @(Get-ChildItem -LiteralPath $OutDir -Filter 'AGENTS-HUB-ONE-BASELINE-*.json' -File -ErrorAction SilentlyContinue |
             Sort-Object Name -Descending)
    if ($cand.Count -gt 0) { $BaselinePath = $cand[0].FullName }
}
if (-not (Test-Path -LiteralPath $BaselinePath)) {
    Write-Host "FAIL: baseline JSON not found. Expected evidence\AGENTS-HUB-ONE-BASELINE-*.json" -ForegroundColor Red
    exit 1
}
$baseline = Get-Content -LiteralPath $BaselinePath -Raw | ConvertFrom-Json
$baseFiles = @{}
foreach ($p in $baseline.files.PSObject.Properties) { $baseFiles[$p.Name] = $p.Value }
Write-Host ("  baseline    : {0}" -f (Split-Path $BaselinePath -Leaf))
Write-Host ("  baseline ref: {0} ({1} files, {2} placeholders)" -f $baseline.meta.head, $baseline.meta.fileCount, $baseline.meta.placeholderCount)

# ---- resolve and report the live Hub path ---------------------------------
$hubResolved = $null
try { $hubResolved = (Resolve-Path -LiteralPath $HubPath -ErrorAction Stop).Path } catch { $hubResolved = $HubPath }
$hubExists = Test-Path -LiteralPath $hubResolved
Write-Host ("  live hub    : {0}" -f $hubResolved)
Write-Host ("  exists      : {0}" -f $hubExists)
if (-not $hubExists) {
    Write-Host '  NOTE: live Hub not found at the resolved path. Re-run with -HubPath if it lives elsewhere.' -ForegroundColor Yellow
}

# ---- enumerate the live Hub ----------------------------------------------
$live = @{}
$rememberFact = [ordered]@{ exists=$false; contentsInspected=$false; method='Test-Path existence check only; no enumeration' }
if ($hubExists) {
    # EXISTENCE ONLY. Established while listing the PARENT directory during
    # traversal. .remember is never passed to Get-ChildItem.
    $rememberFact.exists = Test-Path -LiteralPath (Join-Path $hubResolved $RememberRel)

    # Pre-descent pruning traversal. See scripts/lib/SafeTraversal.ps1.
    # Limits are set high so a real Hub completes; if they are ever reached the
    # traversal reports INCOMPLETE rather than silently omitting files.
    $trav = Get-SafeChildItems -Root $hubResolved -FilesOnly -MaxDepth 128 -MaxItems 200000
    $pruneProof = Test-SafePruning -Traversal $trav
    if (-not $pruneProof.pass) {
        Write-Host 'FAIL: pruning invariant violated. Aborting before any report is written.' -ForegroundColor Red
        foreach ($v in $pruneProof.violations) { Write-Host "  $v" -ForegroundColor Red }
        exit 1
    }
    Write-Host ("  completeness : {0}" -f $trav.completeness) -ForegroundColor $(if ($trav.completeness -eq 'COMPLETE') { 'Green' } else { 'Red' })
    foreach ($reason in $trav.incompleteReasons) { Write-Host "    - $reason" -ForegroundColor Red }
    if (@($trav.untraversedReparsePoints).Count -gt 0) {
        Write-Host ("  reparse points excluded : {0}" -f @($trav.untraversedReparsePoints).Count) -ForegroundColor Yellow
        foreach ($rp in $trav.untraversedReparsePoints) { Write-Host "    - [$($rp.kind)] $($rp.path)" -ForegroundColor Yellow }
    }
    $rootLen = ($hubResolved.TrimEnd('\')).Length
    $items = $trav.items
    foreach ($f in $items) {
        $rel = $f.FullName.Substring($rootLen).TrimStart('\')
        $sha = $null
        if ($f.Length -gt 0) {
            $h = Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256 -ErrorAction SilentlyContinue
            if ($h) { $sha = $h.Hash }
        }
        $live[$rel] = [ordered]@{
            size = $f.Length
            sha256 = $sha
            placeholder = ($f.Length -eq 0)
            modifiedUtc = $f.LastWriteTimeUtc.ToString('o')
        }
    }
}
Write-Host ("  live files  : {0}" -f $live.Count)

# ---- compare -------------------------------------------------------------
$onlyLive = @(); $onlyGitHub = @(); $different = @(); $identical = @(); $placeholderInGitHub = @()

foreach ($rel in $live.Keys) {
    if (-not $baseFiles.ContainsKey($rel)) { $onlyLive += $rel; continue }
    $b = $baseFiles[$rel]; $l = $live[$rel]
    if ($b.placeholder -and -not $l.placeholder) {
        $placeholderInGitHub += [ordered]@{ path=$rel; liveSize=$l.size; gitHubSize=0 }
    } elseif ($b.sha256 -ne $l.sha256) {
        $different += [ordered]@{ path=$rel; liveSize=$l.size; gitHubSize=$b.size }
    } else {
        $identical += $rel
    }
}
foreach ($rel in $baseFiles.Keys) { if (-not $live.ContainsKey($rel)) { $onlyGitHub += $rel } }

Write-Host ''
Write-Host ("  only in live Hub            : {0}" -f $onlyLive.Count)          -ForegroundColor Yellow
Write-Host ("  placeholder in GitHub, real live : {0}" -f $placeholderInGitHub.Count) -ForegroundColor Yellow
Write-Host ("  content differs             : {0}" -f $different.Count)         -ForegroundColor Yellow
Write-Host ("  only in GitHub              : {0}" -f $onlyGitHub.Count)
Write-Host ("  identical                   : {0}" -f $identical.Count)         -ForegroundColor Green

# ---- emit ----------------------------------------------------------------
if (-not (Test-Path -LiteralPath $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }
$jsonPath = Join-Path $OutDir "LIVE-HUB-INVENTORY-$stamp.json"
$mdPath   = Join-Path $OutDir "LIVE-HUB-INVENTORY-$stamp.md"

$R = [ordered]@{
    meta = [ordered]@{
        generatedUtc = $stampISO
        script = 'Invoke-HubInventory.ps1'
        machine = $env:COMPUTERNAME
        hubPathResolved = $hubResolved
        hubExists = $hubExists
        traversal = 'pre-descent pruning via lib/SafeTraversal.ps1; no -Recurse; all reparse points (file and directory) excluded before the directory/file split'
        completeness = if ($hubExists) { $trav.completeness } else { 'INCOMPLETE' }
        incompleteReasons = if ($hubExists) { @($trav.incompleteReasons) } else { @('live Hub not found at the resolved path') }
        exhaustivenessScope = 'Complete within the physical Hub tree. Excludes safety-pruned directories, noise-pruned directories, and any reparse-point target. No claim is made about content behind those boundaries.'
        baselineFile = (Split-Path $BaselinePath -Leaf)
        baselineRef = $baseline.meta.head
        readOnly = $true
        networkCalls = $false
        contentEmitted = $false
    }
    counts = [ordered]@{
        liveFiles = $live.Count
        gitHubFiles = $baseFiles.Count
        onlyInLive = $onlyLive.Count
        placeholderInGitHubRealInLive = $placeholderInGitHub.Count
        contentDiffers = $different.Count
        onlyInGitHub = $onlyGitHub.Count
        identical = $identical.Count
        prunedForSafety = if ($hubExists) { @($trav.prunedForSafety).Count } else { 0 }
        prunedForNoise = if ($hubExists) { @($trav.prunedForNoise).Count } else { 0 }
        untraversedReparsePoints = if ($hubExists) { @($trav.untraversedReparsePoints).Count } else { 0 }
        traversalFailures = if ($hubExists) { @($trav.traversalFailures).Count } else { 0 }
        depthLimited = if ($hubExists) { @($trav.depthLimited).Count } else { 0 }
    }
    exclusionsAndFailures = if ($hubExists) { [ordered]@{
        prunedForSafety = @($trav.prunedForSafety)
        prunedForNoise = @($trav.prunedForNoise)
        untraversedReparsePoints = @($trav.untraversedReparsePoints)
        traversalFailures = @($trav.traversalFailures)
        depthLimited = @($trav.depthLimited)
        truncated = $trav.truncated
    } } else { $null }
    onlyInLive = @($onlyLive | Sort-Object)
    placeholderInGitHubRealInLive = $placeholderInGitHub
    contentDiffers = $different
    onlyInGitHub = @($onlyGitHub | Sort-Object)
    identical = @($identical | Sort-Object)
    liveInventory = $live
    remember = $rememberFact
    pruningProof = if ($hubExists) { [ordered]@{
        pass = $pruneProof.pass
        prunedForSafety = @($trav.prunedForSafety)
        visitedDirectoryCount = $pruneProof.visitedDirectoryCount
        visitedDirectories = @($trav.visitedDirectories)
        violations = @($pruneProof.violations)
        proofMethod = 'no visited directory is at or beneath a safety-pruned directory'
    } } else { $null }
    unverified = @(
        'design-systems\.remember: existence only. Nothing inside was read, hashed, enumerated, or counted (stop condition B-2).',
        'No file contents were emitted; only path, size, SHA256 and modified time.',
        'Baseline reflects GitHub agents-hub -- captured while named agents-hub-one -- at the recorded ref, not any later commit.',
        'A file identical by SHA256 is byte-identical; semantic equivalence was not assessed.',
        'Reparse points of either kind, file or directory, were excluded before the directory/file split; they were never returned and never hashed, and nothing behind them is inventoried.',
        'The inventory is exhaustive only within the physical Hub tree, excluding pruned directories and reparse-point targets.'
    )
}
$R | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

$L = New-Object System.Collections.Generic.List[string]
$L.Add('# Live Hub Inventory')
$L.Add('')
$L.Add("**Generated:** $stampISO")
$L.Add("**Machine:** $env:COMPUTERNAME")
$L.Add("**Live Hub inspected:** ``$hubResolved`` (exists: $hubExists)")
$L.Add("**Compared against:** ``$(Split-Path $BaselinePath -Leaf)`` at ref ``$($baseline.meta.head)``")
$L.Add('**Method:** read-only, no network. No file contents emitted. Reparse points of either kind excluded; nothing hashed through a link.')
$L.Add('')
$travComplete = if ($hubExists) { $trav.completeness } else { 'INCOMPLETE' }
$L.Add("## Completeness: $travComplete")
$L.Add('')
if ($travComplete -ne 'COMPLETE') {
    $L.Add('**This inventory is INCOMPLETE. Do not treat it as a full picture of the Hub.**')
    $L.Add('')
    if ($hubExists) { foreach ($reason in $trav.incompleteReasons) { $L.Add("- $reason") } }
    else { $L.Add('- live Hub not found at the resolved path') }
} else {
    $L.Add('Every directory in the accessible Hub tree was enumerated. No item cap, no')
    $L.Add('depth cap, and no enumeration error was encountered.')
}
$L.Add('')
$L.Add('Scope of that claim: complete within the **physical** Hub tree. It excludes')
$L.Add('safety-pruned directories, noise-pruned directories, and the targets of any')
$L.Add('reparse point. No claim is made about content behind those boundaries.')
$L.Add('')
$L.Add('## Counts')
$L.Add('')
$L.Add('| Metric | Count |')
$L.Add('|---|---|')
$L.Add("| Live Hub files | $($live.Count) |")
$L.Add("| GitHub baseline files | $($baseFiles.Count) |")
$L.Add("| **Only in live Hub** | **$($onlyLive.Count)** |")
$L.Add("| **Placeholder in GitHub, real content live** | **$($placeholderInGitHub.Count)** |")
$L.Add("| **Content differs** | **$($different.Count)** |")
$L.Add("| Only in GitHub | $($onlyGitHub.Count) |")
$L.Add("| Identical | $($identical.Count) |")
$L.Add('')
if ($onlyLive.Count -gt 0) {
    $L.Add('## Present live, absent from GitHub')
    $L.Add('')
    $L.Add('These are unrepresented in `agents-hub` and must be classified before consolidation.')
    $L.Add('')
    foreach ($p in ($onlyLive | Sort-Object)) { $L.Add("- ``$p`` ($($live[$p].size) bytes)") }
    $L.Add('')
}
if ($placeholderInGitHub.Count -gt 0) {
    $L.Add('## Placeholder in GitHub, real content live')
    $L.Add('')
    $L.Add('| Path | Live size | GitHub |')
    $L.Add('|---|---|---|')
    foreach ($e in $placeholderInGitHub) { $L.Add("| ``$($e.path)`` | $($e.liveSize) | 0-byte placeholder |") }
    $L.Add('')
}
if ($different.Count -gt 0) {
    $L.Add('## Content differs')
    $L.Add('')
    $L.Add('| Path | Live size | GitHub size |')
    $L.Add('|---|---|---|')
    foreach ($e in $different) { $L.Add("| ``$($e.path)`` | $($e.liveSize) | $($e.gitHubSize) |") }
    $L.Add('')
}
if ($onlyGitHub.Count -gt 0) {
    $L.Add('## Only in GitHub, absent live')
    $L.Add('')
    foreach ($p in ($onlyGitHub | Sort-Object)) { $L.Add("- ``$p``") }
    $L.Add('')
}
$L.Add('## Exclusions and failures')
$L.Add('')
if ($hubExists) {
    $L.Add('**Safety-pruned** (never entered, STATE.md B-2):')
    $L.Add('')
    if (@($trav.prunedForSafety).Count -gt 0) { foreach ($p in $trav.prunedForSafety) { $L.Add("- ``$p``") } } else { $L.Add('- none found') }
    $L.Add('')
    $L.Add('**Noise-pruned** (never entered, not safety-critical):')
    $L.Add('')
    if (@($trav.prunedForNoise).Count -gt 0) { foreach ($p in $trav.prunedForNoise) { $L.Add("- ``$p``") } } else { $L.Add('- none found') }
    $L.Add('')
    $L.Add('**Not traversed -- reparse points, file and directory** (junction, symlink, mount).')
    $L.Add('Detected by attribute before the directory/file split, so neither an alias nor a')
    $L.Add('file link can bypass the name-based rule. Never returned, never hashed. Targets')
    $L.Add('are not inventoried:')
    $L.Add('')
    if (@($trav.untraversedReparsePoints).Count -gt 0) { foreach ($rp in $trav.untraversedReparsePoints) { $L.Add("- ``$($rp.path)`` [$($rp.kind)] -- $($rp.note)") } } else { $L.Add('- none found') }
    $L.Add('')
    $L.Add('**Traversal failures** (could not enumerate; forces INCOMPLETE):')
    $L.Add('')
    if (@($trav.traversalFailures).Count -gt 0) { foreach ($tf in $trav.traversalFailures) { $L.Add("- ``$($tf.path)`` -- $($tf.reason)") } } else { $L.Add('- none')
    }
    $L.Add('')
    $L.Add('**Depth-limited** (not descended; forces INCOMPLETE):')
    $L.Add('')
    if (@($trav.depthLimited).Count -gt 0) { foreach ($dl in $trav.depthLimited) { $L.Add("- ``$($dl.path)`` -- $($dl.note)") } } else { $L.Add('- none') }
    $L.Add('')
    $L.Add("**Item cap reached:** $($trav.truncated)")
} else {
    $L.Add('Not applicable: live Hub not found at the resolved path.')
}
$L.Add('')
$L.Add('## design-systems\.remember')
$L.Add('')
$L.Add("Exists: $($rememberFact.exists)")
$L.Add('')
$L.Add('Contents inspected: false')
$L.Add('')
$L.Add('Nothing inside was read, hashed, enumerated, or counted. Existence was established')
$L.Add('while listing the parent directory. Stop condition B-2 in `STATE.md`.')
$L.Add('')
$L.Add('### Pre-descent pruning proof')
$L.Add('')
if ($hubExists) {
    $L.Add("- Safety-pruned directories: $(@($trav.prunedForSafety).Count)")
    foreach ($p in $trav.prunedForSafety) { $L.Add("  - ``$p`` -- identified while listing its parent; never entered") }
    $L.Add("- Directories actually passed to Get-ChildItem: $($pruneProof.visitedDirectoryCount)")
    $L.Add("- Violations (visited at or beneath a pruned directory): $(@($pruneProof.violations).Count)")
    $L.Add("- Verdict: **$(if ($pruneProof.pass) { 'PASS' } else { 'FAIL' })**")
} else {
    $L.Add('- Not applicable: live Hub not found at the resolved path.')
}
$L.Add('')
$L.Add('## Explicitly NOT verified')
$L.Add('')
foreach ($u in $R.unverified) { $L.Add("- $u") }
($L -join "`r`n") | Set-Content -LiteralPath $mdPath -Encoding UTF8

Write-Host ''
Write-Host "  JSON : $jsonPath"
Write-Host "  MD   : $mdPath"
Write-Host ''
if ($travComplete -eq 'COMPLETE') {
    Write-Host 'INVENTORY WRITTEN -- Completeness: COMPLETE. No system changes were made.' -ForegroundColor Green
    Write-Host 'Commit both files to workspace-governor.' -ForegroundColor Yellow
    exit 0
} else {
    Write-Host 'INVENTORY WRITTEN -- Completeness: INCOMPLETE.' -ForegroundColor Red
    Write-Host 'Part of the accessible Hub tree was skipped. The reports say so explicitly.' -ForegroundColor Red
    Write-Host 'Do not use this as the reconciliation input until the cause is resolved.' -ForegroundColor Red
    exit 2
}
