#!/usr/bin/env python3
"""Verify that migrated Hub artifacts still match the source package they came from.

Read-only. Modifies nothing. Exit 0 only if every check ran and passed.

    python3 Assert-HubSourceFidelity.py <path-to-.agents-hub> <path-to-agents-hub-two>

Why this exists: the other two checks prove the Hub is internally well-formed and
that its references resolve. Neither reads the source package, so the load-bearing
claims of the migration -- that routes are verbatim, that carried agent fields are
unaltered, that the template content is unchanged apart from one recorded field,
that every source formula fact and citation survived the consolidation -- were
asserted in prose and verified by nobody. This script reads both sides.

It checks fidelity, not judgement. It cannot tell whether a transformation was the
right one; it tells you whether the content still says what the source said.
"""
import json
import os
import re
import sys

PASS, FAIL = [], []


def ok(m):
    PASS.append(m); print("PASS  %s" % m)


def bad(m):
    FAIL.append(m); print("FAIL  %s" % m)


def load(p):
    return json.load(open(p, encoding="utf-8-sig"))


# Recorded, deliberate divergences. Each must name what changed and why, so a
# silent alteration cannot hide behind an exemption.
EXEMPT = {
    ("templates/verification-checklist.json", "human_review_required"):
        "false -> null: a canonical template must not ship a default answer to an "
        "approval question owned by rules/AUTONOMY-AND-PROTECTED-BOUNDARIES.md",
}


