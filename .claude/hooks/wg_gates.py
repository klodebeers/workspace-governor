#!/usr/bin/env python3
"""Repository invariants, checked against what a commit actually records.

WHY THIS FILE EXISTS SEPARATELY
-------------------------------
The first version of these gates lived in a Claude Code `PreToolUse` hook that
parsed the shell command. An independent audit defeated it in eight ways in a
few minutes -- `git -C .`, an absolute path to git, `sh -c`, a variable holding
the command name, a repository alias, and `commit-tree` + `update-ref` all
produced exit 0 and empty output. A parser guessing what git will do cannot be
the carrier.

A git hook is. It runs after git has decided what the commit contains, for every
invocation form, so none of those bypasses reach it. What a git hook cannot see
-- `--no-verify`, and the plumbing commands that write history without running
hooks -- is refused earlier, by the `PreToolUse` guard in `gate_commit.py`.

INVARIANTS AND THEIR OWNERS
---------------------------
Every check below cites the rule it enforces. This file owns none of them.

1. `DECISIONS.md` entries are append-only -- `AGENTS.md` File ownership.
2. No secret value in the repository -- `AGENTS.md` Secrets.
3. Every `.ps1` is pure ASCII -- `scripts/README.md` section 1.
4. A durable verification claim names a re-runnable artifact -- `DECISIONS.md`
   D-53. The phrase list here is a **proxy** for that rule, chosen in D-93, not
   a rule of its own.
5. Hub verification scripts pass when a Hub clone is reachable -- D-65.

A CHECK THAT CANNOT RUN FAILS
-----------------------------
`LEARNINGS.md` L-026: "A check that cannot run must fail, never skip." Earlier
these paths returned "skipped" on a note that reached only the debug log, so a
skip was operationally a pass -- and one byte that UTF-8 could not decode was
enough to trigger it, silently removing checks 2 and 3 from a commit carrying
exactly the defect they exist to catch. Every git call here reads bytes and
never decodes blindly; a git failure blocks and names itself.
"""

import importlib.util
import io
import json
import os
import re
import subprocess

APPEND_ONLY = ('DECISIONS.md',)
ENTRY_MARKERS = (b'**D-', b'**C-')
ASCII_ONLY_SUFFIXES = ('.ps1',)
HUB_CLONE_ENV = 'WG_HUB_CLONE'
HUB_CLONE_DEFAULT = '/workspace/agents-hub-one'
HUB_SCRIPTS = ('Assert-ReferenceIntegrity.py', 'Test-HubRegistrySchema.py')

SECRET_PATTERNS = (
    (rb'-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----',
     'a private key block', False),
    (rb'\bghp_[A-Za-z0-9]{30,}', 'a GitHub personal access token', False),
    (rb'\bgithub_pat_[A-Za-z0-9_]{30,}', 'a GitHub fine-grained token', False),
    (rb'\bgh[osru]_[A-Za-z0-9]{30,}', 'a GitHub OAuth or app token', False),
    (rb'\bAKIA[0-9A-Z]{16}\b', 'an AWS access key id', False),
    (rb'\bASIA[0-9A-Z]{16}\b', 'an AWS temporary access key id', False),
    (rb'\bxox[abprs]-[A-Za-z0-9-]{12,}', 'a Slack token', False),
    (rb'\bsk-ant-[A-Za-z0-9_-]{24,}', 'an Anthropic API key', False),
    # Base64 payloads match this shape, so an inline data: URI is excluded.
    (rb'\bAIza[0-9A-Za-z_-]{33,}', 'a Google API key', True),
    (rb'\bglpat-[A-Za-z0-9_-]{20,}', 'a GitLab token', False),
    (rb'\bnpm_[A-Za-z0-9]{34,}', 'an npm token', False),
)

# Whitespace-tolerant: git joins several -m values with a blank line, which
# split "by construction" across a paragraph break and slipped the old pattern.
CLAIM_PATTERNS = (
    r'by\s+construction',
    r'trivially\s+(?:true|holds|correct)',
    r'holds\s+by\s+definition',
)

# A claim is refused only when nothing re-runnable is named beside it. D-53 asks
# for the artifact, not for different wording, and the gate should say the same.
ARTIFACT_HINTS = (
    r'\bscripts/', r'\.py\b', r'\bAssert-', r'\bTest-', r'\btest_hooks\b',
    r'\b[0-9a-f]{7,40}\b', r'\.githooks/',
)


class Finding(object):
    """One refusal, with the rule it enforces named."""

    def __init__(self, gate, detail):
        self.gate = gate
        self.detail = detail

    def __str__(self):
        return '%s: %s' % (self.gate, self.detail)


