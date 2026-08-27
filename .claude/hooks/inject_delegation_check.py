#!/usr/bin/env python3
"""UserPromptSubmit hook: put the delegation criteria in front of the decision.

WHAT RULE THIS CARRIES
----------------------
`rules/VERIFICATION-RESOLUTION.md` § Performer selection. The rule is read once
and applied from memory afterwards, which is how it came to be followed only when
someone asked. This puts the two required-delegation conditions into context at
the moment a prompt is about reviewing, auditing or verifying -- so the choice is
made in front of the rule rather than from a recollection of it.

It is guidance, not a gate: it cannot refuse anything. The refusal half lives in
`gate_delegation.py`, which catches a claim of independent review with no
delegate behind it. Neither can judge whether delegation was warranted.

WHY IT IS CONDITIONAL
---------------------
Injecting this on every prompt would make it wallpaper. It fires only when the
prompt is plausibly about the work the rule governs.

CONTRACT
--------
stdin  : UserPromptSubmit hook JSON.  stdout : text added to session context.
exit   : always 0. This must never block a prompt.
"""

import json
import os
import re
import subprocess
import sys

TRIGGERS = (
    r'\breview', r'\baudit', r'\bverif', r'\bvalidat', r'\bdouble[- ]check',
    r'\bcheck (?:my|your|the) work', r'\bsecond opinion', r'\bcritique',
    r'\bassess', r'\bsanity[- ]check', r'\bconfirm (?:that|it|this|whether)',
    r'\bis (?:it|this) (?:correct|right|complete)', r'\bare (?:you|we) sure',
    r'\bsign off', r'\bproof', r'\bprove\b', r'\badversarial',
)

NOTICE = """<!-- injected by .claude/hooks/inject_delegation_check.py -->
PERFORMER CHECK -- this prompt looks like review, audit or verification work.
rules/VERIFICATION-RESOLUTION.md, Performer selection, requires a delegate rather
than inline work when either of these holds:

  1. The work reviews, audits or adversarially checks something THIS session
     produced. Self-review cannot supply independence: the reviewer has already
     reached the conclusion under review. The delegate gets the authoritative
     source, the approved scope and the result, and is denied your rationale
     (DECISIONS.md D-60).
  2. A clean result from a check this session authored would be the basis for a
     completion claim. The author of a check is the worst judge of whether it
     checks anything (D-65).

Neither applies to: sequential work, edits to the same file, work with many
dependencies, or one fact whose location is already known.

Three things delegation never does. It does not transfer the obligation -- every
finding is verified against the source before it is accepted OR rejected. It does
not launder a refusal. And a delegate told the conclusion has produced a rubber
stamp, not a review.

A claim of independent review with no delegate in the record is refused at the end
of the session. Saying plainly that you checked your own work is always available
and is a different claim."""


def repo_root(cwd):
    try:
        out = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=cwd,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=10)
    except Exception:
        return None
    if out.returncode != 0:
        return None
    return out.stdout.decode('utf-8', 'replace').strip() or None


def prompt_text(payload):
    """The submitted prompt, under the key the CLI actually sends.

    The CLI builds a UserPromptSubmit payload as
    `{session_id, transcript_path, cwd, permission_mode, hook_event_name, prompt}`.
    `user_prompt` is a telemetry attribute and has never been a payload key, so a
    hook reading it saw an empty string and every trigger missed -- silently, and
    in the safe-looking direction: no output is indistinguishable from no match.
    Both keys are accepted so a payload shape change cannot re-break this quietly,
    and test_hooks.py asserts the CLI shape specifically.
    """
    text = payload.get('prompt')
    if text is None:
        text = payload.get('user_prompt')
    # A non-string prompt reached re.search and raised TypeError, exit 1, against
    # this module's stated never-raise contract. The payload is external input;
    # its shape is not ours to assume.
    return text if isinstance(text, str) else ''


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    cwd = payload.get('cwd') or os.getcwd()
    root = repo_root(cwd)
    if not root:
        return 0
    if not os.path.isfile(os.path.join(root, 'rules',
                                       'VERIFICATION-RESOLUTION.md')):
        return 0
    prompt = prompt_text(payload)
    if not prompt:
        return 0
    if not any(re.search(t, prompt, re.I) for t in TRIGGERS):
        return 0
    print(NOTICE)
    return 0


if __name__ == '__main__':
    sys.exit(main())
