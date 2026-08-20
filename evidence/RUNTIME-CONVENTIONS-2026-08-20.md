# Evidence -- runtime conventions and their constraints on the canonical Hub

**Date:** 2026-08-20
**Method:** independent subagent review against current official vendor
documentation. Findings integrated here by the parent agent; this is a backoffice
evidence record, not an authority.
**Status:** Claude Code section verified against current docs. Codex section
pending a parallel review.

## Claude Code

### Correction to conflict C-03 -- carried forward from the predecessor as stated, and imprecise

The predecessor recorded, and this backoffice carried forward:

> "Claude Code's global-versus-project loading behaviour can allow project
> instructions to take priority while semantic governance forbids lower layers
> from weakening Global Governance."

**Verdict: partially valid, materially imprecise.** It conflates two different
layers.

| Layer | Behaviour | Can a project override a higher scope? |
|---|---|---|
| `CLAUDE.md` instructions, all scopes | **Context, not enforced configuration.** Concatenated, ordered filesystem-root down to working directory, so project content appears later and has recency advantage | Advisory only. It can *instruct* a departure; it cannot enforce one |
| Settings -- permissions, hooks, managed configuration | **Enforced.** Strict precedence: managed > command line > local > project > user | **No.** Managed settings cannot be overridden by any other scope, apart from narrow documented exceptions |

So a project file **cannot weaken an enforced managed policy**, because instructions
and enforcement operate on different layers. The recency advantage is real but
advisory.

**Consequence for the Hub.** Placing governance in the Hub and importing it makes
it *available*, never *enforced*. If a Hub rule must bind, it needs an enforcement
carrier -- managed settings or a hook -- expressed through `runtime-adapters/`.
This is predecessor learning L-001 restated with a mechanism: source placement
establishes neither discovery nor enforcement.

C-03 is therefore **narrowed, not closed**: the adapter-finalization blocker stands,
but its reason changes from "project can outrank global" to "instruction placement
alone enforces nothing; an enforcement carrier must be chosen per rule".

### Runtime-native paths that cannot be centralised

Claude Code discovers these by hard-coded path. Moving them into a semantic tree
orphans them -- they silently stop loading. Each is therefore adapter or native
territory, never a canonical Hub directory.

| Component | Required location |
|---|---|
| Project instructions | `./CLAUDE.md` or `./.claude/CLAUDE.md`; also walked up the tree |
| Settings | `./.claude/settings.json`, `./.claude/settings.local.json` |
| Skills | `./.claude/skills/<name>/SKILL.md`, or `~/.claude/skills/` |
| Path-scoped rules | `./.claude/rules/*.md`, matched on `paths:` frontmatter |
| MCP servers | `.mcp.json` at project root; `~/.claude.json` for user scope |
| Hooks | inside `settings.json`, or a plugin's hook manifest |
| Plugin manifest | `.claude-plugin/plugin.json` at the plugin root |

### The legitimate centralisation mechanism

`CLAUDE.md` supports `@path` imports -- relative or absolute, up to 4 hops, with
cycle detection. **This is the supported way for a project to consume canonical
Hub governance without copying it**, and it directly serves the one-owner rule: the
Hub owns the text, the project imports it, no second copy exists.

It is also the mechanism by which `AGENT-SSOT.json` and `USER-SSOT.json` can be
reachable from a runtime once placed in the Hub -- subject to the scope gating
already required for the Greyed-scoped file.

### Enforceable vs advisory, for policy design

- Enforced: `permissions.allow` / `permissions.deny`, managed-only keys, hooks,
  sandbox flags. Hooks block deterministically on a specific non-zero exit path;
  other failures do not block.
- Advisory or startup-only: model selection, output style, and all `CLAUDE.md`
  content.

This is the practical basis for the `rules/` versus `policies/` split in the
accepted taxonomy: `rules/` is readable governance, `policies/` is the
machine-verifiable form, and only the latter can be carried into an enforcement
mechanism.

### Not verified

- Behaviour of an enterprise-deployed managed `CLAUDE.md` relative to
  server-managed settings. Needs a managed environment to test.
- Whether additional-directory instruction loading can source governance from a
  central repository path in this environment.

## OpenAI / Codex

Pending independent review. Not asserted here until that evidence exists.
