# Pending global-governance promotions

Rules held locally in `workspace-governor` that belong in shared governance once
the canonical owner exists. This file records the promotion obligation only; each
rule's content stays in its own file, which remains its sole owner.

---

## P-01 — Verification Resolution Rule

**Status:** Pending promotion.

```text
Current rule:
workspace-governor/rules/VERIFICATION-RESOLUTION.md

Current enforcement:
workspace-governor/AGENTS.md references the rule

Target:
final canonical .agents-hub shared engineering/verification governance

Promotion trigger:
canonical .agents-hub structure and rule ownership are finalized
```

**Why it is pending rather than placed:** the canonical `.agents-hub` does not yet
exist. Per `DECISIONS.md` D-01, neither source repository is canonical; both are
inputs. There is therefore no shared rule owner to receive this rule, and the
local copy is a temporary binding, not its intended home.

### Terms of the obligation

- This is a **cross-agent standing rule**, not a `workspace-governor` policy. Its
  local placement is an interim measure.
- It **must be promoted** into the finalized canonical `.agents-hub` as soon as the
  appropriate shared rule owner is established.
- After promotion the full rule must have **one canonical owner**. No second copy
  of the rule body may persist as an authority.
- **Governed runtime adapters must expose or materialize the rule** as appropriate
  for each runtime, so governed agents are actually bound by it rather than
  merely having it committed somewhere.
- **Successful promotion must be verified before the temporary workspace copy is
  retired.** Retiring the local copy first would leave a period with no
  enforceable owner.

### On promotion

1. Verify the finalized `.agents-hub` contains the rule under its accepted
   canonical owner.
2. Verify the relevant runtime/adaptation paths make it available to governed
   agents.
3. Remove the temporary `workspace-governor` binding/reference if it is no longer
   required.
4. Archive the temporary `workspace-governor` rule and this promotion record with
   provenance. Do not hard-delete either.
5. Update `STATE.md` so the promotion is no longer shown as pending.

Steps 1 and 2 are the verification this rule itself governs: the sufficient
result is that the rule is present under its canonical owner and reachable by
governed agents. Nothing beyond that is required to close the promotion.
