"""Context check (not part of the claim): below the root's children, do tree
nodes of the 418 components depend on the race rule / e.p. / passed test?

  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I verify/bench/C2-refute/deeper.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import indep as I  # noqa: E402

ROOT = HERE.parents[2]
rows = [json.loads(x) for x in (ROOT / "bench/data/components.jsonl").read_text().splitlines()]
comp_rule_dep, nodes_rule_dep, nodes_total, comp_test_dep = 0, 0, 0, 0
examples = []
for r in rows:
    w, st = r["width"], I.parse(r["position"])
    nodes, _ = I.tree(w, st, False, True)
    nonterm = [q for q, j in nodes.items() if not (j[0] or j[1])]
    vals = {}
    for s in I.SETTINGS:
        sv = I.Solver(w, *s)
        # e.p.-off trees carry no ep flags: strip them for lookup
        vals[s] = {q: sv.node(q if s[2] else (q[0], q[1], None)) for q in nonterm}
    nodes_total += len(nonterm)
    dep = [q for q in nonterm if len({vals[s][q].id for s in I.SETTINGS}) > 1]
    tdep = [q for q in nonterm if any(vals[(False, ru, e)][q] is not vals[(True, ru, e)][q]
                                      for ru in ("count", "mover", "opponent") for e in (True, False))]
    comp_test_dep += bool(tdep)
    if dep:
        comp_rule_dep += 1
        nodes_rule_dep += len(dep)
        if len(examples) < 5:
            q = dep[0]
            examples.append({"component": r["position"], "node": I.ptext(q),
                             "values": {I.sname(s): I.fmt(vals[s][q]) for s in I.SETTINGS}})
print(json.dumps({
    "non-terminal tree nodes (all components)": nodes_total,
    "components with some non-terminal node whose value differs between the two passed tests": comp_test_dep,
    "components with some non-terminal node whose value differs across the 12 settings": comp_rule_dep,
    "such nodes": nodes_rule_dep,
    "examples": examples,
}, indent=1))
