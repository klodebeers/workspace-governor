#!/usr/bin/env python3
"""Static structural checks for the PowerShell tooling in this repository.

WHY THIS EXISTS
---------------
This repository is maintained from an environment that has no PowerShell, so
the scripts here cannot be executed before they are handed to the local Windows
operator. Delimiter balance was the only static gate, and it does not catch
ordering or name-collision defects. Two such defects reached committed code and
would have broken the scripts at run time on the operator's machine.

This tool is a cloud-side static gate only. It does NOT verify behaviour and it
does NOT replace or weaken the required local Windows runtime verification
recorded in STATE.md.

CHECKS
------
1. Delimiter balance over code with string literals and comments removed.
2. Indexed assignment (`$X[...] = `) before `$X` is bound in scope.
3. Indexed assignment with no container constructor before it in scope.
   Existence alone is not enough: a leaked loop binding makes the name exist
   while holding a value of the wrong type, so the indexed write still fails.
4. A loop variable colliding case-insensitively with a container in the same
   or an enclosing scope. PowerShell variable names are case-insensitive, so
   `foreach ($r in ...)` silently overwrites a result object named `$R`.

Scope model: PowerShell creates a variable scope per function, not per block,
so only function bodies open a new scope here.

USAGE
-----
    python3 scripts/Assert-ScriptStructure.py scripts/*.ps1 scripts/lib/*.ps1
    python3 scripts/Assert-ScriptStructure.py --selftest

Exit status 0 = all checks pass. Non-zero = at least one finding.
Read-only: this tool opens files for reading and writes nothing.
"""

import os
import re
import sys

# Names bound by PowerShell scope modifiers, not ordinary variables.
_SCOPE_WORDS = ('env', 'script', 'global', 'using', 'local', 'private')

_RE_INDEXED = re.compile(
    r'\s*\$([A-Za-z_][A-Za-z0-9_]*)\s*\[[^\]]*\]\s*(\+?=)\s*\S')
_RE_PLAIN = re.compile(r'\s*\$([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\S')
_RE_LOOPBIND = re.compile(r'\bfor(?:each)?\s*\(\s*\$([A-Za-z_][A-Za-z0-9_]*)')
_RE_FOREACH_IN = re.compile(
    r'\bforeach\s*\(\s*\$([A-Za-z_][A-Za-z0-9_]*)\s+in\b')
_RE_FUNC = re.compile(r'\bfunction\s+[A-Za-z_][\w-]*')
_RE_PARAM = re.compile(r'\bparam\s*\(')
_RE_VAR = re.compile(r'\$([A-Za-z_][A-Za-z0-9_]*)')
_RE_CTOR = re.compile(
    r'=\s*(\[[A-Za-z.]+\]\s*)?(@\{|@\(|\[?ordered\]?\s*@\{|New-Object|.*::new\()')


def strip_literals(src):
    """Blank the contents of every literal and comment in a single pass.

    Single-pass matters: stripping one quote style before the other lets a
    quote inside a literal of the opposite kind be read as an opener, which
    silently corrupts the rest of the file and produces a false pass. Line
    structure and delimiters are preserved so line numbers stay accurate.
    """
    out = list(src)
    i, n = 0, len(src)

    def blank(a, b):
        for k in range(a, min(b, n)):
            if out[k] != '\n':
                out[k] = ' '

    while i < n:
        c = src[i]
        if c == '@' and i + 1 < n and src[i + 1] in '"\'':          # here-string
            q = src[i + 1]
            end = src.find(q + '@', i + 2)
            end = n if end == -1 else end
            blank(i + 2, end)
            i = end + 2
            continue
        if c == '<' and src.startswith('<#', i):                    # block comment
            end = src.find('#>', i + 2)
            end = n if end == -1 else end + 2
            blank(i, end)
            i = end
            continue
        if c == '#':                                               # line comment
            end = src.find('\n', i)
            end = n if end == -1 else end
            blank(i, end)
            i = end
            continue
        if c in '"\'':
            q, j = c, i + 1
            while j < n:
                if src[j] == '`' and q == '"':      # backtick escape, "..." only
                    j += 2
                    continue
                if src[j] == q:
                    if j + 1 < n and src[j + 1] == q:      # doubled = escaped
                        j += 2
                        continue
                    break
                j += 1
            blank(i + 1, j)
            i = j + 1
            continue
        i += 1
    return ''.join(out)


