# Runtime adapters, as two production repositories actually do it

**Date:** 2026-08-27
**Sources, read at these commits:** `klodebeers/gym` at `d71871e` (a fork of
`NVIDIA-NeMo/Gym`), `klodebeers/nemo-platform` at `78607cd`. Both public, both
cloned and inspected directly. Supplied by the user as references.
**Status:** Verified by inspection of committed trees. Not adopted -- adoption is
plan-level and gated; see § What is gated.

## Why this matters here

`plans/AGENT-HUB-CONSOLIDATION.md` Step 9 is "reconcile and implement thin runtime
adapters", not started, and `DECISIONS.md` D-75 names the two files to wire.
`evidence/USER-SCOPE-HOOK-CARRIER-2026-08-27.md` Finding 1 argues that pair is the
wrong deliverable. These two repositories have already built the thing Step 9
describes, and the shape they arrived at answers questions this project has been
deciding in the abstract.

## The pattern

**One canonical tree, projected into each runtime's native path by symlink.**

`nemo-platform` projects whole directories:

    .claude/skills   -> ../.agents/skills
    .cursor/skills   -> ../.agents/skills
    web/.claude/skills  -> ../.agents/skills
    web/.cursor/skills  -> ../.agents/skills

`Gym` projects per item, which lets each runtime carry a **subset**:

    .claude/skills/<name> -> ../../.agents/skills/<name>   (7 of 7 skills)
    .codex/skills/<name>  -> ../../.agents/skills/<name>   (4 of 7 skills)

Every target is **relative**, so the tree is portable and no clone path is baked
in. Git stores them as mode `120000`, so the projection is committed, not a local
setup step somebody must remember.

## Four things this settles that were open here

**1. The wiring is one file, not two.** `Gym/CLAUDE.md` is itself a symlink to
`AGENTS.md` -- mode `120000`, target `AGENTS.md`. `AGENTS.md` is the real 9,883-byte
file. Claude Code discovers `CLAUDE.md`, Codex discovers `AGENTS.md`, and there is
exactly one file to maintain.

D-75 names `.claude/CLAUDE.md` and `.codex/AGENTS.md` as "the two files to be
wired", which reads as two documents to keep in step. The reference answer is one
document and a link. `workspace-governor` already achieves the same end differently
-- its `CLAUDE.md` is an 11-byte `@AGENTS.md` import -- but the Hub, which has no
`CLAUDE.md` at all, does not.

**2. The projection lives in the runtime-native path, not in an `adapters/`
directory.** D-68 settled the adapter directory's name as `adapters/`, and the plan
already notes that "a file placed under `adapters/` would never be discovered by
either runtime". These repositories confirm the consequence: there is no adapter
directory. The adapter *is* the symlink sitting where the runtime looks.

**3. Per-runtime interface metadata is carried by the canonical item, not by a
separate adapter file.** `.agents/skills/nemo-gym-debugging/` contains `SKILL.md`,
`references/`, `scripts/` and `agents/openai.yaml` -- the last holding
`display_name`, `short_description` and `default_prompt`. The runtime-specific
presentation travels *inside* the thing it presents, so it cannot drift away from
it, and the one-owner rule holds without a reconciliation step.

**4. A canonical tree can be projected into more than one working root.**
`nemo-platform` symlinks `web/.claude/skills` as well as `.claude/skills`. That is
the answer to the coverage hole recorded in
`evidence/HOOK-SCOPE-RESOLUTION-2026-08-27.md`: project-scoped configuration
resolves from the session's original working directory, not the git root, so a
session started in a subdirectory sees nothing. They fix it by projecting into each
directory people actually start sessions in.

## The risk this carries, and it is the failure mode of the day

**Symlinks in git on Windows are conditional.** Without `core.symlinks=true` and
either Developer Mode or elevation, git checks a symlink out as a **plain text file
containing its target path**. `CLAUDE.md` would then be a one-line file whose entire
content is the string `AGENTS.md`.

Nothing errors. The runtime finds a `CLAUDE.md`, reads it, and gets a filename
instead of a contract. That is the same shape as every other defect found today: a
silent failure whose signature is indistinguishable from working software.

The operator machine is Windows. So if this pattern is adopted here, the checkout
condition is not a footnote -- it is the first thing to verify, and it needs a gate
that refuses rather than a note that asks. `evidence/RUNTIME-CONVENTIONS-2026-08-20.md`
already recorded that "symlinks are the verified affordance for resolving a
runtime-bound path to neutral content"; what it did not record is what happens when
the affordance is unavailable.

## What is immediately usable, and what is gated

**Usable now, no plan step involved:** the shape itself, as evidence for the Step 9
design discussion, and the Windows checkout question, which is answerable on the
operator's machine by `git config core.symlinks` and looking at whether a checked-out
symlink is a link or a one-line file.

**Gated, and not done here:** applying it to `.agents-hub`. Step 9 requires Step 3's
owner map, `STATE.md` § Stop conditions forbids modifying live Hub governance without
approval, and Step 8 still has eleven agent definitions behind the D-47 schema. The
reference does not lift those gates; it tells us what to build when they lift.

## What I would propose, stated as a proposal

Replace D-75's "two files to wire" with: **one canonical `AGENTS.md`, a committed
`CLAUDE.md` symlink beside it, and a gate that refuses a checkout where that symlink
materialised as a text file.** The gate is the part these references do not have and
this repository would need, because here the operator is on the platform where the
mechanism silently degrades.
