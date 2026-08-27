#!/usr/bin/env python3
"""Refuse a rule-trigger table whose entries no longer resolve.

WHY THIS EXISTS
---------------
`.claude/hooks/rule-triggers.json` names an owning file and an exact heading per
entry, and `inject_rules.py` reads that section live. That design removes the
second copy of a rule, but it moves the failure: a renamed or deleted heading
makes the hook inject a NOT READ notice instead of the rule, and a table full of
those is indistinguishable from a table that is working.

LEARNINGS.md L-027 is the reason this is a committed verifier rather than a
claim: a generator that has been thrown away proves nothing, while a verifier
re-reads both sides on demand.

It deliberately imports the matcher from the hook itself. A checker that
reimplements the thing it checks verifies its own copy, and the two drift --
which is L-026's defect class.

CHECKS
------
1. Every entry has an id, a file, a heading, and either `always` or `triggers`.
2. Ids are unique.
3. Every named file exists under the root.
4. Every heading resolves, exactly and case-insensitively, to a non-empty body.
5. Every heading resolves EXACTLY ONCE. Two identical headings in one file make
   the injected text depend on document order, which is silent ambiguity.
6. Every trigger pattern compiles as a regular expression.

USAGE
-----
    python3 scripts/Assert-RuleTriggerFidelity.py
    python3 scripts/Assert-RuleTriggerFidelity.py --selftest

Exit status 0 = all checks pass. Non-zero = at least one finding, or a check
that could not run. A check that cannot run fails; it never skips.
Read-only: this tool opens files for reading and writes nothing outside a
temporary directory used by --selftest.
"""

import json
import os
import re
import subprocess
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_HOOKS = os.path.join(os.path.dirname(_HERE), '.claude', 'hooks')
if _HOOKS not in sys.path:
    sys.path.insert(0, _HOOKS)

try:
    from inject_rules import normalise, section  # noqa: E402
except Exception as exc:  # pragma: no cover - surfaced, never swallowed
    # Raise rather than sys.exit: wg_gates.check_rule_triggers imports this
    # module, and SystemExit is not an Exception, so exiting here would tear
    # down the whole pre-commit run past its findings mechanism instead of
    # producing one finding. Running as __main__ still fails, below.
    if __name__ == '__main__':
        sys.stderr.write('cannot import the matcher from inject_rules.py: %s\n'
                         % exc)
        sys.stderr.write('The check cannot run, so it fails rather than passing.\n')
        sys.exit(2)
    raise ImportError('inject_rules.py is not importable: %s' % exc)


def repo_root():
    try:
        out = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=_HERE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=10)
    except Exception:
        return os.path.dirname(_HERE)
    if out.returncode != 0:
        return os.path.dirname(_HERE)
    return out.stdout.decode('utf-8', 'replace').strip() or os.path.dirname(_HERE)


def heading_count(path, heading):
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as handle:
            lines = handle.read().splitlines()
    except Exception:
        return 0
    want = normalise(heading)
    hits = 0
    for line in lines:
        match = re.match(r'^#{1,6}\s+(.*)$', line)
        if match and normalise(match.group(1)) == want:
            hits += 1
    return hits


def audit(root, table):
    findings = []
    seen = set()
    entries = table.get('entries')
    if not isinstance(entries, list) or not entries:
        return ['table has no entries']
    for position, entry in enumerate(entries):
        label = entry.get('id') or '#%d' % position
        if not entry.get('id'):
            findings.append('%s: no id' % label)
        elif entry['id'] in seen:
            findings.append('%s: duplicate id' % label)
        else:
            seen.add(entry['id'])
        name = entry.get('file')
        heading = entry.get('heading')
        if not name or not heading:
            findings.append('%s: entry needs both file and heading' % label)
            continue
        if not entry.get('always') and not entry.get('triggers'):
            findings.append('%s: needs either always or triggers' % label)
        for pattern in entry.get('triggers') or ():
            try:
                re.compile(pattern)
            except re.error as exc:
                findings.append('%s: trigger %r does not compile: %s'
                                % (label, pattern, exc))
        path = os.path.join(root, name)
        if not os.path.isfile(path):
            findings.append('%s: %s does not exist' % (label, name))
            continue
        hits = heading_count(path, heading)
        if hits == 0:
            findings.append('%s: heading %r not found in %s'
                            % (label, heading, name))
            continue
        if hits > 1:
            findings.append('%s: heading %r appears %d times in %s; the injected '
                            'text would depend on document order'
                            % (label, heading, hits, name))
            continue
        body = section(path, heading)
        if not body:
            findings.append('%s: heading %r in %s resolves to an empty section'
                            % (label, heading, name))
    return findings