def _function_scopes(lines):
    """Scope path per line: a tuple of enclosing function ids, outermost first."""
    scope_of = [()] * (len(lines) + 2)
    stack, open_depth = [], []
    depth, counter = 0, 0
    pending = False
    for ln, line in enumerate(lines, 1):
        scope_of[ln] = tuple(stack)
        # The `function` keyword and the brace opening its body can share a
        # line, so both are handled in positional order. Handling the brace
        # first consumes it before the keyword registers, and then no function
        # scope is ever opened -- which silently flattens every scope.
        marks = [m.start() for m in _RE_FUNC.finditer(line)]
        mi = 0
        for ch_i, ch in enumerate(line):
            while mi < len(marks) and marks[mi] <= ch_i:
                pending = True
                mi += 1
            if ch == '{':
                if pending:
                    counter += 1
                    stack.append(counter)
                    open_depth.append(depth)
                    pending = False
                depth += 1
            elif ch == '}':
                depth -= 1
                if open_depth and depth == open_depth[-1]:
                    open_depth.pop()
                    stack.pop()
        if mi < len(marks):
            pending = True
    return scope_of


def _enclosing_loopvars(lines):
    """Set of foreach variables whose block encloses each line."""
    at = [set() for _ in range(len(lines) + 2)]
    active = []                      # (name_lower, brace_depth_at_open)
    depth, pending = 0, None
    for ln, line in enumerate(lines, 1):
        at[ln] = set(v for v, _ in active)
        marks = [(m.start(), m.group(1).lower())
                 for m in _RE_FOREACH_IN.finditer(line)]
        mi = 0
        for ch_i, ch in enumerate(line):
            while mi < len(marks) and marks[mi][0] <= ch_i:
                pending = marks[mi][1]
                mi += 1
            if ch == '{':
                if pending is not None:
                    active.append((pending, depth))
                    at[ln].add(pending)
                    pending = None
                depth += 1
            elif ch == '}':
                depth -= 1
                while active and depth <= active[-1][1]:
                    active.pop()
        if mi < len(marks):
            pending = marks[-1][1]
    return at


def _encloses(a, b):
    """True when scope a is b or encloses it."""
    return len(a) <= len(b) and tuple(b[:len(a)]) == tuple(a)


