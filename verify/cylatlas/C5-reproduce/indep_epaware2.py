"""Do the other C5 values survive an e.p.-aware passed test?  (independent, no cylcgt)
  cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/cylatlas/C5-reproduce/indep_epaware2.py
"""
import os, sys
from functools import lru_cache
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep_sum as T

def solver(cfg, aware):
    def passer(side, W, B, ep):
        mine = W if side == "W" else B
        theirs = B if side == "W" else W
        for f, r in mine:
            if not T.is_passed(cfg, side, f, r, W, B):
                continue
            if aware and ep and ep[1] == (f, r) and ep[2] != side and any((g, r) in theirs for g in cfg.adj(f)):
                continue
            return True
        return False
    def decided(mover, W, B, ep):
        wp, bp = passer("W", W, B, ep), passer("B", W, B, ep)
        if wp and bp:
            opp = "B" if mover == "W" else "W"
            if cfg.rule == "mover": win = mover
            elif cfg.rule == "opponent": win = opp
            else: win = opp if T.dist(cfg, opp, W, B) <= T.dist(cfg, mover, W, B) else mover
            return 1 if win == "W" else -1
        return 1 if wp else (-1 if bp else 0)
    @lru_cache(maxsize=None)
    def wins(W, B, ep, X, side):
        sgn = 1 if side == "W" else -1; other = "B" if side == "W" else "W"
        for (W2, B2, e2) in T.pawn_moves(cfg, side, W, B, ep):
            d = decided(side, W2, B2, e2)
            if d == sgn: return True
            if d == -sgn: continue
            if not wins(W2, B2, e2, X, other): return True
        for X2 in (X[0] if side == "W" else X[1]):
            if not wins(W, B, ep, X2, other): return True
        return False
    return wins

for board, n, rule, text, label, X in [
        ("cyl", 4, "count", "W: a2 c2 / B: b7 d7", "{3/2+-1/2|-3/2+-1/2}", T.neg(T.H_CYL4)),
        ("cyl", 4, "count", "W: a2 c2 / B: b7 d7", "+-1/2 (the e.p.-off value)", T.PM_HALF),
        ("cyl", 3, "opponent", "W: a2 b3 / B: a5 c5", "*2", T.STAR2),
        ("flat", 4, "mover", "W: a2 c2 / B: b7 d7", "*2", T.STAR2)]:
    W, B = T.parse(text)
    for aware in (False, True):
        cfg = T.Cfg(n, board == "cyl", True, rule)
        wins = solver(cfg, aware)
        z = not wins(W, B, None, X, "W") and not wins(W, B, None, X, "B")
        print(f"{board}{n} {rule} ep=on test={'ep-aware' if aware else 'textbook'} {text} == {label}: {z}")
