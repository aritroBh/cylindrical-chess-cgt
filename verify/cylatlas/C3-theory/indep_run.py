"""Independent re-evaluation (textbook passed test, count rule, e.p. on) of flat single components / rings:
game tree from sumtest/sumsolver.py's move generator, passer test and race resolution (it does not import
cylcgt.pawns); canonical forms from cylcgt.cgt.  Positions from this directory's own enumerator.
  PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-theory/indep_run.py <flat|ring> <n> <minp> <maxp> <out.jsonl>"""
import json, os, sys, time
sys.setrecursionlimit(100000)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from functools import lru_cache
from cylcgt import cgt
from sumtest.sumsolver import Geometry, Rules
from enum_own import positions
from cgtkey import key
BIG = 256
kind, n, minp, maxp, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
wrap = kind == "ring"
geo = Geometry(n, wrap)
rules = Rules(geo, ep=True, ep_aware=False, race_rule="count")

@lru_cache(maxsize=None)
def val(st):
    if st == "L": return cgt.integer(BIG)
    if st == "R": return cgt.integer(-BIG)
    W, B, e = st
    kids = {}
    for white in (True, False):
        o = []
        for c in rules.moves(W, B, e, white):
            res = rules.resolve(*c, white)
            o.append(val(res if res else c))
        kids[white] = o
    return cgt.make(kids[True], kids[False])

t0 = time.time(); c = 0
with open(out, "w") as fh:
    for w, b, pos in positions(n, wrap, maxp):   # enum_own uses cylcgt.pawns.passed only to skip initial passers
        if w + b < minp: continue
        W, B = geo.parse(str(pos))
        assert not rules.has_initial_passer(W, B)
        g = val((W, B, -1))
        fh.write(json.dumps({"kind": kind, "n": n, "w": w, "b": b, "pos": str(pos), "key": key(g)}) + "\n")
        c += 1
print("done", c, round(time.time() - t0), flush=True)