def analyse(src):
    """Return a list of finding strings for one PowerShell source string."""
    code = strip_literals(src)
    lines = code.split('\n')
    scope_of = _function_scopes(lines)
    loopvars_at = _enclosing_loopvars(lines)
    fails = []

    # 1. delimiter balance
    for name, o, c in (('braces', '{', '}'),
                       ('parens', '(', ')'),
                       ('brackets', '[', ']')):
        if code.count(o) != code.count(c):
            fails.append('%s unbalanced: %d %s vs %d %s'
                         % (name, code.count(o), o, code.count(c), c))

    # Binding sites: plain assignment, loop binding, param declaration.
    binds, ctors = [], []
    for ln, line in enumerate(lines, 1):
        sc = scope_of[ln]
        m = _RE_PLAIN.match(line)
        if m:
            binds.append((m.group(1).lower(), ln, sc))
            rest = line[m.end(1):]
            if _RE_CTOR.search(rest):
                ctors.append((m.group(1).lower(), ln, sc))
        for m in _RE_LOOPBIND.finditer(line):
            binds.append((m.group(1).lower(), ln, sc))
        if _RE_PARAM.search(line):
            for m in _RE_VAR.finditer(line):
                binds.append((m.group(1).lower(), ln, sc))

    for ln, line in enumerate(lines, 1):
        m = _RE_INDEXED.match(line)
        if not m:
            continue
        v = m.group(1).lower()
        if v in _SCOPE_WORDS:
            continue
        sc = scope_of[ln]

        # 2. bound at all, before this line, in scope
        if not [b for b in binds if b[0] == v and b[1] < ln
                and _encloses(b[2], sc)]:
            later = [b for b in binds if b[0] == v and _encloses(b[2], sc)]
            if later:
                fails.append('L%d: $%s indexed-assigned before its binding at L%d'
                             % (ln, m.group(1), min(b[1] for b in later)))
            else:
                fails.append('L%d: $%s indexed-assigned but never bound in an '
                             'enclosing scope' % (ln, m.group(1)))

        # 3. a real container constructor precedes it. A variable bound by an
        #    enclosing foreach is already an element of a built collection and
        #    needs no constructor of its own.
        if v not in loopvars_at[ln]:
            if not [c for c in ctors if c[0] == v and c[1] < ln
                    and _encloses(c[2], sc)]:
                fails.append('L%d: $%s indexed-assigned with no container '
                             'constructor before it in scope' % (ln, m.group(1)))

    # 4. loop variable colliding with a container in scope
    for ln, line in enumerate(lines, 1):
        sc = scope_of[ln]
        for m in _RE_LOOPBIND.finditer(line):
            v = m.group(1).lower()
            clash = [c for c in ctors
                     if c[0] == v and c[1] != ln and _encloses(c[2], sc)]
            if clash:
                fails.append('L%d: loop variable $%s collides case-insensitively '
                             'with container built at L%d in the same or an '
                             'enclosing scope'
                             % (ln, m.group(1), min(c[1] for c in clash)))

    return fails


# --- self-test --------------------------------------------------------------
# A checker that only ever passes proves nothing. Each case below is a defect
# this tool exists to catch, drawn from defects that reached committed code.
_SELFTEST = [
    ('indexed write before the container is built',
     '$state = "PRESENT"\n'
     '$R[\'00_hubState\'] = @{ s = $state }\n'
     '$R = [ordered]@{ meta = $state }\n',
     'constructor'),
    ('loop variable overwriting a container of the same name',
     '$P = New-Object System.Collections.Generic.List[string]\n'
     '$P.Add("x")\n'
     'foreach ($p in $paths) { $P.Add("- $p") }\n',
     'collides'),
    ('function-local name must not mask a file-scope defect',
     'function Get-Thing {\n'
     '    $r = [ordered]@{ a = 1 }\n'
     '    return $r\n'
     '}\n'
     '$R[\'k\'] = 1\n'
     '$R = [ordered]@{}\n',
     'constructor'),
    ('single quotes inside a double-quoted literal must not break stripping',
     '$msg = "it\'s fine { unbalanced-looking"\n'
     '$H = @{}\n'
     '$H[\'k\'] = $msg\n',
     None),
    ('loop variable indexing its own element is legitimate',
     '$hits = @()\n'
     '$hits += [ordered]@{ a = 1 }\n'
     'foreach ($h in $hits) { $h[\'b\'] = 2 }\n',
     None),
]


def selftest():
    ok = True
    for name, src, expect in _SELFTEST:
        found = analyse(src)
        if expect is None:
            good = not found
        else:
            good = any(expect in f for f in found)
        print('%-4s %s' % ('PASS' if good else 'FAIL', name))
        if not good:
            ok = False
            for f in found:
                print('       got: ' + f)
            if expect:
                print('       expected a finding containing %r' % expect)
    print('\nself-test: %s' % ('PASS' if ok else 'FAIL'))
    return 0 if ok else 1


def main(argv):
    if '--selftest' in argv:
        return selftest()
    if not argv:
        print(__doc__)
        return 2
    rc = 0
    for path in argv:
        findings = analyse(open(path, encoding='utf-8').read())
        print('%-44s %s' % (os.path.basename(path),
                            'OK' if not findings else 'FAIL'))
        for f in findings:
            print('    ' + f)
            rc = 1
    return rc


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
