"""Sweep every reference in a repository and report the ones that do not resolve.

Read-only. Modifies nothing. Exit 0 = no dangling reference.

    python3 Assert-ReferenceIntegrity.py <repo-root>

Covers two token classes, because the first version of this check assumed its own
scope and reported a clean result over half the references:
  * every backtick path token in every live Markdown file;
  * every path-valued field in every JSON file ($schema, $id, definition, path).

Three model corrections are baked in, each of which produced a false positive that
would have damaged correct content if acted on:
  * a token that asserts its own absence is not a broken reference (ALLOW);
  * reference resolution is scoped to one repository, so cross-repository and
    absolute paths are out of scope rather than defects (EXTERNAL);
  * a token is resolved against the referencing document first and the repository
    root second -- root-only resolution made valid sibling references look broken.

Verify the checker before trusting a clean run: introduce one fabricated reference,
confirm it is reported, then remove it.
"""
import os, re, json, sys
ROOT = (sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)).rstrip('/')

# Scope guard. This check is calibrated for the canonical Agent Hub: a
# self-contained tree whose references are repository-internal paths. Pointed at
# this backoffice it reported 1022 dangling references, essentially all false --
# bare filenames in prose, git refs such as `origin/main`, `owner/repo` names, and
# paths inside other repositories. A run like that is worse than no run, because
# 1022 findings look like a result. The tool enforces its own scope rather than
# relying on the operator to remember it. A backoffice profile does not exist yet.
_MARKERS = ('AGENTS.md', 'CATALOG.md', 'rules')
if not all(os.path.exists(os.path.join(ROOT, m)) for m in _MARKERS):
    sys.exit("refusing to run: %s does not look like the canonical Agent Hub "
             "(expected AGENTS.md, CATALOG.md and rules/ at its root). This check "
             "is calibrated for that tree only; running it elsewhere produces "
             "false positives, not findings." % ROOT)
# Documented exceptions. A token that ASSERTS its own absence is not a broken reference.
ALLOW = {
    'design-systems\\.remember\\',   # present in the materialized Hub, absent from the repo; CATALOG instructs preservation
    'policies\\', 'prompts\\', 'skills\\', 'tools\\', 'runbooks\\',   # candidate domains CATALOG states are intentionally absent
}
EXTERNAL = ('agents-hub-two/', 'workspace-governor/', 'mcp-gateway/')   # other repositories: out of this repo's resolution scope
SKIP_DOCS = {'references/AGENTS-MD-LIVE-AUDIT-2026-08-16.md'}  # dated evidence: true when written
TOKEN = re.compile(r'`([^`\n]+)`')
dangling, absolute, checked, unreadable = [], 0, 0, []

def exists(tok, docdir):
    p = tok.replace('\\', '/')
    isdir = p.endswith('/')
    p = p.rstrip('/')
    for base in (docdir, ROOT):                 # doc-relative first, then repo root
        cand = os.path.join(base, p)
        if os.path.isdir(cand) if isdir else os.path.exists(cand):
            return True
    return False

def looks_like_path(t):
    if t in ALLOW: return False
    if re.match(r'^[A-Za-z]:[\\/]', t): return None      # absolute: outside the repo
    if t.startswith(('http://','https://','urn:')): return False
    if t.startswith(EXTERNAL): return None                # another repository: out of scope, not a defect
    if ' ' in t.strip(): return False
    return bool(re.search(r'[\\/]', t)) or bool(re.match(r'^[A-Za-z0-9._-]+\.(md|json|ps1|py|txt)$', t))

# markdown backtick tokens
for dp, dns, fns in os.walk(ROOT):
    if '.git' in dp.split(os.sep): continue
    for fn in fns:
        full = os.path.join(dp, fn)
        rel = os.path.relpath(full, ROOT).replace(os.sep, '/')
        if rel in SKIP_DOCS or not fn.endswith('.md'): continue
        for tok in TOKEN.findall(open(full, encoding='utf-8').read()):
            v = looks_like_path(tok)
            if v is None:
                globals().__setitem__('absolute', absolute + 1); absolute += 1; continue
            if not v: continue
            checked += 1
            if not exists(tok, dp): dangling.append((rel, tok, 'md'))

# JSON path-valued fields
JSON_KEYS = {'definition', 'path', '$schema', '$id'}   # $schema/$id added: the first sweep assumed its own scope
def walk(o, rel, full):
    global checked
    if isinstance(o, dict):
        for k, v in o.items():
            if k in JSON_KEYS and isinstance(v, str) and v:
                if looks_like_path(v) is not True:      # URL, URN, absolute path, or exempt
                    walk(v, rel, full); continue
                checked += 1
                if not exists(v, os.path.dirname(full)): dangling.append((rel, v, 'json:'+k))
            walk(v, rel, full)
    elif isinstance(o, list):
        for i in o: walk(i, rel, full)

for dp, dns, fns in os.walk(ROOT):
    if '.git' in dp.split(os.sep): continue
    for fn in fns:
        if not fn.endswith('.json'): continue
        full = os.path.join(dp, fn); rel = os.path.relpath(full, ROOT).replace(os.sep,'/')
        # utf-8-sig, not utf-8: some JSON evidence in this project carries a BOM that
        # a strict utf-8 read rejects. Unparseable files are reported, never skipped
        # silently -- an unreadable file is an uncovered file, not a passing one.
        try:
            data = json.load(open(full, encoding='utf-8-sig'))
        except Exception as exc:
            unreadable.append((rel, str(exc).split('(')[0].strip()))
            continue
        walk(data, rel, full)

print("tokens checked: %d | absolute (out of repo, skipped): %d | dangling: %d | unreadable JSON: %d"
      % (checked, absolute, len(dangling), len(unreadable)))
for d in dangling: print("  DANGLING", d)
for u in unreadable: print("  UNREADABLE", u)
sys.exit(1 if (dangling or unreadable) else 0)
