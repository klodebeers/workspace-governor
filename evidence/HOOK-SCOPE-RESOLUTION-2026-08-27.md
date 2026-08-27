# Hook scope resolution, read from the implementation

**Date:** 2026-08-27
**Source:** `@anthropic-ai/claude-code` **2.1.42**, bundle at
`/opt/node22/lib/node_modules/@anthropic-ai/claude-code/cli.js`, read
2026-08-27. Minified identifiers are given so every claim is re-locatable.
**Status:** Verified by reading implementation, and re-checked independently in
this session against the same bundle. `rules/VERIFICATION-RESOLUTION.md`
§ Authority selection accepts *"implementation source at a pinned commit,
recorded with its date"* for vendor product behaviour; this is that, and it
supersedes the "prior research file" basis flagged in
`evidence/USER-SCOPE-HOOK-CARRIER-2026-08-27.md` Finding 1.

**Version caveat.** The operator runs Windows and may be on a different CLI
version. The resolution logic is platform-independent, but the version must be
confirmed with `claude --version` before this is treated as covering that
machine.

## The question issue #43 asked, and its answer

*Does a hook registered only at user scope fire for a session started in any
working directory?*

**Yes**, and no live trial is needed to establish it.

- The scope list is `["userSettings", "projectSettings", "localSettings",
  "flagSettings", "policySettings"]`.
- `userSettings` resolves to
  `join(CLAUDE_CONFIG_DIR ?? join(homedir(), ".claude"), "settings.json")`. It is
  **home-anchored and never consults the working directory**.
- `projectSettings` and `localSettings` resolve from the session's original cwd.
- Settings are folded in that order with lodash `mergeWith` and customizer `SAA`;
  `KH5` makes **arrays concatenate**, so a project's `hooks.UserPromptSubmit`
  does not shadow the user one -- both survive.
- The execution path (`j_A` -> `y8().hooks` -> `uSA` -> `iI`) consults neither
  cwd, nor git-ness, nor project identity when deciding whether a user-scope hook
  is eligible.

**So the three-directory trial samples a variable the resolution code never
reads.** It could only have re-confirmed this, while remaining blind to the
conditions below.

## The finding that changes the design

**A project can silently disable every user-scope hook in its own directory.**

`disableAllHooks` is a **scalar** boolean. Under the same fold, a later scope's
defined scalar overwrites an earlier one, and project and local settings are both
later than user settings. `iI` returns immediately on `y8().disableAllHooks`.

So any project carrying `disableAllHooks: true` in its own
`.claude/settings.json` or `.claude/settings.local.json` turns off the
user-scope carrier for work done in that directory -- with no error, and nothing
in the user's own configuration to indicate it.

**Consequence for Step 9.** "User scope is the carrier" is unsupportable as an
*enforcement* claim. `AGENTS.md` § Enforcement 1 is explicit: *"A gate has no
bypass. A gate with an escape hatch is a suggestion with extra steps."* A carrier
that a drifting project can switch off is the advisory failure of
`USER-SCOPE-HOOK-CARRIER` Finding 1 with extra steps.

**The bypass-proof carrier is `policySettings` -- managed settings.** It is the
only scope that survives `allowManagedHooksOnly`, which when set true in managed
settings makes `j_A()` return *only* managed hooks. The bundle's own message:

> Only hooks from managed settings can run. User-defined hooks from
> `~/.claude/settings.json`, `.claude/settings.json`, and
> `.claude/settings.local.json` are blocked.

Evaluating managed settings as the carrier is a different question from the one
#43 asks, and is opened as its own item.

## Four other conditions that gate the outcome, none of them the working directory

1. **`policySettings.allowManagedHooksOnly === true`** blocks all user, project
   and local hooks (`vp()`, `j_A()`).
2. **`disableAllHooks: true`** at any scope, per above.
3. **Workspace trust.** `vs4()` skips *every* hook for an **interactive** session
   whose cwd has no accepted trust, logging *"Skipping ... hook execution -
   workspace trust not accepted"*. Non-interactive sessions bypass this, so a
   first-visit directory behaves differently from a familiar one, and `claude -p`
   differently from an interactive session.
4. **Config-dir relocation and Cowork.** `CLAUDE_CONFIG_DIR` moves what "user
   scope" means, and in Cowork mode the user file read is `cowork_settings.json`,
   not `settings.json` -- a hook in the latter is simply never read.

Also: a settings file that fails JSON parse or schema validation contributes
**nothing** while other scopes still load (`f46` returns `settings: null`).
Startup surfaces *"Found invalid settings files: ... They will be ignored."* --
so a typo in the user file looks exactly like "user scope does not work".

## Two instruments that beat the trial

- **`/hooks` in the CLI** labels every registered hook with its source --
  *"User settings (~/.claude/settings.json)"*, *"Project settings
  (.claude/settings.json)"*, *"Plugin hooks"* (`XR7`). One keystroke per
  directory reads out what the register-probe-remove cycle was trying to infer,
  and mutates nothing.
- **`claude --debug`** emits *"Found N hook matchers in settings"* and
  *"Matched N unique hooks"* (`uSA`), which separates *not registered* from
  *registered but failing to execute* -- the two failure modes an empty probe log
  conflates.

## What the probe still cannot attribute

The probe logs a timestamp, cwd and event name. It does **not** log which
settings source invoked it. Hooks are deduplicated by exact command string, so
the same script registered at project scope under a different path string is a
distinct hook writing an indistinguishable line. Any live run must pass a source
marker in the command and record it, or the log does not evidence the claim it is
cited for.

## Coverage hole this exposes in the current record

`projectSettings` resolves from the session's **original cwd**, not the git root.
A session started in a *subdirectory* of `workspace-governor` therefore loads no
project hooks at all. The injector set committed under D-95 does not govern those
sessions, and the record said only that it governs "this repository".
