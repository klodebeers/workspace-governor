# Step 1 -- accepted target tree and item classification

**Date:** 2026-08-21
**Gate:** SATISFIED. `Assert-RememberPruning.ps1` returned `PASS` (fail-closed);
`Invoke-HubInventory.ps1` returned `Completeness: COMPLETE`. Evidence committed at
`12f93e6`.
**Inputs, all now fully known:** live `.agents-hub` (9 files, verified);
`agents-hub-two` (27 files, reconciled at revision 2); predecessor backoffice
(carried in full).
**Status:** Classification complete. **Nothing applied.** Restructuring requires
approval per `plans/AGENT-HUB-CONSOLIDATION.md` § 6.7.

## The finding that closes B-6

The live Hub holds **9 files, every one byte-identical to the GitHub baseline at
`47c0187`**. Zero files exist live that the baseline lacks. Zero content differs.
The 7 baseline-only files are exactly the 7 zero-byte placeholders, which do not
exist on disk at all.

B-6 was recorded on the premise that the live Hub might hold real content behind
GitHub's placeholders, leaving the consolidation inputs unknown. **It does not.**
The premise is disproved, not merely aged out, and the inputs are now fully known.

Two consequences:

- `references\AGENTS-MD-LIVE-AUDIT-2026-08-16.md` **is live in the Hub**, confirming
  D-15's direction -- the Hub keeps the live-state audit -- and confirming that the
  predecessor v0.4.2 § 4.1 ledger row was wrong to say retire the Hub copy. Now
  verified against live state rather than inferred.
- `governance-templates/` and both `runtime-adapters/` subdirectories are confirmed
  **genuinely empty** on disk. They were empty scaffolding, not unexamined content.

## Live Hub, item by item

| Live item | Class | Destination | Basis |
|---|---|---|---|
| `rules\AGENTS.md` | **Move** | `AGENTS.md` at Hub root | D-27 makes the root file the non-negotiable bootstrap, router and precedence entrypoint. The file already declares itself the root contract and says "read this file first", so it cannot live inside the directory its own routing table addresses |
| `rules\ENGINEER-OWNERSHIP.md` | Keep | `rules/` | Sole owner of ownership, intake, technical decision resolution |
| `rules\AUTONOMY-AND-PROTECTED-BOUNDARIES.md` | Keep | `rules/` | Sole owner of autonomy, approval, protected boundaries |
| `rules\CONTEXT-AND-ORCHESTRATION.md` | Keep | `rules/` | Sole owner of context, delegation, continuity |
| `rules\VERIFICATION-AND-EVIDENCE.md` | Keep | `rules/` | Sole owner of done, testing, audit, evidence |
| `README.md` | Keep | Hub root | Navigation and boundary statement |
| `CATALOG.md` | **Keep -- decided** | Hub root | Resolves plan delta D-l. The taxonomy made it conditional; the live Codex global instruction file **requires** Hub `README.md` and `CATALOG.md`. A runtime consumer already depends on it, and the artifact exists with real content. Conditional-on-justification is satisfied |
| `STATE.md` | **Retire from the Hub** | `workspace-governor` | Decided below. Mutable management state, not agent-consumable desired state |
| `references\AGENTS-MD-LIVE-AUDIT-2026-08-16.md` | Keep | `references/` | D-15. Hub keeps the live-state audit; the backoffice keeps the authoring research |
| `governance-templates\` + 4 empty subdirectories | **Retire** | -- | Verified empty. The taxonomy forbids empty scaffolding, and `templates/` is the accepted owner once real templates land |
| `runtime-adapters\codex\`, `runtime-adapters\claude-code\` | Keep as boundary | `runtime-adapters/` | Empty, but the directory is the adapter boundary and D-29 establishes that every canonical source directory needs a projection. Populating them is Step 9, not Step 1 |
| `design-systems\` (holds only `.remember`) | **Conflict** | preserve in place, visibly excluded | B-2 unresolved. Cannot be classified. The `Conflict` guard applies: this may not be silently converted to another class |
| 7 baseline-only `placeholder.md` files | **Retire** | -- | Zero bytes, no content, and empty scaffolding is forbidden. They exist in the repository and not on disk; retiring them removes the divergence |

## The one substantive Step-1 decision: Hub-root `STATE.md`

The taxonomy left this open. Deciding it from actual content: the live file is a
mutable operational checkpoint -- current work, blockers, next action. The directive
draws the line as **agent-consumable desired state** may be canonical Hub material,
while **backoffice management state** is `workspace-governor` material. A checkpoint
of in-flight consolidation work is the second. It also states plainly that
management state, migration state and consolidation progress are not automatically
added to the live Hub.

**Retire it from the Hub.** Its continuity role is already served by
`workspace-governor/STATE.md`, which is the current, maintained record. Keeping both
creates two mutable state files for one concern and invites drift -- the failure D-33
forbids between the repository and its local materialization.

This also removes the predecessor completion criterion that presumed a Hub-root
`STATE.md`. Recorded as satisfied-by-decision rather than left ambiguous.

## Accepted target tree -- smallest structure the actual content supports

```text
.agents-hub/
|-- AGENTS.md              root bootstrap, router, precedence  (moved from rules/)
|-- README.md              navigation and boundary
|-- CATALOG.md             inventory; required by the live Codex configuration
|-- rules/                 4 files: ownership, autonomy, context, verification
|-- agents/                11 specialist definitions          (from agents-hub-two)
|-- orchestration/         routing, topology, sequence, entry point (from agents-hub-two)
|-- registry/              identity and classification, plus its schema (from agents-hub-two)
|-- templates/             4 output templates                 (from agents-hub-two)
|-- context/               domain knowledge, e.g. the quadruplicated formula notes
|-- runtime-adapters/      codex/, claude-code/ -- boundary; populated at Step 9
|-- references/            1 retained audit
`-- design-systems/        EXCLUDED, preserved in place, B-2 unresolved
```

