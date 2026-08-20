<#
.SYNOPSIS
  Read-only evidence collection for section 5 of the MCP Gateway directive.

.DESCRIPTION
  Collects an evidence-based current-state map of the local coding-agent
  environment. Emits machine-readable JSON and a human-readable Markdown
  report suitable for committing to the workspace-governor repository.

  SAFETY CONTRACT. This script:
    - performs NO writes anywhere except the files it emits into -OutDir
    - never installs, modifies, deletes, moves, renames, reconfigures or repairs
    - never emits a secret VALUE; records names, locations and metadata only
    - does not read or hash 'design-systems\.remember' contents (unresolved
      provenance and sensitivity hold in Workspace Governor STATE.md); records
      existence only; never enumerated, counted, read, or hashed
    - reports "not found" instead of failing when a path is absent
    - makes no network calls

  This is evidence collection only. It performs no analysis and proposes
  no changes.

.PARAMETER HubPath
  Canonical Agent Hub. Default: $env:USERPROFILE\.agents-hub

.PARAMETER WorkspaceRoot
  Governed workspace root. Default: C:\KloWorkspaces

.PARAMETER OutDir
  Output directory. Default: .\evidence

.EXAMPLE
  .\Invoke-GatewayDiscovery.ps1
#>

[CmdletBinding()]
param(
    # Candidate location of the canonical .agents-hub. It may not exist: the
    # canonical Hub is the OUTPUT of consolidating agents-hub-one and
    # agents-hub-two, not a precondition of discovery (DECISIONS.md D-02, D-05,
    # D-06). Absence is a valid, reportable state, not an error.
    [string]$HubPath       = (Join-Path $env:USERPROFILE '.agents-hub'),

    # Pre-consolidation source repositories. Inventoried when the canonical Hub
    # is absent, so discovery still describes reality instead of returning
    # empty hub-derived results.
    [string[]]$SourceRepoPaths = @(),

    [string]$WorkspaceRoot = 'C:\KloWorkspaces',
    [string]$OutDir        = (Join-Path (Get-Location) 'evidence')
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

# ============================================================================
# REDACTION
# ============================================================================
$SensitiveKeyPattern = '(?i)(token|secret|password|passwd|pwd|api[-_]?key|apikey|auth|bearer|credential|private[-_]?key|client[-_]?secret|connection[-_]?string|sas|signature|cookie|session)'
$SecretShapePatterns = @(
    '^sk-[A-Za-z0-9_\-]{16,}',
    '^gh[pousr]_[A-Za-z0-9]{16,}',
    '^ntn_[A-Za-z0-9]{16,}',
    '^xox[baprs]-',
    '^ey[A-Za-z0-9_\-]{10,}\.',
    '^[A-Za-z0-9+/]{40,}={0,2}$',
    '^[0-9a-fA-F]{40,}$'
)

function Test-LooksSecret {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) { return $false }
    foreach ($p in $SecretShapePatterns) { if ($Value -match $p) { return $true } }
    return $false
}

function Protect-Value {
    param([string]$Key, $Value)
    if ($null -eq $Value) { return $null }
    if ($Value -is [bool] -or $Value -is [int] -or $Value -is [long] -or $Value -is [double]) { return $Value }
    $s = [string]$Value
    if ($Key -match $SensitiveKeyPattern) { return '[REDACTED:key-name]' }
    if (Test-LooksSecret -Value $s)       { return '[REDACTED:value-shape]' }
    if ($s -match '^[a-zA-Z][a-zA-Z0-9+.\-]*://[^/@]*:[^/@]*@') {
        return ($s -replace '://[^/@]*:[^/@]*@', '://[REDACTED:userinfo]@')
    }
    if ($s.Length -gt 400) { return $s.Substring(0,400) + '...[truncated]' }
    return $s
}

function ConvertTo-SafeTree {
    param($Node, [int]$Depth = 0, [string]$KeyName = '')
    if ($Depth -gt 6) { return '[depth-limit]' }
    if ($null -eq $Node) { return $null }
    if ($Node -is [System.Management.Automation.PSCustomObject]) {
        $o = [ordered]@{}
        foreach ($p in $Node.PSObject.Properties) {
            $o[$p.Name] = ConvertTo-SafeTree -Node $p.Value -Depth ($Depth+1) -KeyName $p.Name
        }
        return $o
    }
    if ($Node -is [System.Collections.IDictionary]) {
        $o = [ordered]@{}
        foreach ($k in $Node.Keys) {
            $o[[string]$k] = ConvertTo-SafeTree -Node $Node[$k] -Depth ($Depth+1) -KeyName ([string]$k)
        }
        return $o
    }
    if ($Node -is [System.Collections.IEnumerable] -and $Node -isnot [string]) {
        $a = @(); foreach ($i in $Node) { $a += ,(ConvertTo-SafeTree -Node $i -Depth ($Depth+1) -KeyName $KeyName) }
        return $a
    }
    return (Protect-Value -Key $KeyName -Value $Node)
}

# ============================================================================
# READ-ONLY INSPECTION HELPERS
# ============================================================================
$script:RememberGuard = '(?i)\\design-systems\\\.remember($|\\)'

function Get-PathFact {
    param([string]$Path, [switch]$Hash)
    $r = [ordered]@{ path=$Path; exists=$false; type=$null; sizeBytes=$null; modifiedUtc=$null; sha256=$null }
    if ([string]::IsNullOrWhiteSpace($Path)) { return $r }
    if (-not (Test-Path -LiteralPath $Path)) { return $r }
    $i = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if ($null -eq $i) { return $r }
    $r.exists = $true
    $r.type = if ($i.PSIsContainer) { 'directory' } else { 'file' }
    $r.modifiedUtc = $i.LastWriteTimeUtc.ToString('o')
    if (-not $i.PSIsContainer) {
        $r.sizeBytes = $i.Length
        if ($Hash -and ($Path -notmatch $script:RememberGuard)) {
            $h = Get-FileHash -LiteralPath $Path -Algorithm SHA256 -ErrorAction SilentlyContinue
            if ($h) { $r.sha256 = $h.Hash }
        }
    }
    return $r
}

