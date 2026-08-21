#!/usr/bin/env python3
"""Check that references in the canonical Agent Hub resolve, and that its index
covers the tree.

Read-only. Modifies nothing. Exit 0 only if every check ran and passed.

    python3 Assert-ReferenceIntegrity.py <path-to-.agents-hub>

Coverage, stated precisely because an earlier version overstated it:
  * Markdown: backtick tokens that look like a repository path, AND link targets of
    the form [text](target). A backtick token is treated as a path when it contains
    a separator or ends in a known extension. Tokens containing a space are treated
    as prose, not paths -- so `rules/DOES NOT EXIST.md` is NOT checked. That is a
    real limit, not a claim of completeness.
  * JSON: every repository-path-shaped token in every string value, wherever it
    appears -- not only under keys named "path" or "definition". "$schema" and "$id"
    are checked by URI semantics instead, since they are identifiers. A string that
    opens with 'repo@sha' is a lineage string: the paths inside it belong to that
    repository at that commit, so they are out of scope rather than dangling.
  * Index: every tracked artifact appears in CATALOG.md, and every CATALOG.md path
    exists.

Three model corrections are baked in, each of which produced a false positive that
would have damaged correct content if acted on:
  * a token that asserts its own absence is not a broken reference (ALLOW);
  * reference resolution is scoped to one repository, so cross-repository and
    absolute paths are out of scope rather than defects (EXTERNAL);
  * a token is resolved against the referencing document first and the repository
    root second -- root-only resolution made valid sibling references look broken.

And one inversion, found by audit: $id is a URI, not a path. Resolving it as a path
made the correct absolute form look uncheckable and the defective relative form look
clean, rewarding the exact regression the schema rewrite removed.
"""
import json
import os
import re
import sys

# Documented exceptions. A token that ASSERTS its own absence is not a broken reference.
ALLOW = {
    'design-systems\\.remember\\',   # present in the materialized Hub, not tracked here
    'policies\\', 'prompts\\', 'skills\\', 'tools\\', 'runbooks\\',   # stated as intentionally absent
    'runtime-adapters\\', 'governance-templates\\', 'STATE.md',   # retired; nameable as absent
    'adapters\\', 'adapters\\claude\\', 'adapters\\codex\\', 'adapters\\generic\\',   # accepted names, created with their first adapter
}
EXTERNAL = ('agents-hub-two/', 'workspace-governor/', 'mcp-gateway/')
SKIP_DOCS = {'references/AGENTS-MD-LIVE-AUDIT-2026-08-16.md'}   # dated evidence: true when written
BACKTICK = re.compile(r'`([^`\n]+)`')
MDLINK = re.compile(r'\[[^\]\n]*\]\(([^)\s]+)\)')
JSON_PATH_KEYS = {'path', 'definition'}
# Repository-path-shaped tokens embedded anywhere in a JSON string value.
EMBEDDED = re.compile(r'[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+\.(?:md|json|py|ps1|txt|yaml|yml)')
# A lineage string: 'repo@sha ...'. Paths inside it belong to that repository.
LINEAGE = re.compile(r'^[a-z0-9.-]+@[0-9a-f]{7,40}\b')

dangling, unreadable, uri_defects, index_defects = [], [], [], []
absolute = 0
checked = 0


def looks_like_path(t):
    """True = check it as a repository path. None = out of scope. False = not a path."""
    if t in ALLOW:
        return False
    if re.match(r'^[A-Za-z]:[\\/]', t):
        return None
    if t.startswith(('http://', 'https://', 'urn:', 'mailto:', '#')):
        return False
    if t.replace('\\', '/').startswith(EXTERNAL):
        return None
    if ' ' in t.strip():
        return False
    return bool(re.search(r'[\\/]', t)) or bool(
        re.match(r'^[A-Za-z0-9._-]+\.(md|json|ps1|py|txt|yaml|yml)$', t))


def resolve(root, tok, docdir):
    p = tok.replace('\\', '/')
    isdir = p.endswith('/')
    p = p.rstrip('/')
    for base in (docdir, root):
        cand = os.path.join(base, p)
        if (os.path.isdir(cand) if isdir else os.path.exists(cand)):
            return True
    return False