### Deliberately not created, and why

| Directory | Why not |
|---|---|
| `policies/` | No machine-verifiable policy artifact exists yet. The only candidate, the registry schema, must be rewritten first -- it omits two of its target's eight keys and forbids the two-coordinator model it validates. Create it with its first real artifact |
| `prompts/` | The four `agents-hub-two` prompt files are **loading instructions** -- "read `package-layout.json` first", "read this agent file as the entry point". That is adapter material, not a canonical reusable prompt. Routed to `runtime-adapters/` |
| `skills/`, `tools/`, `runbooks/` | No artifact of any of these kinds exists in either input |
| `archive/`, `evaluations/`, `packages/` | Removed from the taxonomy by D-27; history belongs to the backoffice |

**On the apparent conflict:** the directive's ownership rules name `policies/` and
`prompts/`, and also require the smallest structure actual content supports with no
empty or speculative directories. Those are not in tension. The ownership rules
define what a directory owns **if it exists**; the tree is content-driven. Both are
created by their first accepted artifact.

## Coverage proof

| Input | Items | Classified |
|---|---|---|
| Live `.agents-hub` files | 9 | 9 |
| Live empty directory groups | 3 | 3 |
| Baseline-only placeholders | 7 | 7 |
| `agents-hub-two` artifacts | 27 | 27, at revision 2 |
| **Total** | **46** | **46** |

One item is `Conflict` and therefore intentionally unresolved: `design-systems\`.
Every other item has a class and a destination.

## Not verified

- Semantic equivalence. Nine files are byte-identical to the baseline; that is
  identity, not an assessment of whether their content is correct or current.
- Anything inside `design-systems\.remember`. Existence only.
- Whether any runtime currently loads the live Hub. The inventory records file
  state, never discovery, loading or enforcement. The fresh-session bootstrap
  assignment remains open.
