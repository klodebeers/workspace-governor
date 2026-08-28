# CLI_PAYLOAD_KEYS: payloads in this suite must match the CLI's own shape.
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
GATE_DELEGATION = os.path.join(HOOKS, 'gate_delegation.py')
INJECT_DELEGATION = os.path.join(HOOKS, 'inject_delegation_check.py')
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
    write(path, 'rules/VERIFICATION-RESOLUTION.md',
          '# Verification Resolution Rule\n\n## Performer selection\n')
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
# Delegation: a claim of independent review needs an independent performer
# --------------------------------------------------------------------------

CLAIM = 'Two adversarial auditors reviewed this independently.'
DISCLAIMED = 'No independent review ran; I checked my own work.'


def transcript(root, name, delegates):
    """Write a synthetic transcript with `delegates` delegate spawns."""
    path = os.path.join(root, name)
    with open(path, 'w', encoding='utf-8') as handle:
        handle.write(json.dumps({'type': 'assistant', 'message': {
            'content': [{'type': 'text', 'text': 'working'}]}}) + '\n')
        for _ in range(delegates):
            handle.write(json.dumps({'type': 'assistant', 'message': {
                'content': [{'type': 'tool_use', 'name': 'Agent',
                             'input': {}}]}}) + '\n')
    return path


def stop_payload(root, message, transcript_path, session='d1'):
    return {'hook_event_name': 'Stop', 'cwd': root, 'session_id': session,
            'transcript_path': transcript_path,
            'last_assistant_message': message}


def case_delegation(tmp):
    root = make_repo(os.path.join(tmp, 'delegation'))
    none = transcript(root, 'none.jsonl', 0)
    one = transcript(root, 'one.jsonl', 1)

    code, _, err = run_hook(GATE_DELEGATION, stop_payload(root, CLAIM, none))
    check('delegation gate refuses a review claim with no delegate', code, 2, err)
    check_in('the refusal cites the performer rule', 'Performer selection', err)

    check('delegation gate allows the same claim with a delegate',
          run_hook(GATE_DELEGATION, stop_payload(root, CLAIM, one, 'd2'))[0], 0)

    check('delegation gate ignores a message making no such claim',
          run_hook(GATE_DELEGATION,
                   stop_payload(root, 'I fixed the parser and pushed.', none,
                                'd3'))[0], 0)

    check('delegation gate allows an honest self-review statement',
          run_hook(GATE_DELEGATION, stop_payload(root, DISCLAIMED, none, 'd4'))[0], 0)

    for phrasing in ('An independent audit confirmed it.',
                     'I adversarially verified the fix.',
                     'This got a blind review before landing.',
                     'It was reviewed independently.'):
        code, _, _ = run_hook(GATE_DELEGATION,
                              stop_payload(root, phrasing, none, 'd-' + phrasing[:6]))
        check('delegation gate catches %r' % phrasing[:28], code, 2)

    # A claim it cannot check must fail, not pass -- LEARNINGS.md L-026.
    code, _, err = run_hook(GATE_DELEGATION,
                            stop_payload(root, CLAIM,
                                         os.path.join(root, 'missing.jsonl'), 'd5'))
    check('an unreadable transcript fails rather than passing', code, 2, err)
    check_in('it says the check could not run', 'COULD NOT RUN', err)

    # Raised once per message, and again when the message changes.
    payload = stop_payload(root, CLAIM, none, 'd6')
    check('delegation gate raises a claim once',
          run_hook(GATE_DELEGATION, payload)[0], 2)
    check('delegation gate does not repeat the same claim',
          run_hook(GATE_DELEGATION, payload)[0], 0)
    check('delegation gate raises again on a different claim',
          run_hook(GATE_DELEGATION,
                   stop_payload(root, 'An independent audit says otherwise.',
                                none, 'd6'))[0], 2)

    nogates = make_repo(os.path.join(tmp, 'delegation-other'), with_gates=False)
    os.remove(os.path.join(nogates, 'rules', 'VERIFICATION-RESOLUTION.md'))
    check('delegation gate leaves a repository without the rule alone',
          run_hook(GATE_DELEGATION, stop_payload(nogates, CLAIM, none, 'd7'))[0], 0)


