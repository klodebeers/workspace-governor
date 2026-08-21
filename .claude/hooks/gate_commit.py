#!/usr/bin/env python3
"""PreToolUse hook: mechanical gates on `git commit` and `git push`.

WHY THIS EXISTS
---------------
Every rule this repository holds was guidance until now. DECISIONS.md C-03 and
D-74 both record the reason: a CLAUDE.md is read, not enforced, and enforcement
needs a hook or a managed setting. Three failure classes recurred despite being
written down, and all three are mechanically detectable at commit time:

  1. Deleting or rewriting a line of the append-only DECISIONS.md.
  2. A commit message asserting a fidelity or verification claim that no
     committed check performs -- "true by construction" (D-53).
  3. Non-ASCII bytes in a PowerShell script, which breaks a parse cascade on
     the Windows 5.1 operator's machine (scripts/README.md section 1).

It also refuses a secret in staged content, and a plain force-push, which
rewrites history someone else may have checked out.

CONTRACT
--------
stdin  : PreToolUse hook JSON with tool_name and tool_input.
exit 0 : nothing to gate, or every gate passed. Notes on stderr are advisory.
exit 2 : blocked. stderr states which gate, on what, and what to do.

WHAT THIS DOES NOT DO
---------------------
It does not judge whether a claim is TRUE, only whether the message asserts a
class of claim that has burned this project before. A skipped check is printed
as SKIPPED and is never counted as a pass -- reporting a skip as a pass is
itself a defect this project has committed (DECISIONS.md D-65).

Read-only with respect to the working tree: it inspects the index and writes
nothing.
"""

import json
import os
import re
import shlex
import subprocess
import sys

APPEND_ONLY = ('DECISIONS.md',)
ASCII_ONLY_SUFFIXES = ('.ps1',)
HUB_CLONE_ENV = 'WG_HUB_CLONE'
HUB_CLONE_DEFAULT = '/workspace/agents-hub-one'

# High-precision only. A pattern that fires on prose about secrets would train
# the reader to ignore this gate, which is worse than not having it.
SECRET_PATTERNS = (
    (r'-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----',
     'a private key block'),
    (r'\bghp_[A-Za-z0-9]{30,}', 'a GitHub personal access token'),
    (r'\bgithub_pat_[A-Za-z0-9_]{30,}', 'a GitHub fine-grained token'),
    (r'\bgh[osru]_[A-Za-z0-9]{30,}', 'a GitHub OAuth or app token'),
    (r'\bAKIA[0-9A-Z]{16}\b', 'an AWS access key id'),
    (r'\bASIA[0-9A-Z]{16}\b', 'an AWS temporary access key id'),
    (r'\bxox[abprs]-[A-Za-z0-9-]{12,}', 'a Slack token'),
    (r'\bsk-ant-[A-Za-z0-9_-]{24,}', 'an Anthropic API key'),
    (r'\bAIza[0-9A-Za-z_-]{33,}', 'a Google API key'),
    (r'\bglpat-[A-Za-z0-9_-]{20,}', 'a GitLab token'),
    (r'\bnpm_[A-Za-z0-9]{34,}', 'an npm token'),
)

# Claim classes that have been committed here without a check behind them.
CLAIM_PATTERNS = (
    (r'by construction',
     'an unperformed-verification claim (DECISIONS.md D-53). Name the '
     'committed check that proves it, or state the claim as unverified.'),
    (r'trivially (?:true|holds|correct)',
     'an unperformed-verification claim. Say what was run.'),
    (r'holds by definition',
     'an unperformed-verification claim. Say what was run.'),
)


def git(root, args, timeout=60):
    """Run git in root. Returns (returncode, stdout)."""
    try:
        out = subprocess.run(['git'] + args, cwd=root, capture_output=True,
                             text=True, timeout=timeout)
    except Exception as exc:
        return 1, 'git %s failed: %s' % (' '.join(args), exc)
    return out.returncode, out.stdout


def repo_root(cwd):
    code, out = git(cwd, ['rev-parse', '--show-toplevel'], timeout=10)
    if code != 0:
        return None
    return out.strip() or None


def tokens_after(tokens, word):
    """Tokens from the first bare occurrence of `word` onward, or []."""
    for i, tok in enumerate(tokens):
        if tok == word:
            return tokens[i:]
    return []


