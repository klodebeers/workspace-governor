<#
.SYNOPSIS
  Sole owner of directory traversal for the Workspace Governor scripts.

.DESCRIPTION
  Provides pre-descent pruning, reparse-point containment, and fail-closed
  completeness accounting.

  WHY PRE-DESCENT PRUNING. `Get-ChildItem -Recurse` traverses every subtree
  before returning, so filtering its output with Where-Object is too late: the
  protected directory has already been read. This module performs manual
  iterative traversal and decides whether to enter each directory BEFORE
  entering it.

  WHY REPARSE-POINT CONTAINMENT. A name-based prune list is defeated by an
  alias. A junction or symlink named anything at all can target
  design-systems\.remember, or a location outside the Hub entirely. Name
  checks alone therefore cannot enforce STATE.md B-2. Directory reparse points
  are detected by attribute and never traversed. The read boundary stays
  physically inside the Hub tree.

  WHY FAIL-CLOSED COMPLETENESS. A reconciliation inventory that silently omits
  files is worse than no inventory. Item caps, depth caps and enumeration
  errors are recorded individually and force completeness to INCOMPLETE. The
  caller cannot report success while part of the accessible tree was skipped.

  INVARIANT. This file contains the only Get-ChildItem call in the traversal
  path, and it is single-level. No script in scripts/ may use -Recurse.
  scripts/Assert-RememberPruning.ps1 enforces that statically.

  Excluded directories are recorded as existing. Nothing inside them is
  listed, counted, read, or hashed.
#>

# Never entered, for safety. Recorded as existing only.
# design-systems\.remember — unresolved provenance and sensitivity, STATE.md B-2.
$script:SafetyPrunedNames = @('.remember')

# Never entered, to keep inventories meaningful. Not safety-critical.
$script:NoisePrunedNames = @('.git', 'node_modules')

