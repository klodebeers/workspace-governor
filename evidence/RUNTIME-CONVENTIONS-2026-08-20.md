# Evidence -- runtime conventions and their constraints on the canonical Hub

**Date:** 2026-08-20
**Method:** independent subagent review against current official vendor
documentation. Findings integrated here by the parent agent; this is a backoffice
evidence record, not an authority.
**Status:** Both sections verified by independent review. Claude Code against
current published docs; Codex against pinned implementation source, with the
canonical prose docs egress-blocked and a recheck owed.

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

**Precedence resolved 2026-08-21.** Applicable `CLAUDE.md` files are **additive**:
all of them stay in context rather than one replacing another, loaded broader scope
to more specific -- managed organization policy, then user-level, then
repository/project, then nested directories, then project-local. Because project
instructions load after user instructions, **project-level guidance normally takes
effective precedence over machine-level guidance on conflict**, and more-specific
directory instructions outrank broader ones.

The safe reading is therefore "more specific wins on conflict", **not** "the
repository file replaces the machine file". Managed organization policy is different
in kind: it is intended for organization-wide security and compliance requirements
and carries higher authority than user or repository instructions.

C-03 is therefore **closed on precedence and open on enforcement.** The precedence
question is answered. The distinction that mattered survives untouched and is the
part still open: **`CLAUDE.md` guidance is not itself an enforcement mechanism.**
Precedence decides which guidance wins when two files disagree; it does not make
any of it binding. Anything that must hold regardless still needs an enforcement
carrier -- a managed setting or a hook -- chosen per rule. The adapter-finalization
blocker stands on that ground alone.

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

**Source:** the `openai/codex` implementation at pinned commit
`9e680a52e7008684062144ba86850be90b1c60d1` (2026-08-20), corroborated where they
overlap by the published OpenAI prose mirror. **`developers.openai.com` is
egress-blocked from this environment**, and every `docs/*.md` in the repository is
a stub pointing there, so the behavioural detail below is read from shipped source
rather than canonical prose. A recheck from an unrestricted environment is owed.

### Cross-confirmation of predecessor research

The predecessor's `research/AGENTS-MD-RESEARCH-AND-LIVE-AUDIT-2026-08-16.md`
recorded a 32 KiB combined instruction budget, `project_doc_max_bytes` unset, and
root-to-cwd one-file-per-directory concatenation. **Independently confirmed from
source, four days later.** Two separate reviews, four days apart, different
methods, same numbers. That research is therefore a live design constraint, not
"re-verify only" as previously classified.

### The binding constraint on the root bootstrap

| Property | Value |
|---|---|
| AGENTS.md budget | `project_doc_max_bytes`, default **32 KiB** |
| Scope of the budget | **Shared across the whole root-to-cwd chain**, and further shared across turn environments |
| Consumption order | **Root first** |
| Over-budget behaviour | The file is **truncated mid-content at the byte boundary**. The warning goes to logs only, **never to the model** |
| `= 0` | Disables AGENTS.md entirely |
| Files per directory | Exactly one: `AGENTS.override.md` > `AGENTS.md` > configured fallbacks |
| Count of files | No cap. The byte budget is the only limit |

**Consequence, and it is severe.** An oversized root `AGENTS.md` **silently starves
every nested one**. No error surfaces to the model or the user; governance simply
stops being present. Since D-27 makes root `.agents-hub/AGENTS.md` the
non-negotiable always-loaded bootstrap, its size is a correctness property, not a
style preference. Governance content belongs **behind router references from a
small root file**, never inline.

This is exactly the constraint class held only in the predecessor's
`research/GOVERNANCE-FILE-CREATION-GUIDE-2026-08-16.md` -- per-file size and
truncation budgets, and "critical content appears before any known truncation
boundary." That guide is a bound dependency of `HUB-DOCUMENTATION.md`, not
optional reading.

### The one affordance that makes a neutral tree workable

**`AGENTS.md` may be a symlink.** Path resolution follows symlinks, and the source
states plainly that symlinks are allowed. This is the verified mechanism by which a
runtime-bound path can resolve to canonical neutral content without copying it --
the Codex counterpart to Claude Code's `@path` imports.

### Concrete conflicts with a semantic-ownership tree

Named failures, not general caution. All read from source.