def parse(command):
    """shlex the command. Returns (tokens, error_text_or_None)."""
    try:
        return shlex.split(command), None
    except ValueError as exc:
        return [], str(exc)


def commit_tokens(tokens):
    """The token slice belonging to the git commit invocation, or []."""
    for i, tok in enumerate(tokens):
        if tok != 'git':
            continue
        for j in range(i + 1, len(tokens)):
            if tokens[j].startswith('-'):
                continue
            if tokens[j] == 'commit':
                return tokens[j:]
            break
    return []


def commits_all_tracked(ctokens):
    """True when the commit stages tracked modifications itself (-a/--all)."""
    for tok in ctokens:
        if tok == '--all':
            return True
        if tok.startswith('--'):
            continue
        if tok.startswith('-') and len(tok) > 1 and 'a' in tok[1:]:
            return True
    return False


def commit_message(ctokens, root):
    """Return (message_or_None, note_or_None)."""
    i = 0
    parts = []
    while i < len(ctokens):
        tok = ctokens[i]
        if tok in ('-m', '--message') and i + 1 < len(ctokens):
            parts.append(ctokens[i + 1])
            i += 2
            continue
        if tok.startswith('--message='):
            parts.append(tok.split('=', 1)[1])
            i += 1
            continue
        if tok in ('-F', '--file') and i + 1 < len(ctokens):
            path = os.path.join(root, ctokens[i + 1])
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                    parts.append(fh.read())
            except Exception as exc:
                return None, ('message file %s unreadable (%s), message gate '
                              'SKIPPED -- not a pass' % (ctokens[i + 1], exc))
            i += 2
            continue
        i += 1
    if parts:
        return '\n'.join(parts), None
    return None, ('no -m/-F message found in the command, message gate '
                  'SKIPPED -- not a pass')


def numstat(root, diff_args, path):
    """Return (added, deleted) for path, or None when path is untouched."""
    code, out = git(root, ['diff'] + diff_args + ['--numstat', '--', path])
    if code != 0:
        return None
    for line in out.splitlines():
        cells = line.split('\t')
        if len(cells) < 3:
            continue
        try:
            return int(cells[0]), int(cells[1])
        except ValueError:
            return None
    return None


def changed_paths(root, diff_args):
    code, out = git(root, ['diff'] + diff_args + ['--name-only'])
    if code != 0:
        return []
    return [p for p in out.splitlines() if p.strip()]


def added_lines(root, diff_args):
    code, out = git(root, ['diff'] + diff_args + ['-U0'])
    if code != 0:
        return []
    lines = []
    for line in out.splitlines():
        if line.startswith('+') and not line.startswith('+++'):
            lines.append(line[1:])
    return lines


def blob(root, diff_args, path):
    """Staged (or working-tree, for -a) content of path, as bytes."""
    if diff_args == ['--cached']:
        code, out = git(root, ['show', ':' + path])
        if code == 0:
            return out.encode('utf-8', errors='surrogateescape')
        return None
    full = os.path.join(root, path)
    try:
        with open(full, 'rb') as fh:
            return fh.read()
    except Exception:
        return None


def gate_push(tokens, blocks):
    ptokens = tokens_after(tokens, 'push')
    if not ptokens:
        return
    joined = ' '.join(ptokens)
    if '--force-with-lease' in joined:
        return
    for tok in ptokens:
        if tok == '--force' or (tok.startswith('-') and not tok.startswith('--')
                                and 'f' in tok[1:]):
            blocks.append(
                'FORCE PUSH. A plain force-push rewrites history that another '
                'checkout may hold. Use --force-with-lease, and only on a '
                'branch you created.')
            return
        if tok.startswith('+') and ':' in tok:
            blocks.append(
                'FORCE PUSH via a leading-plus refspec (%s). Same objection: '
                'use --force-with-lease.' % tok)
            return