def main(hub, src):
    for marker in ("AGENTS.md", "CATALOG.md", "rules"):
        if not os.path.exists(os.path.join(hub, marker)):
            sys.exit("refusing to run: %s does not look like the canonical Agent Hub." % hub)
    for marker in ("agents", "config", "templates"):
        if not os.path.exists(os.path.join(src, marker)):
            sys.exit("refusing to run: %s does not look like the source package "
                     "(expected agents/, config/, templates/)." % src)

    S = lambda p: load(os.path.join(src, p))
    H = lambda p: load(os.path.join(hub, p))

    # ---- routes are verbatim ------------------------------------------------
    routing = H("orchestration/routing.json")
    gen = S("agents/AGENT-COORDINATOR-ORCHESTRATOR.json")["routing_logic"]["patterns"]
    notion = S("agents/NOTION-COORDINATOR-ORCHESTRATOR.json")["routing_logic"]["patterns"]
    expected = ([{"domain": "general", "trigger": p["trigger"], "route_to": p["route_to"],
                  "output": p["output"]} for p in gen if "route_to" in p]
                + [{"domain": "notion-operations", "trigger": p["trigger"],
                    "route_to": p["route_to"], "output": p["output"]} for p in notion])
    got = routing.get("routes")
    if got == expected:
        ok("all %d routes are byte-identical to the source, in source order" % len(expected))
    else:
        bad("routes differ from the source. expected %d, got %d; first divergence at index %s"
            % (len(expected), len(got or []),
               next((i for i, (a, b) in enumerate(zip(expected, got or [])) if a != b), "end")))

    # ---- the pre-routing condition is verbatim ------------------------------
    src_pre = [p for p in gen if "route_to" not in p]
    hub_pre = routing.get("pre_routing") or []
    if len(src_pre) == len(hub_pre) == 1 and \
            hub_pre[0].get("condition") == src_pre[0]["trigger"]:
        ok("the pre-routing condition matches the source pattern that carries no destination")
    else:
        bad("the pre-routing condition does not match the source: source %r, hub %r"
            % ([p.get("trigger") for p in src_pre], [p.get("condition") for p in hub_pre]))

    # No source routing pattern may be silently dropped.
    src_dests = {p["route_to"] for p in gen if "route_to" in p} | {p["route_to"] for p in notion}
    hub_dests = {r["route_to"] for r in got or []}
    missing = sorted(src_dests - hub_dests)
    if missing:
        bad("source routing destinations absent from the Hub: %s" % missing)
    else:
        ok("every source routing destination is present (%d)" % len(src_dests))

    # ---- carried agent-definition fields are unaltered ----------------------
    a_src = S("agents/NOTION-FORMULA-LOGIC-AGENT.json")
    a_hub = H("agents/notion-formula-logic.json")
    for hub_key, src_key in (("purpose", "purpose"),
                             ("responsibilities", "primary_responsibilities"),
                             ("required_inputs", "required_inputs"),
                             ("outputs", "outputs"),
                             ("rules", "rules")):
        if a_hub.get(hub_key) == a_src.get(src_key):
            ok("agent definition %s is identical to source %s" % (hub_key, src_key))
        else:
            bad("agent definition %s differs from source %s" % (hub_key, src_key))

    # ---- registry identity strings trace to the source ---------------------
    reg = H("registry/agent-registry.json")
    src_reg = S("config/agent-registry.json")
    roles = {a["id"]: a["role"] for a in src_reg["specialists"] + src_reg["non_notion_agents"]}
    names = {a["id"]: a["name"] for a in src_reg["specialists"] + src_reg["non_notion_agents"]}
    unmarked = []
    for a in reg["agents"]:
        src_role = roles.get(a["id"])
        if src_role is None:
            unmarked.append("%s: id absent from the source registry" % a["id"])
            continue
        norm = src_role[0].upper() + src_role[1:]
        if not norm.endswith("."):
            norm += "."
        if a["responsibility"] != norm and "responsibility_source" not in a:
            unmarked.append("%s: responsibility %r is not the normalised source role %r and "
                            "carries no responsibility_source" % (a["id"], a["responsibility"], norm))
        if a["name"] != names.get(a["id"]) and "name_source" not in a \
                and "folded_ids" not in a:
            unmarked.append("%s: name %r differs from source %r with nothing recording it. "
                            "A responsibility marker does not cover a name."
                            % (a["id"], a["name"], names.get(a["id"])))
    if unmarked:
        for u in unmarked:
            bad("registry identity string unaccounted for -- %s" % u)
    else:
        ok("every registry identity string is the source string, or is marked as authored")

    # Every source id must resolve: carried as a live id, or recorded as folded.
    live = {a["id"] for a in reg["agents"]}
    folded = {f for a in reg["agents"] for f in a.get("folded_ids", [])}
    src_ids = set(roles) | {"notion-coordinator-orchestrator"}
    unresolvable = sorted(src_ids - live - folded)
    if unresolvable:
        bad("source agent id(s) resolve to nothing in the Hub: %s" % unresolvable)
    else:
        ok("every source agent id resolves, as a live id or a recorded fold (%d live, %d folded)"
           % (len(live), len(folded)))

    # ---- template content, with recorded exemptions -------------------------
    t_src = S("templates/verification-checklist-template.json")
    t_hub = H("templates/verification-checklist.json")
    if set(t_src) != set(t_hub):
        bad("template field set changed: source %s, hub %s" % (sorted(t_src), sorted(t_hub)))
    else:
        ok("template field set is unchanged from source (%d fields)" % len(t_src))
    for k in t_src:
        key = ("templates/verification-checklist.json", k)
        same = t_src[k] == t_hub.get(k)
        if key in EXEMPT:
            # A recorded exemption REQUIRES the divergence. Reverting it is a defect,
            # not a silent return to source: the divergence is a settled decision.
            if same:
                bad("template %s no longer diverges from source, but the divergence is "
                    "required -- %s" % (k, EXEMPT[key]))
            else:
                ok("template %s diverges as required -- %s" % (k, EXEMPT[key]))
        elif not same:
            bad("template %s changed from %r to %r with no recorded exemption"
                % (k, t_src[k], t_hub.get(k)))

    # ---- the consolidated context file lost nothing ------------------------
    ctx = open(os.path.join(hub, "context/NOTION-FORMULA-V2.md"), encoding="utf-8-sig").read()
    refs = S("agents/NOTION-SYSTEM-DEPENDENCIES.json")["validated_references"]
    lost = [u for u in refs if u not in ctx]
    if lost:
        bad("cited source reference(s) absent from the context file: %s" % lost)
    else:
        ok("every source validated_reference appears in the context file (%d)" % len(refs))

    # Each platform capability the source names must still be stated.
    caps = {"multi-line": r"multi-?line", "type-aware output": r"type-aware",
            "richer outputs": r"richer (property )?outputs",
            "related database access": r"related database",
            "dot notation": r"dot notation", "let/lets": r"`let`|let and lets|let/lets"}
    absent = sorted(k for k, pat in caps.items() if not re.search(pat, ctx, re.IGNORECASE))
    if absent:
        bad("platform capability named in the source but not in the context file: %s" % absent)
    else:
        ok("every platform capability the source names is stated in the context file (%d)" % len(caps))

    # Each source implication must still be represented. Keyword coverage was not
    # enough: deleting the whole consequences section passed a capabilities-only check.
    IMPLICATIONS = {
        "explicit transform for richer outputs": r"transform",
        "legacy formulas may need adjustment": r"[Ll]egacy formulas may",
        "rollup-first workaround often unnecessary": r"rollup-first",
        "property type change affects formula output": r"[Pp]roperty type changes may affect",
        "schema and formula work are coupled": r"retyped or restructured",
        "formula logic has its own verification model": r"own verification model",
    }
    missing_imp = sorted(k for k, pat in IMPLICATIONS.items()
                         if not re.search(pat, ctx, re.IGNORECASE))
    if missing_imp:
        bad("source implication(s) absent from the context file: %s" % missing_imp)
    else:
        ok("every source implication is represented in the context file (%d)" % len(IMPLICATIONS))

    # A source obligation must be stated as an obligation, or recorded as owed
    # elsewhere. The context file must at least declare that it does not absorb them.
    if re.search(r"does not absorb the obligations", ctx):
        ok("the context file declares that it does not absorb source obligations")
    else:
        bad("the context file no longer declares that it does not absorb the obligations "
            "that accompanied this material; without that, a dropped must reads as absent")

    # The four source keys must be named, so the consolidation is traceable.
    for key in ("notion_formula_v2_guidance", "notion_formula_v2_notes",
                "formula_2_0_notes", "notion_formula_v2_considerations"):
        holder = {"notion_formula_v2_guidance": "NOTION-COORDINATOR-ORCHESTRATOR.json",
                  "notion_formula_v2_notes": "NOTION-SYSTEM-DEPENDENCIES.json",
                  "formula_2_0_notes": "NOTION-FORMULA-LOGIC-AGENT.json",
                  "notion_formula_v2_considerations": "NOTION-SCHEMA-RELATIONS-AGENT.json"}[key]
        if holder in ctx:
            ok("context provenance names the source file holding %s" % key)
        else:
            bad("context provenance does not name %s, which holds %s" % (holder, key))

    # ---- no source governance block leaked into the Hub --------------------
    leaked = []
    for dirpath, dirnames, filenames in os.walk(hub):
        if ".git" in dirpath.split(os.sep):
            continue
        for fn in filenames:
            if not fn.endswith((".json", ".md")):
                continue
            body = open(os.path.join(dirpath, fn), encoding="utf-8-sig").read()
            for block in ("escalation_rules", "communication_style", "decision_rules",
                          "handoff_contract", "core_responsibilities", "dependency_chain",
                          "ownership", "verification_rules"):
                if '"%s"' % block in body:
                    leaked.append("%s carries source block %s"
                                  % (os.path.relpath(os.path.join(dirpath, fn), hub), block))
    if leaked:
        for l in leaked:
            bad("source governance block leaked into the Hub -- %s" % l)
    else:
        ok("no source governance block (escalation_rules, communication_style, decision_rules, "
           "handoff_contract, core_responsibilities, dependency_chain, ownership, "
           "verification_rules) appears in any Hub artifact, .json or .md")

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
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
