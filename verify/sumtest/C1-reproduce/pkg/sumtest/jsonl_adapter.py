"""Our own solver behind the JSON-lines interface of opencode_spec.md.

Used only to validate sumtest/run_opencode_impl.py.  Convention: textbook passer test
(--aware switches to the e.p.-aware test).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sumtest.sumsolver import REF_NAMES, Geometry, Rules, SumSolver, Trees, reference_set  # noqa: E402

SPEC_KEYS = {"dup*": "double-up*", "tiny1": "tiny(1)"}


def main():
    aware = "--aware" in sys.argv
    solvers = {}
    for line in sys.stdin:
        if not line.strip():
            continue
        p = json.loads(line)
        k = (p["files"], p["wrap"], p["ep"], p["race_rule"])
        if k not in solvers:
            geo = Geometry(p["files"], p["wrap"])
            T = Trees()
            ref = reference_set(T)
            solvers[k] = (geo, ref, SumSolver(Rules(geo, ep=p["ep"], ep_aware=aware, race_rule=p["race_rule"]), T))
        geo, ref, s = solvers[k]
        W, B = geo.parse(f"W: {' '.join(p['white'])} / B: {' '.join(p['black'])}")
        wl, wr = s.solve(s.start_state(W, B))
        print(json.dumps({"id": p["id"], "outcomes": {SPEC_KEYS.get(n, n): s.outcome(wl, wr, ref[n]) for n in REF_NAMES}}))


if __name__ == "__main__":
    main()
