#!/usr/bin/env python3
"""Stop gate: a claim of independent review needs an independent performer.

WHAT RULE THIS ENFORCES
-----------------------
`rules/VERIFICATION-RESOLUTION.md` § Performer selection: review, audit or
adversarial checking of this session's own work is delegated, not done inline,
and "a claim that work was independently reviewed, audited or adversarially
checked requires an independent performer in the record."

WHY A GATE AND NOT A REMINDER
-----------------------------
The rule existed as practice before it existed as text, and it was followed when
someone asked for it and skipped otherwise. What is mechanically visible is not
whether delegation was warranted -- that is judgement, and a gate does not have
it -- but whether a session that *claims* an independent review actually ran one.
That claim is checkable against the transcript, and a false one is worse than no
review at all, because it is a false statement about method.

WHAT IT CANNOT DO
-----------------
It cannot see work that should have been delegated and was not, because no
documented hook fires on that. It catches the claim, not the omission. Stated
here so the gap is not mistaken for coverage.

CONTRACT
--------
stdin  : Stop hook JSON, with `last_assistant_message` and `transcript_path`.
exit 0 : no claim made, or a claim with a delegate behind it.
exit 2 : a claim with no delegate in the transcript, or a claim that could not be
         checked. Raised once per session per message.
"""

import hashlib
import json
import os
import re
import subprocess
import sys

# Tool names that spawn a separate agent with its own context.
DELEGATE_TOOLS = frozenset(('Agent', 'Task', 'Workflow'))

CLAIM_PATTERNS = (
    r'independent(?:ly)?\s+(?:review|audit|verif|check)',
    r'independent\s+(?:review|audit|verification|check|auditor|reviewer)',
    r'adversarial(?:ly)?\s+(?:review|audit|verif|check)',
    r'blind\s+(?:review|audit)',
    r'(?:review|audit)ed\s+independently',
    r'second\s+pair\s+of\s+eyes',
)

# An honest statement that no independent review happened must not be refused --
# saying so plainly is what the rule asks for when nothing was delegated.
DISCLAIMER_PATTERNS = (
    r'no\s+independent',
    r'not\s+independent(?:ly)?',
    r'without\s+(?:an\s+)?independent',
    r'reviewed\s+my\s+own',
    r'self[- ]review',
    r'checked\s+my\s+own',
    r'no\s+delegate',
    r'no\s+subagent',
)


def git(cwd, args):
    try:
        out = subprocess.run(['git'] + args, cwd=cwd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, timeout=30)
    except Exception:
        return 1, ''
    return out.returncode, out.stdout.decode('utf-8', 'replace').strip()


def repo_root(cwd):
    code, out = git(cwd, ['rev-parse', '--show-toplevel'])
    return out if code == 0 and out else None


def claims_independence(message):
    if not message:
        return None
    for pattern in DISCLAIMER_PATTERNS:
        if re.search(pattern, message, re.I):
            return None
    for pattern in CLAIM_PATTERNS:
        found = re.search(pattern, message, re.I)
        if found:
            return found.group(0)
    return None


def count_delegates(transcript_path):
    """Return the number of delegate spawns, or None when it cannot be read."""
    if not transcript_path or not os.path.isfile(transcript_path):
        return None
    count = 0
    try:
        with open(transcript_path, 'r', encoding='utf-8', errors='replace') as handle:
            for line in handle:
                line = line.strip()
                if not line or '"tool_use"' not in line:
                    continue
                try:
                    record = json.loads(line)
                except Exception:
                    # A malformed line is not proof of absence; fall back to a
                    # textual match rather than silently counting zero.
                    if any('"name": "%s"' % t in line or '"name":"%s"' % t in line
                           for t in DELEGATE_TOOLS):
                        count += 1
                    continue
                count += count_in(record)
    except Exception:
        return None
    return count


def count_in(node):
    """Walk a transcript record for tool_use blocks naming a delegate tool."""
    found = 0
    if isinstance(node, dict):
        if node.get('type') == 'tool_use' and node.get('name') in DELEGATE_TOOLS:
            found += 1
        for value in node.values():
            found += count_in(value)
    elif isinstance(node, list):
        for item in node:
            found += count_in(item)
    return found


def marker_path(root, session):
    code, out = git(root, ['rev-parse', '--git-path',
                           'wg-delegation-gate-%s' % session])
    if code != 0 or not out:
        return None
    return out if os.path.isabs(out) else os.path.join(root, out)


def already_raised(marker, fingerprint):
    if not marker:
        return False
    try:
        if os.path.isfile(marker):
            with open(marker, 'r', encoding='utf-8') as handle:
                if handle.read().strip() == fingerprint:
                    return True
        with open(marker, 'w', encoding='utf-8') as handle:
            handle.write(fingerprint)
    except Exception:
        return False
    return False


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
        return 0        # not a repository this rule is held in

    message = payload.get('last_assistant_message') or ''
    claim = claims_independence(message)
    if not claim:
        return 0        # nothing claimed, so nothing to check

    delegates = count_delegates(payload.get('transcript_path'))

    session = re.sub(r'[^A-Za-z0-9_.-]', '_',
                     str(payload.get('session_id') or 'nosession'))[:64]
    fingerprint = hashlib.sha256(
        ('%s|%s' % (claim, message)).encode('utf-8', 'replace')).hexdigest()
    marker = marker_path(root, session)

    if delegates is None:
        if already_raised(marker, fingerprint):
            return 0
        sys.stderr.write(
            'DELEGATION GATE COULD NOT RUN: this message claims %r, and the '
            'transcript could not be read to confirm a delegate performed it. A '
            'check that cannot run fails rather than passing (LEARNINGS.md '
            'L-026). Either name who performed the review, or say plainly that '
            'you checked your own work.\n' % claim)
        return 2

    if delegates > 0:
        return 0

    if already_raised(marker, fingerprint):
        return 0
    sys.stderr.write(
        'DELEGATION GATE: this message claims %r, and no delegate ran in this '
        'session.\n\n'
        'rules/VERIFICATION-RESOLUTION.md, Performer selection: a claim that work '
        'was independently reviewed, audited or adversarially checked requires an '
        'independent performer in the record. An agent reviewing its own work has '
        'already reached the conclusion under review.\n\n'
        'Two honest ways forward. Delegate the review -- the delegate gets the '
        'source, the approved scope and the result, and is denied your rationale '
        '(DECISIONS.md D-60). Or say plainly that you checked your own work, which '
        'is a different claim and is worth making accurately.\n' % claim)
    return 2


if __name__ == '__main__':
    sys.exit(main())