function Get-SafeJsonFile {
    param([string]$Path)
    $o = [ordered]@{ file=(Get-PathFact -Path $Path -Hash); parsed=$null; parseError=$null }
    if (-not $o.file.exists) { return $o }
    try {
        $raw = Get-Content -LiteralPath $Path -Raw -ErrorAction Stop
        $o.parsed = ConvertTo-SafeTree -Node ($raw | ConvertFrom-Json -ErrorAction Stop)
    } catch { $o.parseError = $_.Exception.Message }
    return $o
}

function Get-SafeTextFile {
    param([string]$Path, [int]$MaxLines = 250)
    $o = [ordered]@{ file=(Get-PathFact -Path $Path -Hash); lines=@(); truncated=$false; readError=$null }
    if (-not $o.file.exists) { return $o }
    try {
        $all = @(Get-Content -LiteralPath $Path -ErrorAction Stop)
        if ($all.Count -gt $MaxLines) { $o.truncated = $true; $all = $all[0..($MaxLines-1)] }
        $safe = @()
        foreach ($line in $all) {
            $k = ''
            if ($line -match '^\s*([A-Za-z0-9_\-\.\[\]"]+)\s*[:=]') { $k = $Matches[1] }
            if ($k -and ($k -match $SensitiveKeyPattern)) { $safe += ($k + ' = [REDACTED:key-name]') }
            elseif (Test-LooksSecret -Value $line.Trim()) { $safe += '[REDACTED:line-shape]' }
            else { $safe += $line }
        }
        $o.lines = $safe
    } catch { $o.readError = $_.Exception.Message }
    return $o
}

