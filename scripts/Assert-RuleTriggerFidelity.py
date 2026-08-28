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
# Where the matcher lives. The repository's own .claude/hooks wins whenever that
# directory exists, so a repo that has the directory but is MISSING
# inject_rules.py still fails to import -- which is the condition the gate must
# report as CHECK COULD NOT RUN. WG_HOOKS_DIR is consulted only when the
# repo-relative directory is absent entirely, which is the mutation harness
# running a copy out of a temp tree. An unconditional override hid the missing
# -injector case; a purely relative path broke under the harness and made every
# mutation look caught for an environmental reason. Both were wrong.
_LOCAL_HOOKS = os.path.join(os.path.dirname(_HERE), '.claude', 'hooks')
_HOOKS = (_LOCAL_HOOKS if os.path.isdir(_LOCAL_HOOKS)
          else (os.environ.get('WG_HOOKS_DIR') or _LOCAL_HOOKS))
if _HOOKS not in sys.path:
    sys.path.insert(0, _HOOKS)

try:
    from inject_rules import inside, normalise, positive_int, section  # noqa: E402
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
    """Headings matching `heading`, ignoring fenced code blocks.

    A ``` block containing a line like `## Stop conditions` is not a heading,
    and counting it refused every commit with a duplicate-heading finding that
    named a fence the author could not see in the message. section() reads the
    first real section and was always right; the counter was the defect.
    """
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as handle:
            lines = handle.read().splitlines()
    except Exception:
        return 0
    want = normalise(heading)
    hits = 0
    fence = None
    for line in lines:
        stripped = line.strip()
        marker = re.match(r'^(`{3,}|~{3,})', stripped)
        if marker:
            token = marker.group(1)[0]
            if fence is None:
                fence = token
            elif fence == token:
                fence = None
            continue
        if fence is not None:
            continue
        match = re.match(r'^#{1,6}\s+(.*)$', line)
        if match and normalise(match.group(1)) == want:
            hits += 1
    return hits


# A quantifier nested in a quantified group -- (a+)+ -- backtracks exponentially,
# and the shape is unambiguous, so it is refused statically.
RISKY_NESTED = re.compile(r'\(([^()]*[+*][^()]*)\)\s*[*+]')

# Alternation is NOT refused statically. The first attempt flagged any quantified
# group containing "|", which refuses (foo|bar)+ -- a safe and ordinary pattern.
# A checker that rejects valid tables is a defect, not a gate. Whether a pattern
# actually backtracks is measured instead, below.
BACKTRACK_PROBES = ('a' * 44 + '!', 'ab' * 26 + '!', 'x' * 40 + 'y')
BACKTRACK_BUDGET_SECONDS = 2


