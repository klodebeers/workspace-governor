#!/usr/bin/env python3
"""PreToolUse guard: refuse the ways a command can get around the git hooks.

WHAT CHANGED, AND WHY
---------------------
This hook used to hold the content gates itself, parsing the shell command to
find `git commit`. An independent audit defeated that in eight ways within
minutes: `git -C .`, an absolute path to git, `sh -c '...'`, a variable holding
the command name, a repository alias, `commit-tree` plus `update-ref`, and
`filter-branch` all produced exit 0 with empty output. A parser guessing what
git will do is the wrong carrier, so the content gates moved to `.githooks/`,
where git runs them against the staged tree for every invocation form.

This hook now owns only what a git hook structurally cannot see:

1. `--no-verify` / `-n`, which tells git to skip the hooks.
2. A plumbing sequence that writes history without running any hook --
   `commit-tree`, `update-ref`, `filter-branch`, `fast-import`.
3. A force-push, which rewrites history another checkout may hold.
4. `core.hooksPath` not pointing at `.githooks`, which makes every gate in this
   repository inert. Setting it is a per-clone step, so the guard refuses
   mutating git commands until it is set rather than trusting that it was.

That last one is the important one: it converts "someone remembered to run the
setup" into something the tooling establishes for itself.

CONTRACT
--------
stdin  : PreToolUse hook JSON.
exit 0 : nothing this hook owns is wrong.
exit 2 : refused. stderr says which, and what to do.

LIMITS, STATED
--------------
Detection here is textual and therefore best-effort -- that is exactly why the
content gates are not in this file. The failure mode is bounded: a command this
hook does not recognise still meets the git hooks. Only the four cases above can
evade those, and those four are matched on the whole command string rather than
on a parse, so quoting tricks do not hide them.
"""

import json
import os
import re
import subprocess
import sys

HOOKS_PATH_EXPECTED = '.githooks'

# Matched against the raw command string, not a tokenisation: `sh -c "..."`,
# eval, and a variable holding the verb all still contain these words.
NO_VERIFY = re.compile(r'(?:--no-verify|\s-[a-zA-Z]*n[a-zA-Z]*\s)')
PLUMBING = (
    ('commit-tree', 'writes a commit object without running any git hook'),
    ('update-ref', 'moves a ref without running any git hook'),
    ('filter-branch', 'rewrites history without running the per-commit hooks'),
    ('fast-import', 'writes history wholesale without running any git hook'),
)
FORCE_PUSH = re.compile(r'(?:^|\s)(?:--force(?!-with-lease)|-[a-zA-Z]*f[a-zA-Z]*)'
                        r'(?:\s|$)')
MIRROR = re.compile(r'(?:^|\s)--mirror(?:\s|$)')
PLUS_REFSPEC = re.compile(r'(?:^|\s)\+[^\s:]+:[^\s]+')

# Anything that can write to the repository. An unrecognised git subcommand is
# treated as mutating, because a repository alias can name anything.
READ_ONLY_SUBCOMMANDS = frozenset((
    'status', 'log', 'diff', 'show', 'rev-parse', 'rev-list', 'ls-files',
    'ls-tree', 'cat-file', 'blame', 'shortlog', 'describe', 'grep', 'config',
    'remote', 'help', 'version', 'name-rev', 'symbolic-ref', 'for-each-ref',
    'check-ignore', 'count-objects', 'verify-commit', 'whatchanged', 'worktree',
))


def git(root, args):
    try:
        out = subprocess.run(['git'] + args, cwd=root, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, timeout=30)
    except Exception:
        return 1, ''
    return out.returncode, out.stdout.decode('utf-8', 'replace').strip()


def repo_root(cwd):
    code, out = git(cwd, ['rev-parse', '--show-toplevel'])
    return out if code == 0 and out else None


def subcommands(command):
    """Every token that directly follows a git-like token."""
    found = []
    tokens = re.split(r'\s+', command.strip())
    for i, tok in enumerate(tokens):
        base = tok.rsplit('/', 1)[-1].rsplit('\\', 1)[-1]
        if base not in ('git', 'git.exe'):
            continue
        j = i + 1
        while j < len(tokens):
            nxt = tokens[j]
            if nxt.startswith('-'):
                # `git -C <dir> commit` and friends: skip the flag's argument.
                j += 2 if nxt in ('-C', '-c', '--git-dir', '--work-tree') else 1
                continue
            found.append(nxt)
            break
    return found


def mentions_git(command):
    return re.search(r'(?:^|[\s/\\\'"$(=;&|])git(?:\.exe)?(?:\s|$|\'|")', command) \
        is not None


def looks_mutating(command):
    """True when the command could write to the repository."""
    subs = subcommands(command)
    if not subs:
        # git is named but the subcommand is indirect -- a variable, an eval, a
        # wrapper. Treat as mutating: the cost is one config read.
        return mentions_git(command)
    return any(s not in READ_ONLY_SUBCOMMANDS for s in subs)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if payload.get('tool_name') != 'Bash':
        return 0
    command = (payload.get('tool_input') or {}).get('command') or ''
    if not command or not mentions_git(command):
        return 0

    cwd = payload.get('cwd') or os.getcwd()
    root = repo_root(cwd)
    if not root:
        return 0
    # Scoped to a repository that carries these gates.
    if not os.path.isfile(os.path.join(root, '.githooks', 'pre-commit')):
        return 0

    blocks = []

    if NO_VERIFY.search(command):
        blocks.append(
            'HOOK BYPASS: this command tells git to skip its hooks. The gates in '
            '.githooks/ are the carriers for the append-only invariant, the secret '
            'scan, script encoding and the Hub checks. AGENTS.md Enforcement: a gate '
            'has no bypass. If a gate is wrong, fix the gate.')

    for word, why in PLUMBING:
        if word in command:
            blocks.append(
                'HOOK BYPASS via `%s`, which %s. Use an ordinary commit so the gates '
                'run.' % (word, why))

    if 'push' in subcommands(command) or re.search(r'\bpush\b', command):
        after = command.split('push', 1)[1]
        if '--force-with-lease' not in after.split('&&')[0].split(';')[0]:
            head = after.split('&&')[0].split(';')[0]
            if FORCE_PUSH.search(head):
                blocks.append(
                    'FORCE PUSH. It rewrites history another checkout may hold. Use '
                    '--force-with-lease, and only on a branch you created.')
            elif MIRROR.search(head):
                blocks.append(
                    'FORCE PUSH via --mirror, which force-updates every ref. Same '
                    'objection: use --force-with-lease on a named branch.')
            elif PLUS_REFSPEC.search(head):
                blocks.append(
                    'FORCE PUSH via a leading-plus refspec. Same objection.')

    if looks_mutating(command):
        code, value = git(root, ['config', '--get', 'core.hooksPath'])
        if value != HOOKS_PATH_EXPECTED:
            blocks.append(
                'GATES NOT INSTALLED IN THIS CLONE: core.hooksPath is %s, so nothing '
                'in .githooks/ runs and every content gate is inert. Run:\n'
                '    git config core.hooksPath %s\n'
                'This is refused rather than warned about because a gate nobody '
                'installed reports no findings, which reads exactly like a clean '
                'result.' % (repr(value) if value else 'unset', HOOKS_PATH_EXPECTED))

    if not blocks:
        return 0
    sys.stderr.write('\nREFUSED (%d finding(s)):\n' % len(blocks))
    for i, block in enumerate(blocks, 1):
        sys.stderr.write('\n%d. %s\n' % (i, block))
    return 2


if __name__ == '__main__':
    sys.exit(main())
