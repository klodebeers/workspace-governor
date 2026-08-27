#!/usr/bin/env python3
"""Authoritative content gates. Runs on the staged tree, for every git form.

Enabled by `git config core.hooksPath .githooks`, which the PreToolUse guard in
.claude/hooks/gate_commit.py refuses to let a commit proceed without.

Exit 0 = commit proceeds. Exit 1 = git refuses the commit.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import wg_gates as G                                    # noqa: E402


def main():
    findings = []
    spec = ['--cached']
    G.check_append_only(ROOT, spec, findings)
    G.check_secrets(ROOT, spec, findings)
    G.check_ascii_scripts(ROOT, spec, findings)
    G.check_hub_scripts(ROOT, spec, findings)
    G.check_rule_triggers(ROOT, spec, findings)
    text = G.render(findings, 'PRE-COMMIT GATES REFUSED THIS COMMIT')
    if text:
        sys.stderr.write(text + '\n')
    return 1 if G.blocking(findings) else 0


if __name__ == '__main__':
    sys.exit(main())
