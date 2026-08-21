#!/usr/bin/env python3
"""Stop hook: refuse to end a session with governed changes uncommitted.

AGENTS.md states the persistence requirement: durable project information is
written to this repository in the same working session, and "a session that
establishes a decision or a material finding and ends without recording it has
failed, regardless of what else it produced." This is the mechanical half of it.

WHAT IT KNOWS AND WHAT IT DOES NOT
----------------------------------
It cannot know whether a decision was settled -- that is judgement. It knows
that governed files were modified and never committed, and it reports exactly
that.

CORRECTIONS FROM THE 2026-08-21 AUDIT
-------------------------------------
- The marker path was built as `<root>/.git/...`. In a linked worktree `.git` is
  a file, the write raised, and the except-return-0 path disabled the gate
  completely. It now asks git for the path.
- The governed list omitted `AGENT-SSOT.json` and `USER-SSOT.json`, which the
  AGENTS.md ownership table names. An uncommitted change to either passed.
- The loop guard hashed status letters and paths, so replacing a dirty file's
  contents entirely reused the marker and the gate stayed quiet. It now hashes
  the content.

KNOWN LIMIT, NOT A SKIP
-----------------------
`git stash` makes a dirty tree clean, and this gate then permits the stop. The
work is preserved but unpersisted, which is the failure the gate exists to catch.
No mechanism here detects it; it is stated rather than glossed.

CONTRACT
--------
stdin  : Stop hook JSON.  exit 0 : clean, out of scope, or already raised.
exit 2 : governed files are dirty; stderr names them.
"""

import hashlib
import json
import os
import re
import subprocess
import sys

GOVERNED_PREFIXES = (
    'plans/', 'evidence/', 'rules/', '_intake-hub/', 'scripts/', '.claude/',
    '.githooks/',
)
GOVERNED_ROOT_FILES = (
    'AGENTS.md', 'CLAUDE.md', 'STATE.md', 'DECISIONS.md', 'LEARNINGS.md',
    'README.md', 'PENDING.md', 'PENDING-GLOBAL-PROMOTIONS.md',
    'AGENT-SSOT.json', 'USER-SSOT.json', '.gitignore',
)
MAX_UNTRACKED_HASH_BYTES = 2 * 1024 * 1024


def git(root, args):
    try:
        out = subprocess.run(['git'] + args, cwd=root, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, timeout=60)
    except Exception:
        return 1, b''
    return out.returncode, out.stdout


def repo_root(cwd):
    code, out = git(cwd, ['rev-parse', '--show-toplevel'])
    if code != 0:
        return None
    return out.decode('utf-8', 'replace').strip() or None


def marker_path(root, session):
    """Ask git where to write, so a linked worktree works."""
    code, out = git(root, ['rev-parse', '--git-path', 'wg-stop-gate-%s' % session])
    if code != 0:
        return None
    rel = out.decode('utf-8', 'replace').strip()
    if not rel:
        return None
    return rel if os.path.isabs(rel) else os.path.join(root, rel)


def is_governed(path):
    return path in GOVERNED_ROOT_FILES or path.startswith(GOVERNED_PREFIXES)


def dirty_entries(root):
    code, out = git(root, ['status', '--porcelain', '-z'])
    if code != 0:
        return None
    entries = []
    fields = out.split(b'\x00')
    i = 0
    while i < len(fields):
        field = fields[i]
        if len(field) < 4:
            i += 1
            continue
        status = field[:2].decode('ascii', 'replace')
        path = field[3:].decode('utf-8', 'surrogateescape')
        if status[0] in 'RC':
            # rename/copy: the origin path follows as its own NUL-separated field
            i += 1
        entries.append((status.strip(), path))
        i += 1
    return [(s, p) for s, p in entries if is_governed(p)]


def content_fingerprint(root, dirty):
    """Hash the actual changes, not the status letters."""
    digest = hashlib.sha256()
    for status, path in sorted(dirty):
        digest.update(('%s %s\n' % (status, path)).encode('utf-8', 'replace'))
    code, out = git(root, ['diff', 'HEAD'])
    if code == 0:
        digest.update(out)
    for status, path in sorted(dirty):
        if '?' not in status:
            continue
        full = os.path.join(root, path)
        try:
            if os.path.isfile(full) \
                    and os.path.getsize(full) <= MAX_UNTRACKED_HASH_BYTES:
                with open(full, 'rb') as handle:
                    digest.update(handle.read())
        except Exception:
            digest.update(b'<unreadable>')
    return digest.hexdigest()


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    cwd = payload.get('cwd') or os.getcwd()
    root = repo_root(cwd)
    if not root:
        return 0
    if not (os.path.isfile(os.path.join(root, 'DECISIONS.md'))
            and os.path.isfile(os.path.join(root, 'STATE.md'))):
        return 0

    dirty = dirty_entries(root)
    if dirty is None:
        sys.stderr.write('PERSISTENCE GATE COULD NOT RUN: git status failed, so '
                         'whether governed work is uncommitted is unknown. Check '
                         'by hand before ending the session.\n')
        return 2
    if not dirty:
        return 0

    session = re.sub(r'[^A-Za-z0-9_.-]', '_',
                     str(payload.get('session_id') or 'nosession'))[:64]
    fingerprint = content_fingerprint(root, dirty)
    marker = marker_path(root, session)
    if marker:
        try:
            if os.path.isfile(marker):
                with open(marker, 'r', encoding='utf-8') as handle:
                    if handle.read().strip() == fingerprint:
                        return 0
            with open(marker, 'w', encoding='utf-8') as handle:
                handle.write(fingerprint)
        except Exception:
            pass          # unwritable marker means it nags again, never that it stops

    sys.stderr.write(
        'PERSISTENCE GATE: %d governed file(s) changed and not committed.\n\n'
        % len(dirty))
    for status, path in dirty:
        sys.stderr.write('  %-3s %s\n' % (status or '??', path))
    sys.stderr.write(
        '\nAGENTS.md: durable project information must be written to this '
        'repository in the same working session, not left in session state.\n'
        'Commit what is durable, or state plainly why it is not being kept.\n'
        'This exact set is raised once; changing the content raises it again.\n')
    return 2


if __name__ == '__main__':
    sys.exit(main())
