# Evidence -- corrected authority model and Hub asset placement

**Date:** 2026-08-20
**Status:** Architecture correction recorded. No file moved, deleted, or renamed.
**Trigger:** User correction, 2026-08-20.

## The error

Two governing artifacts were installed inside `workspace-governor` and described
as authoritative. `workspace-governor` is the Agent Hub **backoffice**. It is not
the live source of agent governance, so it cannot hold a live governing
authority.

| What was done | Why it was wrong |
|---|---|
| `AGENT-SSOT.json` made bootstrap item 0 of `workspace-governor/AGENTS.md`, described as "binding" and as outranking this repository's governance | Installed a live governing authority in the backoffice. The Hub root `AGENTS.md` is the bootstrap, router and authority mechanism. |
| `USER-SSOT.json` described as "binding" here | Same category error. |
| D-23 concluded `USER-SSOT.json` should **not** go to the Hub because it is Greyed-scoped | Confused **scope** with **placement**. Greyed scope is a *loading condition*, not a location. A company-specific asset is still a Hub asset; the Hub routes to it when that company's context is relevant. |

The two SSOT files were supplied *for the Agent Hub*. Staging them here was
correct; declaring them authoritative here was not.

## Corrected model

```
agents-hub          Live governance authority. Root AGENTS.md is the bootstrap,
                    router and authority mechanism, routing agents to the
                    applicable SSOT or rule BY SCOPE.
                      - AGENT-SSOT.json   Hub asset. Agent behavior.
                      - USER-SSOT.json    Hub asset. Greyed-scoped; loaded and
                                          applied only in Greyed context.

workspace-governor  Agent Hub backoffice. Research, reconciliation, change
                    preparation, evidence, backups, archives, recovery and
                    provenance, and the implementation work that updates or
                    corrects the Hub. MAY retain copies as backup, archive,
                    provenance or temporary staging. Such copies must NEVER
                    act as competing live authorities.

agents-hub-two      Source material pending reconciliation. Not an authority.
```

## Applied now

- `AGENTS.md` bootstrap item 0 no longer presents the SSOTs as authorities; it
  states they are Hub assets and that the copies here are staging and provenance.
- `AGENTS.md` § Standing rules records the correction and drops the "binding" and
  "outranks" claims for both files.
- `AGENTS.md` ownership table marks both as backoffice staging copies.
- `STATE.md` stop condition replaced: neither file is a live authority here.
- `PENDING-GLOBAL-PROMOTIONS.md` P-02 corrected; the Greyed-scope reasoning that
  excluded `USER-SSOT.json` from the Hub is withdrawn.

Nothing moved or deleted, per instruction.

## Required once `agents-hub` is established

| # | Change | Detail |
|---|---|---|
| 1 | Place `AGENT-SSOT.json` in `agents-hub` | Hub asset. Root level, alongside the root `AGENTS.md` contract -- it is a root behavior contract, not a routed topic rule. |
| 2 | Place `USER-SSOT.json` in `agents-hub` | Hub asset, Greyed-scoped. Placement must make the scope condition explicit so it is not loaded outside Greyed context. |
| 3 | Add scope-based routing to the Hub root `AGENTS.md` | Its routing table currently routes by *encountered condition* to a topic rule. It needs entries routing to each SSOT, and for `USER-SSOT.json` the route must carry the company-scope condition. Without this, placement alone does not make either file reachable. |
| 4 | Reduce the `workspace-governor` copies to backup/provenance | Retain deliberately as backoffice records, clearly labelled, never as live authority. Do not silently keep an unlabelled second copy. |
| 5 | Move `rules/VERIFICATION-RESOLUTION.md` to `agents-hub` | **See below -- its interim justification has expired.** |
| 6 | Re-scope `PENDING-GLOBAL-PROMOTIONS.md` P-03 | The duplication between `AGENT-SSOT.json` § `verification_and_audit` and `rules/VERIFICATION-RESOLUTION.md` becomes a Hub-internal ownership conflict once both are in the Hub, not a cross-repository one. Resolve it there. |
| 7 | Verify before retiring anything | Confirm the Hub holds each asset under its intended owner and that the Hub root routes to it, before any local copy stops being treated as the working record. |

## Consequence beyond the SSOTs

Every pending promotion in `PENDING-GLOBAL-PROMOTIONS.md` was blocked on one
premise: *no canonical Hub exists to own the rule.* Canonicalization discharges
that premise. The interim arrangement -- cross-agent rules held in the backoffice
and declared binding there -- no longer has a justification.

This applies most directly to `rules/VERIFICATION-RESOLUTION.md`. It was created
in this repository on 2026-08-19/20 and bound by `workspace-governor/AGENTS.md`
explicitly because "the canonical `.agents-hub` does not yet exist to own it"
(P-01). That reason is now spent. Under the corrected model it is the same
category error as the SSOTs: a cross-agent rule acting as a live authority from
the backoffice.

It is **not** moved in this step. Doing so would exceed the current directive,
and the user created that file and its promotion record by explicit instruction,
so retiring the local binding is theirs to confirm. Recorded here as change 5.

## Not affected by this correction

The rename and canonicalization work already applied stands. The authority
relationship recorded in `README.md` and `STATE.md`, the reference updates, and
the blocker B-4 resolution are consistent with the corrected model and are
reinforced by it -- `workspace-governor` is named as backoffice throughout, and
no updated reference asserts governance authority for it.
