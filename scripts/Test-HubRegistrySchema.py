#!/usr/bin/env python3
"""Validate the canonical Hub registry, and check the cross-artifact invariants
that a JSON Schema cannot express.

Read-only. Modifies nothing. Exit 0 only if every check ran and passed.

    python3 Test-HubRegistrySchema.py <path-to-.agents-hub>

Design notes, each from a demonstrated defect in an earlier version:
  * A skipped check is a FAILURE, not a pass. The earlier version printed
    "RESULT: PASS -- ... and cross-artifact checks all behaved as required" after
    deleting orchestration/routing.json, because the skip branch added nothing to
    the failure list. Nothing here reports success for a check that did not run.
  * Negative-case fixtures are selected by the property under test, never by
    role_class. Selecting the orchestrator entry and assuming it is unmigrated
    produced a false FAILURE the moment the orchestrator gained a definition.
  * Missing fixtures abort with a stated reason rather than raising StopIteration.
  * Schema validity is necessary and not sufficient: id uniqueness, definition
    agreement, and domain coherence are checked in code because JSON Schema cannot
    express them.
"""
import copy
import json
import os
import sys

try:
    from jsonschema import Draft202012Validator as V
except ImportError:
    sys.exit("jsonschema is required: pip install jsonschema")

PASS, FAIL = [], []


def ok(msg):
    PASS.append(msg)
    print("PASS  %s" % msg)


def bad(msg):
    FAIL.append(msg)
    print("FAIL  %s" % msg)


def load(path):
    return json.load(open(path, encoding="utf-8-sig"))


