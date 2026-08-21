#!/usr/bin/env python3
"""UserPromptSubmit hook: read the authoritative plan position out of STATE.md.

WHY THIS EXISTS
---------------
Work was executed under step labels that belonged to other steps, and two
prerequisite steps were passed over without any error appearing (DECISIONS.md
D-73, D-74). The rule against naming a step from memory was then written into
AGENTS.md -- a rule that is read, not enforced. This hook removes the need to
recall: STATE.md's position table enters context on every prompt, so the
authoritative answer is present before any step is named.

CONTRACT
--------
stdin  : UserPromptSubmit hook JSON.
stdout : text added to the session context. Never blocks.
exit   : always 0. A failure here must never stop work, so every error path
         emits a visible NOT READ notice instead of an exception.

Read-only. This tool writes nothing.
"""

import json
import os
import subprocess
import sys

MAX_CHARS = 3000


def repo_root(cwd):
    """Return the git top level for cwd, or None."""
    try:
        out = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            cwd=cwd, capture_output=True, text=True, timeout=10)
    except Exception:
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip() or None


def section(text, heading):
    """Return the body of a '## heading' section, up to the next '## '."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith('## ') and heading.lower() in line.lower():
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
    """Return (col1, col2) for each data row of the first markdown table."""
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) < 2:
            continue
        if set(cells[0]) <= set('-: '):
            continue
        if cells[0].lower().startswith('plan step'):
            continue
        if cells[0] == '#':
            continue
        rows.append((cells[0], cells[1]))
    return rows


def clip(text, limit=180):
    text = ' '.join(text.split())
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + ' [...]'


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
        # Not this repository. Say nothing rather than guess.
        return 0
    try:
        with open(state_path, 'r', encoding='utf-8') as handle:
            text = handle.read()
    except Exception as exc:
        print('POSITION NOT READ: STATE.md could not be opened (%s). '
              'Do not name a plan step until it has been read.' % exc)
        return 0

    out = []
    out.append('<!-- injected by .claude/hooks/inject_plan_position.py, '
               'read from STATE.md at prompt time -->')
    out.append('AUTHORITATIVE PLAN POSITION, read from STATE.md just now. '
               'This outranks recollection. Do not name a step, phase or '
               'position from memory (AGENTS.md, DECISIONS.md D-73/D-74).')

    body = section(text, 'Position in the plan sequence')
    if body is None:
        out.append('POSITION NOT READ: no "Position in the plan sequence" '
                   'section in STATE.md. Read the file before naming a step.')
    else:
        rows = table_rows(body)
        if not rows:
            out.append('POSITION NOT READ: the section holds no table rows.')
        else:
            out.append('')
            out.append('Plan step -> state:')
            for name, state in rows:
                out.append('  %s -- %s' % (name, clip(state, 80)))

    blockers = section(text, 'Blockers')
    if blockers:
        rows = table_rows(blockers)
        out.append('')
        if rows:
            out.append('Blockers on record (struck-through rows are closed):')
            for name, effect in rows:
                out.append('  %s -- %s' % (name, clip(effect)))
        else:
            out.append('Blockers, first lines:')
            for line in first_lines(blockers, 4):
                out.append('  ' + line)

    nxt = section(text, 'Next action')
    if nxt:
        out.append('')
        out.append('Next action, first lines:')
        for line in first_lines(nxt, 5):
            out.append('  ' + line)

    out.append('')
    out.append('Issue register: github.com/klodebeers/workspace-governor/issues '
               '-- every open item is filed there.')

    rendered = '\n'.join(out)
    if len(rendered) > MAX_CHARS:
        rendered = rendered[:MAX_CHARS] + '\n  [truncated -- read STATE.md]'
    print(rendered)
    return 0


if __name__ == '__main__':
    sys.exit(main())
