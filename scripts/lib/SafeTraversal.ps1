<#
.SYNOPSIS
  Sole owner of directory traversal for the Workspace Governor scripts.

.DESCRIPTION
  Provides pre-descent pruning. A protected directory is identified while
  listing its PARENT, and is never passed to Get-ChildItem.

  WHY THIS EXISTS. `Get-ChildItem -Recurse` traverses every subtree before
  returning, so filtering its output with Where-Object is too late: the
  protected directory has already been read. This module performs manual
  iterative traversal and decides whether to enter each directory BEFORE
  entering it.

  INVARIANT. This file contains the only Get-ChildItem call in the traversal
  path, and it is single-level. No script in scripts/ may use -Recurse.
  scripts/Assert-RememberPruning.ps1 enforces that statically.

  Protected directories are recorded as existing. Nothing inside them is
  listed, counted, read, or hashed.
#>

# Directories never entered, for safety. Recorded as existing only.
# design-systems\.remember — unresolved provenance and sensitivity, STATE.md B-2.
$script:SafetyPrunedNames = @('.remember')

# Directories never entered, to keep inventories meaningful. Not safety-critical.
$script:NoisePrunedNames = @('.git', 'node_modules')

function Get-SafeChildItems {
    <#
    .SYNOPSIS
      Single-level iterative traversal with pre-descent pruning.
    .OUTPUTS
      Ordered hashtable: root, exists, items, visitedDirectories,
      prunedForSafety, prunedForNoise, truncated.
      visitedDirectories lists every directory actually passed to
      Get-ChildItem, which is what makes pruning provable.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][string]$Root,
        [int]$MaxDepth = 64,
        [switch]$FilesOnly,
        [string]$Filter = '',
        [int]$MaxItems = 5000
    )

    $result = [ordered]@{
        root               = $Root
        exists             = $false
        items              = @()
        visitedDirectories = @()
        prunedForSafety    = @()
        prunedForNoise     = @()
        truncated          = $false
    }
    if ([string]::IsNullOrWhiteSpace($Root)) { return $result }
    if (-not (Test-Path -LiteralPath $Root)) { return $result }
    $result.exists = $true

    # If the root itself is protected, do not enter it at all.
    $rootLeaf = Split-Path $Root -Leaf
    if ($script:SafetyPrunedNames -contains $rootLeaf) {
        $result.prunedForSafety += $Root
        return $result
    }

    $stack = New-Object System.Collections.Stack
    $stack.Push([pscustomobject]@{ Path = $Root; Depth = 0 })
    $count = 0

    while ($stack.Count -gt 0) {
        $node = $stack.Pop()
        if ($node.Depth -gt $MaxDepth) { continue }

        # ---------------------------------------------------------------
        # The ONLY Get-ChildItem in the traversal path. Single-level: no
        # -Recurse. A directory reaches this line only after its name was
        # checked against the prune lists while its parent was listed.
        # ---------------------------------------------------------------
        $result.visitedDirectories += $node.Path
        $children = @(Get-ChildItem -LiteralPath $node.Path -Force -ErrorAction SilentlyContinue)

        foreach ($c in $children) {
            if ($c.PSIsContainer) {

                # PRE-DESCENT DECISION. Made before any listing of $c.
                if ($script:SafetyPrunedNames -contains $c.Name) {
                    $result.prunedForSafety += $c.FullName
                    continue    # never pushed, never listed, never counted
                }
                if ($script:NoisePrunedNames -contains $c.Name) {
                    $result.prunedForNoise += $c.FullName
                    continue
                }

                if (-not $FilesOnly) {
                    if ([string]::IsNullOrEmpty($Filter) -or $c.Name -like $Filter) {
                        if ($count -lt $MaxItems) { $result.items += $c; $count++ }
                        else { $result.truncated = $true }
                    }
                }
                $stack.Push([pscustomobject]@{ Path = $c.FullName; Depth = ($node.Depth + 1) })

            } else {
                if ([string]::IsNullOrEmpty($Filter) -or $c.Name -like $Filter) {
                    if ($count -lt $MaxItems) { $result.items += $c; $count++ }
                    else { $result.truncated = $true }
                }
            }
        }
    }
    return $result
}

function Test-SafePruning {
    <#
    .SYNOPSIS
      Proves pre-descent pruning from traversal run data.
    .DESCRIPTION
      Positive proof, not absence-from-output. Asserts that no directory in
      visitedDirectories is the same as, or beneath, any directory in
      prunedForSafety. If a protected directory had been traversed, it would
      appear in visitedDirectories and this check would fail.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory=$true)]$Traversal)

    $violations = @()
    foreach ($p in $Traversal.prunedForSafety) {
        $prefix = $p.TrimEnd('\') + '\'
        foreach ($v in $Traversal.visitedDirectories) {
            if ($v -eq $p) { $violations += "visited the pruned directory itself: $v"; continue }
            if ($v.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
                $violations += "visited a descendant of a pruned directory: $v"
            }
        }
    }
    foreach ($it in $Traversal.items) {
        foreach ($p in $Traversal.prunedForSafety) {
            $prefix = $p.TrimEnd('\') + '\'
            if ($it.FullName.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
                $violations += "returned an item beneath a pruned directory: $($it.FullName)"
            }
        }
    }
    return [ordered]@{
        pass                    = ($violations.Count -eq 0)
        prunedForSafetyCount    = @($Traversal.prunedForSafety).Count
        visitedDirectoryCount   = @($Traversal.visitedDirectories).Count
        itemCount               = @($Traversal.items).Count
        violations              = $violations
    }
}

function Get-SafetyPrunedNames { return $script:SafetyPrunedNames }
