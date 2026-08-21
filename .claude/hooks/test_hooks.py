#!/usr/bin/env python3
"""Prove every gate in both directions, and prove the suite is not vacuous.

WHY THE SECOND HALF EXISTS
--------------------------
The first version of this harness reported 31 of 31 passing. An independent
audit then mutated the source in 25 places and found that **10 mutations
survived undetected** -- including deleting all six governed-path prefixes from
the persistence gate, and making the Hub check never block on failure. A suite
that passes when the code is broken is not evidence, so `--mutations` now breaks
each gate on purpose and requires the suite to notice.

DECISIONS.md D-65: a check must fail the defect it was written to catch and pass
clean input. This file is where that is demonstrated, for both halves.

USAGE
-----
    python3 .claude/hooks/test_hooks.py               # the suite
    python3 .claude/hooks/test_hooks.py --mutations   # suite + mutation proof

Exit 0 = every case behaved as specified. Non-zero = a gate is wrong, and it is
wrong until it is fixed. Fixtures live in a temp directory; nothing outside it
is read or written.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HOOKS = os.environ.get('WG_HOOKS_DIR') or os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GITHOOKS = os.environ.get('WG_GITHOOKS_DIR') or os.path.join(REPO, '.githooks')
GATE_COMMIT = os.path.join(HOOKS, 'gate_commit.py')
GATE_STOP = os.path.join(HOOKS, 'gate_persistence.py')
INJECT = os.path.join(HOOKS, 'inject_plan_position.py')
NO_HUB = os.path.join(tempfile.gettempdir(), 'wg-no-such-hub')

RESULTS = []


def env(extra=None):
    merged = dict(os.environ)
    merged['WG_HUB_CLONE'] = NO_HUB
    if extra:
        merged.update(extra)
    return merged


def run_hook(script, payload, extra_env=None):
    proc = subprocess.run([sys.executable, script], input=json.dumps(payload),
                          capture_output=True, text=True, timeout=180,
                          env=env(extra_env))
    return proc.returncode, proc.stdout, proc.stderr


def git(root, *args, **kwargs):
    return subprocess.run(['git'] + list(args), cwd=root, capture_output=True,
                          text=True, timeout=120, env=env(kwargs.get('extra_env')))


def write(root, rel, text):
    full = os.path.join(root, rel)
    parent = os.path.dirname(full)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(full, 'w', encoding='utf-8') as handle:
        handle.write(text)


def write_bytes(root, rel, data):
    full = os.path.join(root, rel)
    parent = os.path.dirname(full)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(full, 'wb') as handle:
        handle.write(data)


def make_repo(path, with_gates=True):
    os.makedirs(path)
    git(path, 'init', '-q')
    git(path, 'config', 'user.email', 'gate@test.local')
    git(path, 'config', 'user.name', 'gate test')
    write(path, 'DECISIONS.md',
          '# Decisions\n\nPreamble line.\n\n**D-1.** First.\n**D-2.** Second.\n')
    write(path, 'STATE.md', '# State\n\n## Position in the plan sequence\n\n'
                            '| Plan step | State |\n|---|---|\n| 1 | Done |\n\n'
                            '## Next action\n\nDo the next thing.\n')
    write(path, 'AGENTS.md', '# Agents\n')
    if with_gates:
        os.makedirs(os.path.join(path, '.claude', 'hooks'), exist_ok=True)
        for name in ('wg_gates.py', 'git_pre_commit.py', 'git_commit_msg.py'):
            shutil.copy(os.path.join(HOOKS, name),
                        os.path.join(path, '.claude', 'hooks', name))
        os.makedirs(os.path.join(path, '.githooks'), exist_ok=True)
        for name in ('pre-commit', 'commit-msg'):
            target = os.path.join(path, '.githooks', name)
            shutil.copy(os.path.join(GITHOOKS, name), target)
            os.chmod(target, 0o755)
        git(path, 'config', 'core.hooksPath', '.githooks')
    git(path, 'add', '-A')
    git(path, 'commit', '-q', '-m', 'base', '--no-verify')
    return path


def check(name, got, want, detail=''):
    ok = got == want
    RESULTS.append((ok, name))
    print('%s  %-62s got=%s want=%s' % ('PASS' if ok else 'FAIL', name, got, want))
    if not ok and detail:
        print('      ' + str(detail).replace('\n', '\n      ')[:700])


def check_in(name, needle, haystack):
    """A content assertion that records a result instead of raising."""
    ok = needle in haystack
    RESULTS.append((ok, name))
    print('%s  %-62s expected text present=%s' % ('PASS' if ok else 'FAIL', name, ok))
    if not ok:
        print('      looked for %r in: %s' % (needle, str(haystack)[:400]))


def commit_payload(root, command):
    return {'hook_event_name': 'PreToolUse', 'tool_name': 'Bash', 'cwd': root,
            'tool_input': {'command': command}}


# --------------------------------------------------------------------------
# git hooks: the authoritative content gates, exercised through real commits
# --------------------------------------------------------------------------

def case_append_only(tmp):
    root = make_repo(os.path.join(tmp, 'ao-entry-edit'))
    write(root, 'DECISIONS.md',
          '# Decisions\n\nPreamble line.\n\n**D-1.** First, reworded.\n**D-2.** Second.\n')
    git(root, 'add', 'DECISIONS.md')
    out = git(root, 'commit', '-m', 'edit')
    check('git hook refuses a rewritten entry line', out.returncode, 1, out.stderr)
    check_in('the refusal names the append-only rule', 'APPEND-ONLY VIOLATION', out.stderr)

    root = make_repo(os.path.join(tmp, 'ao-entry-delete'))
    write(root, 'DECISIONS.md', '# Decisions\n\nPreamble line.\n\n**D-1.** First.\n')
    git(root, 'add', 'DECISIONS.md')
    check('git hook refuses a deleted entry line',
          git(root, 'commit', '-m', 'drop').returncode, 1)

    root = make_repo(os.path.join(tmp, 'ao-append'))
    write(root, 'DECISIONS.md',
          '# Decisions\n\nPreamble line.\n\n**D-1.** First.\n**D-2.** Second.\n'
          '**D-3.** Third.\n')
    git(root, 'add', 'DECISIONS.md')
    check('git hook allows a pure append',
          git(root, 'commit', '-m', 'append D-3').returncode, 0)

    # Prose outside an entry is editable; the audit found the old gate refused it.
    root = make_repo(os.path.join(tmp, 'ao-prose'))
    write(root, 'DECISIONS.md',
          '# Decisions\n\nPreamble line, corrected.\n\n**D-1.** First.\n**D-2.** Second.\n')
    git(root, 'add', 'DECISIONS.md')
    check('git hook allows a non-entry line correction',
          git(root, 'commit', '-m', 'fix a typo in the preamble').returncode, 0)

    # Every invocation form the old command-parsing gate let through.
    for label, args in (
            ('-am with nothing staged', ['commit', '-am', 'x']),
            ('git -C .', ['-C', '.', 'commit', '-am', 'x']),
            ('a pathspec commit', ['commit', '-m', 'x', '--', 'DECISIONS.md']),
    ):
        root = make_repo(os.path.join(tmp, 'ao-form-' + label.replace(' ', '-')))
        write(root, 'DECISIONS.md',
              '# Decisions\n\nPreamble line.\n\n**D-1.** Changed.\n**D-2.** Second.\n')
        check('git hook refuses via %s' % label, git(root, *args).returncode, 1)

    root = make_repo(os.path.join(tmp, 'ao-alias'))
    git(root, 'config', 'alias.save', 'commit')
    write(root, 'DECISIONS.md',
          '# Decisions\n\nPreamble line.\n\n**D-1.** Changed.\n**D-2.** Second.\n')
    check('git hook refuses via a repository alias',
          git(root, 'save', '-am', 'x').returncode, 1)


def case_secrets(tmp):
    root = make_repo(os.path.join(tmp, 'secret-bad'))
    write(root, 'config.txt', 'token = ghp_' + 'a' * 36 + '\n')
    git(root, 'add', 'config.txt')
    out = git(root, 'commit', '-m', 'config')
    check('git hook refuses a token value', out.returncode, 1, out.stderr)
    check_in('the refusal names the secret rule', 'SECRET IN COMMITTED CONTENT',
             out.stderr)

    # The audit's finding: one undecodable byte used to delete this gate silently.
    root = make_repo(os.path.join(tmp, 'secret-cp1252'))
    write_bytes(root, 'config.txt',
                b'token = ghp_' + b'a' * 36 + b'\nnote \x97 cp1252\n')
    git(root, 'add', 'config.txt')
    check('a token survives an undecodable byte in the same diff',
          git(root, 'commit', '-m', 'config').returncode, 1)

    root = make_repo(os.path.join(tmp, 'secret-prose'))
    write(root, 'notes.md',
          'Never write a token here. A ghp_ prefixed token belongs in the operator\n'
          'credential store, referenced by location. AKIA-style keys likewise.\n')
    git(root, 'add', 'notes.md')
    check('git hook allows prose about secrets',
          git(root, 'commit', '-m', 'notes').returncode, 0)

    # A base64 data: URI matches the Google-key shape; the audit hit this.
    root = make_repo(os.path.join(tmp, 'secret-datauri'))
    write(root, 'page.md',
          'icon: data:image/png;base64,AIza' + 'B' * 40 + 'ZZ\n')
    git(root, 'add', 'page.md')
    check('git hook allows a base64 data URI',
          git(root, 'commit', '-m', 'icon').returncode, 0)

    root = make_repo(os.path.join(tmp, 'secret-self'))
    shutil.copy(os.path.join(HOOKS, 'wg_gates.py'),
                os.path.join(root, 'copy_of_gates.py'))
    git(root, 'add', 'copy_of_gates.py')
    check('git hook allows its own pattern source',
          git(root, 'commit', '-m', 'add gate source').returncode, 0)


def case_ascii(tmp):
    # cp1252 em dash: exactly the defect scripts/README.md section 1 describes,
    # and exactly what the old gate passed because UTF-8 could not decode it.
    root = make_repo(os.path.join(tmp, 'ascii-cp1252'))
    write_bytes(root, 'Do-Thing.ps1', b'Write-Output "em dash \x97 here"\r\n')
    git(root, 'add', 'Do-Thing.ps1')
    out = git(root, 'commit', '-m', 'ps1')
    check('git hook refuses a cp1252 em dash in a .ps1', out.returncode, 1, out.stderr)
    check_in('the refusal names the encoding rule',
             'NON-ASCII IN A POWERSHELL SCRIPT', out.stderr)

    root = make_repo(os.path.join(tmp, 'ascii-utf8'))
    write_bytes(root, 'Do-Thing.ps1',
                'Write-Output "em dash — here"\n'.encode('utf-8'))
    git(root, 'add', 'Do-Thing.ps1')
    check('git hook refuses a UTF-8 em dash in a .ps1',
          git(root, 'commit', '-m', 'ps1').returncode, 1)

    root = make_repo(os.path.join(tmp, 'ascii-good'))
    write(root, 'Do-Thing.ps1', 'Write-Output "plain ascii only"\n')
    git(root, 'add', 'Do-Thing.ps1')
    check('git hook allows a pure-ASCII .ps1',
          git(root, 'commit', '-m', 'ps1').returncode, 0)

    # An edit to a file that already exists: the staged blob is what matters, and
    # reading HEAD instead would check the previous version's bytes.
    root = make_repo(os.path.join(tmp, 'ascii-modified'))
    write(root, 'Do-Thing.ps1', 'Write-Output "clean to begin with"\n')
    git(root, 'add', 'Do-Thing.ps1')
    git(root, 'commit', '-q', '-m', 'clean ps1')
    write_bytes(root, 'Do-Thing.ps1', b'Write-Output "now with \x97 in it"\r\n')
    git(root, 'add', 'Do-Thing.ps1')
    check('git hook refuses a bad edit to a previously clean .ps1',
          git(root, 'commit', '-m', 'edit ps1').returncode, 1)

    root = make_repo(os.path.join(tmp, 'ascii-repaired'))
    write_bytes(root, 'Do-Thing.ps1', b'Write-Output "bad \x97 byte"\r\n')
    git(root, 'add', 'Do-Thing.ps1')
    git(root, 'commit', '-q', '-m', 'bad ps1', '--no-verify')
    write(root, 'Do-Thing.ps1', 'Write-Output "repaired, pure ascii"\n')
    git(root, 'add', 'Do-Thing.ps1')
    check('git hook allows a repair to an already-bad .ps1',
          git(root, 'commit', '-m', 'repair ps1').returncode, 0)

    root = make_repo(os.path.join(tmp, 'ascii-md'))
    write(root, 'note.md', 'an em dash — in prose is fine\n')
    git(root, 'add', 'note.md')
    check('git hook ignores non-script files',
          git(root, 'commit', '-m', 'note').returncode, 0)


def case_message(tmp):
    root = make_repo(os.path.join(tmp, 'msg'))
    write(root, 'a.txt', 'x\n')
    git(root, 'add', 'a.txt')
    out = git(root, 'commit', '-m', 'fidelity is true by construction')
    check('commit-msg hook refuses an unbacked claim', out.returncode, 1, out.stderr)
    check_in('the refusal cites D-53', 'D-53', out.stderr)

    # Every message form the old command parser missed.
    for label, args in (
            ('-am', ['commit', '-am', 'holds by definition']),
            ('sticky -m', ['commit', '-mtrivially true']),
            ('split across two -m', ['commit', '-m', 'fidelity is true by',
                                     '-m', 'construction, see the script']),
    ):
        r = make_repo(os.path.join(tmp, 'msg-' + label.replace(' ', '-')))
        write(r, 'a.txt', 'x\n')
        if '-am' not in args:
            git(r, 'add', 'a.txt')
        check('commit-msg hook refuses via %s' % label, git(r, *args).returncode, 1)

    r = make_repo(os.path.join(tmp, 'msg-file'))
    write(r, 'a.txt', 'x\n')
    write(r, 'msg.txt', 'fidelity is true by construction\n')
    git(r, 'add', 'a.txt')
    check('commit-msg hook refuses via --file=',
          git(r, 'commit', '--file=msg.txt').returncode, 1)

    # Clean input, both shapes that must pass.
    r = make_repo(os.path.join(tmp, 'msg-backed'))
    write(r, 'a.txt', 'x\n')
    git(r, 'add', 'a.txt')
    check('commit-msg hook allows the phrase when an artifact is named',
          git(r, 'commit', '-m',
              'not true by construction: proved by scripts/Assert-X.py').returncode, 0)

    r = make_repo(os.path.join(tmp, 'msg-plain'))
    write(r, 'a.txt', 'x\n')
    git(r, 'add', 'a.txt')
    check('commit-msg hook allows an ordinary message',
          git(r, 'commit', '-m', 'add a file').returncode, 0)


def case_hub_checks(tmp):
    """Both directions of gate 5, which the old suite never exercised at all."""
    root = make_repo(os.path.join(tmp, 'hub-absent'))
    write(root, 'scripts/Assert-ReferenceIntegrity.py', 'import sys\nsys.exit(0)\n')
    write(root, 'scripts/Test-HubRegistrySchema.py', 'import sys\nsys.exit(0)\n')
    git(root, 'add', '-A')
    out = git(root, 'commit', '-m', 'touch scripts')
    check('an unreachable Hub clone blocks rather than skipping',
          out.returncode, 1, out.stderr)
    check_in('the refusal says a skip is not a pass', 'HUB CHECKS COULD NOT RUN',
             out.stderr)

    hub = os.path.join(tmp, 'fake-hub')
    os.makedirs(hub)
    root = make_repo(os.path.join(tmp, 'hub-fail'))
    write(root, 'scripts/Assert-ReferenceIntegrity.py',
          'import sys\nprint("dangling reference")\nsys.exit(1)\n')
    write(root, 'scripts/Test-HubRegistrySchema.py', 'import sys\nsys.exit(0)\n')
    git(root, 'add', '-A')
    out = git(root, 'commit', '-m', 'touch scripts', extra_env={'WG_HUB_CLONE': hub})
    check('a failing Hub check blocks the commit', out.returncode, 1, out.stderr)

    root = make_repo(os.path.join(tmp, 'hub-pass'))
    write(root, 'scripts/Assert-ReferenceIntegrity.py', 'import sys\nsys.exit(0)\n')
    write(root, 'scripts/Test-HubRegistrySchema.py', 'import sys\nsys.exit(0)\n')
    git(root, 'add', '-A')
    check('passing Hub checks allow the commit',
          git(root, 'commit', '-m', 'touch scripts',
              extra_env={'WG_HUB_CLONE': hub}).returncode, 0)

    # The committed copy is what runs: a doctored working tree must not help.
    root = make_repo(os.path.join(tmp, 'hub-worktree-swap'))
    write(root, 'scripts/Assert-ReferenceIntegrity.py', 'import sys\nsys.exit(1)\n')
    write(root, 'scripts/Test-HubRegistrySchema.py', 'import sys\nsys.exit(0)\n')
    git(root, 'add', '-A')
    write(root, 'scripts/Assert-ReferenceIntegrity.py', 'import sys\nsys.exit(0)\n')
    check('the staged checker runs, not the working-tree one',
          git(root, 'commit', '-m', 'touch scripts',
              extra_env={'WG_HUB_CLONE': hub}).returncode, 1)

    root = make_repo(os.path.join(tmp, 'hub-untouched'))
    write(root, 'note.md', 'nothing to do with scripts\n')
    git(root, 'add', '-A')
    check('a commit outside scripts/ and evidence/ needs no Hub clone',
          git(root, 'commit', '-m', 'note').returncode, 0)


# --------------------------------------------------------------------------
# PreToolUse guard: only the bypasses a git hook cannot see
# --------------------------------------------------------------------------

def case_guard(tmp):
    root = make_repo(os.path.join(tmp, 'guard'))
    for command, want, label in (
            ('git commit --no-verify -m x', 2, 'refuses --no-verify'),
            ('git commit -n -m x', 2, 'refuses -n'),
            ('git commit-tree $T -p HEAD -m x', 2, 'refuses commit-tree'),
            ('git update-ref HEAD $C', 2, 'refuses update-ref'),
            ('git filter-branch --tree-filter "true" HEAD', 2, 'refuses filter-branch'),
            ('git push --force origin main', 2, 'refuses --force'),
            ('git push -f origin main', 2, 'refuses -f'),
            ('git push --mirror origin', 2, 'refuses --mirror'),
            ('git push origin +main:main', 2, 'refuses a plus refspec'),
            ('git push --force origin main && echo --force-with-lease', 2,
             'a later --force-with-lease does not disarm the push gate'),
            ('git push --force-with-lease origin main', 0, 'allows a lease push'),
            ('git push -u origin main', 0, 'allows an ordinary push'),
            ('git commit -m ok', 0, 'allows an ordinary commit'),
            ('git status', 0, 'allows git status'),
            ('ls -la', 0, 'ignores a command with no git'),
    ):
        code, _, err = run_hook(GATE_COMMIT, commit_payload(root, command))
        check('guard %s' % label, code, want, err)

    code, _, err = run_hook(GATE_COMMIT, {
        'hook_event_name': 'PreToolUse', 'tool_name': 'Read', 'cwd': root,
        'tool_input': {'command': 'git commit --no-verify -m x'}})
    check('guard ignores a non-Bash tool carrying the same command', code, 0, err)

    # hooksPath unset means every content gate is inert, so it is refused.
    bare = make_repo(os.path.join(tmp, 'guard-unconfigured'))
    git(bare, 'config', '--unset', 'core.hooksPath')
    code, _, err = run_hook(GATE_COMMIT, commit_payload(bare, 'git commit -m x'))
    check('guard refuses a commit when core.hooksPath is unset', code, 2, err)
    check_in('the refusal gives the setup command', 'core.hooksPath', err)
    code, _, err = run_hook(GATE_COMMIT, commit_payload(bare, 'git status'))
    check('guard still allows a read-only command when unconfigured', code, 0, err)

    nogates = make_repo(os.path.join(tmp, 'guard-other-repo'), with_gates=False)
    code, _, err = run_hook(GATE_COMMIT, commit_payload(nogates, 'git commit -m x'))
    check('guard leaves a repository without these gates alone', code, 0, err)


# --------------------------------------------------------------------------
# Stop gate
# --------------------------------------------------------------------------

def case_persistence(tmp):
    root = make_repo(os.path.join(tmp, 'stop'))
    payload = {'hook_event_name': 'Stop', 'cwd': root, 'session_id': 'sess-1'}
    check('stop gate allows a clean tree', run_hook(GATE_STOP, payload)[0], 0)

    write(root, 'STATE.md', '# State\n\nchanged\n')
    code, _, err = run_hook(GATE_STOP, payload)
    check('stop gate refuses an uncommitted governed file', code, 2, err)
    check_in('the refusal names the file', 'STATE.md', err)
    check('stop gate raises the same content once',
          run_hook(GATE_STOP, payload)[0], 0)

    write(root, 'STATE.md', '# State\n\ndifferent content entirely\n')
    check('stop gate raises again when the content changes, not just the path',
          run_hook(GATE_STOP, payload)[0], 2)

    for name in ('AGENT-SSOT.json', 'USER-SSOT.json'):
        r = make_repo(os.path.join(tmp, 'stop-' + name))
        write(r, name, '{"a":1}\n')
        check('stop gate governs %s' % name,
              run_hook(GATE_STOP, {'hook_event_name': 'Stop', 'cwd': r,
                                   'session_id': 's'})[0], 2)

    for rel in ('plans/p.md', 'evidence/e.md', 'rules/r.md', '_intake-hub/i.md',
                'scripts/s.py', '.claude/c.json', '.githooks/h'):
        r = make_repo(os.path.join(tmp, 'stop-prefix-' + rel.replace('/', '-')))
        write(r, rel, 'x\n')
        check('stop gate governs %s' % rel,
              run_hook(GATE_STOP, {'hook_event_name': 'Stop', 'cwd': r,
                                   'session_id': 's'})[0], 2)

    r = make_repo(os.path.join(tmp, 'stop-ungoverned'))
    write(r, 'scratch.txt', 'temp\n')
    check('stop gate ignores an ungoverned file',
          run_hook(GATE_STOP, {'hook_event_name': 'Stop', 'cwd': r,
                               'session_id': 's2'})[0], 0)

    # A linked worktree used to disable the gate outright: .git is a file there.
    wt = os.path.join(tmp, 'stop-wt')
    git(root, 'worktree', 'add', '-q', '-b', 'side', wt)
    write(wt, 'DECISIONS.md',
          '# Decisions\n\nPreamble line.\n\n**D-1.** First.\n**D-2.** Second.\n**D-3.** x\n')
    check('stop gate works inside a linked worktree',
          run_hook(GATE_STOP, {'hook_event_name': 'Stop', 'cwd': wt,
                               'session_id': 's3'})[0], 2)

    other = os.path.join(tmp, 'other')
    os.makedirs(other)
    git(other, 'init', '-q')
    write(other, 'README.md', 'unrelated\n')
    check('stop gate ignores another repository',
          run_hook(GATE_STOP, {'hook_event_name': 'Stop', 'cwd': other,
                               'session_id': 's4'})[0], 0)


# --------------------------------------------------------------------------
# Injector
# --------------------------------------------------------------------------

def case_inject(tmp):
    root = make_repo(os.path.join(tmp, 'inject'))
    code, out, err = run_hook(INJECT, {'hook_event_name': 'UserPromptSubmit',
                                       'cwd': root})
    check('injector reads a position table', code, 0, err)
    check_in('injector emits the authority notice', 'AUTHORITATIVE PLAN POSITION', out)
    check_in('injector emits a step row', '1 -- Done', out)
    check_in('injector emits the next action', 'Next action', out)

    # A heading that merely contains the wanted words must not be captured.
    write(root, 'STATE.md',
          '# State\n\n## Current state and blockers\n\nnot the blockers section\n\n'
          '## Blockers\n\n| # | Blocker |\n|---|---|\n| B-9 | the real one |\n\n'
          '## Next action\n\ngo\n')
    code, out, _ = run_hook(INJECT, {'hook_event_name': 'UserPromptSubmit',
                                     'cwd': root})
    check_in('injector matches a heading exactly, not by substring',
             'B-9 -- the real one', out)
    ok = 'not the blockers section' not in out
    RESULTS.append((ok, 'injector does not capture a similarly named section'))
    print('%s  injector does not capture a similarly named section'
          % ('PASS' if ok else 'FAIL'))

    # A closed row whose marker falls past the clip point must still read closed.
    write(root, 'STATE.md',
          '# State\n\n## Blockers\n\n| # | Blocker |\n|---|---|\n| B-1 | %s ~~CLOSED~~ |\n\n'
          '## Next action\n\ngo\n' % ('padding ' * 40))
    code, out, _ = run_hook(INJECT, {'hook_event_name': 'UserPromptSubmit',
                                     'cwd': root})
    check_in('injector labels a closed row it has to clip', '[closed]', out)

    # A large table must not push the next action out of the injection.
    rows = '\n'.join('| %d | %s |' % (i, 'state text ' * 12)
                     for i in range(1, 41))
    write(root, 'STATE.md',
          '# State\n\n## Position in the plan sequence\n\n| Plan step | State |\n'
          '|---|---|\n%s\n\n## Next action\n\nthe decisive line\n' % rows)
    code, out, _ = run_hook(INJECT, {'hook_event_name': 'UserPromptSubmit',
                                     'cwd': root})
    check_in('injector keeps the next action when it must trim', 'the decisive line', out)
    check_in('injector says what it trimmed', 'trimmed to fit', out)

    # A differently worded header row must not be injected as a step.
    write(root, 'STATE.md',
          '# State\n\n## Position in the plan sequence\n\n| Step | Status |\n'
          '|---|---|\n| 7 | Done |\n\n## Next action\n\ngo\n')
    code, out, _ = run_hook(INJECT, {'hook_event_name': 'UserPromptSubmit',
                                     'cwd': root})
    ok = 'Step -- Status' not in out
    RESULTS.append((ok, 'injector does not emit a header row as a step'))
    print('%s  injector does not emit a header row as a step'
          % ('PASS' if ok else 'FAIL'))

    write(root, 'STATE.md', '# State\n\nno position section here\n')
    code, out, _ = run_hook(INJECT, {'hook_event_name': 'UserPromptSubmit',
                                     'cwd': root})
    check('injector never blocks on a missing section', code, 0)
    check_in('injector reports a missing section', 'POSITION NOT READ', out)

    other = os.path.join(tmp, 'inject-other')
    os.makedirs(other)
    git(other, 'init', '-q')
    code, out, _ = run_hook(INJECT, {'hook_event_name': 'UserPromptSubmit',
                                     'cwd': other})
    check('injector is silent outside this repository', code, 0)
    ok = out.strip() == ''
    RESULTS.append((ok, 'injector emits nothing outside this repository'))
    print('%s  injector emits nothing outside this repository'
          % ('PASS' if ok else 'FAIL'))


# --------------------------------------------------------------------------
# Mutation proof: break each gate and require the suite to notice
# --------------------------------------------------------------------------

MUTATIONS = (
    ('wg_gates.py', "if entry_removals:", "if False:",
     'append-only never blocks'),
    ('wg_gates.py', "for m in ENTRY_MARKERS", "for m in ()",
     'append-only sees no entry markers'),
    ('wg_gates.py', "if re.search(pattern, body):", "if False:",
     'secret scan never matches'),
    ('wg_gates.py', "if bad:", "if False:",
     'encoding check never blocks'),
    ('wg_gates.py', "if out.returncode != 0:\n            tail", "if False:\n            tail",
     'Hub check never blocks on failure'),
    ('wg_gates.py', "if not os.path.isdir(hub):", "if False and not os.path.isdir(hub):",
     'unreachable Hub clone silently skips'),
    ('wg_gates.py', "cites_artifact = any(", "cites_artifact = True or any(",
     'claim check always finds an artifact'),
    ('wg_gates.py', "spec = ':' + path if diff_args", "spec = 'HEAD:' + path if diff_args",
     'encoding check reads the wrong tree'),
    ('gate_commit.py', "if NO_VERIFY.search(command):", "if False:",
     'guard stops refusing --no-verify'),
    ('gate_commit.py', "for word, why in PLUMBING:", "for word, why in ():",
     'guard stops refusing plumbing'),
    ('gate_commit.py', "if value != HOOKS_PATH_EXPECTED:", "if False:",
     'guard stops requiring hooksPath'),
    ('gate_persistence.py', "GOVERNED_PREFIXES = (", "GOVERNED_PREFIXES = () or (",
     'CONTROL: a no-op edit must NOT be flagged', 'survives'),
    ('gate_persistence.py', "return path in GOVERNED_ROOT_FILES or path.startswith(GOVERNED_PREFIXES)",
     "return path in () or path.startswith(())",
     'persistence governs nothing'),
    ('gate_persistence.py', "digest.update(out)", "pass",
     'persistence ignores content when fingerprinting'),
    ('gate_persistence.py', "code, out = git(root, ['rev-parse', '--git-path', 'wg-stop-gate-%s' % session])",
     "code, out = (1, b'')",
     'persistence cannot resolve its marker path'),
    ('inject_plan_position.py', "if line.startswith('## ') and normalise(line[3:]) == want:",
     "if line.startswith('## ') and want in normalise(line[3:]):",
     'injector matches a heading by substring again'),
    ('inject_plan_position.py', "if cells[0].lower() in HEADER_CELLS:", "if False:",
     'injector emits header rows as data'),
    ('inject_plan_position.py', "if len(step_lines) > 3:", "if False:",
     'injector truncates the tail instead of the table'),
)


def run_mutations():
    print('\n=== mutation proof: each row breaks a gate and the suite must notice ===')
    survivors = []
    for row in MUTATIONS:
        filename, old, new, label = row[:4]
        expect = row[4] if len(row) > 4 else 'caught'
        work = tempfile.mkdtemp(prefix='wg-mutate-')
        hooks = os.path.join(work, 'hooks')
        ghooks = os.path.join(work, 'githooks')
        shutil.copytree(HOOKS, hooks,
                        ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(GITHOOKS, ghooks)
        target = os.path.join(hooks, filename)
        source = open(target, encoding='utf-8').read()
        if old not in source:
            print('SKIP  %-58s pattern not found -- mutation is stale' % label)
            survivors.append(label + ' (stale mutation)')
            shutil.rmtree(work, ignore_errors=True)
            continue
        open(target, 'w', encoding='utf-8').write(source.replace(old, new, 1))
        proc = subprocess.run(
            [sys.executable, os.path.join(hooks, 'test_hooks.py')],
            capture_output=True, text=True, timeout=900,
            env=env({'WG_HOOKS_DIR': hooks, 'WG_GITHOOKS_DIR': ghooks}))
        noticed = proc.returncode != 0
        wanted = (expect == 'caught')
        verdict = 'caught' if noticed else 'survived'
        ok = (noticed == wanted)
        print('%-8s %-58s suite exit=%d %s' % (verdict, label, proc.returncode,
                                               '' if ok else '<-- WRONG'))
        if not ok:
            survivors.append('%s (expected to be %s)' % (label, expect))
        shutil.rmtree(work, ignore_errors=True)
    print('\n%d mutation(s), %d behaved wrongly.' % (len(MUTATIONS), len(survivors)))
    for label in survivors:
        print('  WRONG: %s' % label)
    return survivors


def main():
    tmp = tempfile.mkdtemp(prefix='wg-hook-tests-')
    try:
        case_append_only(tmp)
        case_secrets(tmp)
        case_ascii(tmp)
        case_message(tmp)
        case_hub_checks(tmp)
        case_guard(tmp)
        case_persistence(tmp)
        case_inject(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    failed = [r for r in RESULTS if not r[0]]
    print('\n%d case(s), %d failed.' % (len(RESULTS), len(failed)))
    for _, name in failed:
        print('  FAILED: %s' % name)
    status = 1 if failed else 0

    if '--mutations' in sys.argv:
        survivors = run_mutations()
        if survivors:
            status = 1
    return status


if __name__ == '__main__':
    sys.exit(main())
