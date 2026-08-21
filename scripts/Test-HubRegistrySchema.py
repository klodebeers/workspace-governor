#!/usr/bin/env python3
"""Prove that the canonical Hub registry schema accepts its instance and rejects
the defect classes the predecessor schema let through.

Read-only. Modifies nothing. Exit 0 = all cases behaved as required.

Usage:
    python3 Test-HubRegistrySchema.py <path-to-.agents-hub>

Why this exists: an earlier revision stated "validated against 8 negative cases"
in a durable record with no artifact anyone could re-run. Under the evidence
standard that is agent confidence presented as verification. The claim now has a
script behind it.
"""
import copy
import json
import os
import sys

try:
    from jsonschema import Draft202012Validator as V
except ImportError:
    sys.exit("jsonschema is required: pip install jsonschema")


def main(hub):
    schema_path = os.path.join(hub, "registry", "agent-registry.schema.json")
    inst_path = os.path.join(hub, "registry", "agent-registry.json")
    for p in (schema_path, inst_path):
        if not os.path.exists(p):
            sys.exit("missing: %s" % p)

    schema = json.load(open(schema_path, encoding="utf-8"))
    base = json.load(open(inst_path, encoding="utf-8"))

    failures = []

    V.check_schema(schema)
    print("PASS  schema is valid JSON Schema draft 2020-12")

    errs = list(V(schema).iter_errors(base))
    if errs:
        failures.append("live instance does not validate: %s" % errs[0].message)
        print("FAIL  live instance validates (%d errors)" % len(errs))
    else:
        print("PASS  live instance validates, 0 errors")

    def orch(d):
        return next(i for i, a in enumerate(d["agents"]) if a["role_class"] == "orchestrator")

    def migrated(d):
        return next(i for i, a in enumerate(d["agents"]) if a["definition_status"] == "migrated")

    negatives = [
        ("pending entry that names a definition",
         lambda d: d["agents"][orch(d)].update(definition="agents/x.json")),
        ("migrated entry with a null definition",
         lambda d: d["agents"][migrated(d)].update(definition=None)),
        ("unknown top-level key -- the predecessor schema's real defect",
         lambda d: d.update(routing_rules={"notion": []})),
        ("unknown key inside an agent entry",
         lambda d: d["agents"][0].update(path="./agents/x.json")),
        ("id that is not kebab-case",
         lambda d: d["agents"][0].update(id="Coordinator_Orchestrator")),
        ("role_class outside the settled classification",
         lambda d: d["agents"][0].update(role_class="helper")),
        ("missing required provenance",
         lambda d: d["agents"][0].pop("provenance")),
        ("empty agents array",
         lambda d: d.update(agents=[])),
    ]

    for label, mutate in negatives:
        d = copy.deepcopy(base)
        mutate(d)
        if list(V(schema).iter_errors(d)):
            print("PASS  rejected: %s" % label)
        else:
            failures.append("accepted a case it must reject: %s" % label)
            print("FAIL  ACCEPTED: %s" % label)

    # Positive control: the model the predecessor schema structurally forbade.
    d = copy.deepcopy(base)
    extra = copy.deepcopy(d["agents"][orch(d)])
    extra.update(id="second-orchestrator", domain="notion-operations")
    d["agents"].append(extra)
    if list(V(schema).iter_errors(d)):
        failures.append("rejected a legitimate second orchestrator entry")
        print("FAIL  rejected: a second orchestrator entry, one role per domain")
    else:
        print("PASS  accepted: a second orchestrator entry, one role per domain")

    # Cross-artifact consistency: routing must resolve against the registry.
    routing_path = os.path.join(hub, "orchestration", "routing.json")
    if os.path.exists(routing_path):
        r = json.load(open(routing_path, encoding="utf-8"))
        ids = {a["id"] for a in base["agents"]}
        doms = {a["domain"] for a in base["agents"]}
        unresolved = sorted({x["route_to"] for x in r["routes"] if x["route_to"] not in ids})
        baddom = sorted({x["domain"] for x in r["routes"] if x["domain"] not in doms})
        routed = {x["route_to"] for x in r["routes"]}
        unroutable = sorted(a["id"] for a in base["agents"]
                            if a["role_class"] == "specialist" and a["id"] not in routed)
        entry_ok = r["entry_point"]["agent"] in ids
        for label, bad in (("route_to values absent from the registry", unresolved),
                           ("route domains absent from the registry", baddom),
                           ("registry specialists with no route", unroutable)):
            if bad:
                failures.append("%s: %s" % (label, bad))
                print("FAIL  %s: %s" % (label, bad))
            else:
                print("PASS  no %s" % label)
        if entry_ok:
            print("PASS  entry_point resolves to a registry id")
        else:
            failures.append("entry_point does not resolve to a registry id")
            print("FAIL  entry_point does not resolve to a registry id")
    else:
        print("SKIP  orchestration/routing.json not present")

    print()
    if failures:
        print("RESULT: FAIL -- %d problem(s)" % len(failures))
        for f in failures:
            print("  - %s" % f)
        return 1
    print("RESULT: PASS -- schema, instance, negative cases, positive control and cross-artifact checks all behaved as required")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