def main(hub):
    for marker in ("AGENTS.md", "CATALOG.md", "rules"):
        if not os.path.exists(os.path.join(hub, marker)):
            sys.exit("refusing to run: %s does not look like the canonical Agent Hub "
                     "(expected AGENTS.md, CATALOG.md and rules/)." % hub)

    schema_path = os.path.join(hub, "registry", "agent-registry.schema.json")
    inst_path = os.path.join(hub, "registry", "agent-registry.json")
    routing_path = os.path.join(hub, "orchestration", "routing.json")
    for p in (schema_path, inst_path, routing_path):
        if not os.path.exists(p):
            sys.exit("refusing to run: required artifact missing: %s. Absence is a "
                     "failure of the tree, not a check to skip." % p)

    schema, base, routing = load(schema_path), load(inst_path), load(routing_path)

    # ---- schema and instance -------------------------------------------------
    try:
        V.check_schema(schema)
        ok("schema is valid JSON Schema draft 2020-12")
    except Exception as exc:
        bad("schema is not valid draft 2020-12: %s" % exc)
        return report()

    if str(schema.get("$id", "")).startswith(("urn:", "http://", "https://")):
        ok("schema $id is an absolute URI, so it resolves in a standard validator")
    else:
        bad("schema $id is not an absolute URI: %r. Draft 2020-12 requires one; a "
            "relative $id is the predecessor schema's defect." % schema.get("$id"))

    declared = base.get("$schema")
    if declared and os.path.exists(os.path.join(os.path.dirname(inst_path), declared)):
        ok("instance declares its own schema, and the declaration resolves")
    else:
        bad("instance does not declare a resolvable schema ($schema=%r); the only "
            "binding would be a path hardcoded in this script" % declared)

    errs = list(V(schema).iter_errors(base))
    if errs:
        bad("live instance does not validate (%d errors, first: %s)" % (len(errs), errs[0].message))
    else:
        ok("live instance validates, 0 errors")

    agents = base.get("agents") or []

    # ---- invariants JSON Schema cannot express ------------------------------
    ids = [a.get("id") for a in agents]
    if len(ids) == len(set(ids)):
        ok("agent ids are unique (%d entries)" % len(ids))
    else:
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        bad("duplicate agent id(s): %s. An id must resolve to exactly one entry." % dupes)

    names = [a.get("name") for a in agents]
    if len(names) == len(set(names)):
        ok("agent names are unique")
    else:
        bad("duplicate agent name(s): %s" % sorted({n for n in names if names.count(n) > 1}))

    folded = [f for a in agents for f in a.get("folded_ids", [])]
    clash = sorted(set(folded) & set(ids))
    if clash:
        bad("folded id(s) collide with a live id: %s" % clash)
    elif len(folded) == len(set(folded)):
        ok("folded ids are unique and do not collide with live ids (%d folded)" % len(folded))
    else:
        bad("duplicate folded id(s): %s" % sorted({f for f in folded if folded.count(f) > 1}))

    # Every definition file must agree with the entry that points at it.
    checked_defs = 0
    for a in agents:
        d = a.get("definition")
        if not d:
            continue
        full = os.path.join(hub, d)
        if not os.path.exists(full):
            bad("definition path does not exist: %s (entry %s)" % (d, a.get("id")))
            continue
        try:
            body = load(full)
        except Exception as exc:
            bad("definition is unreadable: %s (%s)" % (d, exc))
            continue
        checked_defs += 1
        if body.get("id") != a.get("id"):
            bad("definition %s declares id %r but the registry entry pointing at it is %r"
                % (d, body.get("id"), a.get("id")))
        for key in ("name", "domain", "role_class", "canonical_status"):
            if key in body:
                bad("definition %s carries registry-owned field %r; the registry owns it"
                    % (d, key))
    if checked_defs:
        ok("every definition file agrees with its registry entry (%d checked)" % checked_defs)
    else:
        ok("no definition files to cross-check (all entries have definition: null)")

    # ---- routing resolves against the registry ------------------------------
    doms = {a.get("domain") for a in agents}
    id_set = set(ids)
    routes = routing.get("routes") or []
    for label, bad_set in (
        ("route_to values absent from the registry",
         sorted({r.get("route_to") for r in routes if r.get("route_to") not in id_set})),
        ("route domains absent from the registry",
         sorted({r.get("domain") for r in routes if r.get("domain") not in doms})),
        ("domain_selection domains absent from the registry",
         sorted({d.get("domain") for d in routing.get("domain_selection", [])
                 if d.get("domain") not in doms})),
        ("registry specialists with no route",
         sorted(a["id"] for a in agents
                if a.get("role_class") == "specialist"
                and a["id"] not in {r.get("route_to") for r in routes})),
        ("orchestrators used as a route destination",
         sorted({r.get("route_to") for r in routes
                 if r.get("route_to") in {a["id"] for a in agents
                                          if a.get("role_class") == "orchestrator"}})),
    ):
        if bad_set:
            bad("%s: %s" % (label, bad_set))
        else:
            ok("no %s" % label)

    ep = (routing.get("entry_point") or {}).get("agent")
    ep_entry = next((a for a in agents if a.get("id") == ep), None)
    if ep_entry is None:
        bad("entry_point %r does not resolve to a registry id" % ep)
    elif ep_entry.get("role_class") != "orchestrator":
        bad("entry_point %r resolves to role_class %r, not an orchestrator"
            % (ep, ep_entry.get("role_class")))
    else:
        ok("entry_point resolves to a registry orchestrator")

    ep_dom = (routing.get("entry_point") or {}).get("domain")
    if ep_dom in doms:
        ok("entry_point domain exists in the registry")
    else:
        bad("entry_point domain %r is absent from the registry" % ep_dom)

    trig = [r.get("trigger") for r in routes]
    if len(trig) == len(set(trig)):
        ok("route triggers are distinct")
    else:
        bad("duplicate route trigger(s): %s" % sorted({t for t in trig if trig.count(t) > 1}))

    # ---- negative cases, fixtures chosen by the property under test ---------
    def find(pred, what):
        i = next((i for i, a in enumerate(agents) if pred(a)), None)
        if i is None:
            bad("cannot run a negative case: no %s in the registry" % what)
        return i

    i_null = find(lambda a: a.get("definition") is None, "entry with definition: null")
    i_def = find(lambda a: a.get("definition"), "entry with a definition path")
    i_spec = find(lambda a: a.get("role_class") == "specialist", "specialist entry")

    negatives = [("unknown top-level key -- the predecessor schema's real defect",
                  lambda d: d.update(routing_rules={"notion": []})),
                 ("unknown key inside an agent entry",
                  lambda d: d["agents"][0].update(path="./agents/x.json")),
                 ("id that is not kebab-case",
                  lambda d: d["agents"][0].update(id="Coordinator_Orchestrator")),
                 ("role_class outside the settled classification",
                  lambda d: d["agents"][0].update(role_class="helper")),
                 ("canonical_status outside the settled vocabulary",
                  lambda d: d["agents"][0].update(canonical_status="candidate")),
                 ("missing required provenance",
                  lambda d: d["agents"][0].pop("provenance")),
                 ("provenance without repository@commit",
                  lambda d: d["agents"][0].update(provenance="made it up")),
                 ("empty agents array",
                  lambda d: d.update(agents=[]))]
    if i_def is not None:
        negatives.append(("definition path outside agents/",
                          lambda d, i=i_def: d["agents"][i].update(definition="rules/ENGINEER-OWNERSHIP.md")))
    if i_spec is not None:
        negatives.append(("folded_ids on a specialist entry",
                          lambda d, i=i_spec: d["agents"][i].update(folded_ids=["x-agent"])))
    if i_null is not None:
        negatives.append(("two identical agent entries",
                          lambda d, i=i_null: d["agents"].append(copy.deepcopy(d["agents"][i]))))

    for label, mutate in negatives:
        d = copy.deepcopy(base)
        try:
            mutate(d)
        except Exception as exc:
            bad("could not build the negative case %r: %s" % (label, exc))
            continue
        if list(V(schema).iter_errors(d)):
            ok("rejected: %s" % label)
        else:
            bad("ACCEPTED a case it must reject: %s" % label)

    # ---- positive control ---------------------------------------------------
    d = copy.deepcopy(base)
    if i_null is None:
        bad("cannot run the positive control: no entry to clone")
    else:
        extra = copy.deepcopy(d["agents"][i_null])
        extra.update(id="second-orchestrator", name="Second Orchestrator",
                     domain="notion-operations", role_class="orchestrator")
        extra.pop("folded_ids", None)
        d["agents"].append(extra)
        if list(V(schema).iter_errors(d)):
            bad("rejected a legitimate second orchestrator, one role per domain")
        else:
            ok("accepted: a second orchestrator entry, the model the predecessor schema forbade")

    return report()


def report():
    print()
    print("checks run: %d passed, %d failed" % (len(PASS), len(FAIL)))
    if FAIL:
        print("RESULT: FAIL")
        for f in FAIL:
            print("  - %s" % f)
        return 1
    print("RESULT: PASS -- every check listed above ran and passed")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
