#!/usr/bin/env python3
"""Refuse a commit message asserting a verification nothing performs.

Runs for every form that writes a message -- -m, -am, -m"x", --file=, -F -,
heredoc, -C, --amend, editor -- because git hands this hook the assembled
message file rather than the command line.

Exit 0 = message accepted. Exit 1 = git refuses the commit.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import wg_gates as G                                    # noqa: E402


def main():
    if len(sys.argv) < 2:
        sys.stderr.write('commit-msg gate: git passed no message file, so the '
                         'claim check could not run. A check that cannot run '
                         'fails (LEARNINGS.md L-026).\n')
        return 1
    try:
        with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as handle:
            message = handle.read()
    except Exception as exc:
        sys.stderr.write('commit-msg gate: message file unreadable (%s). A check '
                         'that cannot run fails.\n' % exc)
        return 1
    findings = []
    G.check_message(message, findings)
    text = G.render(findings, 'COMMIT MESSAGE REFUSED')
    if text:
        sys.stderr.write(text + '\n')
    return 1 if G.blocking(findings) else 0


if __name__ == '__main__':
    sys.exit(main())
