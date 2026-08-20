# Pre-Descent Pruning Proof

**Verdict:** PASS

Verdict is fail-closed. PASS requires the Hub to exist, A1-A7 to pass, the
runtime pruning test to pass, and traversal completeness to be COMPLETE. A
skipped runtime proof is not a proof.
**Generated:** 2026-08-21T06:28:57.4741392+08:00
**Machine:** BYTEHUB
**Claim under test:** protected directories are pruned before descent, not filtered out of recursive output afterwards.

Filtering after recursion and pruning before descent produce identical
output. Absence of `.remember` from a report therefore proves nothing. This
proof rests on the record of directories actually passed to `Get-ChildItem`.

## Part A -- static invariant

| # | Assertion | Result |
|---|---|---|
| A1 | No `Get-ChildItem -Recurse` in executable code | PASS -- 0 hits |
| A2 | Exactly one traversal `Get-ChildItem`, single-level, in `lib/SafeTraversal.ps1` | PASS -- 1 found |
| A3 | Every traversing script dot-sources the module | PASS |
| A4 | Reparse-point containment present and attribute-based | PASS |
| A5 | Completeness computed and can be INCOMPLETE | PASS |
| A6 | Inventory consumes completeness rather than ignoring it | PASS |
| A7 | Runtime test rejects any reparse point inside returned items | PASS |

Without `-Recurse`, a subtree cannot be traversed before the prune decision is made.

A4 matters twice over. A name-based prune list is defeated by an alias: a
junction named anything can target a protected directory or a location outside
the Hub, so detection is by file attribute. And the test must run BEFORE the
directory/file split -- a container-gated test lets a FILE reparse point reach
the file branch, enter `items`, and be hashed, and `Get-FileHash` follows the
link. A4 asserts the call site precedes the split by line order:
reparse at line 169, split at line 172.

## Part B -- runtime proof

Hub traversed: `C:\Users\Chloe\.agents-hub`

| Metric | Value |
|---|---|
| Directories passed to `Get-ChildItem` | 12 |
| Safety-pruned directories | 1 |
| `.remember` found and pruned | True |
| Items returned | 20 |
| Reparse points not traversed | 0 |
| Noise-pruned | 0 |
| Traversal failures | 0 |
| Depth-limited | 0 |
| Reparse points inside returned items | 0 |
| **Completeness** | **COMPLETE** |
| Violations | 0 |

### Safety-pruned, never entered

- `C:\Users\Chloe\.agents-hub\design-systems\.remember`

**B1 -- no visited directory is at or beneath a pruned directory: PASS**

### Directories actually visited

- `C:\Users\Chloe\.agents-hub`
- `C:\Users\Chloe\.agents-hub\runtime-adapters`
- `C:\Users\Chloe\.agents-hub\runtime-adapters\codex`
- `C:\Users\Chloe\.agents-hub\runtime-adapters\claude-code`
- `C:\Users\Chloe\.agents-hub\rules`
- `C:\Users\Chloe\.agents-hub\references`
- `C:\Users\Chloe\.agents-hub\governance-templates`
- `C:\Users\Chloe\.agents-hub\governance-templates\workspace`
- `C:\Users\Chloe\.agents-hub\governance-templates\project`
- `C:\Users\Chloe\.agents-hub\governance-templates\delegation`
- `C:\Users\Chloe\.agents-hub\governance-templates\component`
- `C:\Users\Chloe\.agents-hub\design-systems`

## Scope

- Part A is a source-level invariant and holds regardless of filesystem state.
- Part B reflects one traversal of one machine at the stated time.
- Neither part inspects anything inside a pruned directory or a reparse point.
  Existence is established while listing the parent.
- Reparse-point targets are outside the read boundary and are not inventoried.
  No exhaustiveness claim covers them.