def case_delegation_injection(tmp):
    root = make_repo(os.path.join(tmp, 'delegation-inject'))

    def ask(prompt):
        return run_hook(INJECT_DELEGATION,
                        {'hook_event_name': 'UserPromptSubmit', 'cwd': root,
                         'prompt': prompt})

    for prompt in ('review the change before I merge it',
                   'audit what you just wrote',
                   'can you verify this is right',
                   'double-check the migration',
                   'prove the gate works'):
        code, out, _ = ask(prompt)
        check('injection fires on %r' % prompt[:26], code, 0)
        check_in('and carries the criteria for %r' % prompt[:18],
                 'PERFORMER CHECK', out)

    for prompt in ('add a function that parses the header',
                   'what is the current plan position'):
        code, out, _ = ask(prompt)
        ok = code == 0 and out.strip() == ''
        RESULTS.append((ok, 'injection stays quiet on %r' % prompt[:26]))
        print('%s  injection stays quiet on %r'
              % ('PASS' if ok else 'FAIL', prompt[:26]))

    nogates = make_repo(os.path.join(tmp, 'delegation-inject-other'),
                        with_gates=False)
    os.remove(os.path.join(nogates, 'rules', 'VERIFICATION-RESOLUTION.md'))
    code, out, _ = run_hook(INJECT_DELEGATION,
                            {'hook_event_name': 'UserPromptSubmit',
                             'cwd': nogates, 'prompt': 'review this'})
    ok = code == 0 and out.strip() == ''
    RESULTS.append((ok, 'injection is silent where the rule is not held'))
    print('%s  injection is silent where the rule is not held'
          % ('PASS' if ok else 'FAIL'))


# --------------------------------------------------------------------------
# Mutation proof: break each gate and require the suite to notice
# --------------------------------------------------------------------------

INJECT_RULES = os.path.join(HOOKS, 'inject_rules.py')
# REPO is derived from __file__, which is wrong under WG_HOOKS_DIR: the
# mutation harness runs a COPY of this suite out of a temp dir, so REPO
# resolves to the temp parent and any repo-relative path breaks. The
# override matches WG_HOOKS_DIR / WG_GITHOOKS_DIR, which exist for exactly
# this reason. Without it the suite crashed in every mutation run, and a
# crash reads as 'the mutation was caught' -- a clean result meaning nothing.
SCRIPTS = os.environ.get('WG_SCRIPTS_DIR') or os.path.join(REPO, 'scripts')
RULE_CHECKER = os.path.join(SCRIPTS, 'Assert-RuleTriggerFidelity.py')

_TABLE = ('{"entries": [{"id": "ev", "file": "AGENTS.md", '
          '"heading": "Evidence standard", "triggers": ["\\\\bverified\\\\b"]}]}')


def _rules_repo(path):
    """A repo wired for the rule injector: table, hook and checker all present."""
    root = make_repo(path)
    if not os.path.isfile(RULE_CHECKER) or not os.path.isfile(INJECT_RULES):
        raise RuntimeError(
            'rule-trigger fixtures missing: %s / %s. Failing loudly rather than '
            'crashing mid-case, because a crash here reads as a caught mutation.'
            % (RULE_CHECKER, INJECT_RULES))
    write(root, 'AGENTS.md',
          '# Agents\n\n## Evidence standard\n\nNever present confidence as '
          'verification.\n\n## Secrets\n\nNone here.\n')
    shutil.copy(INJECT_RULES, os.path.join(root, '.claude', 'hooks',
                                           'inject_rules.py'))
    os.makedirs(os.path.join(root, 'scripts'), exist_ok=True)
    shutil.copy(RULE_CHECKER, os.path.join(root, 'scripts',
                                           'Assert-RuleTriggerFidelity.py'))
    write(root, '.claude/hooks/rule-triggers.json', _TABLE)
    git(root, 'add', '-A')
    git(root, 'commit', '-q', '-m', 'wire rules', '--no-verify')
    return root