def run(root):
    path = os.path.join(root, '.claude', 'hooks', 'rule-triggers.json')
    if not os.path.isfile(path):
        print('FAIL: no rule-triggers.json at %s' % path)
        return 2
    try:
        with open(path, 'r', encoding='utf-8') as handle:
            table = json.load(handle)
    except Exception as exc:
        print('FAIL: rule-triggers.json is unreadable: %s' % exc)
        return 2
    findings = audit(root, table)
    if findings:
        print('FAIL: %d finding(s)' % len(findings))
        for item in findings:
            print('  - %s' % item)
        return 1
    print('PASS: %d entries, every heading resolves exactly once'
          % len(table.get('entries') or ()))
    return 0


_CLEAN_DOC = '# Doc\n\n## Persistence requirement\n\nWrite it down.\n\n## Other\n\nx\n'


def _fixture(root, name, text):
    path = os.path.join(root, name)
    with open(path, 'w', encoding='utf-8') as handle:
        handle.write(text)
    return path


def selftest():
    """Prove each check in both directions: it catches its defect, and it
    passes clean input. A gate proven in one direction only is worthless
    (DECISIONS.md D-65)."""
    cases = []
    with tempfile.TemporaryDirectory() as root:
        _fixture(root, 'OWNER.md', _CLEAN_DOC)
        _fixture(root, 'TWICE.md',
                 '## Persistence requirement\n\na\n\n## Persistence requirement\n\nb\n')
        _fixture(root, 'EMPTY.md', '## Persistence requirement\n\n## Next\n\nx\n')
        good = {'id': 'p', 'file': 'OWNER.md', 'heading': 'Persistence requirement',
                'triggers': ['\\bdecision\\b']}

        def check(name, entry, expect_finding):
            found = audit(root, {'entries': [entry]})
            ok = bool(found) == expect_finding
            cases.append((name, ok, found))

        check('clean entry passes', dict(good), False)
        check('dash form folds (-- vs em dash)',
              dict(good, heading='Persistence requirement'), False)
        check('missing heading caught',
              dict(good, heading='No Such Heading'), True)
        check('missing file caught', dict(good, file='NOPE.md'), True)
        check('duplicate heading caught', dict(good, file='TWICE.md'), True)
        check('empty section caught', dict(good, file='EMPTY.md'), True)
        check('bad regex caught', dict(good, triggers=['[unclosed']), True)
        check('no trigger and not always caught',
              {'id': 'p', 'file': 'OWNER.md',
               'heading': 'Persistence requirement'}, True)
        check('always with no trigger passes',
              {'id': 'p', 'file': 'OWNER.md', 'always': True,
               'heading': 'Persistence requirement'}, False)
        duplicate = audit(root, {'entries': [dict(good), dict(good)]})
        cases.append(('duplicate id caught',
                      any('duplicate id' in f for f in duplicate), duplicate))
        substring = audit(root, {'entries': [dict(good, heading='Persistence')]})
        cases.append(('substring does NOT match a heading',
                      bool(substring), substring))

    failed = 0
    for name, ok, detail in cases:
        print('%-46s %s' % (name, 'ok' if ok else 'FAILED'))
        if not ok:
            failed += 1
            print('    detail: %s' % (detail,))
    print('\n%d/%d selftest cases passed' % (len(cases) - failed, len(cases)))
    return 1 if failed else 0


def main(argv):
    if '--selftest' in argv:
        return selftest()
    return run(repo_root())


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