function Get-TreeInventory {
    param([string]$Root, [int]$MaxDepth = 3, [int]$MaxItems = 500)
    $r = [ordered]@{ root=$Root; exists=$false; items=@(); itemCount=0; truncated=$false; skipped=@() }
    if ([string]::IsNullOrWhiteSpace($Root) -or -not (Test-Path -LiteralPath $Root)) { return $r }
    $r.exists = $true
    $rootLen = ($Root.TrimEnd('\')).Length
    # Pre-descent pruning. Protected directories are never passed to Get-ChildItem.
    $trav = Get-SafeChildItems -Root $Root -MaxDepth $MaxDepth -MaxItems $MaxItems
    foreach ($p in $trav.prunedForSafety) {
        $r.skipped += "$p (stop condition B-2: existence recorded, never entered)"
    }
    $r.truncated = $trav.truncated
    $all = $trav.items
    $n = 0
    foreach ($e in $all) {
        if ($n -ge $MaxItems) { $r.truncated = $true; break }
        $r.items += [ordered]@{
            rel  = $e.FullName.Substring($rootLen).TrimStart('\')
            type = if ($e.PSIsContainer) { 'dir' } else { 'file' }
            size = if ($e.PSIsContainer) { $null } else { $e.Length }
        }
        $n++
    }
    $r.itemCount = $n
    return $r
}

function Get-CommandFact {
    param([string]$Name, [string]$VersionArg = '--version')
    $r = [ordered]@{ name=$Name; present=$false; source=$null; version=$null }
    $c = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $c) { return $r }
    $r.present = $true
    $r.source = if ($c.Source) { $c.Source } else { $c.Name }
    try { $r.version = (& $Name $VersionArg 2>$null | Select-Object -First 1) } catch { $r.version = $null }
    return $r
}

function Get-GitRepoFact {
    param([string]$Path)
    $r = [ordered]@{ path=$Path; exists=(Test-Path -LiteralPath $Path); isGitRepo=$false; remoteOrigin=$null; branch=$null; headShort=$null }
    if (-not $r.exists) { return $r }
    if (-not (Test-Path -LiteralPath (Join-Path $Path '.git'))) { return $r }
    $r.isGitRepo = $true
    try { $r.remoteOrigin = (& git -C $Path config --get remote.origin.url 2>$null | Select-Object -First 1) } catch {}
    try { $r.branch       = (& git -C $Path rev-parse --abbrev-ref HEAD 2>$null | Select-Object -First 1) } catch {}
    try { $r.headShort    = (& git -C $Path rev-parse --short HEAD 2>$null | Select-Object -First 1) } catch {}
    return $r
}

# ============================================================================
# REPORT
# ============================================================================
# ============================================================================
# HUB STATE. Determined first, because most sections below are only meaningful
# if a canonical Hub exists. Where it does not, those sections report
# applicable = false with a reason, rather than an empty result that would read
# as "nothing found". Absence from tool output is not evidence of absence
# (AGENTS.md, Evidence standard).
# ============================================================================
$hubPresent = Test-Path -LiteralPath $HubPath
$hubHasRules = $false
if ($hubPresent) { $hubHasRules = Test-Path -LiteralPath (Join-Path $HubPath 'rules') }

$resolvedSources = @()
if (@($SourceRepoPaths).Count -gt 0) {
    foreach ($sp in $SourceRepoPaths) { if (Test-Path -LiteralPath $sp) { $resolvedSources += $sp } }
} else {
    foreach ($n in @('agents-hub-one','agents-hub-two')) {
        $cand = Join-Path $WorkspaceRoot $n
        if (Test-Path -LiteralPath $cand) { $resolvedSources += $cand }
    }
}

$hubState =
    if ($hubPresent -and $hubHasRules) { 'PRESENT' }
    elseif ($hubPresent) { 'PRESENT_WITHOUT_RULES' }
    elseif (@($resolvedSources).Count -gt 0) { 'ABSENT_PRE_CONSOLIDATION_SOURCES_FOUND' }
    else { 'ABSENT' }

$hubAbsentReason = 'The canonical .agents-hub does not exist at the supplied path. It is the output of consolidating agents-hub-one and agents-hub-two (DECISIONS.md D-02, D-05). Hub-derived findings are therefore not applicable, not empty.'

# Roots to scan. When the canonical Hub is absent its path contributes nothing,
# so the pre-consolidation sources stand in.
#
# The source repositories normally live INSIDE the workspace root, so the roots
# overlap and the same file is reachable by two paths. Roots are deliberately
# NOT collapsed to the outermost one: depth limits are measured per root, and
# collapsing would silently drop files that are within depth of a source root
# but beyond depth of the workspace root. Instead the overlap is disclosed and
# findings are deduplicated by canonical full path before any count is reported.
$scanRoots = @()
if ($hubPresent) { $scanRoots += $HubPath } else { $scanRoots += $resolvedSources }
$scanRoots += $WorkspaceRoot
$scanRootsResolved = @()
# Loop variable is named $scanRoot, not $r. PowerShell variable names are
# case-insensitive, so a file-scope $r and the result object $R are the same
# variable; a leaked $r would silently overwrite $R.
foreach ($scanRoot in $scanRoots) {
    if ([string]::IsNullOrWhiteSpace($scanRoot)) { continue }
    if (-not (Test-Path -LiteralPath $scanRoot)) { continue }
    try { $scanRootsResolved += (Resolve-Path -LiteralPath $scanRoot).Path } catch { $scanRootsResolved += $scanRoot }
}
$scanRoots = @($scanRootsResolved | Select-Object -Unique)

# Which roots contain which. Recorded so a reader knows counts were deduplicated.
$rootOverlaps = @()
foreach ($a in $scanRoots) {
    foreach ($b in $scanRoots) {
        if ($a -eq $b) { continue }
        $pref = $b.TrimEnd('\') + '\'
        if ($a.StartsWith($pref, [System.StringComparison]::OrdinalIgnoreCase)) {
            $rootOverlaps += [ordered]@{ inner = $a; outer = $b }
        }
    }
}

function Select-UniqueByFullName {
    <#
    .SYNOPSIS
      Deduplicates filesystem findings by canonical full path, case-insensitively.
    .DESCRIPTION
      Overlapping scan roots return the same file more than once. Counts must be
      reported over distinct paths, not distinct discoveries.
    #>
    param($Items)
    $seen = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
    $out = @()
    foreach ($i in $Items) {
        if ($null -eq $i) { continue }
        $fn = $null
        if ($i.PSObject.Properties['FullName']) { $fn = $i.FullName }
        elseif ($i.PSObject.Properties['path']) { $fn = $i.path }
        if ([string]::IsNullOrWhiteSpace($fn)) { continue }
        if ($seen.Add($fn)) { $out += $i }
    }
    return @($out)
}

Write-Host ("  hub state    : {0}" -f $hubState) -ForegroundColor $(if ($hubState -eq 'PRESENT') { 'Green' } else { 'Yellow' })
Write-Host ("  hub path     : {0}" -f $HubPath)
if (-not $hubPresent) {
    Write-Host '  NOTE: canonical Hub absent. Hub-derived sections report not-applicable.' -ForegroundColor Yellow
    foreach ($sp in $resolvedSources) { Write-Host ("    pre-consolidation source: {0}" -f $sp) -ForegroundColor Yellow }
}
Write-Host ''

$R = [ordered]@{
    meta = [ordered]@{
        generatedUtc  = $stampISO
        script        = 'Invoke-GatewayDiscovery.ps1'
        schemaVersion = '1.1'
        directive     = 'mcp-gateway section 5 -- Discovery. Evidence collection only.'
        readOnly      = $true
        networkCalls  = $false
        secretsPolicy = 'names, locations and configuration metadata only; values never collected'
        hubPath       = $HubPath
        hubState      = $hubState
        hubPresupposed = $false
        workspaceRoot = $WorkspaceRoot
        machine       = $env:COMPUTERNAME
    }
}

# Hub state is recorded as the first section, AFTER $R exists. Computing it
# earlier is required because meta reads $hubState. Assigning into $R before
# this point failed at runtime and was then discarded when $R was rebuilt: the
# name was not empty but held a leaked file-scope loop value of the wrong type,
# so the indexed assignment could not be applied.
$R['00_hubState'] = [ordered]@{
    hubPath = $HubPath
    hubPresent = $hubPresent
    hubHasRulesDirectory = $hubHasRules
    hubState = $hubState
    preConsolidationSources = @($resolvedSources)
    scanRoots = @($scanRoots)
    scanRootOverlaps = @($rootOverlaps)
    deduplicationNote = 'Scan roots overlap where a source repository lives inside the workspace root. Findings are deduplicated by canonical full path before any count is reported.'
    interpretation = if ($hubPresent) { 'Canonical Hub present at the supplied path.' } else { $hubAbsentReason }
    note = 'Discovery does not presuppose the canonical Hub exists. Sections whose meaning depends on it carry an applicable flag.'
}
Write-Host '=== MCP Gateway Discovery -- read-only evidence collection ===' -ForegroundColor Cyan

# --- 1. .agents-hub location and structure ----------------------------------
Write-Host '[ 1/14] .agents-hub location and structure'
$R['01_agentsHub'] = [ordered]@{
    canonicalHubApplicable = $hubPresent
    notApplicableReason = if ($hubPresent) { $null } else { $hubAbsentReason }
    hubState  = $hubState
    canonicalHub = [ordered]@{
    hub       = Get-PathFact -Path $HubPath
    inventory = Get-TreeInventory -Root $HubPath -MaxDepth 3
    rootFiles = [ordered]@{
        'README.md'  = Get-PathFact -Path (Join-Path $HubPath 'README.md')  -Hash
        'CATALOG.md' = Get-PathFact -Path (Join-Path $HubPath 'CATALOG.md') -Hash
        'STATE.md'   = Get-PathFact -Path (Join-Path $HubPath 'STATE.md')   -Hash
        'AGENTS.md'  = Get-PathFact -Path (Join-Path $HubPath 'AGENTS.md')  -Hash
    }
    rulesDir = Get-TreeInventory -Root (Join-Path $HubPath 'rules') -MaxDepth 1
    rememberExists = (Test-Path -LiteralPath (Join-Path $HubPath 'design-systems\.remember'))
    rememberContentsInspected = $false
    rememberNote = 'Existence only. Nothing inside was enumerated, counted, read, or hashed, per STATE.md stop condition B-2.'
    }
    preConsolidationInspectionAttempted = (-not $hubPresent)
    preConsolidationSourcesFound = if ($hubPresent) { 0 } else { @($resolvedSources).Count }
    preConsolidationSources = if ($hubPresent) { @() } else {
        $si = @()
        foreach ($sp in $resolvedSources) {
            $si += [ordered]@{
                path = $sp
                inventory = Get-TreeInventory -Root $sp -MaxDepth 3
                rulesDir = Get-TreeInventory -Root (Join-Path $sp 'rules') -MaxDepth 1
            }
        }
        $si
    }
    semanticNote = 'canonicalHub describes the canonical .agents-hub only. Source-repository findings are never substituted into it; they live under preConsolidationSources.'
}

# --- 2. Claude Code configuration and native controls -----------------------
Write-Host '[ 2/14] Claude Code configuration and native controls'
$R['02_claudeCode'] = [ordered]@{
    cli            = Get-CommandFact -Name 'claude'
    dir            = Get-TreeInventory -Root (Join-Path $env:USERPROFILE '.claude') -MaxDepth 2
    globalClaudeMd = Get-PathFact -Path (Join-Path $env:USERPROFILE '.claude\CLAUDE.md') -Hash
    settings       = Get-SafeJsonFile -Path (Join-Path $env:USERPROFILE '.claude\settings.json')
    settingsLocal  = Get-SafeJsonFile -Path (Join-Path $env:USERPROFILE '.claude\settings.local.json')
    projectConfig  = Get-SafeJsonFile -Path (Join-Path $env:USERPROFILE '.claude.json')
    appDataDir     = Get-PathFact -Path (Join-Path $env:APPDATA 'Claude')
    nativeControlNote = 'permissions allow/ask/deny rules and sandbox settings are runtime-native controls outside Gateway authority (directive section 4)'
}

# --- 3. Codex configuration and native controls -----------------------------
Write-Host '[ 3/14] Codex configuration and native controls'
$R['03_codex'] = [ordered]@{
    cli            = Get-CommandFact -Name 'codex'
    dir            = Get-TreeInventory -Root (Join-Path $env:USERPROFILE '.codex') -MaxDepth 2
    configToml     = Get-SafeTextFile -Path (Join-Path $env:USERPROFILE '.codex\config.toml') -MaxLines 300
    agentsMd       = Get-SafeTextFile -Path (Join-Path $env:USERPROFILE '.codex\AGENTS.md') -MaxLines 300
    agentsOverride = Get-PathFact -Path (Join-Path $env:USERPROFILE '.codex\AGENTS.override.md') -Hash
    stalePathScan  = @()
    stalePathNote  = 'Workspace Governor STATE.md records an ACTIVE governance conflict: stale absolute paths in the Codex authority file blocking adapter activation. This scan locates them; it does not fix them.'
}
$codexAgents = Join-Path $env:USERPROFILE '.codex\AGENTS.md'
if (Test-Path -LiteralPath $codexAgents) {
    $hits = @(Select-String -LiteralPath $codexAgents -Pattern 'C:\\Users\\[A-Za-z0-9._-]+','C:\\Workspace' -AllMatches -ErrorAction SilentlyContinue)
    foreach ($h in $hits) { $R['03_codex'].stalePathScan += [ordered]@{ line=$h.LineNumber; match=$h.Matches[0].Value } }
}

# --- 4. Existing MCP configurations -----------------------------------------
Write-Host '[ 4/14] existing MCP configurations'
$claudeMcp = @()
foreach ($src in @($R['02_claudeCode'].projectConfig, $R['02_claudeCode'].settings, $R['02_claudeCode'].settingsLocal)) {
    if ($src -and $src.parsed) {
        foreach ($top in @('mcpServers','mcp_servers')) {
            if ($src.parsed[$top]) { foreach ($k in $src.parsed[$top].Keys) { $claudeMcp += $k } }
        }
    }
}
$codexMcp = @()
$codexToml = Join-Path $env:USERPROFILE '.codex\config.toml'
if (Test-Path -LiteralPath $codexToml) {
    $m = @(Select-String -LiteralPath $codexToml -Pattern '^\s*\[mcp_servers\.([^\]]+)\]' -AllMatches -ErrorAction SilentlyContinue)
    foreach ($x in $m) { $codexMcp += $x.Matches[0].Groups[1].Value }
}
$R['04_mcpConfigurations'] = [ordered]@{
    claudeServerNames = @($claudeMcp | Sort-Object -Unique)
    codexServerNames  = @($codexMcp  | Sort-Object -Unique)
    claudeRawRedacted = if ($R['02_claudeCode'].projectConfig.parsed) { $R['02_claudeCode'].projectConfig.parsed['mcpServers'] } else { $null }
    note = 'Server names and redacted configuration metadata only. Any token or header value is redacted.'
}

# --- 5. PATH and environment entries relevant to coding agents --------------
Write-Host '[ 5/14] PATH and environment entries relevant to coding agents'
$agentPathPattern = '(?i)(node|npm|nvm|python|pip|git|claude|codex|anthropic|openai|pnpm|yarn|bun|deno|\.local\\bin|AppData\\Roaming\\npm)'
$pathEntries = @()
foreach ($p in ($env:PATH -split ';')) {
    if ([string]::IsNullOrWhiteSpace($p)) { continue }
    $pathEntries += [ordered]@{
        entry = $p
        exists = (Test-Path -LiteralPath $p)
        agentRelevant = [bool]($p -match $agentPathPattern)
    }
}
$agentEnvPattern = '(?i)^(ANTHROPIC_|CLAUDE_|CODEX_|OPENAI_|MCP_|NODE_|NPM_|PYTHON|PIP_|GIT_|PATHEXT$|PATH$)'
$envRelevant = @()
foreach ($e in @(Get-ChildItem Env: -ErrorAction SilentlyContinue)) {
    if ($e.Name -match $agentEnvPattern) {
        $envRelevant += [ordered]@{
            name = $e.Name
            value = (Protect-Value -Key $e.Name -Value $e.Value)
            valuePresent = -not [string]::IsNullOrWhiteSpace($e.Value)
        }
    }
}
$R['05_pathAndEnvironment'] = [ordered]@{
    pathEntryCount = $pathEntries.Count
    pathEntries = $pathEntries
    agentRelevantPathCount = @($pathEntries | Where-Object { $_.agentRelevant }).Count
    relevantEnvVars = $envRelevant
    note = 'Values redacted where the name or shape indicates a credential.'
}

# --- 6. Installed / runtime dependencies relevant to the Gateway ------------
Write-Host '[ 6/14] installed and runtime dependencies'
$R['06_runtimeDependencies'] = [ordered]@{
    os        = [ordered]@{
        caption   = [string](Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue).Caption
        version   = [string][System.Environment]::OSVersion.Version
        is64Bit   = [System.Environment]::Is64BitOperatingSystem
    }
    powershell = [ordered]@{ version=[string]$PSVersionTable.PSVersion; edition=[string]$PSVersionTable.PSEdition }
    commands  = @(
        (Get-CommandFact -Name 'node'),
        (Get-CommandFact -Name 'npm'),
        (Get-CommandFact -Name 'npx'),
        (Get-CommandFact -Name 'pnpm'),
        (Get-CommandFact -Name 'yarn'),
        (Get-CommandFact -Name 'python'),
        (Get-CommandFact -Name 'pip'),
        (Get-CommandFact -Name 'git'),
        (Get-CommandFact -Name 'docker'),
        (Get-CommandFact -Name 'uv')
    )
    globalNpmPackages = (& { try { @(& npm ls -g --depth=0 2>$null) } catch { @() } })
    pipPackages       = (& { try { @(& pip list --disable-pip-version-check 2>$null | Select-Object -First 60) } catch { @() } })
    note = 'Read-only queries. Directive section 27 requires Node.js/TypeScript or Python, no Docker requirement, and clean operation on this Windows environment.'
}

# --- 7. Shared assets and tool registries -----------------------------------
Write-Host '[ 7/14] shared assets and tool registries'
$regPatterns = @('CATALOG.md','agent-registry.json','registry.json','catalog.json','package-layout.json','*.schema.json')

# Canonical Hub registries. Populated ONLY from the canonical Hub. Empty and
# not-applicable when the Hub is absent -- never backfilled from a source repo.
$regHub = @()
if ($hubPresent) {
    foreach ($n in $regPatterns) {
        foreach ($f in @((Get-SafeChildItems -Root $HubPath -MaxDepth 3 -FilesOnly -Filter $n).items)) {
            $regHub += (Get-PathFact -Path $f.FullName -Hash)
        }
    }
}
$regHub = Select-UniqueByFullName -Items $regHub

# Pre-consolidation source registries. A separate field with separate semantics.
$regSrc = @()
if (-not $hubPresent) {
    foreach ($sp in $resolvedSources) {
        foreach ($n in $regPatterns) {
            foreach ($f in @((Get-SafeChildItems -Root $sp -MaxDepth 3 -FilesOnly -Filter $n).items)) {
                $regSrc += (Get-PathFact -Path $f.FullName -Hash)
            }
        }
    }
}
$regSrc = Select-UniqueByFullName -Items $regSrc

$R['07_sharedAssetsAndRegistries'] = [ordered]@{
    canonicalHubApplicable = $hubPresent
    notApplicableReason = if ($hubPresent) { $null } else { $hubAbsentReason }
    canonicalHubSearchedRoots = if ($hubPresent) { @($HubPath) } else { @() }
    canonicalHubRegistryCandidates = $regHub
    canonicalHubRegistryCount = @($regHub).Count
    canonicalHubTemplatesDir = if ($hubPresent) { Get-TreeInventory -Root (Join-Path $HubPath 'templates') -MaxDepth 2 } else { $null }
    canonicalHubSkillsDir    = if ($hubPresent) { Get-TreeInventory -Root (Join-Path $HubPath 'skills') -MaxDepth 2 } else { $null }
    canonicalHubAgentsDir    = if ($hubPresent) { Get-TreeInventory -Root (Join-Path $HubPath 'agents') -MaxDepth 2 } else { $null }
    preConsolidationInspectionAttempted = (-not $hubPresent)
    preConsolidationSourcesFound = if ($hubPresent) { 0 } else { @($resolvedSources).Count }
    preConsolidationSearchedRoots = if ($hubPresent) { @() } else { @($resolvedSources) }
    preConsolidationRegistryCandidates = $regSrc
    preConsolidationRegistryCount = @($regSrc).Count
    semanticNote = 'A canonicalHub* count of 0 with canonicalHubApplicable false means the canonical Hub does not exist, not that no registries exist anywhere. Source findings are reported separately and are never merged into the canonical fields.'
}

# --- 8. Scripts and APIs potentially relevant for exposure ------------------
Write-Host '[ 8/14] candidate scripts and APIs for exposure'
$sc = @()
foreach ($root in $scanRoots) {
    if (-not (Test-Path -LiteralPath $root)) { continue }
    foreach ($ext in @('*.ps1','*.py','*.js','*.mjs','*.ts','*.cmd','*.bat','*.sh')) {
        $found = @((Get-SafeChildItems -Root $root -MaxDepth 3 -FilesOnly -Filter $ext).items)
        foreach ($f in $found) { $sc += [ordered]@{ path=$f.FullName; ext=$f.Extension; size=$f.Length } }
    }
}
$sc = Select-UniqueByFullName -Items $sc
$R['08_scriptsAndApis'] = [ordered]@{
    applicable = $true
    hubIncludedInSearch = $hubPresent
    searchedRoots = @($scanRoots)
    scanRootOverlaps = @($rootOverlaps)
    deduplicatedByFullPath = $true
    candidates = $sc
    count = @($sc).Count
    note = 'Inventory only. No script was executed. When the canonical Hub is absent its path contributes nothing and the pre-consolidation sources are searched instead.'
}

# --- 9. Authentication and secrets mechanisms (no values) ------------------
Write-Host '[ 9/14] authentication and secrets mechanisms (names and locations only)'
$envSecretNames = @()
foreach ($e in @(Get-ChildItem Env: -ErrorAction SilentlyContinue)) {
    if ($e.Name -match $SensitiveKeyPattern) {
        $envSecretNames += [ordered]@{ name=$e.Name; valuePresent=(-not [string]::IsNullOrWhiteSpace($e.Value)); length=([string]$e.Value).Length; value='[NOT COLLECTED]' }
    }
}
$dotenv = @()
foreach ($root in $scanRoots) {
    if (-not (Test-Path -LiteralPath $root)) { continue }
    $found = @((Get-SafeChildItems -Root $root -MaxDepth 3 -FilesOnly).items | Where-Object { $_.Name -match '^\.env' })
    foreach ($f in $found) { $dotenv += [ordered]@{ path=$f.FullName; size=$f.Length; contentsRead=$false } }
}
$credFiles = @()
foreach ($c in @(
    (Join-Path $env:USERPROFILE '.claude\.credentials.json'),
    (Join-Path $env:USERPROFILE '.codex\auth.json'),
    (Join-Path $env:USERPROFILE '.config\anthropic')
)) { $f = Get-PathFact -Path $c; $f['contentsRead'] = $false; $credFiles += $f }
$dotenv = Select-UniqueByFullName -Items $dotenv
$R['09_authAndSecrets'] = [ordered]@{
    applicable = $true
    hubIncludedInSearch = $hubPresent
    searchedRoots = @($scanRoots)
    scanRootOverlaps = @($rootOverlaps)
    deduplicatedByFullPath = $true
    sensitiveEnvVarNames = $envSecretNames
    dotEnvFiles = $dotenv
    credentialStoreLocations = $credFiles
    windowsCredentialManager = 'not enumerated by this script; run "cmdkey /list" manually if an inventory is required'
    note = 'No secret value was read, printed, or written. Directive section 16 requires documenting secret references, not values. Credential file existence recorded; contents never opened.'
}

# --- 10. Audit and logging mechanisms --------------------------------------
Write-Host '[10/14] audit and logging mechanisms'
$logsHub = @()
if ($hubPresent) {
    foreach ($c in @((Join-Path $HubPath 'audit'), (Join-Path $HubPath 'logs'))) { $logsHub += (Get-PathFact -Path $c) }
}
$logsRuntime = @()
foreach ($c in @(
    (Join-Path $env:USERPROFILE '.claude\logs'), (Join-Path $env:USERPROFILE '.claude\history'),
    (Join-Path $env:USERPROFILE '.codex\log'), (Join-Path $env:USERPROFILE '.codex\logs'),
    (Join-Path $env:USERPROFILE '.codex\sessions')
)) { $logsRuntime += (Get-PathFact -Path $c) }
$R['10_auditAndLogging'] = [ordered]@{
    canonicalHubApplicable = $hubPresent
    notApplicableReason = if ($hubPresent) { $null } else { 'Canonical Hub audit and log paths are not applicable while the Hub is absent. Runtime candidates are evaluated independently below.' }
    canonicalHubCandidates = $logsHub
    canonicalHubExistingCount = @($logsHub | Where-Object { $_.exists }).Count
    runtimeCandidates = $logsRuntime
    runtimeExistingCount = @($logsRuntime | Where-Object { $_.exists }).Count
    semanticNote = 'Hub and runtime log locations are counted separately. A zero Hub count while the Hub is absent is not evidence that no audit mechanism exists.'
}

# --- 11. Duplicated governance locations -----------------------------------
Write-Host '[11/14] duplicated governance locations'
$gov = @()
# Canonical Hub governance. Populated only when the Hub exists.
$govHub = @()
if ($hubPresent) {
    foreach ($c in @((Join-Path $HubPath 'rules\AGENTS.md'), (Join-Path $HubPath 'AGENTS.md'))) {
        $govHub += (Get-PathFact -Path $c -Hash)
    }
}
# Pre-consolidation source governance. Separate field, separate semantics.
$govSrc = @()
if (-not $hubPresent) {
    foreach ($sp in $resolvedSources) {
        foreach ($c in @((Join-Path $sp 'rules\AGENTS.md'), (Join-Path $sp 'AGENTS.md'))) {
            $govSrc += (Get-PathFact -Path $c -Hash)
        }
    }
}
foreach ($c in @(
    (Join-Path $env:USERPROFILE '.codex\AGENTS.md'),
    (Join-Path $env:USERPROFILE '.claude\CLAUDE.md'),
    (Join-Path $WorkspaceRoot 'workspace-governor\AGENTS.md'),
    (Join-Path $WorkspaceRoot 'workspace-governor\CLAUDE.md')
)) { $gov += (Get-PathFact -Path $c -Hash) }
$dupGroups = @()
$present = @($gov | Where-Object { $_.exists -and $_.sha256 })
foreach ($g in ($present | Group-Object -Property sha256)) {
    if ($g.Count -gt 1) { $dupGroups += [ordered]@{ sha256=$g.Name; paths=@($g.Group | ForEach-Object { $_.path }) } }
}
# Duplication is assessed across every governance file actually inspected:
# canonical Hub (if present), pre-consolidation sources (if the Hub is absent),
# and the runtime files. Grouping by hash spans all three sets on purpose --
# that is the point of the check -- but each set is reported separately so no
# source finding is presented as a canonical-Hub finding.
$govAll = Select-UniqueByFullName -Items (@($govHub) + @($govSrc) + @($gov))
$presentAll = @($govAll | Where-Object { $_.exists -and $_.sha256 })
$dupGroups = @()
foreach ($g in ($presentAll | Group-Object -Property sha256)) {
    if ($g.Count -gt 1) { $dupGroups += [ordered]@{ sha256=$g.Name; paths=@($g.Group | ForEach-Object { $_.path }) } }
}
$R['11_duplicatedGovernance'] = [ordered]@{
    canonicalHubApplicable = $hubPresent
    notApplicableReason = if ($hubPresent) { $null } else { 'Canonical Hub governance paths are not applicable while the Hub is absent. Duplication across runtimes and the pre-consolidation sources is still assessed.' }
    canonicalHubGovernanceFiles = $govHub
    preConsolidationInspectionAttempted = (-not $hubPresent)
    preConsolidationSourcesFound = if ($hubPresent) { 0 } else { @($resolvedSources).Count }
    preConsolidationSourceGovernanceFiles = $govSrc
    runtimeGovernanceFiles = $gov
    identicalContentGroups = $dupGroups
    note = 'Identical sha256 proves a literal copy. Different hashes do not rule out semantic overlap, which requires manual review under HUB-MANAGEMENT.md.'
}

# --- 12. Runtime-native capabilities outside Gateway authority -------------
Write-Host '[12/14] runtime-native capabilities outside Gateway authority'
$R['12_runtimeNativeCapabilities'] = [ordered]@{
    claudeCodeCandidates = @('shell/Bash execution','filesystem read/write/edit','web fetch and search','native permission allow/ask/deny rules','sandbox and network settings')
    codexCandidates      = @('shell execution','filesystem access','native MCP allow/deny lists','approval modes')
    note = 'Candidate list for confirmation. The local agent must confirm the actually enabled set from the configuration captured in items 2, 3 and 4, and document the protecting native control for each, per directive sections 4 and 21.'
}

# --- 13. Direct-access paths that could bypass Gateway governance ----------
Write-Host '[13/14] direct-access bypass paths'
$overlap = @()
foreach ($n in $R['04_mcpConfigurations'].claudeServerNames) {
    if ($R['04_mcpConfigurations'].codexServerNames -contains $n) { $overlap += $n }
}
$R['13_bypassPaths'] = [ordered]@{
    claudeDirectMcpServers = $R['04_mcpConfigurations'].claudeServerNames
    codexDirectMcpServers  = $R['04_mcpConfigurations'].codexServerNames
    configuredInBothRuntimes = $overlap
    note = 'Every server listed here is currently reachable directly by that runtime. Any of them intended to become Gateway-governed is a bypass path. Directive section 20 requires documenting and migrating these safely, never breaking them during discovery.'
}

# --- 14. Repository and workspace paths ------------------------------------
Write-Host '[14/14] repository and workspace paths'
# Probe the ACTUAL repository state, which currently includes the two
# pre-consolidation source repositories. Omitting them would describe an
# architecture that does not yet exist while hiding the one that does.
$repoCandidates = @(
    (Join-Path $WorkspaceRoot 'workspace-governor'),
    (Join-Path $WorkspaceRoot 'agents-hub-one'),
    (Join-Path $WorkspaceRoot 'agents-hub-two'),
    (Join-Path $WorkspaceRoot 'mcp-gateway'),
    (Join-Path $WorkspaceRoot 'atrium_workspace'),
    $HubPath
)
foreach ($sp in $resolvedSources) { $repoCandidates += $sp }
$repoCandidates = @($repoCandidates | Where-Object { $_ } | Select-Object -Unique)
$repos = @()
foreach ($pth in $repoCandidates) { $repos += (Get-GitRepoFact -Path $pth) }

function Get-RepoByLeaf { param([string]$Leaf) return ($repos | Where-Object { (Split-Path $_.path -Leaf) -ieq $Leaf } | Select-Object -First 1) }

$R['14_repositoryPaths'] = [ordered]@{
    workspaceRoot = Get-TreeInventory -Root $WorkspaceRoot -MaxDepth 1
    hubState = $hubState
    architectureComponents = [ordered]@{
        'workspace-governor' = Get-RepoByLeaf -Leaf 'workspace-governor'
        'mcp-gateway'        = Get-RepoByLeaf -Leaf 'mcp-gateway'
        '.agents-hub'        = [ordered]@{
            path = $HubPath
            present = $hubPresent
            state = $hubState
            note = if ($hubPresent) { 'canonical Hub present' } else { 'canonical .agents-hub: ABSENT -- it is the output of consolidating agents-hub-one and agents-hub-two' }
            repo = ($repos | Where-Object { $_.path -eq $HubPath } | Select-Object -First 1)
        }
    }
    preConsolidationSourceRepositories = [ordered]@{
        inspected = $true
        'agents-hub-one' = Get-RepoByLeaf -Leaf 'agents-hub-one'
        'agents-hub-two' = Get-RepoByLeaf -Leaf 'agents-hub-two'
    }
    humanLayer = [ordered]@{ 'atrium_workspace' = Get-RepoByLeaf -Leaf 'atrium_workspace' }
    allProbed = $repos
    note = 'Target architecture is workspace-governor (control), .agents-hub (canonical desired state) and mcp-gateway (enforcement). While .agents-hub is absent, agents-hub-one and agents-hub-two are the actual pre-consolidation sources and are reported as such, not as the canonical Hub.'
}

# --- Explicit non-verification ---------------------------------------------
$R['unverified'] = @(
    'Windows Credential Manager contents not enumerated.',
    'design-systems\.remember contents deliberately not read or hashed (STATE.md stop condition).',
    'Credential file contents never opened; existence and size only.',
    'Secret values never collected anywhere in this report.',
    'MCP protocol versions not negotiated. Directive section 6 requires live verification against current official documentation.',
    'Runtime MCP capability subsets not probed; requires a live session per directive sections 24 to 26.',
    'No script in item 8 was executed.',
    'Semantic (as opposed to literal) governance duplication not determined; requires manual review.'
)

# ============================================================================
# EMIT
# ============================================================================
if (-not (Test-Path -LiteralPath $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }
$jsonPath = Join-Path $OutDir "GATEWAY-DISCOVERY-$stamp.json"
$mdPath   = Join-Path $OutDir "GATEWAY-DISCOVERY-$stamp.md"

$R | ConvertTo-Json -Depth 14 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

$L = New-Object System.Collections.Generic.List[string]
$L.Add('# Gateway Discovery -- Current-State Map')
$L.Add('')
$L.Add("**Generated:** $stampISO")
$L.Add("**Machine:** $env:COMPUTERNAME")
$L.Add('**Scope:** `mcp-gateway` directive section 5 -- Discovery. Evidence collection only.')
$L.Add('**Method:** read-only. Nothing was installed, modified, deleted, moved, renamed, reconfigured or repaired.')
$L.Add('**Secrets:** names, locations and metadata only. No secret value was collected.')
$L.Add('')
$L.Add('## Summary')
$L.Add('')
$L.Add("**Hub state:** $hubState")
$L.Add('')
if (-not $hubPresent) {
    $L.Add('The canonical `.agents-hub` does not exist at the supplied path. It is the')
    $L.Add('output of consolidating `agents-hub-one` and `agents-hub-two`, not a')
    $L.Add('precondition of discovery. Sections whose meaning depends on it are marked')
    $L.Add('**not applicable** rather than reported as empty -- an empty result would read')
    $L.Add('as "nothing exists", which is a different and false claim.')
    $L.Add('')
    if (@($resolvedSources).Count -gt 0) {
        $L.Add('Pre-consolidation sources inventoried instead:')
        $L.Add('')
        foreach ($sp in $resolvedSources) { $L.Add("- ``$sp``") }
    } else {
        $L.Add('No pre-consolidation source repository was found either. Supply')
        $L.Add('`-SourceRepoPaths` if they live outside the workspace root.')
    }
    $L.Add('')
}
$L.Add('| # | Item | Finding |')
$L.Add('|---|---|---|')
$L.Add("| 1 | .agents-hub | state=$hubState, canonical exists=$($R['01_agentsHub'].canonicalHub.hub.exists), $($R['01_agentsHub'].canonicalHub.inventory.itemCount) items |")
$L.Add("| 2 | Claude Code | CLI present=$($R['02_claudeCode'].cli.present), version=$($R['02_claudeCode'].cli.version) |")
$L.Add("| 3 | Codex | CLI present=$($R['03_codex'].cli.present), stale-path hits=$($R['03_codex'].stalePathScan.Count) |")
$L.Add("| 4 | MCP configs | Claude: $(@($R['04_mcpConfigurations'].claudeServerNames) -join ', ') / Codex: $(@($R['04_mcpConfigurations'].codexServerNames) -join ', ') |")
$L.Add("| 5 | PATH | $($R['05_pathAndEnvironment'].pathEntryCount) entries, $($R['05_pathAndEnvironment'].agentRelevantPathCount) agent-relevant |")
$L.Add("| 6 | Dependencies | node=$(($R['06_runtimeDependencies'].commands | Where-Object {$_.name -eq 'node'}).version), python=$(($R['06_runtimeDependencies'].commands | Where-Object {$_.name -eq 'python'}).version) |")
$L.Add("| 7 | Registries | canonical Hub: $($R['07_sharedAssetsAndRegistries'].canonicalHubRegistryCount) (applicable=$hubPresent) / pre-consolidation sources: $($R['07_sharedAssetsAndRegistries'].preConsolidationRegistryCount) |")
$L.Add("| 8 | Scripts/APIs | $($R['08_scriptsAndApis'].count) candidates |")
$L.Add("| 9 | Secrets | $($R['09_authAndSecrets'].sensitiveEnvVarNames.Count) env names, $($R['09_authAndSecrets'].dotEnvFiles.Count) .env files (values NOT collected) |")
$L.Add("| 10 | Audit/logging | canonical Hub: $($R['10_auditAndLogging'].canonicalHubExistingCount) (applicable=$hubPresent) / runtime: $($R['10_auditAndLogging'].runtimeExistingCount) |")
$L.Add("| 11 | Duplicated governance | $($R['11_duplicatedGovernance'].identicalContentGroups.Count) identical-content groups |")
$L.Add("| 12 | Native capabilities | candidate list requires confirmation |")
$L.Add("| 13 | Bypass paths | $(@($R['13_bypassPaths'].configuredInBothRuntimes).Count) servers configured in both runtimes |")
$L.Add("| 14 | Repositories | workspace root exists=$($R['14_repositoryPaths'].workspaceRoot.exists); canonical .agents-hub present=$hubPresent; sources probed: agents-hub-one, agents-hub-two |")
$L.Add('')
$L.Add('## Codex governance-conflict check')
$L.Add('')
if ($R['03_codex'].stalePathScan.Count -gt 0) {
    $L.Add('Stale absolute paths found in the Codex authority file. This is the active conflict recorded in Workspace Governor `STATE.md`, which blocks Codex adapter activation. **Not modified by this script.**')
    $L.Add('')
    $L.Add('| Line | Match |')
    $L.Add('|---|---|')
    foreach ($h in $R['03_codex'].stalePathScan) { $L.Add("| $($h.line) | ``$($h.match)`` |") }
} else {
    $L.Add('No stale `C:\Users\...` or `C:\Workspace` paths detected in the Codex authority file. If `STATE.md` still records that conflict, the record itself needs reconciling.')
}
$L.Add('')
$L.Add('## Explicitly NOT verified')
$L.Add('')
foreach ($u in $R['unverified']) { $L.Add("- $u") }
$L.Add('')
$L.Add('## Full structured findings')
$L.Add('')
$L.Add("See ``$(Split-Path $jsonPath -Leaf)`` in this directory.")
($L -join "`r`n") | Set-Content -LiteralPath $mdPath -Encoding UTF8

Write-Host ''
Write-Host 'DISCOVERY COMPLETE -- no system changes were made.' -ForegroundColor Green
Write-Host "  JSON : $jsonPath"
Write-Host "  MD   : $mdPath"
