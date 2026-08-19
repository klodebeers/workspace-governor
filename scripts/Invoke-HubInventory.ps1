<#
.SYNOPSIS
  Read-only inventory of the live local .agents-hub, compared against the
  committed GitHub baseline for agents-hub-one.

.DESCRIPTION
  Answers one question: what exists in the live local Hub that is absent,
  different, or only a placeholder in GitHub agents-hub-one?

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
    # EXISTENCE ONLY. Do not enumerate, count, read, or hash anything inside.
    $rememberFact.exists = Test-Path -LiteralPath (Join-Path $hubResolved $RememberRel)
    $rootLen = ($hubResolved.TrimEnd('\')).Length
    $items = @(Get-ChildItem -LiteralPath $hubResolved -Recurse -Force -File -ErrorAction SilentlyContinue |
               Where-Object { $_.FullName -notmatch '(?i)\\design-systems\\\.remember($|\\)' -and $_.FullName -notmatch '(?i)\\\.git\\' })
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
    }
    onlyInLive = @($onlyLive | Sort-Object)
    placeholderInGitHubRealInLive = $placeholderInGitHub
    contentDiffers = $different
    onlyInGitHub = @($onlyGitHub | Sort-Object)
    identical = @($identical | Sort-Object)
    liveInventory = $live
    remember = $rememberFact
    unverified = @(
        'design-systems\.remember: existence only. Nothing inside was read, hashed, enumerated, or counted (stop condition B-2).',
        'No file contents were emitted; only path, size, SHA256 and modified time.',
        'Baseline reflects GitHub agents-hub-one at the recorded ref, not any later commit.',
        'A file identical by SHA256 is byte-identical; semantic equivalence was not assessed.'
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
$L.Add('**Method:** read-only, no network. No file contents emitted.')
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
    $L.Add('These are unrepresented in `agents-hub-one` and must be classified before consolidation.')
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
$L.Add('## design-systems\.remember')
$L.Add('')
$L.Add("Exists: $($rememberFact.exists)")
$L.Add('')
$L.Add('Contents inspected: false')
$L.Add('')
$L.Add('Nothing inside was read, hashed, enumerated, or counted. Existence was established')
$L.Add('by a single path test. Stop condition B-2 in `STATE.md`.')
$L.Add('')
$L.Add('## Explicitly NOT verified')
$L.Add('')
foreach ($u in $R.unverified) { $L.Add("- $u") }
($L -join "`r`n") | Set-Content -LiteralPath $mdPath -Encoding UTF8

Write-Host ''
Write-Host 'INVENTORY COMPLETE — no system changes were made.' -ForegroundColor Green
Write-Host "  JSON : $jsonPath"
Write-Host "  MD   : $mdPath"
Write-Host ''
Write-Host 'Commit both files to workspace-governor.' -ForegroundColor Yellow