def git_bytes(root, args, timeout=120):
    """Run git and return (returncode, stdout_bytes, error_text).

    Never decodes. A caller that gets a non-zero return must block, not skip.
    """
    try:
        out = subprocess.run(['git'] + args, cwd=root, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, timeout=timeout)
    except Exception as exc:
        return 1, b'', 'git %s could not run: %s' % (' '.join(args), exc)
    if out.returncode != 0:
        return (out.returncode, out.stdout,
                'git %s exited %d: %s' % (' '.join(args), out.returncode,
                                          out.stderr.decode('utf-8', 'replace')[:300]))
    return 0, out.stdout, ''


def lines(data):
    return data.split(b'\n')


def check_append_only(root, diff_args, findings):
    """Refuse a commit that removes or rewrites a DECISIONS.md entry line."""
    for path in APPEND_ONLY:
        code, out, err = git_bytes(root, ['diff'] + diff_args + ['-U0', '--', path])
        if code != 0:
            findings.append(Finding(
                'CHECK COULD NOT RUN',
                'the append-only check on %s failed to read its diff (%s). A check '
                'that cannot run fails rather than skipping -- LEARNINGS.md L-026.'
                % (path, err)))
            continue
        removed = [ln[1:] for ln in lines(out)
                   if ln.startswith(b'-') and not ln.startswith(b'---')]
        entry_removals = [ln for ln in removed
                          if any(m in ln for m in ENTRY_MARKERS)]
        if entry_removals:
            findings.append(Finding(
                'APPEND-ONLY VIOLATION',
                '%s removes or rewrites %d entry line(s), starting with %r. Entries '
                'are append-only: supersede one with a new entry rather than editing '
                'it (AGENTS.md File ownership).'
                % (path, len(entry_removals),
                   entry_removals[0].decode('utf-8', 'replace')[:90])))
        elif removed:
            findings.append(Finding(
                'NOTE ONLY -- ALLOWED',
                '%s removes %d line(s) that carry no entry marker. Prose and '
                'headings outside an entry are editable; the entries are not.'
                % (path, len(removed))))


def check_secrets(root, diff_args, findings):
    code, out, err = git_bytes(root, ['diff'] + diff_args + ['-U0'])
    if code != 0:
        findings.append(Finding(
            'CHECK COULD NOT RUN',
            'the secret scan failed to read the diff (%s). A check that cannot run '
            'fails rather than skipping -- LEARNINGS.md L-026.' % err))
        return
    for ln in lines(out):
        if not ln.startswith(b'+') or ln.startswith(b'+++'):
            continue
        body = ln[1:]
        for pattern, what, skip_data_uri in SECRET_PATTERNS:
            if skip_data_uri and b'base64,' in body:
                continue
            if re.search(pattern, body):
                findings.append(Finding(
                    'SECRET IN COMMITTED CONTENT',
                    '%s. This repository records references and locations, never '
                    'values (AGENTS.md Secrets). Remove it from the commit, and '
                    'from history if it was ever committed.' % what))
                break


def check_ascii_scripts(root, diff_args, findings):
    code, out, err = git_bytes(root, ['diff'] + diff_args + ['--name-only', '-z'])
    if code != 0:
        findings.append(Finding(
            'CHECK COULD NOT RUN',
            'the encoding check could not list changed files (%s). L-026: a check '
            'that cannot run fails.' % err))
        return
    paths = [p.decode('utf-8', 'surrogateescape')
             for p in out.split(b'\x00') if p]
    for path in paths:
        if not path.endswith(ASCII_ONLY_SUFFIXES):
            continue
        spec = ':' + path if diff_args == ['--cached'] else 'HEAD:' + path
        code, data, err = git_bytes(root, ['show', spec])
        if code != 0:
            full = os.path.join(root, path)
            if not os.path.isfile(full):
                continue          # deleted in this commit; nothing to encode
            with open(full, 'rb') as handle:
                data = handle.read()
        bad = [i for i, byte in enumerate(bytearray(data)) if byte > 127]
        if bad:
            findings.append(Finding(
                'NON-ASCII IN A POWERSHELL SCRIPT',
                '%s carries %d byte(s) above 0x7F, first at offset %d (0x%02X). '
                'Windows PowerShell 5.1 reads a non-BOM source as ANSI and one such '
                'byte breaks a parse cascade on the operator machine '
                '(scripts/README.md section 1).'
                % (path, len(bad), bad[0], bytearray(data)[bad[0]])))


