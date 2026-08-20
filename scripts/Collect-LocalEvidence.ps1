<#
    Collect-LocalEvidence.ps1

    ONE self-contained read-only evidence collector. Paste it into PowerShell and
    run it once. It has no dependency on any repository and dot-sources nothing.

    IT DOES NOT CHANGE ANYTHING. No install, modify, delete, move, rename,
    reconfigure or repair. It only reads, and writes its two output files.

    SAFETY PROPERTIES
      - design-systems\.remember is NEVER entered. Its existence is recorded while
        listing its parent; nothing inside is listed, read, counted or hashed.
      - No -Recurse anywhere. Traversal is manual and decides whether to enter a
        directory BEFORE entering it.
      - Reparse points (junctions, symlinks, mounts) are excluded before the
        directory/file split, so a linked FILE is never hashed and a linked
        DIRECTORY is never followed outside the tree.
      - Secret-shaped values are redacted. Names and locations only.
      - Completeness fails closed: if any part of the tree was skipped, the report
        says INCOMPLETE.
      - Pure ASCII source, so Windows PowerShell 5.1 cannot mis-decode it.

    OUTPUT
      LOCAL-EVIDENCE-<yyyy-MM-dd>.json  full detail
      LOCAL-EVIDENCE-<yyyy-MM-dd>.md    concise report
      Written to -OutDir (default: the current directory).
#>

[CmdletBinding()]
param(
    [string]$HubPath       = (Join-Path $env:USERPROFILE '.agents-hub'),
    [string]$WorkspaceRoot = 'C:\KloWorkspaces',
    [string]$OutDir        = (Get-Location).Path,
    [int]$MaxDepth         = 64,
    [int]$MaxItems         = 100000
)

$ErrorActionPreference = 'Continue'
$stamp    = Get-Date
$stampDay = $stamp.ToString('yyyy-MM-dd')
$stampIso = $stamp.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

# Names never entered. .remember is a hard safety barrier.
$SafetyPruned = @('.remember')
$NoisePruned  = @('.git', 'node_modules', '.venv', '__pycache__')

# ---------- helpers ---------------------------------------------------------

