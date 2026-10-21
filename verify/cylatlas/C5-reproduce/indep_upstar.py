"""Independent check of two opponent-rule ring values with nim part >= 2.
  cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/cylatlas/C5-reproduce/indep_upstar.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep_scan as S
from functools import lru_cache

@lru_cache(maxsize=None)
def add(x, y):
    L = [add(a, y) for a in x[0]] + [add(x, b) for b in y[0]]
    R = [add(a, y) for a in x[1]] + [add(x, b) for b in y[1]]
    return (tuple(L), tuple(R))

STAR = S.NIMS[1]; ZERO = S.ZERO
UP = ((ZERO,), (STAR,)); DOWN = ((STAR,), (ZERO,))
for text, label, X in [("W: a2 b3 / B: a5 c6", "up*3", add(DOWN, S.NIMS[3])),
                       ("W: a2 b3 / B: a6 c6", "dbl-up*2", add(add(DOWN, DOWN), S.NIMS[2])),
                       ("W: a2 b3 / B: a5 c6", "control up*", add(DOWN, STAR)),
                       ("W: a2 b3 / B: a5 c6", "control up", DOWN)]:
    for ep in (True, False):
        S.CFG.clear(); S.CFG.update(n=3, wrap=True, ep=ep, rule="opponent")
        for f in (S.comp_children, S.can_produce, S.wins): f.cache_clear()
        W, B = text.split("/")
        sq = lambda t: ("abc".index(t[0]), int(t[1]))
        c = S.comp_key([sq(t) for t in W.split(":")[1].split()], [sq(t) for t in B.split(":")[1].split()], None)
        z = not S.wins((c,), 0, X, "W") and not S.wins((c,), 0, X, "B")
        print(f"cyl3 opponent ep={int(ep)} {text} == {label}: {z}")