| # | Conflict |
|---|---|
| 1 | **A top-level `skills/` is invisible.** Discovery roots are `.agents/skills` and `.codex/skills` per directory, `~/.agents/skills`, `$CODEX_HOME/skills`, a system config root, and plugin roots. A neutral `skills/` matches none |
| 2 | **No configuration key registers an extra skills root.** An internal parameter exists but nothing populates it from config. A neutral tree must be symlinked into `.agents/skills` or shipped as a plugin |
| 3 | **A top-level `agents/` is not read, and the native format is TOML.** Agent roles are discovered under `<config folder>/agents/**/*.toml`. A Markdown `agents/` tree has no consumer |
| 4 | **`tools/` is inert.** MCP servers come only from TOML config layers or a plugin manifest |
| 5 | **`prompts/` has no located native consumer**; slash commands are migrated into skills. Marked NOT VERIFIED -- the relevant doc page is blocked |
| 6 | **`rules/`, `policies/`, `registry/`, `orchestration/`, `runbooks/`, `templates/`, `context/`, `references/`, `runtime-adapters/` are never auto-loaded.** Reachable only if the root `AGENTS.md` routes to them and the agent reads them on demand |
| 7 | **Directory-scoped precedence cannot express cross-cutting ownership.** An `AGENTS.md` inside `policies/` scopes to `policies/**` only. Only the root file has repository-wide scope |
| 8 | **`.agents/` and `.codex/` are read-only to the agent by default** in the workspace-write sandbox. Authoring must happen with the canonical repository as its own project root |
| 9 | **A nested git checkout severs the chain.** Project-root discovery stops at the first `.git` and never walks past it. **Vendoring the Hub as a nested git repository silently breaks the consumer repository's bootstrap** -- its root `AGENTS.md` is not loaded at all when cwd is inside the nested repo |
| 10 | **Skill scan depth is 6.** Deep semantic nesting under a skills root can exceed it |

Conflict 6 is not a defect -- it is the expected shape for a neutral source, and it
restates the standing rule that placement establishes neither discovery nor
enforcement. Conflicts 1 to 4 mean the taxonomy's `skills/`, `agents/`, `tools/`
and `prompts/` are **canonical source directories only**, never runtime-consumed
directly. Every one requires an adapter projection.

Conflict 9 is the most dangerous operationally, because it fails silently and would
be attributed to anything but its cause.

### Runtime-native, cannot be centralised

`AGENTS.md` at the repository root and at each governed directory (symlinkable, but
the path is fixed); `$CODEX_HOME/AGENTS.md` and its override; all TOML config
layers, which carry **MCP declarations, hooks, agent roles, sandbox and approval
policy, and model settings**; project trust state, held per machine; the skill roots
listed above, with `SKILL.md` a fixed filename; agent role TOML; plugin manifests;
hook declarations; and auth and session state.

### Selected hard limits

Skill `description` required and capped at 1,024 characters; injected `SKILL.md`
body truncated at 8,000 bytes; skills catalogue budget defaults to 2% of the
context window with a 10,000-token cap, and **over-budget skills are silently
omitted**; skill name 64 characters, qualified name 129.

Silent omission and silent truncation appear three times in this section. Every
one of them is a case where governance stops applying and nothing says so.

### Precedence -- resolved

A repository-level `AGENTS.md` **normally outranks** the machine-level
`~/.codex/AGENTS.md` when their instructions conflict. The mechanism is the
concatenation order: the global file loads first, then repository and nested files
from the repository root toward the working directory, so repository instructions
appear later and take precedence over broader machine-level guidance. Files closer
to the working directory outrank the repository root.

Effective order, broadest to most specific:

```
system / developer / user instructions
  -> machine or global instructions
    -> repository-root instructions
      -> nested-directory instructions
```

Within any single level, `AGENTS.override.md` **replaces** `AGENTS.md` at that same
location. `~/.codex/AGENTS.override.md` replaces the machine-level file; a
repository's own override replaces its repository-level file. An override does
**not** let a machine-level file outrank repository instructions merely by being
named `.override.md` -- global still loads before project. System, developer and
direct user instructions remain above both.

This confirms the depth-based reading the earlier review inferred from source and
withdraws the third-party claim that a home override beats everything.

**Consequence for the Hub.** Machine-level governance is not a ceiling. A governed
repository can legitimately outrank the Hub's machine-level projection, so anything
that must hold everywhere cannot rely on placement at the machine level alone -- it
needs an enforcement carrier, which is the same conclusion C-03 reaches for Claude
Code.

### Not verified

- Canonical prose docs: `developers.openai.com` is egress-blocked here. Recheck owed
  from an unrestricted environment.
- ~~Global versus repository precedence.~~ **RESOLVED 2026-08-21** from vendor
  documentation. See below.
- Whether the global `AGENTS.md` counts against the 32 KiB budget. Code path
  suggests not; not documented.
