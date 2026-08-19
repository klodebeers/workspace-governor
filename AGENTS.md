# Workspace Governor — Operating Instructions

**Authority:** Project router for this repository. Owns bootstrap order and the
persistence requirement. Owns no governance rule.

You are operating in the management and orchestration repository for the agent
control plane. This repository is not the Agent Hub, not the Gateway, and not a
runtime.

## Bootstrap order

Read in this order before deciding or changing anything:

1. `README.md` — purpose, scope, managed components, repository relationships.
2. `STATE.md` — current verified state, phase, blockers, open work, next action.
3. `DECISIONS.md` — settled decisions. Treat each as settled within its recorded
   scope. Do not reopen or silently re-litigate one.
4. The artefact relevant to the task — `mcp-gateway` for control-plane build work,
   `scripts/` for tooling, `evidence/` for prior findings.

Then inspect the live target before proposing or making a change. `STATE.md` is
continuity evidence, not proof that anything remains unchanged.

## Persistence requirement

**Durable project information must be written to this repository. It must not be
left only in session state.**

Write to the repository, in the same working session, whenever any of these occur:

| Trigger | Destination |
|---|---|
| A decision is settled | `DECISIONS.md` — new entry with rationale and who decided it |
| Verified state changes | `STATE.md` — replace the stale content |
| A blocker appears, changes, or clears | `STATE.md` |
| Work is completed or abandoned | `STATE.md` open work |
| The next action changes | `STATE.md` |
| Evidence is produced | `evidence/SUBJECT-yyyy-MM-dd.md` |

A session that establishes a decision or a material finding and ends without
recording it has failed, regardless of what else it produced.

Corollary: do not rely on conversation history as a source. If a claim is not in
this repository or verifiable against a live source, treat it as unverified and say
so rather than asserting it.

## File ownership

One owner per concern. Do not duplicate content between these files.

| File | Sole owner of |
|---|---|
| `README.md` | Purpose, scope, managed components, repository relationships |
| `STATE.md` | Current verified state, phase, blockers, open work, next action |
| `DECISIONS.md` | Settled decisions and their rationale. Append-only. |
| `AGENTS.md` | Bootstrap order, persistence requirement, file ownership |
| `mcp-gateway` | Gateway build and configuration requirements |

If `STATE.md` and `DECISIONS.md` appear to conflict, `DECISIONS.md` governs what was
settled and `STATE.md` governs what is currently true. Report the conflict; do not
resolve it silently.

## Evidence standard

- State whether a result is verified, partially verified, or blocked. Never present
  agent confidence as verification.
- Name the specific detail that is unverified rather than omitting it.
- Absence from tool output is not evidence of absence in the system.
- Do not claim a component is installed, active, discovered or enforced merely
  because its source is present.
- Record evidence in `evidence/` using `SUBJECT-yyyy-MM-dd` naming.

## Ownership split

Per `rules/ENGINEER-OWNERSHIP.md` — currently in `agents-hub-one`, destined for
`.agents-hub/rules/` after consolidation: the user owns intended outcome,
business rules, acceptance criteria, risk tolerance and reserved human decisions.
The agent owns ordinary engineering decisions and must make and prove them rather
than routing them back to the user.

Escalate only an unresolved matter that exceeds granted authority, crosses a
protected boundary, or genuinely requires business judgement.

## Stop conditions

`STATE.md` holds the current stop conditions. Read them before acting. They are
binding, and they apply to tooling authored here as well as to direct changes.

## Secrets

Never write a secret value into this repository — not into decisions, state,
evidence, tooling, or commit messages. Record references and locations only.
