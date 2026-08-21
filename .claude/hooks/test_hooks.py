#!/usr/bin/env python3
"""Prove every gate in both directions.

WHY THIS EXISTS
---------------
DECISIONS.md D-65: a check must fail the defect it was written to catch, and
pass clean input. A gate proven in only one direction is worth nothing -- five
checker defects in this project made a clean result meaningless, and each was
found by testing the other direction.

USAGE
-----
    python3 .claude/hooks/test_hooks.py

Exit 0 = every case behaved as specified. Non-zero = at least one gate is
wrong, and the gate is wrong until it is fixed.

Each case builds a throwaway git repository under a temp directory. Nothing
outside that directory is read or written.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HOOKS = os.path.dirname(os.path.abspath(__file__))
GATE_COMMIT = os.path.join(HOOKS, 'gate_commit.py')
GATE_STOP = os.path.join(HOOKS, 'gate_persistence.py')
INJECT = os.path.join(HOOKS, 'inject_plan_position.py')

RESULTS = []


def run_hook(script, payload, env=None):
    merged = dict(os.environ)
    # Point the Hub check at a path that does not exist, so a fixture commit
    # never depends on a Hub clone being present.
    merged['WG_HUB_CLONE'] = os.path.join(tempfile.gettempdir(), 'no-such-hub')
    if env:
        merged.update(env)
    proc = subprocess.run([sys.executable, script], input=json.dumps(payload),
                          capture_output=True, text=True, timeout=180,
                          env=merged)
    return proc.returncode, proc.stdout, proc.stderr


def git(root, *args):
    return subprocess.run(['git'] + list(args), cwd=root, capture_output=True,
                          text=True, timeout=60)


def make_repo(path):
    os.makedirs(path)
    git(path, 'init', '-q')
    git(path, 'config', 'user.email', 'gate@test.local')
    git(path, 'config', 'user.name', 'gate test')
    write(path, 'DECISIONS.md', '# Decisions\n\n**D-1.** First.\n**D-2.** Second.\n')
    write(path, 'STATE.md', '# State\n\n## Position in the plan sequence\n\n'
                            '| Plan step | State |\n|---|---|\n| 1 | Done |\n')
    write(path, 'AGENTS.md', '# Agents\n')
    git(path, 'add', '-A')
    git(path, 'commit', '-q', '-m', 'base')
    return path


def write(root, rel, text):
    full = os.path.join(root, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True) if os.path.dirname(rel) \
        else None
    with open(full, 'w', encoding='utf-8') as fh:
        fh.write(text)


def write_bytes(root, rel, data):
    full = os.path.join(root, rel)
    with open(full, 'wb') as fh:
        fh.write(data)


def commit_payload(root, command):
    return {'hook_event_name': 'PreToolUse', 'tool_name': 'Bash', 'cwd': root,
            'tool_input': {'command': command}}


def check(name, got, want, detail=''):
    ok = got == want
    RESULTS.append((ok, name, got, want, detail))
    print('%s  %-58s exit=%s want=%s' % ('PASS' if ok else 'FAIL', name, got,
                                         want))
    if not ok and detail:
        print('      ' + detail.replace('\n', '\n      ')[:900])


def case_append_only(tmp):
    # Defect direction: an existing line rewritten.
    root = make_repo(os.path.join(tmp, 'append-bad'))
    write(root, 'DECISIONS.md',
          '# Decisions\n\n**D-1.** First, reworded.\n**D-2.** Second.\n')
    git(root, 'add', 'DECISIONS.md')
    code, _, err = run_hook(GATE_COMMIT, commit_payload(root, 'git commit -m "edit"'))
    check('append-only blocks a rewritten line', code, 2, err)
    assert 'APPEND-ONLY' in err, err

    # Defect direction: a line deleted.
    root = make_repo(os.path.join(tmp, 'append-del'))
    write(root, 'DECISIONS.md', '# Decisions\n\n**D-1.** First.\n')
    git(root, 'add', 'DECISIONS.md')
    code, _, err = run_hook(GATE_COMMIT, commit_payload(root, 'git commit -m "drop"'))
    check('append-only blocks a deleted line', code, 2, err)

    # Clean direction: a pure append.
    root = make_repo(os.path.join(tmp, 'append-good'))
    write(root, 'DECISIONS.md',
          '# Decisions\n\n**D-1.** First.\n**D-2.** Second.\n**D-3.** Third.\n')
    git(root, 'add', 'DECISIONS.md')
    code, _, err = run_hook(GATE_COMMIT, commit_payload(root, 'git commit -m "append D-3"'))
    check('append-only passes a pure append', code, 0, err)

    # -a form must be gated too, with nothing staged.
    root = make_repo(os.path.join(tmp, 'append-dash-a'))
    write(root, 'DECISIONS.md', '# Decisions\n\n**D-1.** Changed.\n**D-2.** Second.\n')
    code, _, err = run_hook(GATE_COMMIT, commit_payload(root, 'git commit -am "edit"'))
    check('append-only blocks via -am with nothing staged', code, 2, err)


def case_secrets(tmp):
    root = make_repo(os.path.join(tmp, 'secret-bad'))
    write(root, 'config.txt', 'token = ghp_' + 'a' * 36 + '\n')
    git(root, 'add', 'config.txt')
    code, _, err = run_hook(GATE_COMMIT, commit_payload(root, 'git commit -m "config"'))
    check('secret gate blocks a token value', code, 2, err)
    assert 'SECRET' in err, err

    root = make_repo(os.path.join(tmp, 'secret-prose'))
    write(root, 'notes.md',
          'Never write a token into this repository. A ghp_ prefixed personal\n'
          'access token belongs in the operator credential store, referenced\n'
          'by location only. AKIA-style keys likewise.\n')
    git(root, 'add', 'notes.md')
    code, _, err = run_hook(GATE_COMMIT, commit_payload(root, 'git commit -m "notes"'))
    check('secret gate passes prose about secrets', code, 0, err)

    # The gate script itself must be committable: its own patterns must not
    # match their own source text.
    root = make_repo(os.path.join(tmp, 'secret-self'))
    shutil.copy(GATE_COMMIT, os.path.join(root, 'gate_commit.py'))
    git(root, 'add', 'gate_commit.py')
    code, _, err = run_hook(GATE_COMMIT, commit_payload(root, 'git commit -m "add gate"'))
    check('secret gate passes its own source', code, 0, err)


def case_ascii(tmp):
    root = make_repo(os.path.join(tmp, 'ascii-bad'))
    write_bytes(root, 'Do-Thing.ps1',
                'Write-Output "em dash \xe2\x80\x94 here"\n'.encode('latin-1'))
    git(root, 'add', 'Do-Thing.ps1')
    code, _, err = run_hook(GATE_COMMIT, commit_payload(root, 'git commit -m "ps1"'))
    check('ascii gate blocks non-ASCII in a .ps1', code, 2, err)
    assert 'NON-ASCII' in err, err

    root = make_repo(os.path.join(tmp, 'ascii-good'))
    write(root, 'Do-Thing.ps1', 'Write-Output "plain ascii only"\n')
    git(root, 'add', 'Do-Thing.ps1')
    code, _, err = run_hook(GATE_COMMIT, commit_payload(root, 'git commit -m "ps1"'))
    check('ascii gate passes a pure-ASCII .ps1', code, 0, err)

    # A non-.ps1 file with non-ASCII is out of scope and must not be blocked.
    root = make_repo(os.path.join(tmp, 'ascii-md'))
    write(root, 'note.md', 'an em dash — in prose is fine\n')
    git(root, 'add', 'note.md')
    code, _, err = run_hook(GATE_COMMIT, commit_payload(root, 'git commit -m "note"'))
    check('ascii gate ignores non-script files', code, 0, err)


def case_message(tmp):
    root = make_repo(os.path.join(tmp, 'msg-bad'))
    write(root, 'a.txt', 'x\n')
    git(root, 'add', 'a.txt')
    code, _, err = run_hook(GATE_COMMIT, commit_payload(
        root, 'git commit -m "routes are verbatim, so fidelity is true by construction"'))
    check('message gate blocks a by-construction claim', code, 2, err)
    assert 'COMMIT MESSAGE CLAIM' in err, err

    root = make_repo(os.path.join(tmp, 'msg-good'))
    write(root, 'a.txt', 'x\n')
    git(root, 'add', 'a.txt')
    code, _, err = run_hook(GATE_COMMIT, commit_payload(
        root, 'git commit -m "routes verified byte-identical by a committed script"'))
    check('message gate passes a named-check claim', code, 0, err)

    # A message with no -m must be reported as a skip, never silently passed.
    root = make_repo(os.path.join(tmp, 'msg-none'))
    write(root, 'a.txt', 'x\n')
    git(root, 'add', 'a.txt')
    code, _, err = run_hook(GATE_COMMIT, commit_payload(root, 'git commit'))
    check('message gate reports SKIPPED with no -m', code, 0, err)
    assert 'SKIPPED' in err, err


def case_push(tmp):
    root = make_repo(os.path.join(tmp, 'push'))
    for command, want, label in (
            ('git push --force origin main', 2, 'blocks --force'),
            ('git push -f origin main', 2, 'blocks -f'),
            ('git push origin +main:main', 2, 'blocks a plus refspec'),
            ('git push --force-with-lease origin main', 0, 'passes lease'),
            ('git push -u origin main', 0, 'passes an ordinary push'),
    ):
        code, _, err = run_hook(GATE_COMMIT, commit_payload(root, command))
        check('push gate %s' % label, code, want, err)


def case_out_of_scope(tmp):
    root = make_repo(os.path.join(tmp, 'scope'))
    code, _, err = run_hook(GATE_COMMIT, {
        'hook_event_name': 'PreToolUse', 'tool_name': 'Read', 'cwd': root,
        'tool_input': {'file_path': 'DECISIONS.md'}})
    check('gate ignores a non-Bash tool', code, 0, err)
    code, _, err = run_hook(GATE_COMMIT, commit_payload(root, 'ls -la'))
    check('gate ignores a command with no git', code, 0, err)
    code, _, err = run_hook(GATE_COMMIT, commit_payload(root, 'git status'))
    check('gate ignores git status', code, 0, err)
    # An unbalanced quote must be reported, not silently treated as clean.
    code, _, err = run_hook(GATE_COMMIT, commit_payload(root, 'git commit -m "oops'))
    check('gate reports an untokenisable command', code, 0, err)
    assert 'SKIPPED' in err, err


def case_persistence(tmp):
    root = make_repo(os.path.join(tmp, 'stop'))
    payload = {'hook_event_name': 'Stop', 'cwd': root, 'session_id': 'sess-1'}

    code, _, err = run_hook(GATE_STOP, payload)
    check('stop gate passes a clean tree', code, 0, err)

    write(root, 'STATE.md', '# State\n\nchanged\n')
    code, _, err = run_hook(GATE_STOP, payload)
    check('stop gate blocks an uncommitted governed file', code, 2, err)
    assert 'STATE.md' in err, err

    code, _, err = run_hook(GATE_STOP, payload)
    check('stop gate raises the same set only once', code, 0, err)

    write(root, 'DECISIONS.md',
          '# Decisions\n\n**D-1.** First.\n**D-2.** Second.\n**D-3.** New.\n')
    code, _, err = run_hook(GATE_STOP, payload)
    check('stop gate blocks again when the set changes', code, 2, err)

    # An ungoverned file must not block a stop.
    root = make_repo(os.path.join(tmp, 'stop-ungoverned'))
    write(root, 'scratch.txt', 'temp\n')
    code, _, err = run_hook(GATE_STOP, {'hook_event_name': 'Stop', 'cwd': root,
                                        'session_id': 'sess-2'})
    check('stop gate ignores an ungoverned file', code, 0, err)

    # A repository that is not this one must be left alone.
    other = os.path.join(tmp, 'other')
    os.makedirs(other)
    git(other, 'init', '-q')
    write(other, 'README.md', 'unrelated\n')
    code, _, err = run_hook(GATE_STOP, {'hook_event_name': 'Stop', 'cwd': other,
                                        'session_id': 'sess-3'})
    check('stop gate ignores another repository', code, 0, err)


def case_inject(tmp):
    root = make_repo(os.path.join(tmp, 'inject'))
    code, out, err = run_hook(INJECT, {'hook_event_name': 'UserPromptSubmit',
                                       'cwd': root})
    check('injector reads a position table', code, 0, err)
    assert 'AUTHORITATIVE PLAN POSITION' in out, out
    assert '1 -- Done' in out, out

    # Missing section: must say so, not stay silent.
    write(root, 'STATE.md', '# State\n\nno position section here\n')
    code, out, err = run_hook(INJECT, {'hook_event_name': 'UserPromptSubmit',
                                       'cwd': root})
    check('injector reports a missing position section', code, 0, err)
    assert 'POSITION NOT READ' in out, out

    # Not this repository: silence, and never a failure.
    other = os.path.join(tmp, 'inject-other')
    os.makedirs(other)
    git(other, 'init', '-q')
    code, out, err = run_hook(INJECT, {'hook_event_name': 'UserPromptSubmit',
                                       'cwd': other})
    check('injector is silent outside this repository', code, 0, err)
    assert out.strip() == '', out


def main():
    tmp = tempfile.mkdtemp(prefix='wg-hook-tests-')
    try:
        case_append_only(tmp)
        case_secrets(tmp)
        case_ascii(tmp)
        case_message(tmp)
        case_push(tmp)
        case_out_of_scope(tmp)
        case_persistence(tmp)
        case_inject(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    failed = [r for r in RESULTS if not r[0]]
    print('\n%d case(s), %d failed.' % (len(RESULTS), len(failed)))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
