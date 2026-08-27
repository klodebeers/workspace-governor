#!/usr/bin/env python3
"""UserPromptSubmit hook: put the rule that governs this prompt in front of it.

WHY THIS EXISTS
---------------
The bootstrap in AGENTS.md asks an agent to read ~259 KB before it acts, and
that set carries 121 self-correcting statements. Under context pressure what
survives compression is the narrative, not the current rule -- which is how work
came to be executed under step labels belonging to other steps (D-73). Reading
more governance does not fix a drift caused by too much governance.

inject_plan_position.py and inject_delegation_check.py already answer this, for
two rules: put the authoritative text in context at the moment it applies, so
the answer arrives before the question. This generalises that to a table.

WHAT IT DOES NOT DO
-------------------
It cannot refuse anything. Injection is the advisory half of an enforcement
carrier; the refusing half is a gate (DECISIONS.md C-03, D-74, and
.claude/hooks/README.md). Adding an entry to the table enforces nothing.

WHY THE TABLE HOLDS NO RULE TEXT
--------------------------------
Each entry names an owning file and an exact heading, and the section is read
live when the trigger fires. A copy here would be a second owner of the rule --
forbidden by AGENTS.md File ownership -- and would drift with no error. What can
rot is a heading, and Assert-RuleTriggerFidelity.py refuses a commit when one
stops resolving.

Headings are matched EXACTLY after normalisation, never by substring. Substring
matching is a defect this repository has already paid for: `section()` in
inject_plan_position.py matched `## Current state and blockers` for a request for
`## Blockers`, and the real section was silently never read.

GOVERNANCE ROOT
---------------
Resolution order: $WG_RULES_ROOT, else the enclosing git worktree. The override
exists so this same hook can later be installed at user scope against a
governance root that is not the current repository, without a rewrite. Until
that root is verified to load (see evidence/USER-SCOPE-HOOK-CARRIER), this hook
governs only sessions whose working directory is inside this repository.

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

TABLE_NAME = 'rule-triggers.json'
FALLBACK_ENTRY_CHARS = 1400
FALLBACK_TOTAL_CHARS = 4200


def repo_root(cwd):
    override = os.environ.get('WG_RULES_ROOT')
    if override and os.path.isdir(override):
        return override
    try:
        out = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=cwd,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=10)
    except Exception:
        return None
    if out.returncode != 0:
        return None
    return out.stdout.decode('utf-8', 'replace').strip() or None


def normalise(text):
    """Heading text reduced to what a match should ignore: level, case, spacing.

    Dash forms are folded together because the same heading is written with an
    ASCII `--` in one file and an em dash in another, and a table entry should
    not have to know which.
    """
    text = text.strip().lstrip('#').strip()
    text = text.replace('—', '--').replace('–', '--')
    text = re.sub(r'\s+', ' ', text)
    return text.casefold().rstrip(' .:')


def section(path, heading):
    """Return the body under an exactly-matching heading, or None.

    None means "not found", and every caller must surface that rather than
    substituting silence: a rule that did not load must say so.
    """
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as handle:
            lines = handle.read().splitlines()
    except Exception:
        return None
    want = normalise(heading)
    start = None
    depth = 0
    for index, line in enumerate(lines):
        match = re.match(r'^(#{1,6})\s+(.*)$', line)
        if not match:
            continue
        if start is None:
            if normalise(match.group(2)) == want:
                start = index + 1
                depth = len(match.group(1))
            continue
        if len(match.group(1)) <= depth:
            return '\n'.join(lines[start:index]).strip()
    if start is None:
        return None
    return '\n'.join(lines[start:]).strip()


def clip(text, limit):
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit('\n', 1)[0].rstrip()
    return cut + '\n[... trimmed to %d chars; read the section in full ...]' % limit


def load_table(root):
    path = os.path.join(root, '.claude', 'hooks', TABLE_NAME)
    try:
        with open(path, 'r', encoding='utf-8') as handle:
            return json.load(handle), None
    except FileNotFoundError:
        return None, 'no %s found at %s' % (TABLE_NAME, path)
    except Exception as exc:
        return None, '%s is unreadable: %s' % (TABLE_NAME, exc)


def selected(entries, prompt):
    for entry in entries:
        if entry.get('always'):
            yield entry
            continue
        triggers = entry.get('triggers') or ()
        for pattern in triggers:
            try:
                hit = re.search(pattern, prompt, re.I)
            except re.error:
                hit = None
            if hit:
                yield entry
                break


def render(root, entry, entry_cap):
    source = '%s > %s' % (entry.get('file'), entry.get('heading'))
    body = section(os.path.join(root, entry.get('file', '')),
                   entry.get('heading', ''))
    if body is None:
        return ('RULE NOT READ -- %s did not resolve. The rule it carries is not\n'
                'in front of you; do not treat its absence as permission.\n'
                % source)
    head = 'RULE IN SCOPE -- %s' % source
    why = entry.get('why')
    if why:
        head += '\n(why now: %s)' % why
    return '%s\n\n%s\n' % (head, clip(body, entry_cap))


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    prompt = payload.get('user_prompt') or ''
    cwd = payload.get('cwd') or os.getcwd()
    root = repo_root(cwd)
    if not root:
        return 0
    table, error = load_table(root)
    if error:
        # Silent only when there is no table at all: this hook may be installed
        # against a root that does not use it. An unreadable table is different
        # and must be visible.
        if not error.startswith('no '):
            print('RULE TABLE NOT READ -- %s' % error)
        return 0
    entry_cap = int(table.get('max_chars_per_entry') or FALLBACK_ENTRY_CHARS)
    total_cap = int(table.get('max_chars_total') or FALLBACK_TOTAL_CHARS)
    chunks = []
    spent = 0
    withheld = []
    for entry in selected(table.get('entries') or (), prompt):
        piece = render(root, entry, entry_cap)
        if spent + len(piece) > total_cap:
            withheld.append(entry.get('id') or '?')
            continue
        chunks.append(piece)
        spent += len(piece)
    if not chunks:
        return 0
    print('<!-- injected by .claude/hooks/inject_rules.py -->')
    print('\n'.join(chunks))
    if withheld:
        print('WITHHELD for total length: %s. These rules apply and were not\n'
              'shown; read them before deciding.' % ', '.join(withheld))
    return 0


if __name__ == '__main__':
    sys.exit(main())