def walk_json(root, obj, rel, full):
    global checked
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and v:
                if k == '$id':
                    # A schema identifier must be an absolute URI. A relative path
                    # here is the predecessor schema's defect, so it must fail.
                    if not re.match(r'^[a-z][a-z0-9+.-]*:', v):
                        uri_defects.append((rel, v, '$id must be an absolute URI'))
                elif k == '$schema':
                    # An instance may point at its schema by relative path; that
                    # path must resolve. An absolute URI is accepted as-is.
                    if re.match(r'^[a-z][a-z0-9+.-]*:', v):
                        pass
                    else:
                        checked += 1
                        if not resolve(root, v, os.path.dirname(full)):
                            dangling.append((rel, v, 'json:$schema'))
                elif LINEAGE.match(v):
                    # A lineage string names another repository at another commit, so
                    # the paths inside it are out of this repository's scope by
                    # construction -- the repo@sha prefix is the scope marker.
                    global absolute
                    absolute += len(EMBEDDED.findall(v))
                else:
                    # Every other string value: a repository path may appear anywhere,
                    # not only under a key we thought to name. An earlier version
                    # checked "path" and "definition" only, so 10 of the 14 real
                    # references in these artifacts -- every cross-owner pointer in
                    # authority blocks -- went unexamined.
                    for tok in EMBEDDED.findall(v):
                        if looks_like_path(tok) is True:
                            checked += 1
                            if not resolve(root, tok, os.path.dirname(full)):
                                dangling.append((rel, tok, 'json:' + k))
            walk_json(root, v, rel, full)
    elif isinstance(obj, list):
        for i in obj:
            walk_json(root, i, rel, full)


def main(root):
    global absolute, checked
    for marker in ('AGENTS.md', 'CATALOG.md', 'rules'):
        if not os.path.exists(os.path.join(root, marker)):
            sys.exit("refusing to run: %s does not look like the canonical Agent Hub "
                     "(expected AGENTS.md, CATALOG.md and rules/ at its root). This check "
                     "is calibrated for that tree only; elsewhere it produces false "
                     "positives, not findings." % root)

    tracked = []
    for dp, dns, fns in os.walk(root):
        if '.git' in dp.split(os.sep):
            continue
        for fn in fns:
            full = os.path.join(dp, fn)
            rel = os.path.relpath(full, root).replace(os.sep, '/')
            tracked.append(rel)
            if fn.endswith('.md') and rel not in SKIP_DOCS:
                text = open(full, encoding='utf-8').read()
                for tok in BACKTICK.findall(text) + MDLINK.findall(text):
                    v = looks_like_path(tok)
                    if v is None:
                        absolute += 1
                        continue
                    if not v:
                        continue
                    checked += 1
                    if not resolve(root, tok, dp):
                        dangling.append((rel, tok, 'md'))
            if fn.endswith('.json'):
                try:
                    data = json.load(open(full, encoding='utf-8-sig'))
                except Exception as exc:
                    unreadable.append((rel, str(exc).split('(')[0].strip()))
                    continue
                walk_json(root, data, rel, full)

    # Index coverage: the catalog is the Hub's discovery contract.
    catalog = open(os.path.join(root, 'CATALOG.md'), encoding='utf-8').read()
    for rel in sorted(tracked):
        if rel in ('CATALOG.md',):
            continue
        if rel.replace('/', '\\') not in catalog and rel not in catalog:
            index_defects.append(rel)

    print("tokens checked: %d | out of repo, skipped: %d | dangling: %d | "
          "URI defects: %d | unreadable JSON: %d | artifacts missing from CATALOG.md: %d"
          % (checked, absolute, len(dangling), len(uri_defects), len(unreadable),
             len(index_defects)))
    for d in dangling:
        print("  DANGLING", d)
    for u in uri_defects:
        print("  URI", u)
    for u in unreadable:
        print("  UNREADABLE", u)
    for i in index_defects:
        print("  NOT IN CATALOG", i)
    return 1 if (dangling or uri_defects or unreadable or index_defects) else 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
