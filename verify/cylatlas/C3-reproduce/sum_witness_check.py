"""Directly evaluate the flat-8 whole positions found by sums_check.py and compare
with the cylinder ring witness value (same module, count rule, e.p. on).
  .venv/bin/python verify/cylatlas/C3-reproduce/sum_witness_check.py --root <cylcgt root> --which main|ep
"""
import argparse, sys
ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True); ap.add_argument("--which", required=True); a = ap.parse_args()
sys.path.insert(0, a.root)
from cylcgt import cgt, pawns
P = pawns.Pos.parse
CASES = {"main": [
  (3, "W: a2 b3 / B: a5 c7", "W: a2 b2 d2 / B: a7 d3 e5"),
  (3, "W: a2 b4 / B: b7 c6", "W: a2 b2 d2 / B: a5 d7 e7"),
  (4, "W: a2 c2 / B: b6 d7", "W: a2 a3 c2 e3 / B: a5 c7 d7"),
  (4, "W: a2 c2 / B: b7 d7", "W: a2 a3 c3 e3 / B: a5 d6 d7"),
  (4, "W: a2 c3 / B: b7 d7", "W: a2 a3 c2 e3 / B: a6 c7 d7"),
  (4, "W: a2 b6 c3 / B: b7 d7", "W: a2 a5 c3 d2 / B: a6 c5 e5"),
  (4, "W: a2 c2 / B: a3 b6 d7", "W: a2 c2 e2 / B: a3 a6 c5 d7"),
 ], "ep": [
  (3, "W: a2 b3 / B: a5 a7 c5", "W: a2 c2 c3 / B: a3 a6 c6 d5"),
  (3, "W: a2 a3 b4 / B: a7 c7", "W: a2 a5 c2 d3 / B: a6 c5 c6"),
  (4, "W: a2 b6 c2 / B: b7 d7", "W: a2 a3 a4 c2 c3 / B: a6 c5"),
  (4, "W: a2 c2 / B: a3 b7 d7", "W: a2 a3 a4 c2 / B: a6 c4 c7"),
 ]}
def has_big(g, seen=None):
    seen = set() if seen is None else seen
    if g.id in seen: return False
    seen.add(g.id)
    if g.num is not None: return abs(g.num) >= pawns.BIG // 2
    return any(has_big(x, seen) for x in g.L + g.R)
F8 = pawns.Board(8, 8, False, True)
for n, ring, flat in CASES[a.which]:
    gr = pawns.value(pawns.Board(n, 8, True, True), P(ring))
    pf = P(flat)
    gf = pawns.value(F8, pf)
    comps = pawns.components(F8, pf)
    cb = [has_big(pawns._value(F8, c)) for c in comps]
    print(f"C{n} {ring} = {cgt.show(gr)} | flat8 {flat} = {cgt.show(gf)} | equal={gr is gf} comps={len(comps)} comp_has_W={cb} sum_safe={pawns.sum_safe(F8, pf)}")
