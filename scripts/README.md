# Gateway discovery scripts

Read-only evidence collection for section 5 of the `mcp-gateway` directive.
These scripts collect evidence. They perform no analysis and change nothing.

## One command to run

From the repository root, in PowerShell on Windows:

```powershell
.\scripts\Assert-DiscoveryReadOnly.ps1
```

That wrapper runs discovery **and** proves it changed nothing. Do not run
`Invoke-GatewayDiscovery.ps1` on its own unless you do not need the proof.

Optional: add `-Thorough` for SHA256-based comparison (slower, stronger).
Override paths with `-HubPath`, `-WorkspaceRoot`, `-OutDir` if the defaults
are wrong.

## Output format

Three files, written only to `.\evidence\`:

| File | Purpose | Audience |
|---|---|---|
| `GATEWAY-DISCOVERY-<yyyy-MM-dd>.json` | Full structured findings, 14 sections | coding agent |
| `GATEWAY-DISCOVERY-<yyyy-MM-dd>.md` | Summary table, conflict check, non-verified list | human |
| `GATEWAY-DISCOVERY-<yyyy-MM-dd>-READONLY-PROOF.md` | PASS/FAIL that nothing changed | audit record |

All three are UTF-8 text, safe to commit. Naming follows the existing
`evidence/` convention (`SUBJECT-yyyy-MM-dd.md`).

Commit all three together — the proof is only meaningful alongside the
evidence it certifies.

## Coverage — the 14 evidence items

| # | Item |
|---|---|
| 1 | `.agents-hub` location and structure |
| 2 | Claude Code configuration and native controls |
| 3 | Codex configuration and native controls |
| 4 | Existing MCP configurations |
| 5 | PATH and environment entries relevant to coding agents |
| 6 | Installed and runtime dependencies relevant to the Gateway |
| 7 | Shared assets and tool registries |
| 8 | Scripts and APIs potentially relevant for exposure |
| 9 | Authentication and secrets mechanisms (names and locations only) |
| 10 | Audit and logging mechanisms |
| 11 | Duplicated governance locations |
| 12 | Runtime-native capabilities outside Gateway authority |
| 13 | Direct-access paths that could bypass Gateway governance |
| 14 | Repository and workspace paths relevant to the architecture |

## Safety contract

The discovery script:

- performs no writes anywhere except the files it emits into `-OutDir`
- never installs, modifies, deletes, moves, renames, reconfigures or repairs
- makes no network calls
- never emits a secret **value**; records names, locations and metadata only
- does not read or hash `design-systems\.remember` contents, per the
  unresolved provenance and sensitivity hold in Workspace Governor `STATE.md`;
  checks existence only; nothing inside is enumerated, counted, read, or hashed
- reports "not found" rather than failing when a path is absent
- executes none of the scripts it inventories

## How the proof works

`Assert-DiscoveryReadOnly.ps1` verifies in three parts:

- **Part A — static analysis.** Scans the discovery script for every mutating
  cmdlet plus install/network/process-start verbs, and lists each with its line
  number. Passes only if all mutations target `-OutDir`.
- **Part B — filesystem comparison.** Records path, size and last-write time
  for every file under the inspected roots before the run, re-records after,
  and compares. Any modification, creation or deletion outside `-OutDir` fails.
- **Part C — verdict.** Writes the proof document with PASS or FAIL and counts.

Known scope limits, stated in the proof itself: it covers the filesystem roots
listed, excluding `.git`, `node_modules`, `design-systems\.remember` and the
output directory. It does not monitor the registry, services, scheduled tasks
or network state — Part A establishes the script contains no cmdlet that
touches them. Reading a file updates last-*access* time; the comparison uses
last-*write* time and size, which reads do not alter.

## Not verified at authoring time

These scripts were written in a Linux container with no PowerShell available,
so they have **not been executed**. Validation performed was static: delimiter
balance (zero unclosed, no stray closers) and a manual pass for pipeline and
cmdlet syntax. Expect the possibility of a runtime error on first run. If one
occurs, send the error text — the scripts are read-only, so a failure cannot
damage anything.