def case_rule_triggers(tmp):
    # Clean direction: an entry that resolves must not block anything.
    root = _rules_repo(os.path.join(tmp, 'rules-clean'))
    write(root, 'note.md', 'ordinary edit\n')
    git(root, 'add', 'note.md')
    check('git hook allows a commit while every rule entry resolves',
          git(root, 'commit', '-m', 'note').returncode, 0)

    # The silent case: reword the OWNING heading and leave the table alone.
    # Nothing about the table or the hook changes, so only a gate that reads
    # both sides can see it.
    root = _rules_repo(os.path.join(tmp, 'rules-broken'))
    write(root, 'AGENTS.md',
          '# Agents\n\n## Evidence standards\n\nNever present confidence as '
          'verification.\n\n## Secrets\n\nNone here.\n')
    git(root, 'add', 'AGENTS.md')
    out = git(root, 'commit', '-m', 'reword')
    check('git hook refuses a reworded heading that a rule entry cites',
          out.returncode, 1, out.stderr)
    check_in('the refusal names the rule-trigger gate',
             'RULE TRIGGER DOES NOT RESOLVE', out.stderr)

    # A table with no checker beside it must fail, not skip (L-026).
    root = _rules_repo(os.path.join(tmp, 'rules-nochecker'))
    os.remove(os.path.join(root, 'scripts', 'Assert-RuleTriggerFidelity.py'))
    git(root, 'add', '-A')
    out = git(root, 'commit', '-m', 'drop the checker')
    check('git hook refuses when the rule checker is missing',
          out.returncode, 1, out.stderr)
    check_in('the missing checker is reported as unrunnable, not as a pass',
             'CHECK COULD NOT RUN', out.stderr)

    # Table and checker present but the hook itself gone. The checker imports
    # its matcher from inject_rules.py, and that import used to sys.exit(2) --
    # SystemExit is not an Exception, so it tore down the whole pre-commit run
    # past the findings mechanism instead of producing one finding.
    root = _rules_repo(os.path.join(tmp, 'rules-noinjector'))
    os.remove(os.path.join(root, '.claude', 'hooks', 'inject_rules.py'))
    git(root, 'add', '-A')
    out = git(root, 'commit', '-m', 'drop the injector')
    check('git hook refuses when the injector the checker imports is missing',
          out.returncode, 1, out.stderr)
    check_in('a missing injector produces a finding, not a torn-down run',
             'CHECK COULD NOT RUN', out.stderr)
    ok = 'Traceback' not in out.stderr
    RESULTS.append((ok, 'the missing injector does not crash the gate run'))
    print('%s  the missing injector does not crash the gate run'
          % ('ok  ' if ok else 'FAIL'))

    # The split commit: reword the heading in the owning file, update the table,
    # stage only the file. The first gate read the worktree, found it
    # self-consistent, and passed -- leaving HEAD with the new heading and the
    # old table, and the injector emitting NOT READ from then on.
    root = _rules_repo(os.path.join(tmp, 'rules-split-commit'))
    write(root, 'AGENTS.md',
          '# Agents\n\n## Evidence and proof\n\nNever present confidence as '
          'verification.\n\n## Secrets\n\nNone here.\n')
    write(root, '.claude/hooks/rule-triggers.json',
          _TABLE.replace('Evidence standard', 'Evidence and proof'))
    git(root, 'add', 'AGENTS.md')            # the table edit stays UNSTAGED
    out = git(root, 'commit', '-m', 'reword, half staged')
    check('git hook refuses a split commit the worktree hides',
          out.returncode, 1, out.stderr)
    check_in('and names the rule-trigger gate', 'RULE TRIGGER DOES NOT RESOLVE',
             out.stderr)
    git(root, 'add', '-A')                   # both halves together must pass
    check('git hook allows the same change with both halves staged',
          git(root, 'commit', '-m', 'reword, fully staged').returncode, 0)

    # Mirror case: an unstaged edit must not block an unrelated commit.
    root = _rules_repo(os.path.join(tmp, 'rules-unstaged'))
    write(root, 'AGENTS.md', '# Agents\n\n## Something else\n\nx\n')
    write(root, 'unrelated.txt', 'hi\n')
    git(root, 'add', 'unrelated.txt')
    check('an unstaged heading edit does not block an unrelated commit',
          git(root, 'commit', '-m', 'unrelated').returncode, 0)

    # Deleting the table while the carrier stays wired is a bypass, not a skip.
    root = _rules_repo(os.path.join(tmp, 'rules-deleted-table'))
    git(root, 'rm', '-q', '.claude/hooks/rule-triggers.json')
    out = git(root, 'commit', '-m', 'drop the table')
    check('git hook refuses deleting the table while the injector is wired',
          out.returncode, 1, out.stderr)
    check_in('and says the mechanism would go silent',
             'RULE TABLE IS GONE BUT THE INJECTOR IS STILL WIRED', out.stderr)

    # The checker removed from the INDEX but still on disk. The earlier case
    # deleted it from both, so importlib failed either way and the guard that
    # notices "not in this commit" was never exercised -- a mutation of it
    # survived the whole suite. Without the guard the gate imports the worktree
    # copy and passes, so the commit records a table with no checker beside it.
    root = _rules_repo(os.path.join(tmp, 'rules-checker-uncommitted'))
    git(root, 'rm', '-q', '--cached', 'scripts/Assert-RuleTriggerFidelity.py')
    out = git(root, 'commit', '-m', 'uncommit the checker')
    check('git hook refuses a commit that drops the checker but keeps it on disk',
          out.returncode, 1, out.stderr)
    check_in('and reports it as unrunnable rather than passing',
             'CHECK COULD NOT RUN', out.stderr)

    # Item 2 and 3 of the fix audit had no case at all: the truncation mutant
    # and the eviction-order mutant both survived the whole suite. These are
    # the cases that make those mutations fail.
    root = _rules_repo(os.path.join(tmp, 'rules-pointer'))
    big = 'x' * 40 + ' PROHIBITION LINE THAT MUST NEVER APPEAR IN PART.\n'
    write(root, 'AGENTS.md',
          '# Agents\n\n## Evidence standard\n\n' + (big * 40) +
          '\n## Secrets\n\nNone.\n')
    code, out, err = run_hook(INJECT_RULES,
                              {'hook_event_name': 'UserPromptSubmit',
                               'cwd': root, 'prompt': 'is this verified'})
    check('an oversize section runs', code, 0, err)
    check_in('an oversize section is a pointer', 'Too large to quote', out)
    ok = 'PROHIBITION LINE THAT MUST NEVER APPEAR IN PART' not in out
    RESULTS.append((ok, 'no part of an oversize section is emitted'))
    print('%s  no part of an oversize section is emitted'
          % ('ok  ' if ok else 'FAIL'))

    # Eviction: a matched entry must outlive an always-on one that matched
    # nothing, when the total cap cannot hold both.
    root = _rules_repo(os.path.join(tmp, 'rules-eviction'))
    # Bodies sized so the total cap admits exactly one chunk: with both at
    # ~200 chars, a 320-char total holds the first and must withhold the second.
    write(root, 'AGENTS.md',
          '# Agents\n\n## Evidence standard\n\nMATCHED ENTRY BODY. '
          + 'm' * 180 + '\n\n## Secrets\n\nALWAYS ON BODY. '
          + 'a' * 180 + '\n')
    write(root, '.claude/hooks/rule-triggers.json', json.dumps({
        'max_chars_per_entry': 4000, 'max_chars_total': 320,
        'entries': [
            {'id': 'always', 'file': 'AGENTS.md', 'heading': 'Secrets',
             'always': True},
            {'id': 'ev', 'file': 'AGENTS.md', 'heading': 'Evidence standard',
             'triggers': ['\\bverified\\b']},
        ]}))
    code, out, _ = run_hook(INJECT_RULES,
                            {'hook_event_name': 'UserPromptSubmit',
                             'cwd': root, 'prompt': 'is this verified'})
    check_in('the entry the prompt matched survives eviction',
             'MATCHED ENTRY BODY', out)
    check_in('and the always-on entry is the one withheld',
             'WITHHELD for total length: always', out)

    # THE BYPASS. Neuter the checker in the WORKING TREE, stage nothing from
    # scripts/, and commit normally -- no --no-verify. The gate reconstructed
    # the staged table and owning files but then ran the worktree's checker, so
    # `return []` at the top of audit() disarmed it while the commit recorded a
    # clean checker. check_hub_scripts had this right twenty lines above and
    # said why; this side did not.
    root = _rules_repo(os.path.join(tmp, 'rules-worktree-checker'))
    checker = os.path.join(root, 'scripts', 'Assert-RuleTriggerFidelity.py')
    body = open(checker, encoding='utf-8').read()
    open(checker, 'w', encoding='utf-8').write(
        body.replace('def audit(root, table):\n    findings = []',
                     'def audit(root, table):\n    return []\n    findings = []', 1))
    write(root, 'AGENTS.md',
          '# Agents\n\n## Evidence and proof\n\nx\n\n## Secrets\n\nNone.\n')
    git(root, 'add', 'AGENTS.md')          # scripts/ deliberately NOT staged
    out = git(root, 'commit', '-m', 'reword with a neutered worktree checker')
    check('git hook refuses when only the WORKTREE checker was disarmed',
          out.returncode, 1, out.stderr)
    check_in('and it is the rule-trigger gate that refuses',
             'RULE TRIGGER DOES NOT RESOLVE', out.stderr)

    # The mirror of "table gone but injector wired".
    root = _rules_repo(os.path.join(tmp, 'rules-unwired'))
    write(root, '.claude/settings.json',
          json.dumps({'hooks': {'UserPromptSubmit': [
              {'hooks': [{'type': 'command', 'command': 'python3 other.py'}]}]}}))
    git(root, 'add', '-A')
    out = git(root, 'commit', '-m', 'unwire the injector')
    check('git hook refuses an injector present but not wired',
          out.returncode, 1, out.stderr)
    check_in('and says no rule would be injected',
             'RULE INJECTOR IS PRESENT BUT NOT WIRED', out.stderr)

    # A real symlink escaping the root. inside() was lexical, so an in-repo
    # symlink pointing anywhere on the machine passed confinement and section()
    # read straight through it. The earlier cases used ".." and absolute paths,
    # which normpath already refused -- so the realpath guard had no case and a
    # mutation of it survived the whole suite.
    root = _rules_repo(os.path.join(tmp, 'rules-symlink-escape'))
    outside = os.path.join(tmp, 'outside-the-root')
    os.makedirs(outside, exist_ok=True)
    secret = os.path.join(outside, 'ELSEWHERE.md')
    with open(secret, 'w', encoding='utf-8') as handle:
        handle.write('# Elsewhere\n\n## Evidence standard\n\n'
                     'CONTENT FROM OUTSIDE THE GOVERNANCE ROOT.\n')
    link = os.path.join(root, 'looks-local.md')
    try:
        os.symlink(secret, link)
    except (OSError, NotImplementedError):
        RESULTS.append((True, 'symlink escape (skipped: no symlink support)'))
        print('ok    symlink escape (skipped: no symlink support)')
    else:
        write(root, '.claude/hooks/rule-triggers.json', json.dumps({
            'entries': [{'id': 'esc', 'file': 'looks-local.md',
                         'heading': 'Evidence standard', 'always': True}]}))
        code, out, err = run_hook(INJECT_RULES,
                                  {'hook_event_name': 'UserPromptSubmit',
                                   'cwd': root, 'prompt': 'anything'})
        check('a symlink escaping the root still runs', code, 0, err)
        leaked = 'CONTENT FROM OUTSIDE THE GOVERNANCE ROOT' in out
        RESULTS.append((not leaked,
                        'a symlink out of the root does not leak its contents'))
        print('%s  a symlink out of the root does not leak its contents'
              % ('ok  ' if not leaked else 'FAIL'))
        check_in('and it is reported as outside the root',
                 'outside the governance root', out)

    # A repo with no table at all is untouched: not every clone wires this.
    root = make_repo(os.path.join(tmp, 'rules-absent'))
    write(root, 'note.md', 'ordinary edit\n')
    git(root, 'add', 'note.md')
    check('git hook ignores a repo that wires no rule table',
          git(root, 'commit', '-m', 'note').returncode, 0)

    # The injector itself, in both directions.
    root = _rules_repo(os.path.join(tmp, 'rules-inject'))
    code, out, err = run_hook(INJECT_RULES,
                              {'hook_event_name': 'UserPromptSubmit',
                               'cwd': root, 'prompt': 'is it verified'})
    check('rule injector runs', code, 0, err)
    check_in('rule injector emits the triggered rule', 'RULE IN SCOPE', out)
    check_in('rule injector emits the owning section text',
             'Never present confidence as verification', out)

    code, out, _ = run_hook(INJECT_RULES,
                            {'hook_event_name': 'UserPromptSubmit',
                             'cwd': root, 'prompt': 'what time is it'})
    ok = 'RULE IN SCOPE' not in out
    RESULTS.append((ok, 'rule injector stays silent when no trigger matches'))
    print('%s  rule injector stays silent when no trigger matches'
          % ('ok  ' if ok else 'FAIL'))

    write(root, 'AGENTS.md', '# Agents\n\n## Evidence standards\n\nx\n')
    code, out, _ = run_hook(INJECT_RULES,
                            {'hook_event_name': 'UserPromptSubmit',
                             'cwd': root, 'prompt': 'is it verified'})
    check_in('rule injector says NOT READ rather than falling silent',
             'RULE NOT READ', out)


