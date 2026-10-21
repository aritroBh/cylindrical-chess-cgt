"""Variant of the independent sum model with GLOBAL e.p. rights (every move,
including a move in a frozen integer, deletes all old rights). Used to see
whether the e.p.-on table rows disagree because of stale local rights (L1.7)
or because of nested +-BIG cancellation.
cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python -I verify/lemmas/L2.2-sum_safe-counterexample-reproduce/r2_globalep.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from functools import lru_cache
from r2_indep import Game, comps, parse, INF

def strip(Y):
    return frozenset((w, b, None) for (w, b, e) in Y)

class GGame(Game):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.thr = lru_cache(maxsize=None)(self._thr_g)
    def _thr_g(self, Y):
        A, B = INF, -INF
        for Z in Y:
            rest = strip(Y - {Z})
            for d, new in self._component_moves(Z, "W"):
                A = min(A, self.thr(rest | frozenset(new))[1] - d)
            for d, new in self._component_moves(Z, "B"):
                B = max(B, self.thr(rest | frozenset(new))[0] - d)
        if any(e is not None for (_, _, e) in Y):
            sL, sR = self.thr(strip(Y))
            return min(A, max(1, sR + 1)), max(B, min(0, sL - 1))
        return min(A, max(1, B + 1)), max(B, min(0, A - 1))

for n, m, wrap, ep, text, rule in [
    (8, 8, True, True, "W: a2 c4 e4 h2 / B: a6 b5 d7 e7", "count"),
    (8, 8, True, True, "W: a5 b6 d2 e2 / B: a7 c7 e7", "count"),
    (7, 6, False, True, "W: b2 d3 f2 / B: c4 c5 e5 g5", "count"),
    (8, 8, True, True, "W: a3 e2 e4 h6 / B: a4 a5 f5 g7", "opponent"),
    (8, 8, True, False, "W: b2 d4 g3 h5 / B: a7 c7 f7 g4", "count")]:
    x = parse(text)
    g, gg = Game(n, m, wrap, ep, rule), GGame(n, m, wrap, ep, rule)
    print(f"{n}x{m} {'cyl' if wrap else 'flat'} ep={'on' if ep else 'off'} {rule:8s} {text}: "
          f"o(S local ep)={g.S_outcome(x)} o(S global ep)={gg.S_outcome(x)} o(W)={g.W_outcome(x)}", flush=True)
