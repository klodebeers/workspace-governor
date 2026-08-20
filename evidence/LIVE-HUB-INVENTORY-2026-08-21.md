# Live Hub Inventory

**Generated:** 2026-08-21T06:29:01.9830877+08:00
**Machine:** BYTEHUB
**Live Hub inspected:** `C:\Users\Chloe\.agents-hub` (exists: True)
**Compared against:** `AGENTS-HUB-ONE-BASELINE-2026-08-19.json` at ref `47c01870385e8386b6ee41806882b2cd84a7a7d9`
**Method:** read-only, no network. No file contents emitted. Reparse points of either kind excluded; nothing hashed through a link.

## Completeness: COMPLETE

Every directory in the accessible Hub tree was enumerated. No item cap, no
depth cap, and no enumeration error was encountered.

Scope of that claim: complete within the **physical** Hub tree. It excludes
safety-pruned directories, noise-pruned directories, and the targets of any
reparse point. No claim is made about content behind those boundaries.

## Counts

| Metric | Count |
|---|---|
| Live Hub files | 9 |
| GitHub baseline files | 16 |
| **Only in live Hub** | **0** |
| **Placeholder in GitHub, real content live** | **0** |
| **Content differs** | **0** |
| Only in GitHub | 7 |
| Identical | 9 |

## Only in GitHub, absent live

- `design-systems\placeholder.md`
- `governance-templates\component\placeholder.md`
- `governance-templates\delegation\placeholder.md`
- `governance-templates\project\placeholder.md`
- `governance-templates\workspace\placeholder.md`
- `runtime-adapters\claude-code\placeholder.md`
- `runtime-adapters\codex\placeholder.md`

## Exclusions and failures

**Safety-pruned** (never entered, STATE.md B-2):

- `C:\Users\Chloe\.agents-hub\design-systems\.remember`

**Noise-pruned** (never entered, not safety-critical):

- none found

**Not traversed -- reparse points, file and directory** (junction, symlink, mount).
Detected by attribute before the directory/file split, so neither an alias nor a
file link can bypass the name-based rule. Never returned, never hashed. Targets
are not inventoried:

- none found

**Traversal failures** (could not enumerate; forces INCOMPLETE):

- none

**Depth-limited** (not descended; forces INCOMPLETE):

- none

**Item cap reached:** False

## design-systems\.remember

Exists: True

Contents inspected: false

Nothing inside was read, hashed, enumerated, or counted. Existence was established
while listing the parent directory. Stop condition B-2 in `STATE.md`.

### Pre-descent pruning proof

- Safety-pruned directories: 1
  - `C:\Users\Chloe\.agents-hub\design-systems\.remember` -- identified while listing its parent; never entered
- Directories actually passed to Get-ChildItem: 12
- Violations (visited at or beneath a pruned directory): 0
- Verdict: **PASS**

## Explicitly NOT verified

- design-systems\.remember: existence only. Nothing inside was read, hashed, enumerated, or counted (stop condition B-2).
- No file contents were emitted; only path, size, SHA256 and modified time.
- Baseline reflects GitHub .agents-hub -- captured while named agents-hub-one -- at the recorded ref, not any later commit.
- A file identical by SHA256 is byte-identical; semantic equivalence was not assessed.
- Reparse points of either kind, file or directory, were excluded before the directory/file split; they were never returned and never hashed, and nothing behind them is inventoried.
- The inventory is exhaustive only within the physical Hub tree, excluding pruned directories and reparse-point targets.
