# What two NeMo repositories actually enforce, and what they only claim

**Date:** 2026-08-27
**Sources:** `klodebeers/gym` at `d71871e`, `klodebeers/nemo-platform` at
`78607cd` (forks of `NVIDIA-NeMo/Gym` and `NVIDIA-NeMo/nemo-platform`), read
read-only. Study performed by a delegated agent; the two load-bearing claims
below were re-verified independently in this session before recording.
**Status:** Verified by inspection. **Nothing adopted** -- adoption touches the
Hub and `plans/AGENT-HUB-CONSOLIDATION.md`, both gated.

## The finding that matters most, and it is a failure

`nemo-platform/docs/contributing/skills-spec.mdx` § 9 states that two skill
gates -- `scripts/skill-cli-lint.py` (228 lines, lints fenced bash in every
SKILL.md against the live CLI surface) and `scripts/skill-test.py` (202 lines,
runs four-mode routing tests) -- *"both run automatically"* in CI.

**Neither is invoked by anything.** Re-verified here: grepping their names across
`.github/`, `Makefile` and `.pre-commit-config.yaml` returns nothing. Ten
`tests.json` files ship and nothing executes them.

Two well-written gates, a doc asserting they run, and no caller. That is exactly
what `AGENTS.md` § Enforcement forbids -- *"a rule in this file is read; it is not
thereby enforced"* -- observed in a mature production repository. The method that
found it is the one worth keeping: **grep for the gate's name across everything
that could invoke it.** Neither repository ran that check on itself, and neither
has this one.

## Correction to an accepted plan

`plans/AGENT-HUB-CONSOLIDATION.md` § 6.2c proposes `adapters/` with `claude/`,
`codex/` and `generic/` beneath it (`DECISIONS.md` D-68). **Neither reference has
anything resembling a directory of adapter documents.** An adapter is either zero
artifacts (a symlink) or about 25 lines of code -- `BaseAgentInstaller` plus one
subclass per runtime with two methods, `get_install_path` and `format_content`.

Section 6 of that same plan already says not to create a directory because
another system uses the name. Applied honestly, it yields one manifest and one
script, not three subdirectories. Surfaced per the conflict rule; the taxonomy
owner decides.

**And Codex needs no projection at all.** Re-verified: Codex discovers skills
under `.agents/skills/`, which is the canonical tree itself. `.codex/skills/` is
deprecated.

## What is genuinely enforced there, ranked by what transfers here

| Mechanism | Where | Why it matters here |
|---|---|---|
| Regenerate then `git diff --exit-code` | `nemo-platform/.pre-commit-config.yaml` `config-reference-docs` | One line makes a generated doc unable to disagree with its source. `CATALOG.md` is 5.5 KB of hand-maintained inventory tracking a directory tree -- the exact artifact that should never be hand-written |
| Conservative default, machine-inserted, human-flipped | `gym/scripts/add_verified_flag.py` | Inserts `verified: false` into any new config lacking it and **exits 1**, so the author must re-stage. Only a human sets `true`, with `verified_url` carrying the evidence. This is our own evidence standard, expressed as a gate rather than as prose |
| Namespaced projections, gitignored by pattern | `nemo-platform/.gitignore` + `INSTALLED_SKILL_PREFIX` | A projected copy is named `nemo-*` and ignored by glob, so a generated artifact can never be committed as if it were source. Adopt regardless of anything else |
| Content-signature divergence is a hard error | `.../skills/registry.py` `_content_signature`, `DuplicateSkillError` | Equal signatures collapse, a strict superset wins, genuine divergence **names both paths and refuses**. Never picks a winner silently. We have two staged SSOT copies "pending placement" and nothing that would notice them diverging |
| Negative routing in one sentence | `gym/.agents/skills/nemo-gym-blade-analysis/SKILL.md` | *"For generic reward profiling, prefer X; for failed infrastructure jobs, prefer Y."* The highest-value frontmatter habit found, and it costs one sentence |

## What does not transfer

- **Python entry points as the plugin contract.** Requires an installed
  distribution. The Hub is a document store with no package or build. The
  contract *shape* transfers; the mechanism does not.
- **Sigstore skill signing and the three-tier benchmark.** Real in-toto DSSE
  envelopes signed by an NVIDIA CA, produced in a different repository, plus
  sandbox pods and two model endpoints. Do not attempt.
- **The full nine-field frontmatter spec.** Adopted by 20 of 72 skills in its own
  repo and enforced nowhere. Only `name`, `description` and `preconditions` are
  read by code. Copying it wholesale imports a standard neither repo meets.
- **Per-skill symlinks as the primary projection**, on our platform: git on
  Windows materialises a symlink as a text file containing its target unless
  `core.symlinks` is set, and it fails silently.

## What they do better than this repository's `AGENTS.md`

Measured: gym is 9.9 KB across 24 headings; ours is 17.2 KB across 14. Theirs
opens with what the agent should *do*; ours opens with an authority declaration
and a five-item bootstrap before the agent learns what the repository is for.
Theirs cite the exact file, command and failure; ours cite decision identifiers
that need a second lookup to mean anything.

**What we do better and should not give up:** the file-ownership table -- neither
reference has one, and nemo-platform is paying for it, with three files each
carrying a drifted copy of the same skills list. And the
enforcement-versus-instruction distinction, which is the rule that catches the
defect at the top of this file.
