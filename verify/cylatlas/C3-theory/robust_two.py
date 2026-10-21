"""The two values that are cylinder-only (w+b<=5) under all 9 settings: their ring witnesses vs flat 8-file composites
(7-8 pawns), whole-board trees from sumtest's generator + cylcgt.cgt, under all 9 settings.
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-theory/robust_two.py"""
import sys
sys.setrecursionlimit(100000)
from functools import lru_cache
from cylcgt import cgt
from sumtest.sumsolver import Geometry, Rules
def value(text, files, wrap, race, ep, aware):
    geo = Geometry(files, wrap); rules = Rules(geo, ep=ep, ep_aware=aware, race_rule=race)
    @lru_cache(maxsize=None)
    def val(st):
        if st == "L": return cgt.integer(256)
        if st == "R": return cgt.integer(-256)
        W, B, e = st
        kids = {}
        for white in (True, False):
            kids[white] = [val(r if (r := rules.resolve(*c, white)) else c) for c in rules.moves(W, B, e, white)]
        return cgt.make(kids[True], kids[False])
    W, B = geo.parse(text)
    return val((W, B, -1))
cases = [("W: a2 a3 c3 / B: b6 d7", 4, True), ("W: a2 c2 e3 e4 / B: a3 a5 d7 e7", 8, False),
         ("W: a2 c3 / B: b6 b7 d6", 4, True), ("W: a2 a3 c2 d2 / B: a6 c5 c6 e7", 8, False)]
for text, n, wrap in cases:
    row = []
    for race in ("count", "mover", "opponent"):
        for ep, aware in ((True, False), (True, True), (False, False)):
            row.append(cgt.show(value(text, n, wrap, race, ep, aware)))
    print(f"{'cyl' if wrap else 'flat'}{n} {text:34s}", " ; ".join(row))