def case_payload_shape(tmp):
    """The payload contract itself, asserted against the CLI's own shape.

    Every injector case built its payload with `user_prompt`, a key the CLI has
    never sent -- it is a telemetry attribute. The hooks read it, got an empty
    string, and every trigger missed. The suite passed 129/129 against a shape
    that does not exist, which is why nothing caught it: a self-confirming
    fixture proves only that the fixture agrees with itself.
    """
    root = _rules_repo(os.path.join(tmp, 'payload-shape'))
    exact = {'session_id': 's1', 'transcript_path': '/tmp/t.jsonl',
             'cwd': root, 'permission_mode': 'default',
             'hook_event_name': 'UserPromptSubmit',
             'prompt': 'is this verified'}
    code, out, err = run_hook(INJECT_RULES, exact)
    check('injector fires on the exact CLI payload shape', code, 0, err)
    check_in('and reaches a triggered entry, not just the always-on one',
             'Evidence standard', out)

    code, out, err = run_hook(INJECT_DELEGATION, exact)
    check('delegation injector fires on the exact CLI payload shape', code, 0, err)
    check_in('delegation criteria actually reach context', 'PERFORMER CHECK', out)

    # No prompt key at all must not crash: prompt_text() once recursed here.
    code, out, err = run_hook(INJECT_RULES, {'cwd': root})
    check('no prompt key does not crash the injector', code, 0, err)
    code, out, err = run_hook(INJECT_DELEGATION, {'cwd': root})
    check('no prompt key does not crash the delegation injector', code, 0, err)


    # WG_RULES_ROOT relocates the root of governance from an environment
    # variable. Pointed at a directory with no table it used to print nothing
    # at all -- the loudest action, switching every rule off, on the quietest
    # code path.
    empty = os.path.join(tmp, 'empty-governance-root')
    os.makedirs(empty, exist_ok=True)
    code, out, err = run_hook(INJECT_RULES, {'cwd': root, 'prompt': 'anything'},
                              {'WG_RULES_ROOT': empty})
    check('an override root with no table still runs', code, 0, err)
    check_in('and says so rather than falling silent', 'WG_RULES_ROOT', out)
    ok = 'do not treat that as permission' in out
    RESULTS.append((ok, 'and does not let silence read as permission'))
    print('%s  and does not let silence read as permission'
          % ('ok  ' if ok else 'FAIL'))

    # .git is inside the root but is not governance, and section()'s heading
    # regex matches git-config comment lines.
    from inject_rules import inside as _inside
    for name, want in (('.git/config', False), ('.git', False),
                       ('AGENTS.md', True)):
        got = _inside(root, name)
        check('inside(%s)' % name, got, want)

    # The legacy key keeps working, so a payload change cannot re-break this.
    code, out, _ = run_hook(INJECT_RULES, {'cwd': root,
                                           'user_prompt': 'is this verified'})
    check_in('legacy user_prompt key still honoured', 'Evidence standard', out)


