#!/usr/bin/env python3
"""Stop hook: refuse to end a session with governed changes uncommitted.

WHY THIS EXISTS
---------------
AGENTS.md states the persistence requirement: durable project information is
written to this repository in the same working session, and "a session that
establishes a decision or a material finding and ends without recording it has
failed, regardless of what else it produced." That was a rule with nothing
behind it. This hook makes the end of a session the point where an unwritten
change is caught, while the context that produced it still exists.

WHAT IT CAN AND CANNOT KNOW
---------------------------
It cannot know whether a decision was settled -- that is a judgement. It can
know that governed files were modified and never committed, which is the
mechanical half of the same failure. It reports exactly that and nothing more.

CONTRACT
--------
stdin  : Stop hook JSON.
exit 0 : clean tree, not this repository, or this exact set was already raised.
exit 2 : governed files are dirty. stderr names them.

LOOP GUARD
----------
The same dirty set is raised once per session. The marker lives in
.git/wg-stop-gate-<session>, so a second Stop with nothing changed proceeds --
the gate reports, it does not trap.
"""

import hashlib
import json
import os
import re
import subprocess
import sys

GOVERNED_PREFIXES = (
    'plans/', 'evidence/', 'rules/', '_intake-hub/', 'scripts/', '.claude/',
)
GOVERNED_ROOT_FILES = (
    'AGENTS.md', 'CLAUDE.md', 'STATE.md', 'DECISIONS.md', 'LEARNINGS.md',
    'README.md', 'PENDING.md', 'PENDING-GLOBAL-PROMOTIONS.md',
)


def git(root, args):
    try:
        out = subprocess.run(['git'] + args, cwd=root, capture_output=True,
                             text=True, timeout=30)
    except Exception:
        return 1, ''
    return out.returncode, out.stdout


def repo_root(cwd):
    code, out = git(cwd, ['rev-parse', '--show-toplevel'])
    if code != 0:
        return None
    return out.strip() or None


def is_governed(path):
    if path in GOVERNED_ROOT_FILES:
        return True
    return path.startswith(GOVERNED_PREFIXES)


def porcelain_paths(root):
    """Return (status, path) for every entry, resolving renames to the target."""
    code, out = git(root, ['status', '--porcelain'])
    if code != 0:
        return []
    entries = []
    for line in out.splitlines():
        if len(line) < 4:
            continue
        status = line[:2]
        rest = line[3:]
        if ' -> ' in rest:
            rest = rest.split(' -> ', 1)[1]
        entries.append((status.strip(), rest.strip().strip('"')))
    return entries


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    cwd = payload.get('cwd') or os.getcwd()
    root = repo_root(cwd)
    if not root:
        return 0
    # Only this repository carries the persistence requirement.
    if not (os.path.isfile(os.path.join(root, 'DECISIONS.md'))
            and os.path.isfile(os.path.join(root, 'STATE.md'))):
        return 0

    dirty = [(st, path) for st, path in porcelain_paths(root)
             if is_governed(path)]
    if not dirty:
        return 0

    fingerprint = hashlib.sha256(
        '\n'.join(sorted('%s %s' % (st, p) for st, p in dirty)).encode('utf-8')
    ).hexdigest()
    session = re.sub(r'[^A-Za-z0-9_.-]', '_',
                     str(payload.get('session_id') or 'nosession'))[:64]
    marker = os.path.join(root, '.git', 'wg-stop-gate-%s' % session)
    try:
        if os.path.isfile(marker):
            with open(marker, 'r', encoding='utf-8') as fh:
                if fh.read().strip() == fingerprint:
                    return 0
        with open(marker, 'w', encoding='utf-8') as fh:
            fh.write(fingerprint)
    except Exception:
        # A marker that cannot be written must not turn the gate into a trap.
        return 0

    sys.stderr.write(
        'PERSISTENCE GATE: %d governed file(s) changed and not committed.\n\n'
        % len(dirty))
    for status, path in dirty:
        sys.stderr.write('  %-3s %s\n' % (status or '??', path))
    sys.stderr.write(
        '\nAGENTS.md: durable project information must be written to this '
        'repository in the same working session, not left in session state.\n'
        'Commit what is durable, or state plainly why it is not being kept.\n'
        'This set is raised once -- a second stop with the same set proceeds.\n')
    return 2


if __name__ == '__main__':
    sys.exit(main())