function Test-IsReparsePoint {
    <#
    .SYNOPSIS
      True if the item is ANY filesystem reparse point — file or directory.
    .DESCRIPTION
      Attribute-based, so it holds regardless of the link's name or target.
      Deliberately NOT restricted to containers: a FILE reparse point that
      reaches the file branch would be returned in items and then hashed, and
      Get-FileHash follows the link. That reads content from the link target,
      which may be inside design-systems\.remember or outside the Hub.
      Errors resolve to $true: an item whose attributes cannot be read is
      treated as a reparse point and excluded. Fail closed.
    #>
    param($Item)
    if ($null -eq $Item) { return $true }
    try {
        return (($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)
    } catch {
        return $true
    }
}

function Get-SafeChildItems {
    <#
    .SYNOPSIS
      Single-level iterative traversal with pre-descent pruning, reparse-point
      containment, and fail-closed completeness accounting.
    .OUTPUTS
      Ordered hashtable with:
        root, exists, items, visitedDirectories
        prunedForSafety, prunedForNoise      - deliberate exclusions
        untraversedReparsePoints             - deliberate boundary
        traversalFailures                    - could not enumerate
        depthLimited                          - not descended, MaxDepth reached
        truncated                             - MaxItems reached
        completeness                          - COMPLETE or INCOMPLETE
        incompleteReasons                     - why, if INCOMPLETE
      completeness is INCOMPLETE if any of truncated, depthLimited, or
      traversalFailures is non-empty. Deliberate exclusions do not make the
      accessible tree incomplete, but they are always disclosed and the
      exhaustiveness claim is scoped to exclude their targets.
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
        root                    = $Root
        exists                  = $false
        items                   = @()
        visitedDirectories      = @()
        prunedForSafety         = @()
        prunedForNoise          = @()
        untraversedReparsePoints= @()
        traversalFailures       = @()
        depthLimited            = @()
        truncated               = $false
        maxDepth                = $MaxDepth
        maxItems                = $MaxItems
        completeness            = 'INCOMPLETE'
        incompleteReasons       = @()
    }
    if ([string]::IsNullOrWhiteSpace($Root)) {
        $result.incompleteReasons += 'root path was empty'
        return $result
    }
    if (-not (Test-Path -LiteralPath $Root)) {
        $result.incompleteReasons += 'root path does not exist'
        return $result
    }
    $result.exists = $true

    # The root itself: refuse a protected name or a reparse point.
    $rootItem = $null
    try { $rootItem = Get-Item -LiteralPath $Root -Force -ErrorAction Stop } catch {
        $result.traversalFailures += [ordered]@{ path=$Root; reason="could not read root: $($_.Exception.Message)" }
        $result.incompleteReasons += 'root could not be read'
        return $result
    }
    if ($script:SafetyPrunedNames -contains $rootItem.Name) {
        # Nothing was inventoried, so this is not a complete inventory of
        # anything. Refuse rather than report success over an empty result.
        $result.prunedForSafety += $Root
        $result.incompleteReasons += 'supplied root is itself safety-pruned; nothing was inventoried'
        return $result
    }
    if (Test-IsReparsePoint -Item $rootItem) {
        $result.untraversedReparsePoints += [ordered]@{ path=$Root; note='root is a reparse point; not traversed' }
        $result.incompleteReasons += 'root is a reparse point and was not traversed'
        return $result
    }

    $stack = New-Object System.Collections.Stack
    $stack.Push([pscustomobject]@{ Path = $Root; Depth = 0 })
    $count = 0

    while ($stack.Count -gt 0) {
        $node = $stack.Pop()

        # ---------------------------------------------------------------
        # The ONLY Get-ChildItem in the traversal path. Single-level: no
        # -Recurse. A directory reaches this line only after it was checked
        # against the prune lists AND the reparse-point test while its parent
        # was listed.
        # ---------------------------------------------------------------
        $result.visitedDirectories += $node.Path
        $children = @()
        try {
            $children = @(Get-ChildItem -LiteralPath $node.Path -Force -ErrorAction Stop)
        } catch {
            $result.traversalFailures += [ordered]@{ path=$node.Path; reason=$_.Exception.Message }
            continue
        }

        foreach ($c in $children) {

            # ===============================================================
            # PRE-SPLIT DECISION — reparse point, file OR directory, whatever
            # the name. This MUST precede the container/file split: a file
            # reparse point routed to the file branch would be returned in
            # items and then hashed, and Get-FileHash follows the link.
            # ===============================================================
            if (Test-IsReparsePoint -Item $c) {
                $result.untraversedReparsePoints += [ordered]@{
                    path = $c.FullName
                    kind = if ($c.PSIsContainer) { 'directory' } else { 'file' }
                    note = 'reparse point; not traversed, not returned, not hashed; target not inventoried'
                }
                # If it also carries a protected name, disclose it in both
                # places so the safety record is not lost.
                if ($script:SafetyPrunedNames -contains $c.Name) {
                    $result.prunedForSafety += $c.FullName
                }
                continue    # never pushed, never listed, never returned
            }

            if ($c.PSIsContainer) {

                # PRE-DESCENT DECISION — protected name.
                if ($script:SafetyPrunedNames -contains $c.Name) {
                    $result.prunedForSafety += $c.FullName
                    continue    # never pushed, never listed, never counted
                }

                # PRE-DESCENT DECISION — noise.
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

                # PRE-DESCENT DECISION 4 — depth cap. Recorded, not silent.
                if (($node.Depth + 1) -gt $MaxDepth) {
                    $result.depthLimited += [ordered]@{
                        path = $c.FullName
                        note = "not descended; MaxDepth $MaxDepth reached"
                    }
                    continue
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

    # ---- fail-closed completeness -----------------------------------------
    if ($result.truncated) {
        $result.incompleteReasons += "item cap reached (MaxItems $MaxItems); files were omitted"
    }
    if (@($result.depthLimited).Count -gt 0) {
        $result.incompleteReasons += "$(@($result.depthLimited).Count) directory/directories not descended (MaxDepth $MaxDepth)"
    }
    if (@($result.traversalFailures).Count -gt 0) {
        $result.incompleteReasons += "$(@($result.traversalFailures).Count) directory/directories could not be enumerated"
    }
    $result.completeness = if (@($result.incompleteReasons).Count -eq 0) { 'COMPLETE' } else { 'INCOMPLETE' }
    return $result
}

function Test-SafePruning {
    <#
    .SYNOPSIS
      Proves pre-descent pruning and reparse-point containment from run data.
    .DESCRIPTION
      Positive proof, not absence-from-output. Asserts that no directory in
      visitedDirectories is the same as, or beneath, any excluded directory —
      safety-pruned or untraversed reparse point. A traversed exclusion would
      appear in visitedDirectories and fail this check.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory=$true)]$Traversal)

    $violations = @()
    $barriers = @()
    foreach ($p in $Traversal.prunedForSafety) { $barriers += [pscustomobject]@{ Path=$p; Kind='safety-pruned' } }
    foreach ($r in $Traversal.untraversedReparsePoints) { $barriers += [pscustomobject]@{ Path=$r.path; Kind='reparse point' } }

    foreach ($b in $barriers) {
        $prefix = $b.Path.TrimEnd('\') + '\'
        foreach ($v in $Traversal.visitedDirectories) {
            if ($v -eq $b.Path) { $violations += "visited the $($b.Kind) itself: $v" ; continue }
            if ($v.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
                $violations += "visited a descendant of a $($b.Kind): $v"
            }
        }
        foreach ($it in $Traversal.items) {
            if ($it.FullName.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
                $violations += "returned an item beneath a $($b.Kind): $($it.FullName)"
            }
        }
    }

    # No returned item may itself be a reparse point, of either kind. This is
    # the property that stops a file symlink escaping into the inventory and
    # being hashed.
    $reparseInItems = 0
    foreach ($it in $Traversal.items) {
        if (Test-IsReparsePoint -Item $it) {
            $reparseInItems++
            $violations += "returned item is a reparse point: $($it.FullName)"
        }
    }
    return [ordered]@{
        pass                      = ($violations.Count -eq 0)
        prunedForSafetyCount      = @($Traversal.prunedForSafety).Count
        prunedForNoiseCount       = @($Traversal.prunedForNoise).Count
        reparsePointCount         = @($Traversal.untraversedReparsePoints).Count
        traversalFailureCount     = @($Traversal.traversalFailures).Count
        depthLimitedCount         = @($Traversal.depthLimited).Count
        visitedDirectoryCount     = @($Traversal.visitedDirectories).Count
        itemCount                 = @($Traversal.items).Count
        completeness              = $Traversal.completeness
        reparsePointsInItems      = $reparseInItems
        violations                = $violations
    }
}

function Get-SafetyPrunedNames { return $script:SafetyPrunedNames }
function Get-NoisePrunedNames  { return $script:NoisePrunedNames }