def terminates(pattern, budget=BACKTRACK_BUDGET_SECONDS):
    """Run the pattern against adversarial input under a wall-clock budget.

    Measured rather than guessed, in a subprocess so a runaway match can be
    killed: signal-based timeouts are not portable and the operator is on
    Windows. `(a|aa)+$` compiles, passes every static shape test worth having,
    and then stalls the hook for its full timeout on a 44-character prompt --
    which is exactly the failure this is here to catch.

    Returns None when every probe finishes inside the budget.
    """
    program = (
        'import re,sys,json\n'
        'p=json.loads(sys.argv[1]); s=json.loads(sys.argv[2])\n'
        're.search(p, s)\n')
    for probe in BACKTRACK_PROBES:
        try:
            done = subprocess.run(
                [sys.executable, '-c', program, json.dumps(pattern),
                 json.dumps(probe)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=budget)
        except subprocess.TimeoutExpired:
            return ('did not finish matching %d characters within %ds, so it '
                    'would stall every prompt that reaches it'
                    % (len(probe), budget))
        except Exception as exc:
            return 'could not be timed (%s), so it is not accepted' % exc
        if done.returncode != 0:
            return 'raised while matching: %s' % (
                done.stderr.decode('utf-8', 'replace').strip().splitlines()[-1:]
                or 'unknown')
    return None


def compiles_safely(pattern):
    """Reject a pattern that compiles but may not terminate.

    Compiling is not enough: `(a+)+$` and `(a|aa)+$` both compile and then
    backtrack exponentially, stalling the hook for its whole timeout on a
    44-character prompt. The unambiguous nested shape is refused statically; for
    everything else the pattern is timed against adversarial input, because a
    static test broad enough to catch the alternation case also refuses
    `(foo|bar)+`, and a checker that rejects valid tables is a defect.
    """
    try:
        re.compile(pattern)
    except re.error as exc:
        return 'does not compile: %s' % exc
    if RISKY_NESTED.search(pattern):
        return ('nests a quantifier inside a quantified group, which can run '
                'exponentially; rewrite it without the nesting')
    return terminates(pattern)


# An upper bound as well as a lower one. positive_int only refused <= 0, so a
# cap of 50,000,000 passed with zero findings and an entry naming a large file
# would then flood every prompt.
CAP_CEILING = 20000
WHY_VERBATIM_LIMIT = 40


def longest_shared_run(text, source):
    """Longest substring of `text` that appears verbatim in `source`."""
    best = ''
    for start in range(len(text)):
        for end in range(len(text), start + len(best), -1):
            if text[start:end] in source:
                best = text[start:end]
                break
    return best


def audit(root, table):
    findings = []
    seen = set()
    if not isinstance(table, dict):
        return ['the table is not a JSON object']
    for field in ('max_chars_per_entry', 'max_chars_total'):
        if field in table:
            value, bad = positive_int(table.get(field), 1)
            findings.extend('%s %s' % (field, reason) for reason in bad)
            if not bad and value > CAP_CEILING:
                findings.append(
                    '%s is %d, above the %d ceiling. A cap this large lets one '
                    'entry flood every prompt.' % (field, value, CAP_CEILING))
    entries = table.get('entries')
    if not isinstance(entries, list) or not entries:
        return findings + ['table has no entries, or entries is not a list']
    for position, entry in enumerate(entries):
        if not isinstance(entry, dict):
            findings.append('#%d: entry is not an object' % position)
            continue
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
        triggers = entry.get('triggers')
        if not entry.get('always') and not triggers:
            findings.append('%s: needs either always or triggers' % label)
        if triggers is not None:
            if isinstance(triggers, str) or not isinstance(triggers, list):
                findings.append(
                    '%s: triggers must be a list. A bare string iterates per '
                    'CHARACTER, so every single letter becomes a pattern and the '
                    'entry fires on almost any prompt.' % label)
                triggers = []
            for pattern in triggers:
                if not isinstance(pattern, str):
                    findings.append('%s: trigger %r is not a string'
                                    % (label, pattern))
                    continue
                problem = compiles_safely(pattern)
                if problem:
                    findings.append('%s: trigger %r %s' % (label, pattern, problem))
        if not inside(root, name):
            findings.append(
                '%s: %s is outside the governance root. The table decides what '
                'file content reaches the model; it may not name an absolute '
                'path or walk out with "..".' % (label, name))
            continue
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
            findings.append('%s: heading %r appears %d times in %s (outside code '
                            'fences); the injected text would depend on document '
                            'order' % (label, heading, hits, name))
            continue
        body = section(path, heading)
        if not body:
            findings.append('%s: heading %r in %s resolves to an empty section'
                            % (label, heading, name))
            continue
        # The table claims to hold no rule text, and a claim in a docstring is
        # not a check. Every `why` field is injected into context next to the
        # live section, so a `why` that restates the rule IS a second copy --
        # unguarded, and it had already drifted in the commit that created it:
        # one field changed "the ownership table" to "this table", altering the
        # referent of a rule it was quoting.
        why = entry.get('why')
        if isinstance(why, str) and why:
            shared = longest_shared_run(why, body)
            if len(shared) >= WHY_VERBATIM_LIMIT:
                findings.append(
                    '%s: its why field repeats %d characters verbatim from the '
                    'section it points at (%r...). The why says WHEN the rule '
                    'fires; the rule text has one owner and is read live.'
                    % (label, len(shared), shared[:48]))
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
        _fixture(root, 'DASH.md',
                 '## Keeping it current \u2014 ROUTINE\n\nbody\n')
        _fixture(root, 'ASCII_DASH.md',
                 '## Keeping it current -- ROUTINE\n\nbody\n')
        _fixture(root, 'FENCE.md',
                 '## Persistence requirement\n\nbody\n\n## Other\n\n'
                 '```\n## Persistence requirement\n```\n')
        _fixture(root, 'OUTSIDE.md', '## Persistence requirement\n\nbody\n')
        good = {'id': 'p', 'file': 'OWNER.md', 'heading': 'Persistence requirement',
                'triggers': ['\\bdecision\\b']}

        def check(name, entry, expect_finding, expect_text=None):
            """A case that asserts only bool(findings) passes for the wrong
            reason. Two of these did: the path-guard cases produced a
            'heading not found' finding once the guard was removed, so the
            selftest stayed green with the check it names deleted -- the exact
            defect D-65 and L-026 exist to catch."""
            found = audit(root, {'entries': [entry]})
            ok = bool(found) == expect_finding
            if ok and expect_text:
                ok = any(expect_text in item for item in found)
            cases.append((name, ok, found))

        check('clean entry passes', dict(good), False)
        # Was byte-identical to 'clean entry passes' -- same heading, no dash
        # on either side -- so dash folding, the one part of normalise() beyond
        # casefold and whitespace, had zero coverage inside an 11/11 result.
        check('em dash in the file matches -- in the table',
              dict(good, file='DASH.md',
                   heading='Keeping it current -- ROUTINE'), False)
        check('-- in the file matches an em dash in the table',
              dict(good, file='ASCII_DASH.md',
                   heading='Keeping it current \u2014 ROUTINE'), False)
        check('missing heading caught',
              dict(good, heading='No Such Heading'), True,
              'not found in')
        check('missing file caught', dict(good, file='NOPE.md'), True)
        check('duplicate heading caught', dict(good, file='TWICE.md'), True,
              'appears 2 times')
        check('empty section caught', dict(good, file='EMPTY.md'), True,
              'empty section')
        check('bad regex caught', dict(good, triggers=['[unclosed']), True,
              'does not compile')
        check('no trigger and not always caught',
              {'id': 'p', 'file': 'OWNER.md',
               'heading': 'Persistence requirement'}, True)
        check('always with no trigger passes',
              {'id': 'p', 'file': 'OWNER.md', 'always': True,
               'heading': 'Persistence requirement'}, False)
        _fixture(root, 'ECHO.md',
                 '## Persistence requirement\n\n'
                 'A session that establishes a decision and ends without '
                 'recording it has failed.\n')
        check('a why that repeats the rule verbatim is caught',
              dict(good, file='ECHO.md',
                   why='A session that establishes a decision and ends without '
                       'recording it has failed.'), True,
              'repeats')
        check('a why that says when it fires passes',
              dict(good, file='ECHO.md',
                   why='Fires where a durable thing appears.'), False)
        check('a heading inside a code fence is not counted twice',
              dict(good, file='FENCE.md'), False)
        check('triggers as a bare string caught',
              dict(good, triggers='decision'), True,
              'triggers must be a list')
        check('a non-string trigger caught', dict(good, triggers=[7]), True,
              'is not a string')
        check('catastrophic backtracking caught',
              dict(good, triggers=['(a+)+$']), True,
              'nests a quantifier')
        check('an ordinary grouped quantifier still passes',
              dict(good, triggers=['(foo|bar)+']), False)
        check('an absolute file path caught',
              dict(good, file='/etc/hostname'), True,
              'outside the governance root')
        check('a Windows drive-letter path caught on any platform',
              dict(good, file='C:\\Windows\\win.ini'), True,
              'outside the governance root')
        check('an alternation that backtracks is caught by measurement',
              dict(good, triggers=['(a|aa)+$']), True, 'did not finish matching')
        check('a traversing file path caught',
              dict(good, file='../OUTSIDE.md'), True,
              'outside the governance root')
        check('a non-object entry caught', 'not-an-entry', True,
              'not an object')
        caps = audit(root, {'max_chars_per_entry': 'lots', 'entries': [dict(good)]})
        cases.append(('a non-numeric cap caught',
                      any('max_chars_per_entry' in f for f in caps), caps))
        big = audit(root, {'max_chars_total': 50000000, 'entries': [dict(good)]})
        cases.append(('a cap above the ceiling caught',
                      any('ceiling' in f for f in big), big))
        neg = audit(root, {'max_chars_total': -1, 'entries': [dict(good)]})
        cases.append(('a negative cap caught',
                      any('max_chars_total' in f for f in neg), neg))
        shape = audit(root, {'entries': 'oops'})
        cases.append(('entries not a list caught', bool(shape), shape))

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
