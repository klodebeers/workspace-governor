# Open-work migration to the issue register -- 2026-08-21

**Status:** complete for every open item in `STATE.md` § Open work as it stood at
commit `b39a097`. Verified by walking the list item by item; the mapping below is the
walk, not a summary of it.

**Why.** The user directed that all issues be written to
`github.com/klodebeers/workspace-governor/issues`. `STATE.md` § Open work was the
previous register. Keeping both would put one concern under two owners -- the defect
`AGENTS.md` § File ownership exists to prevent, and one this repository has already
paid for once (`DECISIONS.md` D-86).

**What was not migrated, and why.** Items struck through in `STATE.md` were already
closed. They are history, and history stays where it was written; the full prior list
including them is in git at `b39a097`. Nothing was deleted to make this mapping true.

## Mapping

| `STATE.md` item | Issue | Note |
|---|---|---|
| 3 -- execute plan Steps 3 onward | #8 | Recast as Step 5's three preconditions, which is what "Steps 3 onward" now means |
| 4 -- place the SSOT pair | #15 | Merged with 29y; both are the same placement |
| 5 -- open B-3 as a scoped change | #16 | |
| 6 -- placement of D-07..D-09 | #23 | |
| 7 -- trim duplicated research narrative | #24 | Merged with the reference/research overlap mapping half of item 15 |
| 9 -- promote the Verification Resolution Rule | #17 | Merged with 10; the promotion and its ownership question are one item |
| 10 -- duplicate ownership P-03 | #17 | Depends on #1 |
| 12 -- conflict-resolution gaps G-1, G-2 | #7 | Rows in the gap table; not a separate item |
| 13 -- resolve C-03 | #18 | Partly discharged by #5 |
| 15 -- carried predecessor G-01, G-04, G-05 | #24, #25 | Split: overlap mapping to #24, glossary and delivery artifact to #25 |
| 16 -- four discovery-tooling inventory gaps | #26 | |
| 17 -- predecessor spec-02 analysis fields | #27 | |
| 18 -- runtime-neutral continuity pattern | #28 | |
| 19 -- `CATALOG.md` collision | #29 | |
| 22 -- plugin packaging | #30 | Merged with 23; both are deferred-by-decision |
| 23 -- scheduled audits | #30 | |
| 24 -- glossary placement | #25 | |
| 25 -- agent-definition schema | #10 | Merged with 29f, which is the same schema question |
| 26 -- handoff contract | #13 | Merged with 29c |
| 27 -- evidence-record template | #31 | |
| 28a -- populate `context/` | #20 | |
| 28b -- domain implementation per owner | #21 | Reserved for the user |
| 28c -- rename to `adapters/` | #32 | |
| 29a -- three orphaned obligations | #22 | Merged with 29b, a fourth of the same kind |
| 29a-ii -- pre-routing obligation owner | #33 | |
| 29b -- third-party escalation destination | #22 | |
| 29c -- handoff contract before further migration | #13 | |
| 29d -- coordinators' `dependency_chain` | #34 | |
| 29e -- domain selected, no trigger matches | #7 | Gap G-8; not a separate item |
| 29f -- agent-definition shape question | #10 | |
| 29y -- rename and place the user-context SSOTs | #15 | |
| 29z -- runtime wiring, sequenced last | #9 | |
| 29 -- migrate remaining `agents-hub-two` artifacts | #19 | |

## Issues filed that were not `STATE.md` open work

| Issue | Source |
|---|---|
| #1 | U-1, the reserved decision, from the Step 3 ownership map § 6 |
| #2 | U-6, same source; two instances confirmed present in the Hub clone today |
| #3 | `LEARNINGS.md` L-039, recorded with no mechanism behind it |
| #4 | A pattern across three recorded instances, never itself recorded |
| #5 | The missing enforcement carrier -- C-03 and D-74 named it; nothing implemented it |
| #6 | Three obligations owed to Hub rules, from the ownership map and `PENDING-GLOBAL-PROMOTIONS.md` |
| #7 | The thirteen gaps G-1..G-13 |
| #11 | `PENDING.md` P-1 |
| #12 | `STATE.md` § Verification assignments -- the fresh-agent bootstrap test |
| #14 | This migration |
| #35 | The Workspace Orchestrator material, awaiting the user |

## Merges, stated

