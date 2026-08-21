#!/usr/bin/env python3
"""UserPromptSubmit hook: read the authoritative plan position out of STATE.md.

WHY THIS EXISTS
---------------
Work was executed under step labels belonging to other steps, and two
prerequisite steps were passed over with no error appearing (DECISIONS.md D-73,
D-74). AGENTS.md then forbade naming a step from memory -- a rule that is read,
not enforced. This removes the need to recall: STATE.md's position table enters
context on every prompt, so the authoritative answer arrives before the question.

CORRECTIONS FROM THE 2026-08-21 AUDIT
-------------------------------------
- `section()` matched a heading by substring, so `## Current state and blockers`
  captured the request for `## Blockers` and the real section was never read,
  silently. Headings are now matched exactly after normalisation.
- Long rows were clipped at 180 characters, which could cut off a `~~closed~~`
  marker and inject a closed blocker as an open one. A closed row is now
  labelled before it is clipped.
- Overall truncation dropped the tail, and the tail is the next action -- the
  single most decision-relevant part. The position table is now trimmed instead,
  and what was trimmed is named.
- A table header row was skipped only when it began with "plan step", so
  `| Step | Status |` was injected as a step called "Step".

CONTRACT
--------
stdin  : UserPromptSubmit hook JSON.  stdout : text added to session context.
exit   : always 0. A failure here must never stop work, so every error path
         emits a visible NOT READ notice instead of raising.
"""

import json
import os
import re
import subprocess
import sys

MAX_CHARS = 3000
HEADER_CELLS = frozenset(('#', 'plan step', 'step', 'blocker', 'item', 'id',
                          'name', 'file', 'path', 'trigger'))
CLOSED_MARKERS = ('~~', 'CLOSED', 'Closed', 'RESOLVED', 'Resolved')


def git(cwd, args):
    try:
        out = subprocess.run(['git'] + args, cwd=cwd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, timeout=10)
    except Exception:
        return 1, ''
    return out.returncode, out.stdout.decode('utf-8', 'replace').strip()


def repo_root(cwd):
    code, out = git(cwd, ['rev-parse', '--show-toplevel'])
    return out if code == 0 and out else None


def normalise(heading):
    return re.sub(r'[^a-z0-9 ]', '', heading.lower()).strip()


def section(text, heading):
    """Body of the '## heading' section whose title matches exactly."""
    want = normalise(heading)
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith('## ') and normalise(line[3:]) == want:
            start = i + 1
            break
    if start is None:
        return None
    body = []
    for line in lines[start:]:
        if line.startswith('## '):
            break
        body.append(line)
    return '\n'.join(body).strip()


def table_rows(body):
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) < 2 or set(cells[0]) <= set('-: '):
            continue
        if cells[0].lower() in HEADER_CELLS:
            continue
        rows.append((cells[0], cells[1]))
    return rows


def clip(text, limit=180):
    """Shorten a cell without hiding that its item is closed."""
    text = ' '.join(text.split())
    closed = any(m in text for m in CLOSED_MARKERS)
    if len(text) > limit:
        text = text[:limit].rstrip() + ' [...]'
    if closed and '~~' not in text[:12] and not text.startswith('[closed]'):
        text = '[closed] ' + text
    return text


def first_lines(body, count):
    out = []
    for line in body.splitlines():
        if line.strip():
            out.append(line.rstrip())
        if len(out) >= count:
            break
    return out


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    cwd = payload.get('cwd') or os.getcwd()
    root = repo_root(cwd)
    if not root:
        return 0
    state_path = os.path.join(root, 'STATE.md')
    if not os.path.isfile(state_path):
        return 0
    try:
        with open(state_path, 'r', encoding='utf-8') as handle:
            text = handle.read()
    except Exception as exc:
        print('POSITION NOT READ: STATE.md could not be opened (%s). Do not name '
              'a plan step until it has been read.' % exc)
        return 0

    head = ['<!-- injected by .claude/hooks/inject_plan_position.py, read from '
            'STATE.md at prompt time -->',
            'AUTHORITATIVE PLAN POSITION, read from STATE.md just now. This '
            'outranks recollection. Do not name a step, phase or position from '
            'memory (AGENTS.md, DECISIONS.md D-73/D-74).']

    steps = []
    body = section(text, 'Position in the plan sequence')
    if body is None:
        steps.append('POSITION NOT READ: no section titled exactly "Position in '
                     'the plan sequence" in STATE.md. Read the file before naming '
                     'a step.')
    else:
        rows = table_rows(body)
        if not rows:
            steps.append('POSITION NOT READ: that section holds no table rows.')
        else:
            steps.append('')
            steps.append('Plan step -> state:')
            for name, state in rows:
                steps.append('  %s -- %s' % (name, clip(state, 80)))

    blockers = []
    blocker_body = section(text, 'Blockers')
    if blocker_body:
        rows = table_rows(blocker_body)
        blockers.append('')
        if rows:
            blockers.append('Blockers on record:')
            for name, effect in rows:
                blockers.append('  %s -- %s' % (name, clip(effect)))
        else:
            blockers.append('Blockers, first lines:')
            for line in first_lines(blocker_body, 4):
                blockers.append('  ' + line)

    tail = []
    nxt = section(text, 'Next action')
    if nxt:
        tail.append('')
        tail.append('Next action, first lines:')
        for line in first_lines(nxt, 5):
            tail.append('  ' + line)
    tail.append('')
    tail.append('Issue register: github.com/klodebeers/workspace-governor/issues '
                '-- every open item is filed there.')

    # The next action is never the part that gets dropped: trim the step table.
    def render(step_lines, blocker_lines):
        return '\n'.join(head + step_lines + blocker_lines + tail)

    trimmed = 0
    step_lines, blocker_lines = list(steps), list(blockers)
    while len(render(step_lines, blocker_lines)) > MAX_CHARS:
        if len(step_lines) > 3:
            step_lines.pop(-1)
            trimmed += 1
            continue
        if len(blocker_lines) > 2:
            blocker_lines.pop(-1)
            trimmed += 1
            continue
        break
    if trimmed:
        step_lines.append('  [%d row(s) trimmed to fit -- read STATE.md for the '
                          'full table]' % trimmed)
    print(render(step_lines, blocker_lines))
    return 0


if __name__ == '__main__':
    sys.exit(main())
