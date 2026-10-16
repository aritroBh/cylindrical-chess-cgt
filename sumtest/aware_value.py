"""Canonical value of a pawn position under the e.p.-aware passer convention.

HYBRID tool, used only to *name* the value that the brute-force solver's outcome
vectors imply: the game tree comes from sumtest/sumsolver.py's move generator and
passer test (e.p.-aware: a pawn that can be taken en passant right now is not yet
passed); the canonical forms come from cylcgt.cgt.  It also checks that the value's
predicted outcomes equal the brute-force outcome vector.

  PYTHONPATH=. .venv/bin/python -m sumtest.aware_value "W: a2 c2 / B: b7 d7" --files 4
"""
import argparse
from functools import lru_cache

from cylcgt import cgt

from sumtest.compare_cylcgt import ref_games
from sumtest.sumsolver import REF_NAMES, Geometry, Rules, SumSolver, Trees, reference_set

BIG = 256


def value(text, files, wrap, ep=True, aware=True, race_rule="count"):
    geo = Geometry(files, wrap)
    rules = Rules(geo, ep=ep, ep_aware=aware, race_rule=race_rule)

    @lru_cache(maxsize=None)
    def val(st):
        if st == "L":
            return cgt.integer(BIG)
        if st == "R":
            return cgt.integer(-BIG)
        W, B, e = st
        kids = {}
        for white in (True, False):
            out = []
            for c in rules.moves(W, B, e, white):
                res = rules.resolve(*c, white)
                out.append(val(res if res else c))
            kids[white] = out
        return cgt.make(kids[True], kids[False])

    W, B = geo.parse(text)
    v = val((W, B, -1))
    # brute-force outcome vector for the same convention (whole mode, local e.p. right)
    T = Trees()
    ref = reference_set(T)
    s = SumSolver(Rules(geo, ep=ep, ep_aware=aware, race_rule=race_rule), T)
    wl, wr = s.solve(s.start_state(W, B))
    brute = "".join(s.outcome(wl, wr, ref[n]) for n in REF_NAMES)
    R = ref_games()
    pred = "".join(cgt.outcome(cgt.add(v, R[n])) for n in REF_NAMES)
    return v, brute, pred


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("position")
    ap.add_argument("--files", type=int, default=4)
    ap.add_argument("--wrap", action="store_true")
    ap.add_argument("--race", default="count")
    ap.add_argument("--plain", action="store_true", help="textbook passer test instead of e.p.-aware")
    ap.add_argument("--no-ep", action="store_true")
    a = ap.parse_args()
    v, brute, pred = value(a.position, a.files, a.wrap, ep=not a.no_ep, aware=not a.plain, race_rule=a.race)
    print("value          :", cgt.show(v))
    print("mean, temp     :", cgt.mean(v), cgt.temperature(v))
    print("brute outcomes :", brute)
    print("cgt predicted  :", pred, "(agree)" if brute == pred else "(DISAGREE)")


if __name__ == "__main__":
    main()
