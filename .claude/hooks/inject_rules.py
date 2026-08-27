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


def pointer(source, size, limit):
    """What to say when a section will not fit.

    NEVER a prefix. A truncated prohibition is worse than no prohibition: the
    surviving half arrives under an authoritative header, so the agent that
    would have opened the file now has something that looks like the answer.
    Measured on this repository, a 1400-char prefix of STATE.md Stop conditions
    dropped the approval boundary -- the one condition standing between an agent
    and an unapproved change to live governance -- and a prefix of the ownership
    table dropped 11 of its rows plus the STATE/DECISIONS tiebreak, which is the
    two-differing-versions defect the table exists to forbid.

    Stop conditions and ownership tables are also APPENDED to, so a tail-trim
    always drops the newest rule.
    """
    return ('RULE IN SCOPE -- %s\n'
            'Too large to quote (%d chars, cap %d). It is NOT reproduced here, '
            'because half a prohibition reads as the whole one.\n'
            'READ THE SECTION before deciding.\n' % (source, size, limit))


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
    """Entries the prompt actually matched first, always-on entries last.

    Order decides eviction when the total cap is reached, and file order gave
    the always-on entry -- which matched nothing -- priority over entries that
    matched the prompt's own words. Measured: a prompt naming intake and
    DECISIONS.md had both of those evicted by the entry that matched nothing.
    """
    matched, unconditional = [], []
    for entry in entries:
        if entry.get('always'):
            unconditional.append(entry)
            continue
        triggers = entry.get('triggers')
        if isinstance(triggers, str) or not isinstance(triggers, (list, tuple)):
            continue          # a bare string iterates per CHARACTER; the gate
                              # refuses this shape, and the hook will not guess
        for pattern in triggers:
            try:
                hit = re.search(pattern, prompt, re.I)
            except re.error:
                hit = None
            if hit:
                matched.append(entry)
                break
    for entry in matched + unconditional:
        yield entry


def render(root, entry, entry_cap):
    source = '%s > %s' % (entry.get('file'), entry.get('heading'))
    if not inside(root, entry.get('file')):
        return ('RULE NOT READ -- %s is outside the governance root and was not\n'
                'read. Do not treat its absence as permission.\n' % source)
    body = section(os.path.join(root, entry.get('file', '')),
                   entry.get('heading', ''))
    if not body:
        return ('RULE NOT READ -- %s did not resolve. The rule it carries is not\n'
                'in front of you; do not treat its absence as permission.\n'
                % source)
    if len(body) > entry_cap:
        return pointer(source, len(body), entry_cap)
    head = 'RULE IN SCOPE -- %s' % source
    why = entry.get('why')
    if why:
        head += '\n(why now: %s)' % why
    return '%s\n\n%s\n' % (head, body)


def positive_int(value, fallback):
    """A cap the table got wrong must not crash the hook on every prompt.

    int('lots') raised ValueError straight out of main(), so one bad edit to the
    table produced a traceback on every single prompt until someone read a hook
    log. A negative cap was worse: a valid int that withheld everything silently.
    """
    if value is None:
        return fallback, []
    try:
        number = int(value)
    except (TypeError, ValueError):
        return fallback, ['%r is not a number' % (value,)]
    if number <= 0:
        return fallback, ['%r is not positive' % (value,)]
    return number, []


def inside(root, name):
    """True when `name` stays inside `root`.

    The table decides what file content reaches the model. os.path.join throws
    the root away for an absolute path, and `../` walks out, so an entry could
    inject any file on the machine into every prompt. Confine it here and refuse
    it in the gate, rather than trusting the table.
    """
    if not isinstance(name, str) or not name:
        return False
    if os.path.isabs(name) or (len(name) > 1 and name[1] == ':'):
        return False
    target = os.path.normpath(os.path.join(root, name))
    prefix = os.path.normpath(root) + os.sep
    return (target + os.sep).startswith(prefix)


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
    if not isinstance(payload, dict):
        return 0
    prompt = prompt_text(payload)
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
    entry_cap, entry_bad = positive_int(table.get('max_chars_per_entry'),
                                       FALLBACK_ENTRY_CHARS)
    total_cap, total_bad = positive_int(table.get('max_chars_total'),
                                        FALLBACK_TOTAL_CHARS)
    marker = '<!-- injected by .claude/hooks/inject_rules.py -->'
    chunks = []
    spent = len(marker) + 1        # the marker is printed; count it
    withheld = []
    entries = table.get('entries')
    if not isinstance(entries, list):
        print('RULE TABLE NOT READ -- entries is not a list')
        return 0
    entries = [e for e in entries if isinstance(e, dict)]
    for entry in selected(entries, prompt):
        piece = render(root, entry, entry_cap)
        if spent + len(piece) > total_cap:
            withheld.append(entry.get('id') or '?')
            continue
        chunks.append(piece)
        spent += len(piece)
    if not chunks and not withheld:
        return 0
    print(marker)
    if entry_bad or total_bad:
        print('RULE TABLE CAP IGNORED -- %s. Falling back to %d/%d.'
              % (', '.join(entry_bad + total_bad), entry_cap, total_cap))
    if chunks:
        print('\n'.join(chunks))
    if withheld:
        print('WITHHELD for total length: %s. These rules apply and were not\n'
              'shown; read them before deciding.' % ', '.join(withheld))
    return 0


if __name__ == '__main__':
    sys.exit(main())
