#!/usr/bin/env python3
"""Probe: does a hook registered ONLY at user scope fire in every session?

WHAT THIS SETTLES
-----------------
Issue #43. Project hooks in `.claude/settings.json` fire only for sessions whose
working directory is that project, so the injector set in this repository governs
the backoffice and nothing else. A user-scope hook is the only candidate carrier
that reaches every session. Whether it does is not in our verified record -- see
`evidence/USER-SCOPE-HOOK-CARRIER-2026-08-27.md` Finding 3.

WHAT IT DOES
------------
Appends one line to `~/.claude/hook-trace.log`: an ISO timestamp, the session's
working directory, and the hook event name. It prints NOTHING, so it cannot
change what any session sees, and it always exits 0, so it cannot block a prompt
even if it fails outright.

IT IS A MEASUREMENT, NOT A CARRIER. Nothing should be built on it, and it should
be removed once the run is recorded.

READING THE RESULT
------------------
A line appearing proves nothing on its own. The negative direction -- no new line
once the hook is deregistered -- is what rules out a second writer. Both are
required (`DECISIONS.md` D-65). A partial result, firing in some directories and
not others, is a finding to record, not a run to repeat until it passes.

ONE FALSE NEGATIVE TO RULE OUT FIRST
------------------------------------
If the interpreter named in the hook command is not on PATH, the hook does not
run and the log stays empty -- which looks exactly like "user scope does not
load". This repository already carries that lesson: `.githooks/pre-commit` tries
python3, then python, then py -3, precisely because the operator is on Windows.
Confirm the interpreter name BEFORE concluding anything from an empty log.

    python3 --version   /   python --version   /   py -3 --version

Use whichever answers, in the hook command.

USAGE
-----
    python3 scripts/Probe-UserScopeHook.py --selftest

Run the selftest to confirm the probe writes what it claims, before trusting an
empty log to mean anything.
"""

import datetime
import json
import os
import sys

LOG_NAME = 'hook-trace.log'


def log_path():
    return os.path.join(os.path.expanduser('~'), '.claude', LOG_NAME)


def record(payload, path=None):
    """Append one line describing this session. Never raises, never prints."""
    target = path or log_path()
    try:
        stamp = datetime.datetime.now().isoformat(timespec='seconds')
        cwd = ''
        event = ''
        if isinstance(payload, dict):
            cwd = payload.get('cwd') or ''
            event = payload.get('hook_event_name') or ''
        cwd = cwd or os.getcwd()
        line = '%s\tcwd=%s\tevent=%s\n' % (stamp, cwd, event or 'unknown')
        directory = os.path.dirname(target)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(target, 'a', encoding='utf-8') as handle:
            handle.write(line)
        return line
    except Exception:
        # A probe that breaks a session would poison the very thing it measures.
        return None


def selftest():
    """Prove the probe writes, and that it is the thing writing.

    Without this, an empty log is ambiguous between "user scope does not load"
    and "the probe never worked".
    """
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        target = os.path.join(tmp, 'nested', LOG_NAME)
        line = record({'cwd': '/somewhere', 'hook_event_name': 'UserPromptSubmit'},
                      target)
        wrote = line is not None and os.path.isfile(target)
        print('%-52s %s' % ('writes a line, creating the directory',
                            'ok' if wrote else 'FAILED'))
        ok = ok and wrote
        body = open(target, encoding='utf-8').read() if wrote else ''
        named = '/somewhere' in body and 'UserPromptSubmit' in body
        print('%-52s %s' % ('the line names the cwd and the event',
                            'ok' if named else 'FAILED'))
        ok = ok and named
        record({'cwd': '/elsewhere'}, target)
        two = len(open(target, encoding='utf-8').read().strip().splitlines()) == 2
        print('%-52s %s' % ('appends rather than overwrites',
                            'ok' if two else 'FAILED'))
        ok = ok and two
        bad = record('not-a-payload', target)
        print('%-52s %s' % ('a malformed payload still records',
                            'ok' if bad is not None else 'FAILED'))
        ok = ok and bad is not None
        unwritable = record({'cwd': '/x'}, os.path.join(os.devnull, 'no', LOG_NAME))
        print('%-52s %s' % ('an unwritable path returns None, never raises',
                            'ok' if unwritable is None else 'FAILED'))
        ok = ok and unwritable is None
    print('\nselftest %s' % ('passed' if ok else 'FAILED'))
    return 0 if ok else 1


def main(argv):
    if '--selftest' in argv:
        return selftest()
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    record(payload)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