def run_hub_checks(root, notes, blocks):
    """Run the Hub verification scripts when the Hub clone is present."""
    hub = os.environ.get(HUB_CLONE_ENV, HUB_CLONE_DEFAULT)
    scripts = ('Assert-ReferenceIntegrity.py', 'Test-HubRegistrySchema.py')
    if not os.path.isdir(hub):
        notes.append('Hub verification scripts SKIPPED -- no Hub clone at %s. '
                     'A skip is not a pass: do not claim Hub verification in '
                     'this commit.' % hub)
        return
    for name in scripts:
        path = os.path.join(root, 'scripts', name)
        if not os.path.isfile(path):
            notes.append('%s SKIPPED -- not found. Not a pass.' % name)
            continue
        try:
            out = subprocess.run(['python3', path, hub], capture_output=True,
                                 text=True, timeout=120)
        except Exception as exc:
            notes.append('%s SKIPPED -- could not run (%s). Not a pass.'
                         % (name, exc))
            continue
        if out.returncode != 0:
            tail = (out.stdout or '')[-1200:] + (out.stderr or '')[-600:]
            blocks.append('%s FAILED against %s. Fix the Hub tree before '
                          'committing.\n%s' % (name, hub, tail))


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if payload.get('tool_name') != 'Bash':
        return 0
    command = (payload.get('tool_input') or {}).get('command') or ''
    if 'git' not in command:
        return 0

    cwd = payload.get('cwd') or os.getcwd()
    root = repo_root(cwd)
    if not root:
        return 0

    tokens, parse_error = parse(command)
    blocks = []
    notes = []

    if parse_error:
        notes.append('command could not be tokenised (%s); token gates '
                     'SKIPPED -- not a pass.' % parse_error)
    else:
        gate_push(tokens, blocks)

    ctokens = commit_tokens(tokens) if tokens else []
    if not ctokens:
        return report(blocks, notes)

    diff_args = ['HEAD'] if commits_all_tracked(ctokens) else ['--cached']

    # 1. Append-only files.
    for path in APPEND_ONLY:
        stat = numstat(root, diff_args, path)
        if stat is None:
            continue
        added, deleted = stat
        if deleted > 0:
            blocks.append(
                'APPEND-ONLY VIOLATION: %s has %d deleted line(s) in this '
                'commit (+%d/-%d). It is append-only -- an existing entry is '
                'never edited or removed, and a modified line counts as a '
                'deletion. Add a new entry that supersedes the old one.'
                % (path, deleted, added, deleted))

    paths = changed_paths(root, diff_args)

    # 2. Secrets in added content.
    for line in added_lines(root, diff_args):
        for pattern, what in SECRET_PATTERNS:
            if re.search(pattern, line):
                blocks.append(
                    'SECRET IN STAGED CONTENT: %s. This repository records '
                    'references and locations, never values (AGENTS.md '
                    'Secrets). Remove it from the index and from history if '
                    'it was ever committed.' % what)
                break

    # 3. ASCII-only scripts.
    for path in paths:
        if not path.endswith(ASCII_ONLY_SUFFIXES):
            continue
        data = blob(root, diff_args, path)
        if data is None:
            continue
        bad = [i for i, byte in enumerate(bytearray(data)) if byte > 127]
        if bad:
            blocks.append(
                'NON-ASCII IN %s at byte offset %d (%d occurrence(s)). Every '
                '.ps1 here must be pure ASCII: Windows PowerShell 5.1 decodes '
                'non-ASCII differently and one character breaks a parse '
                'cascade on the operator machine (scripts/README.md).'
                % (path, bad[0], len(bad)))

    # 4. Commit-message claim classes.
    message, note = commit_message(ctokens, root)
    if note:
        notes.append(note)
    if message:
        for pattern, why in CLAIM_PATTERNS:
            found = re.search(pattern, message, re.I)
            if found:
                blocks.append('COMMIT MESSAGE CLAIM: "%s" is %s'
                              % (found.group(0), why))

    # 5. Hub verification scripts, when a Hub clone is reachable.
    if any(p.startswith('scripts/') or p.startswith('evidence/')
           for p in paths):
        run_hub_checks(root, notes, blocks)

    return report(blocks, notes)


def report(blocks, notes):
    for note in notes:
        sys.stderr.write('gate note: %s\n' % note)
    if not blocks:
        return 0
    sys.stderr.write('\nCOMMIT GATES BLOCKED THIS COMMAND (%d finding(s)):\n'
                     % len(blocks))
    for i, block in enumerate(blocks, 1):
        sys.stderr.write('\n%d. %s\n' % (i, block))
    sys.stderr.write('\nFix the finding. Do not work around the gate.\n')
    return 2


if __name__ == '__main__':
    sys.exit(main())