**Corrected 2026-08-21 by audit.** Six pairs -- 4 with 29y, 9 with 10, 22 with 23,
25 with 29f, 26 with 29c, 29a with 29b -- so **twelve items became six issues** (#15,
#17, #30, #10, #13, #22). The original wording said "seven items became four issues",
which matched neither the list beside it nor the mapping table above.

Two items (12, 29e) were already rows inside a larger issue and were not duplicated as
standalone ones. The original also named 29f here while the mapping table sends it to
#10 -- it cannot be both a merge-pair member and a row inside another issue.

**This is not evidence that the duplication was harmless.** Item 26 and item 29c
described the same missing handoff contract in different words, **nine lines apart**
(lines 391 and 400 of `STATE.md` at `b39a097`), and both were live. An earlier revision
said "roughly forty lines apart", which the file does not support. A register in which one item can appear
twice without either copy knowing is the condition the move to one issue per item
removes.

## Verification

- Every non-struck item in § Open work at `b39a097` appears exactly once in the
  mapping above. Walked in file order.
- Every issue number cited above was returned by the API call that created it.
- **Not verified:** that each issue body is a faithful rendering of its source item.
  The bodies were written from the source text in the same pass, not diffed against
  it afterwards. A misrendering would not be caught by anything here.

## Audit addendum, 2026-08-21

An independent adversarial audit of this migration ran the same day, given the previous
`STATE.md` at `b39a097` as its source and told not to trust the mapping table. It was
right about more than it was wrong about. Findings confirmed against the source, and
corrected:

**Items genuinely lost, now filed.** U-3, U-4 and U-5 from the ownership map's six
unresolved questions appear in no issue -- confirmed by searching all 35. U-4 is the
worst of the three: the Hub root routes non-governance placement to an owner that is
never named, so the root contract delegates a live decision to a plan that declares
itself not live governance. `DECISIONS.md` D-89 claimed the newly filed set covered
"U-1 and U-6 from the ownership map", so the omission was not one the record admitted.

**Substance lost inside a merge.** Old item 29f was mapped to issue #10 as "the same
schema question". Its actual content -- that the accepted definition shape has no slot
for a specialist's domain-focus block, and that four of the eleven source specialists
carry one that is an internal issue taxonomy rather than platform behaviour, fitting
neither the definition shape nor the `context/` gloss -- appears in no issue. Old item
25's binding constraint, that the schema must be written against **all thirteen source
shapes** rather than the one migrated file, was rendered as "the next eleven have no
contract to be written against". Thirteen is not eleven.

**Steps with no owner.** "Execute plan Steps 3 onward" was mapped to issue #8 and
recast as Step 5's preconditions. Plan Step 10 (partly done) and Step 12 (not started,
carrying the § 6.8 completion criteria) have no issue and no other owner, so under the
new ownership rule they became formally untracked.

**A dependency invented against the source.** Issue #12 stated that the bootstrap test
depends on issue #9, the runtime wiring. The source says the opposite -- "worth doing
before Step 9 adapters, since it measures whether the current bootstrap is found at
all" -- and #9's own close condition is the bootstrap test, so the two could not both
close. #12 also dropped the source's load-bearing condition to run the test where work
actually happens rather than inside `.agents-hub`.

**A claim with no repository basis.** Issue #35 asserted that the user has Workspace
Orchestrator material and said they would locate it. All eleven repository mentions of
Workspace Orchestrator describe a future project explicitly out of scope; the only basis
for the claim is a statement made in session, which `AGENTS.md` forbids relying on.
Relabelled as unverified rather than deleted -- a session statement is a reason to ask,
not a reason to assert.

**The count claim.** "Eleven that had no register at all" is false for at least three:
#7 absorbs mapped items 12 and 29e, #11 was `PENDING.md` P-1, and #12 was a `STATE.md`
verification assignment. What is true is that eleven issues were filed for items that
had no entry in the register the migration replaced.

**One finding rejected, with its ground.** The audit reported that `AGENTS.md`
§ Enforcement asserts "five checker defects" against a cited source (D-65) that says
eight and eleven. The number is correct and sourced -- `LEARNINGS.md` L-026 names
exactly five, each one listed. The defect was the **citation**, not the count, and the
paragraph now cites L-026 for the five and D-65 for the rule. Rejecting the finding as
stated while fixing what it actually found is the distinction `DECISIONS.md` D-87
requires.

**What the audit confirms about this file.** Its completeness claim holds: all 33
non-struck items appear exactly once in the mapping, enumerated independently. Its
"not verified" caveat -- that no issue body was diffed against its source item -- is
exactly what covered the two substance losses above. The caveat was correct to be
there, and it was not enough.