def check_hub_scripts(root, diff_args, findings):
    """Run the Hub verification scripts. Unreachable clone blocks, per L-026."""
    code, out, err = git_bytes(root, ['diff'] + diff_args + ['--name-only', '-z'])
    if code != 0:
        findings.append(Finding('CHECK COULD NOT RUN',
                                'could not list changed files (%s).' % err))
        return
    paths = [p.decode('utf-8', 'surrogateescape')
             for p in out.split(b'\x00') if p]
    if not any(p.startswith('scripts/') or p.startswith('evidence/')
               for p in paths):
        return
    hub = os.environ.get(HUB_CLONE_ENV, HUB_CLONE_DEFAULT)
    if not os.path.isdir(hub):
        findings.append(Finding(
            'HUB CHECKS COULD NOT RUN',
            'no Hub clone at %s, so the reference and schema checks did not run. '
            'This commit touches scripts/ or evidence/, where those checks are the '
            'evidence. Point %s at a clone, or move the change out of those paths. '
            'A skipped check is never a pass (LEARNINGS.md L-026).'
            % (hub, HUB_CLONE_ENV)))
        return
    for name in HUB_SCRIPTS:
        # Run the committed copy, not the working tree: the working tree can be
        # edited to make a failing check pass while the commit keeps the defect.
        spec = ':scripts/' + name if diff_args == ['--cached'] else 'HEAD:scripts/' + name
        code, data, err = git_bytes(root, ['show', spec])
        if code != 0:
            findings.append(Finding(
                'HUB CHECKS COULD NOT RUN',
                'could not read the committed copy of scripts/%s (%s).' % (name, err)))
            continue
        try:
            out = subprocess.run(['python3', '-', hub], input=data,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 timeout=120)
        except Exception as exc:
            findings.append(Finding(
                'HUB CHECKS COULD NOT RUN',
                'scripts/%s could not be executed (%s).' % (name, exc)))
            continue
        if out.returncode != 0:
            tail = (out.stdout.decode('utf-8', 'replace')[-900:]
                    + out.stderr.decode('utf-8', 'replace')[-400:])
            findings.append(Finding(
                'HUB VERIFICATION FAILED',
                'scripts/%s exited %d against %s.\n%s'
                % (name, out.returncode, hub, tail)))


def check_rule_triggers(root, diff_args, findings):
    """Refuse a commit that leaves the rule-trigger table unresolvable.

    Run unconditionally rather than only when the table is in the diff: an
    entry breaks when the OWNING file is renamed or its heading is reworded,
    which touches neither the table nor this gate's own file. That is the
    silent case -- inject_rules.py would emit NOT READ from then on, and a
    table of NOT READ notices reads exactly like a table that is working.
    """
    del diff_args                      # a broken heading is not diff-scoped
    table = os.path.join(root, '.claude', 'hooks', 'rule-triggers.json')
    if not os.path.isfile(table):
        return                         # not every clone wires the injector
    checker = os.path.join(root, 'scripts', 'Assert-RuleTriggerFidelity.py')
    if not os.path.isfile(checker):
        findings.append(Finding(
            'CHECK COULD NOT RUN',
            'rule-triggers.json is present but scripts/Assert-RuleTriggerFidelity.py '
            'is missing, so its entries could not be checked. L-026: a check that '
            'cannot run fails rather than skipping.'))
        return
    try:
        spec = importlib.util.spec_from_file_location('_rtf', checker)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with io.open(table, encoding='utf-8') as handle:
            parsed = json.load(handle)
        broken = module.audit(root, parsed)
    except BaseException as exc:      # SystemExit is not an Exception, and an
                                      # imported module is free to raise one
        findings.append(Finding(
            'CHECK COULD NOT RUN',
            'the rule-trigger check raised %r, so the table was not verified. '
            'L-026: a check that cannot run fails rather than skipping.' % (exc,)))
        return
    for item in broken:
        findings.append(Finding(
            'RULE TRIGGER DOES NOT RESOLVE',
            '%s. inject_rules.py would inject a NOT READ notice instead of the '
            'rule, and a rule that did not load is not a rule that was followed '
            '(.claude/hooks/README.md).' % item))


def check_message(message, findings):
    """Refuse an unbacked verification claim. Proxy for D-53, per D-93."""
    if message is None:
        findings.append(Finding(
            'CHECK COULD NOT RUN',
            'the commit message was unreadable, so the claim check did not run.'))
        return
    cites_artifact = any(re.search(h, message, re.I) for h in ARTIFACT_HINTS)
    for pattern in CLAIM_PATTERNS:
        found = re.search(pattern, message, re.I)
        if not found:
            continue
        if cites_artifact:
            findings.append(Finding(
                'NOTE ONLY -- ALLOWED',
                '"%s" appears, and the message names a re-runnable artifact, so the '
                'claim is backed rather than asserted.' % found.group(0)))
            continue
        findings.append(Finding(
            'UNBACKED VERIFICATION CLAIM',
            '"%s" asserts a property no committed check performs. Name the script, '
            'test or commit that proves it, or state the claim as unverified '
            '(DECISIONS.md D-53).' % found.group(0)))


def blocking(findings):
    return [f for f in findings if not f.gate.startswith('NOTE ONLY')]


def render(findings, header):
    out = []
    notes = [f for f in findings if f.gate.startswith('NOTE ONLY')]
    blocks = blocking(findings)
    for note in notes:
        out.append('gate note: %s' % note.detail)
    if blocks:
        out.append('')
        out.append('%s (%d finding(s)):' % (header, len(blocks)))
        for i, finding in enumerate(blocks, 1):
            out.append('')
            out.append('%d. %s' % (i, finding))
        out.append('')
        out.append('Fix the finding. There is no bypass, by design.')
    return '\n'.join(out)
