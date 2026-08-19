# Workspace Governor State

**Updated:** 2026-08-19
**Phase:** Repository bootstrap complete. Hub reconciliation not started.
**Authority:** Non-authoritative continuity record. Settled decisions live in `DECISIONS.md`.

This file records current state only. It defines no rules. Replace stale
content rather than accumulating a transcript.

## Current verified state

Verified by direct inspection during the session dated 2026-08-19.

| Fact | Evidence |
|---|---|
| `workspace-governor` `main` is at `d57deb9` and contained only the `mcp-gateway` file before this bootstrap | `git ls-tree -r --name-only origin/main` |
| The `mcp-gateway` directive is settled: 46 sections, 1,940 lines, contiguous numbering 1–46, 41 Done-When checkboxes | 22-check verification pass against `origin/main` |
| Directive revision history | `30229ae` v1 45 sections → `b8e38d2` v2 15 sections → `85ac462` v3 46 sections → `d57deb9` three defect fixes |
| `agents-hub-one` is a governance tree with a five-file `rules/` contract, zero runtime-specific names across all five files, and seven 0-byte placeholder files | Clone inspection; `grep -ric` for runtime names returned 0 on all five |
| `agents-hub-two` is an agent operating package: 15 agent definitions, a registry, a JSON schema, 4 prompts, 4 templates. Contains no governance layer — zero occurrences of "governance", "precedence", "runtime-neutral", "catalog", "provenance" | Clone inspection and keyword scan |
| Both source repositories declare themselves to be `.agents-hub` | `agents-hub-one/README.md`; `agents-hub-two/docs/README.md` and `package-layout.json` |
| `agent-governance-toolkit` is an unmodified fork of `microsoft/agent-governance-toolkit`, MIT, HEAD authored upstream 2026-05-11, zero local commits | `git log -1 --format='%an %ad'`; `LICENSE`; `MAINTAINERS.md` |
| Discovery tooling exists on branch `claude/add-github-repos-projects-6r1jgy` at `1d96626`, never executed | `git ls-tree`; no PowerShell available in the authoring environment |

## Blockers

| # | Blocker | Effect | Owner |
|---|---|---|---|
| 1 | Codex authority file contains stale absolute paths and overlaps Hub-owned responsibilities. Recorded as an active conflict in `workspace-governor-agents-hub-one/STATE.md`, which halts Codex adapter activation. | Directive sections 34 and 43 both require Codex to connect, so the Gateway cannot reach DONE. Not deferrable. | Requires user authorization to open as a separate scoped change |
| 2 | Final canonical `.agents-hub` does not exist. Two competing source repositories both claim the identity. | Blocks Gateway directive section 29 rule-folding and final environment discovery | Hub reconciliation |
| 3 | Hub One target tree and ownership map not accepted. `workspace-governor-agents-hub-one/STATE.md` stop condition: do not refactor before acceptance. | Blocks any fold of existing rules | Hub reconciliation |
| 4 | `design-systems/.remember` has unresolved provenance and sensitivity. | Must not be read, hashed, moved, or classified | Requires separate review |
| 5 | Live Windows environment is unreachable from a cloud session. | Gateway directive section 5 items covering local MCP, Claude Code, Codex, secrets and audit mechanisms cannot be collected remotely | Local agent executes discovery |

## Open work

1. Revise the discovery tooling so it does not presuppose that `.agents-hub` exists. Current defaults target `$env:USERPROFILE\.agents-hub` and frame the hub as the subject of inspection.
2. Reconcile `agents-hub-one` and `agents-hub-two` into the final canonical `.agents-hub`. Operation is a consolidation: inspect, classify per item, change, reference-update, verify.
3. Persist the user SSOT. `USERSSOT.json` was supplied in session as an authoritative user-side responsibilities file and exists in no repository. Its placement is undecided.
4. Open blocker 1 as a separate scoped change once authorized.
5. Determine placement of the three agent rulings recorded in `DECISIONS.md` under D-07 through D-09.
6. Merge branch `claude/add-github-repos-projects-6r1jgy` once its tooling is revised per item 1.

## Next action

Reconcile the two Hub source repositories into the final canonical `.agents-hub`. Consolidation precedes final Gateway environment discovery (`DECISIONS.md` D-05).

Do not run Gateway environment discovery, and do not implement the Gateway, before that reconciliation.

## Stop conditions

- Do not read, hash, move, or classify `design-systems/.remember` before its provenance and sensitivity review.
- Do not activate a Codex adapter while blocker 1 is unresolved.
- Do not fold existing Hub rules before the target tree and ownership map are accepted.
- Do not reopen the 46-section directive structure (`DECISIONS.md` D-04).
- Do not adopt `agent-governance-toolkit` without provenance, licence, and generated-output review.

Reinspect live sources before acting. This record is continuity evidence, not proof that anything remains unchanged.