def case_checker_selftest(tmp):
    """Run the checker's own selftest as a suite case.

    Nothing automated ran it, so every check living in
    Assert-RuleTriggerFidelity.py was proven only by a command a human had to
    remember. A mutation of any of them survived the whole suite.
    """
    del tmp
    out = subprocess.run([sys.executable, RULE_CHECKER, '--selftest'],
                         capture_output=True, text=True, env=env())
    check('the rule checker selftest passes', out.returncode, 0,
          out.stdout[-400:] + out.stderr[-400:])
    check_in('and reports every case', 'selftest cases passed', out.stdout)


MUTATIONS = (
    ('wg_gates.py', "        checker = os.path.join(work, checker_rel.replace('/', os.sep))",
     "        checker = os.path.join(root, checker_rel)",
     'gate runs the worktree checker instead of the committed one'),
    ('wg_gates.py', "    if hcode == 0 and scode == 0 and b'inject_rules.py' not in sraw:",
     "    if False:", 'gate stops noticing an unwired injector'),
    ('inject_rules.py', "    if not (real + os.sep).startswith(realroot + os.sep):",
     "    if False:", 'confinement stops resolving symlinks'),
    ('inject_rules.py', "        if os.path.isdir(override) and os.path.isfile(table):",
     "        if os.path.isdir(override):",
     'override root accepted with no table, silently'),
    ('inject_rules.py', "        return pointer(source, len(body), entry_cap)",
     "        return 'RULE IN SCOPE -- %s\\n\\n%s\\n' % (source, body[:entry_cap])",
     'oversize section truncated instead of pointered'),
    ('inject_rules.py', "    for entry in matched + unconditional:",
     "    for entry in unconditional + matched:",
     'always-on entry regains eviction priority'),
    ('scripts/Assert-RuleTriggerFidelity.py', "        if not inside(root, name):",
     "        if False:", 'checker stops refusing a file outside the root'),
    ('scripts/Assert-RuleTriggerFidelity.py', "            _, bad = positive_int(table.get(field), 1)",
     "            _, bad = (1, [])", 'checker stops checking caps'),
    ('scripts/Assert-RuleTriggerFidelity.py', "                problem = compiles_safely(pattern)",
     "                problem = None", 'checker stops checking regex safety'),
    ('scripts/Assert-RuleTriggerFidelity.py', "            if isinstance(triggers, str) or not isinstance(triggers, list):",
     "            if False:", 'checker stops refusing triggers-as-string'),
    ('scripts/Assert-RuleTriggerFidelity.py', "            if len(shared) >= WHY_VERBATIM_LIMIT:",
     "            if False:", 'why-verbatim check disabled'),
    ('wg_gates.py', "prefix = ':' if diff_args == ['--cached'] else 'HEAD:'",
     "prefix = 'HEAD:' if diff_args == ['--cached'] else 'HEAD:'",
     'rule gate reads the wrong tree'),
    # Retargeted: the non-string-prompt fix rewrote the line this used to break.
    # Second time a fix of mine made a row stale, and the harness reporting a
    # stale row as WRONG is what caught both -- a row whose pattern is gone
    # tests nothing while still being counted.
    ('inject_rules.py', "    text = payload.get('prompt')",
     "    text = payload.get('nope')",
     'injector reads a key the CLI does not send'),
    # Survives BY DESIGN, and saying so is the honest record. Once the checker
    # raises ImportError instead of calling sys.exit, `except Exception` catches
    # it too, so flipping this is a no-op today. The BaseException catch guards a
    # FUTURE checker that exits at import; no case can discriminate it now, and
    # pretending one does would be the decorative-case defect D-65 warns about.
    ('wg_gates.py', "except BaseException as exc:", "except Exception as exc:",
     'CONTROL: BaseException catch is redundant while the checker raises',
     'survives'),
    ('wg_gates.py', "for item in broken:", "for item in ():",
     'rule-trigger gate never blocks'),
    # Retargeted after check_rule_triggers was rewritten to read the staged
    # tree: the isfile(checker) guard it used to break no longer exists, and a
    # mutation whose pattern is gone is reported stale -- a decorative case
    # under another name. This breaks the guard that now stands in its place.
    ('wg_gates.py', "    if ccode != 0:", "    if False:",
     'gate stops noticing that the checker is not in the commit'),
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
    ('gate_delegation.py', "CLAIM_PATTERNS = (", "CLAIM_PATTERNS = () or (",
     'CONTROL: a no-op edit to the claim list must NOT be flagged', 'survives'),
    ('gate_delegation.py', "    for pattern in CLAIM_PATTERNS:\n        found = re.search(pattern, message, re.I)",
     "    for pattern in ():\n        found = re.search(pattern, message, re.I)",
     'delegation gate stops recognising a claim'),
    ('gate_delegation.py', "    for pattern in DISCLAIMER_PATTERNS:", "    for pattern in ():",
     'delegation gate refuses an honest self-review statement'),
    ('gate_delegation.py', "    if delegates > 0:", "    if delegates >= 0:",
     'delegation gate treats zero delegates as enough'),
    ('gate_delegation.py', "    if delegates is None:", "    if False:",
     'delegation gate passes a claim it could not check'),
    ('inject_delegation_check.py', "    if not any(re.search(t, prompt, re.I) for t in TRIGGERS):",
     "    if True:",
     'delegation criteria never injected'),
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
        # scripts/ is copied too, so a row may target the checker. Without this
        # the harness could only mutate .claude/hooks/, and every fix living in
        # Assert-RuleTriggerFidelity.py was unreachable: nine such mutations
        # survived because nothing could break the file they live in.
        scripts = os.path.join(work, 'scripts')
        shutil.copytree(SCRIPTS, scripts,
                        ignore=shutil.ignore_patterns('__pycache__'))
        target = (os.path.join(scripts, os.path.basename(filename))
                  if filename.startswith('scripts/')
                  else os.path.join(hooks, filename))
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
            env=env({'WG_HOOKS_DIR': hooks, 'WG_GITHOOKS_DIR': ghooks,
                     'WG_SCRIPTS_DIR': scripts}))
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
        case_delegation(tmp)
        case_delegation_injection(tmp)
        case_rule_triggers(tmp)
        case_payload_shape(tmp)
        case_checker_selftest(tmp)
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