function Test-IsReparse {
    param($Item)
    if ($null -eq $Item) { return $true }
    try { return (($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) }
    catch { return $true }          # unreadable attributes: fail closed
}

function Protect-Value {
    param([string]$Name, [string]$Value)
    if ([string]::IsNullOrEmpty($Value)) { return $null }
    if ($Name -match '(?i)(key|token|secret|password|passwd|pwd|credential|auth|bearer|session|cookie|private)') {
        return '[REDACTED length=' + $Value.Length + ']'
    }
    if ($Value -match '(?i)(sk-[A-Za-z0-9]{8,}|ghp_[A-Za-z0-9]{8,}|xox[baprs]-|-----BEGIN)') {
        return '[REDACTED shape=secret]'
    }
    return $Value
}

function Get-SafeTree {
    <# Manual traversal. Prune decisions happen before descent. #>
    param([string]$Root)
    $out = [ordered]@{
        root = $Root; exists = $false; files = @(); fileCount = 0
        visitedDirectories = @(); safetyPruned = @(); noisePruned = @()
        reparseExcluded = @(); failures = @(); depthLimited = @()
        truncated = $false; completeness = 'INCOMPLETE'; incompleteReasons = @()
    }
    if ([string]::IsNullOrWhiteSpace($Root) -or -not (Test-Path -LiteralPath $Root)) {
        $out.incompleteReasons += 'path does not exist'
        return $out
    }
    $out.exists = $true

    $rootItem = $null
    try { $rootItem = Get-Item -LiteralPath $Root -Force -ErrorAction Stop } catch { }
    if (Test-IsReparse -Item $rootItem) {
        $out.incompleteReasons += 'supplied root is a reparse point; refused'
        return $out
    }
    if ($SafetyPruned -contains (Split-Path $Root -Leaf)) {
        $out.incompleteReasons += 'supplied root is a protected directory; refused'
        return $out
    }

    $stack = New-Object System.Collections.Stack
    $stack.Push(@{ Path = $Root; Depth = 0 })
    $count = 0

    while ($stack.Count -gt 0) {
        $node = $stack.Pop()
        if ($node.Depth -gt $MaxDepth) {
            $out.depthLimited += $node.Path
            $out.incompleteReasons += ('depth limit at ' + $node.Path)
            continue
        }
        $out.visitedDirectories += $node.Path

        $children = @()
        try { $children = @(Get-ChildItem -LiteralPath $node.Path -Force -ErrorAction Stop) }
        catch {
            $out.failures += [ordered]@{ path = $node.Path; reason = $_.Exception.GetType().Name }
            $out.incompleteReasons += ('could not enumerate ' + $node.Path)
            continue
        }

        foreach ($child in $children) {
            # Reparse decided FIRST, before container/file split.
            if (Test-IsReparse -Item $child) {
                $kind = 'file'
                if ($child.PSIsContainer) { $kind = 'directory' }
                $out.reparseExcluded += [ordered]@{ path = $child.FullName; kind = $kind }
                continue
            }
            if ($child.PSIsContainer) {
                if ($SafetyPruned -contains $child.Name) {
                    $out.safetyPruned += $child.FullName          # existence only
                    continue
                }
                if ($NoisePruned -contains $child.Name) {
                    $out.noisePruned += $child.FullName
                    continue
                }
                $stack.Push(@{ Path = $child.FullName; Depth = ($node.Depth + 1) })
            }
            else {
                if ($count -ge $MaxItems) {
                    $out.truncated = $true
                    $out.incompleteReasons += 'item cap reached'
                    continue
                }
                $sha = $null
                if ($child.Length -lt 5MB) {
                    try { $sha = (Get-FileHash -LiteralPath $child.FullName -Algorithm SHA256 -ErrorAction Stop).Hash } catch { }
                }
                $rel = $child.FullName
                if ($rel.StartsWith($Root, [System.StringComparison]::OrdinalIgnoreCase)) {
                    $rel = $rel.Substring($Root.Length).TrimStart('\', '/')
                }
                $out.files += [ordered]@{
                    relativePath = $rel; sizeBytes = $child.Length
                    modifiedUtc = $child.LastWriteTimeUtc.ToString('o'); sha256 = $sha
                }
                $count++
            }
        }
    }
    $out.fileCount = $count
    if (@($out.incompleteReasons).Count -eq 0) { $out.completeness = 'COMPLETE' }
    return $out
}

function Get-ToolFact {
    <# Two discovery methods, and every resolution recorded. #>
    param([string]$Name, [string]$VersionArg = '--version')
    $fact = [ordered]@{
        name = $Name; present = $false; primary = $null
        allResolutions = @(); resolutionCount = 0; multipleInstalls = $false
        version = $null
    }
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($cmd) {
        $fact.present = $true
        if ($cmd.Source) { $fact.primary = $cmd.Source } else { $fact.primary = $cmd.Name }
    }
    try {
        $hits = @(& where.exe $Name 2>$null | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
        $fact.allResolutions = $hits
        $fact.resolutionCount = $hits.Count
        if ($hits.Count -gt 1) { $fact.multipleInstalls = $true }
        if (-not $fact.present -and $hits.Count -gt 0) {
            $fact.present = $true
            $fact.primary = $hits[0]
        }
    } catch { }
    if ($fact.present) {
        try { $fact.version = (& $Name $VersionArg 2>$null | Select-Object -First 1) } catch { }
    }
    return $fact
}

function Get-PathFacts {
    param([string]$Raw, [string]$Scope)
    $list = @()
    if ([string]::IsNullOrWhiteSpace($Raw)) { return $list }
    $seen = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($piece in ($Raw -split ';')) {
        if ([string]::IsNullOrWhiteSpace($piece)) { continue }
        $trimmed = $piece.TrimEnd('\')
        $isDup = -not $seen.Add($trimmed)
        $list += [ordered]@{
            scope = $Scope; entry = $piece
            exists = (Test-Path -LiteralPath $piece)
            duplicate = $isDup
        }
    }
    return $list
}

# ---------- collection -----------------------------------------------------

Write-Host ''
Write-Host '=== Local evidence collection (read-only) ===' -ForegroundColor Cyan
Write-Host ('  host       : ' + $env:COMPUTERNAME)
Write-Host ('  PowerShell : ' + $PSVersionTable.PSVersion + ' (' + $PSVersionTable.PSEdition + ')')
Write-Host ''

$D = [ordered]@{
    meta = [ordered]@{
        script = 'Collect-LocalEvidence.ps1'; schemaVersion = '1.0'
        generatedUtc = $stampIso; readOnly = $true; networkCalls = $false
        secretsPolicy = 'names and locations only; values redacted'
        machine = $env:COMPUTERNAME; user = $env:USERNAME
        hubPath = $HubPath; workspaceRoot = $WorkspaceRoot
    }
}

# 1. Runtime that actually executes this
Write-Host '[1/7] PowerShell and OS'
$D['01_runtime'] = [ordered]@{
    psVersion = [string]$PSVersionTable.PSVersion
    psEdition = [string]$PSVersionTable.PSEdition
    isWindowsPowerShell51 = ([string]$PSVersionTable.PSVersion).StartsWith('5.1')
    clrVersion = [string]$PSVersionTable.CLRVersion
    osVersion = [string][System.Environment]::OSVersion.Version
    is64BitOS = [System.Environment]::Is64BitOperatingSystem
    executionPolicy = [string](Get-ExecutionPolicy -ErrorAction SilentlyContinue)
    note = 'Confirms whether the repository scripts were parsed by 5.1 or 7.'
}

# 2. Live Hub inventory
Write-Host '[2/7] Live Hub inventory (.remember never entered)'
$hubTree = Get-SafeTree -Root $HubPath
$rememberPath = Join-Path $HubPath 'design-systems\.remember'
$D['02_liveHub'] = [ordered]@{
    hubPath = $HubPath
    exists = $hubTree.exists
    fileCount = $hubTree.fileCount
    completeness = $hubTree.completeness
    incompleteReasons = @($hubTree.incompleteReasons)
    files = $hubTree.files
    topLevel = @()
    rememberExists = (Test-Path -LiteralPath $rememberPath)
    rememberContentsInspected = $false
    safetyPruned = @($hubTree.safetyPruned)
    reparseExcluded = @($hubTree.reparseExcluded)
    noisePruned = @($hubTree.noisePruned)
    traversalFailures = @($hubTree.failures)
    depthLimited = @($hubTree.depthLimited)
    visitedDirectoryCount = @($hubTree.visitedDirectories).Count
    note = 'Existence of .remember recorded while listing its parent. Nothing inside was listed, read, counted or hashed.'
}
if ($hubTree.exists) {
    try {
        $D['02_liveHub'].topLevel = @(Get-ChildItem -LiteralPath $HubPath -Force -ErrorAction Stop |
            ForEach-Object { $t = 'file'; if ($_.PSIsContainer) { $t = 'dir' }; ($t + ' ' + $_.Name) })
    } catch { }
}

# 3. Coding-agent runtimes
Write-Host '[3/7] Coding-agent runtimes and dependencies'
$toolNames = @('claude','codex','gh','git','node','npm','npx','pnpm','yarn','bun','deno',
               'python','py','pip','uv','docker','wsl','rg','fd','fzf','jq','pwsh','powershell','wt')
$tools = @()
foreach ($t in $toolNames) { $tools += (Get-ToolFact -Name $t) }
$D['03_tools'] = [ordered]@{
    tools = $tools
    presentCount = @($tools | Where-Object { $_.present }).Count
    multipleInstallTools = @($tools | Where-Object { $_.multipleInstalls } | ForEach-Object { $_.name })
    absentTools = @($tools | Where-Object { -not $_.present } | ForEach-Object { $_.name })
    note = 'Two discovery methods per tool: Get-Command and where.exe. All resolutions recorded so shadowing and multiple installs are visible.'
}

# 4. PATH in all three scopes
Write-Host '[4/7] PATH: user, machine, effective'
$userPath = $null; $machinePath = $null
try { $userPath = [System.Environment]::GetEnvironmentVariable('Path', 'User') } catch { }
try { $machinePath = [System.Environment]::GetEnvironmentVariable('Path', 'Machine') } catch { }
$pUser = Get-PathFacts -Raw $userPath -Scope 'User'
$pMach = Get-PathFacts -Raw $machinePath -Scope 'Machine'
$pEff  = Get-PathFacts -Raw $env:PATH -Scope 'Effective'
$inUser = @($pUser | ForEach-Object { $_.entry.TrimEnd('\') })
$inMach = @($pMach | ForEach-Object { $_.entry.TrimEnd('\') })
$D['04_path'] = [ordered]@{
    userEntries = $pUser
    machineEntries = $pMach
    effectiveEntries = $pEff
    userCount = @($pUser).Count
    machineCount = @($pMach).Count
    effectiveCount = @($pEff).Count
    brokenEntries = @(($pUser + $pMach + $pEff) | Where-Object { -not $_.exists })
    duplicateEntries = @(($pUser + $pMach + $pEff) | Where-Object { $_.duplicate })
    inBothUserAndMachine = @($inUser | Where-Object { $inMach -contains $_ })
    note = 'Effective PATH is the merged process view. User and Machine are read separately so a scope conflict is visible and a fix can name the scope.'
}

# 5. Runtime configuration presence (locations only)
Write-Host '[5/7] Runtime configuration presence'
# Built from environment bases that are actually set. Join-Path throws on a null
# base, and a thrown array initialiser would collapse the whole candidate list
# and report "0 of 0" instead of failing visibly.
$missingBases = @()
function Join-IfBase {
    param([string]$Base, [string]$Leaf, [string]$BaseName)
    if ([string]::IsNullOrWhiteSpace($Base)) {
        if ($script:missingBases -notcontains $BaseName) { $script:missingBases += $BaseName }
        return $null
    }
    return (Join-Path $Base $Leaf)
}
$cfgCandidates = @(
    (Join-IfBase -Base $env:USERPROFILE -Leaf '.claude'                        -BaseName 'USERPROFILE'),
    (Join-IfBase -Base $env:USERPROFILE -Leaf '.claude\settings.json'          -BaseName 'USERPROFILE'),
    (Join-IfBase -Base $env:USERPROFILE -Leaf '.claude\settings.local.json'    -BaseName 'USERPROFILE'),
    (Join-IfBase -Base $env:USERPROFILE -Leaf '.claude.json'                   -BaseName 'USERPROFILE'),
    (Join-IfBase -Base $env:USERPROFILE -Leaf 'CLAUDE.md'                      -BaseName 'USERPROFILE'),
    (Join-IfBase -Base $env:USERPROFILE -Leaf '.claude\CLAUDE.md'              -BaseName 'USERPROFILE'),
    (Join-IfBase -Base $env:USERPROFILE -Leaf '.claude\skills'                 -BaseName 'USERPROFILE'),
    (Join-IfBase -Base $env:USERPROFILE -Leaf '.codex'                         -BaseName 'USERPROFILE'),
    (Join-IfBase -Base $env:USERPROFILE -Leaf '.codex\config.toml'             -BaseName 'USERPROFILE'),
    (Join-IfBase -Base $env:USERPROFILE -Leaf '.codex\AGENTS.md'               -BaseName 'USERPROFILE'),
    (Join-IfBase -Base $env:USERPROFILE -Leaf '.config\codex\config.toml'      -BaseName 'USERPROFILE'),
    (Join-IfBase -Base $env:USERPROFILE -Leaf 'AGENTS.md'                      -BaseName 'USERPROFILE'),
    (Join-IfBase -Base $env:APPDATA     -Leaf 'Claude\claude_desktop_config.json' -BaseName 'APPDATA'),
    'C:\Program Files\ClaudeCode\CLAUDE.md',
    'C:\Program Files\ClaudeCode\managed-settings.json'
) | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
$cfgFacts = @()
foreach ($cp in $cfgCandidates) {
    $item = $null
    $ex = Test-Path -LiteralPath $cp
    if ($ex) { try { $item = Get-Item -LiteralPath $cp -Force -ErrorAction Stop } catch { } }
    $sz = $null; $md = $null; $isDir = $false
    if ($item) {
        $isDir = $item.PSIsContainer
        if (-not $isDir) { $sz = $item.Length }
        $md = $item.LastWriteTimeUtc.ToString('o')
    }
    $cfgFacts += [ordered]@{ path = $cp; exists = $ex; isDirectory = $isDir; sizeBytes = $sz; modifiedUtc = $md }
}
# MCP server NAMES only, from any JSON config found. No values.
$mcpNames = @()
foreach ($jf in @($cfgFacts | Where-Object { $_.exists -and -not $_.isDirectory -and $_.path -match '\.json$' })) {
    try {
        $parsed = Get-Content -LiteralPath $jf.path -Raw -ErrorAction Stop | ConvertFrom-Json
        if ($parsed -and $parsed.PSObject.Properties['mcpServers']) {
            foreach ($prop in $parsed.mcpServers.PSObject.Properties) {
                $mcpNames += [ordered]@{ source = $jf.path; serverName = $prop.Name }
            }
        }
    } catch { }
}
$D['05_runtimeConfig'] = [ordered]@{
    candidateCount = @($cfgCandidates).Count
    environmentBasesMissing = @($missingBases)
    candidates = $cfgFacts
    existingCount = @($cfgFacts | Where-Object { $_.exists }).Count
    mcpServerNames = $mcpNames
    note = 'Presence, size and modified time only. No file contents emitted. MCP server names only, never commands, arguments, environment or tokens. Presence is NOT evidence that a runtime loads the file.'
}

# 6. Codex stale-path scan (line numbers and matched pattern only)
Write-Host '[6/7] Codex stale-path scan'
$stale = @()
$codexFiles = @($cfgFacts | Where-Object { $_.exists -and -not $_.isDirectory -and $_.path -match '(?i)codex' })
foreach ($cf in $codexFiles) {
    try {
        $lineNo = 0
        foreach ($line in (Get-Content -LiteralPath $cf.path -ErrorAction Stop)) {
            $lineNo++
            $m = [regex]::Match($line, '(?i)C:\\Users\\[A-Za-z0-9._-]+|C:\\Workspace[A-Za-z0-9._\\-]*')
            if ($m.Success) {
                $stale += [ordered]@{ file = $cf.path; line = $lineNo; match = $m.Value }
            }
        }
    } catch { }
}
$D['06_codexStalePaths'] = [ordered]@{
    filesScanned = @($codexFiles | ForEach-Object { $_.path })
    hits = $stale
    hitCount = @($stale).Count
    note = 'Matched path fragments only, with line numbers. No surrounding content. Nothing modified.'
}

# 7. Repositories under the workspace root
Write-Host '[7/7] Repositories under the workspace root'
$repoNames = @('.agents-hub','agents-hub','agents-hub-one','agents-hub-two','workspace-governor',
               'workspace-governor-agents-hub-one','mcp-gateway','atrium_workspace','agent-governance-toolkit')
$repos = @()
foreach ($rn in $repoNames) {
    $rp = Join-Path $WorkspaceRoot $rn
    $ex = Test-Path -LiteralPath $rp
    $isGit = $false; $head = $null; $branch = $null
    if ($ex) {
        $isGit = Test-Path -LiteralPath (Join-Path $rp '.git')
        if ($isGit) {
            try { $head = (& git -C $rp rev-parse --short HEAD 2>$null | Select-Object -First 1) } catch { }
            try { $branch = (& git -C $rp rev-parse --abbrev-ref HEAD 2>$null | Select-Object -First 1) } catch { }
        }
    }
    $repos += [ordered]@{ name = $rn; path = $rp; exists = $ex; isGitRepo = $isGit; head = $head; branch = $branch }
}
$D['07_repositories'] = [ordered]@{
    workspaceRootExists = (Test-Path -LiteralPath $WorkspaceRoot)
    repositories = $repos
    presentCount = @($repos | Where-Object { $_.exists }).Count
}

$D['unverified'] = @(
    'Presence of a configuration file is not evidence that a runtime discovered, loaded, or enforced it. Activation requires a fresh-session test.',
    'design-systems\.remember: existence only. Nothing inside was listed, read, counted or hashed.',
    'Reparse points were excluded before the directory/file split. Nothing behind them is inventoried.',
    'File contents were not emitted. Only paths, sizes, modified times and SHA256 hashes.',
    'Inventory is exhaustive only within the physical tree, excluding pruned directories and reparse-point targets.'
)

# ---------- output ---------------------------------------------------------

if (-not (Test-Path -LiteralPath $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }
$jsonPath = Join-Path $OutDir ('LOCAL-EVIDENCE-' + $stampDay + '.json')
$mdPath   = Join-Path $OutDir ('LOCAL-EVIDENCE-' + $stampDay + '.md')
$D | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

$L = New-Object 'System.Collections.Generic.List[string]'
$L.Add('# Local Evidence')
$L.Add('')
$L.Add('- Generated (UTC): ' + $stampIso)
$L.Add('- Host: ' + $env:COMPUTERNAME)
$L.Add('- PowerShell: ' + $D['01_runtime'].psVersion + ' (' + $D['01_runtime'].psEdition + ')')
$L.Add('- Read-only. No configuration was changed. No file contents emitted.')
$L.Add('')
$L.Add('## Summary')
$L.Add('')
$L.Add('| Item | Result |')
$L.Add('|---|---|')
$L.Add('| Windows PowerShell 5.1 | ' + $D['01_runtime'].isWindowsPowerShell51 + ' |')
$L.Add('| Live Hub exists | ' + $D['02_liveHub'].exists + ' |')
$L.Add('| Live Hub files | ' + $D['02_liveHub'].fileCount + ' |')
$L.Add('| Inventory completeness | ' + $D['02_liveHub'].completeness + ' |')
$L.Add('| .remember present (not entered) | ' + $D['02_liveHub'].rememberExists + ' |')
$L.Add('| Reparse points excluded | ' + @($D['02_liveHub'].reparseExcluded).Count + ' |')
$L.Add('| Tools present | ' + $D['03_tools'].presentCount + ' of ' + $toolNames.Count + ' |')
$L.Add('| Tools with multiple installs | ' + (@($D['03_tools'].multipleInstallTools) -join ', ') + ' |')
$L.Add('| PATH entries user / machine / effective | ' + $D['04_path'].userCount + ' / ' + $D['04_path'].machineCount + ' / ' + $D['04_path'].effectiveCount + ' |')
$L.Add('| Broken PATH entries | ' + @($D['04_path'].brokenEntries).Count + ' |')
$L.Add('| Duplicate PATH entries | ' + @($D['04_path'].duplicateEntries).Count + ' |')
$L.Add('| In both User and Machine PATH | ' + @($D['04_path'].inBothUserAndMachine).Count + ' |')
$L.Add('| Runtime config files found | ' + $D['05_runtimeConfig'].existingCount + ' of ' + @($cfgCandidates).Count + ' |')
if (@($missingBases).Count -gt 0) {
    $L.Add('| Environment bases NOT set (candidates skipped) | ' + (@($missingBases) -join ', ') + ' |')
}
$L.Add('| MCP servers configured (names) | ' + @($D['05_runtimeConfig'].mcpServerNames).Count + ' |')
$L.Add('| Codex stale-path hits | ' + $D['06_codexStalePaths'].hitCount + ' |')
$L.Add('| Repositories found | ' + $D['07_repositories'].presentCount + ' of ' + $repoNames.Count + ' |')
$L.Add('')
if ($D['02_liveHub'].completeness -ne 'COMPLETE') {
    $L.Add('## Inventory INCOMPLETE')
    $L.Add('')
    foreach ($reason in @($D['02_liveHub'].incompleteReasons)) { $L.Add('- ' + $reason) }
    $L.Add('')
}
$L.Add('## Live Hub top level')
$L.Add('')
foreach ($entry in @($D['02_liveHub'].topLevel)) { $L.Add('- `' + $entry + '`') }
$L.Add('')
$L.Add('## Tools')
$L.Add('')
$L.Add('| Tool | Present | Resolutions | Multiple | Version |')
$L.Add('|---|---|---|---|---|')
foreach ($tf in $tools) {
    $L.Add('| ' + $tf.name + ' | ' + $tf.present + ' | ' + $tf.resolutionCount + ' | ' + $tf.multipleInstalls + ' | ' + $tf.version + ' |')
}
$L.Add('')
$L.Add('## Runtime configuration present')
$L.Add('')
foreach ($cf in @($cfgFacts | Where-Object { $_.exists })) { $L.Add('- `' + $cf.path + '`') }
$L.Add('')
if (@($D['05_runtimeConfig'].mcpServerNames).Count -gt 0) {
    $L.Add('## MCP servers configured (names only)')
    $L.Add('')
    foreach ($mn in @($D['05_runtimeConfig'].mcpServerNames)) { $L.Add('- ' + $mn.serverName + '  (' + $mn.source + ')') }
    $L.Add('')
}
if ($D['06_codexStalePaths'].hitCount -gt 0) {
    $L.Add('## Codex stale paths')
    $L.Add('')
    $L.Add('| File | Line | Match |')
    $L.Add('|---|---|---|')
    foreach ($sh in $stale) { $L.Add('| ' + $sh.file + ' | ' + $sh.line + ' | `' + $sh.match + '` |') }
    $L.Add('')
}
$L.Add('## Repositories')
$L.Add('')
$L.Add('| Name | Exists | Git | HEAD | Branch |')
$L.Add('|---|---|---|---|---|')
foreach ($rp in $repos) {
    $L.Add('| ' + $rp.name + ' | ' + $rp.exists + ' | ' + $rp.isGitRepo + ' | ' + $rp.head + ' | ' + $rp.branch + ' |')
}
$L.Add('')
$L.Add('## Explicitly NOT verified')
$L.Add('')
foreach ($uv in $D['unverified']) { $L.Add('- ' + $uv) }
($L -join "`r`n") | Set-Content -LiteralPath $mdPath -Encoding UTF8

Write-Host ''
Write-Host '=== Done. Nothing was changed. ===' -ForegroundColor Green
Write-Host ('  Hub exists    : ' + $D['02_liveHub'].exists + '   files: ' + $D['02_liveHub'].fileCount)
$compColor = 'Red'
if ($D['02_liveHub'].completeness -eq 'COMPLETE') { $compColor = 'Green' }
Write-Host ('  Completeness  : ' + $D['02_liveHub'].completeness) -ForegroundColor $compColor
Write-Host ('  .remember     : present=' + $D['02_liveHub'].rememberExists + ' (never entered)')
Write-Host ('  Tools present : ' + $D['03_tools'].presentCount + ' of ' + $toolNames.Count)
Write-Host ('  Codex stale   : ' + $D['06_codexStalePaths'].hitCount + ' hits')
Write-Host ''
Write-Host '  JSON : ' -NoNewline; Write-Host $jsonPath -ForegroundColor Cyan
Write-Host '  MD   : ' -NoNewline; Write-Host $mdPath -ForegroundColor Cyan
Write-Host ''
Write-Host '  Send back the .md file (or both). No secrets are included.' -ForegroundColor Yellow
Write-Host ''
