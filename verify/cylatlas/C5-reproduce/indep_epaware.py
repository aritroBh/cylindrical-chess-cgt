"""Independent probe (no cylcgt): value of flat-4 W a2 c2 / B b7 d7 when the
passed-pawn test respects a live e.p. right (a pawn that the opponent can take
e.p. on the next move is not yet passed).  Compares with the textbook test.
  cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/cylatlas/C5-reproduce/indep_epaware.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep_sum as T

def integer(n): return T.integer(n)
SW31 = T.G([integer(3)], [integer(1)]); SWm1m3 = T.G([integer(-1)], [integer(-3)])
H = T.G([SW31], [SWm1m3])  # {2+-1 | -2+-1}, its own negative

def make(cfg, aware):
    def passer(side, W, B, ep):
        mine = W if side == "W" else B
        for f, r in mine:
            if not T.is_passed(cfg, side, f, r, W, B):
                continue
            if aware and ep and ep[1] == (f, r) and ep[2] != side:
                theirs = B if side == "W" else W
                if any((g, r) in theirs for g in cfg.adj(f)):
                    continue  # can still be taken e.p.
            return True
        return False
    def decided(mover, W, B, ep):
        wp, bp = passer("W", W, B, ep), passer("B", W, B, ep)
        if wp and bp:
            opp = "B" if mover == "W" else "W"
            win = opp if T.dist(cfg, opp, W, B) <= T.dist(cfg, mover, W, B) else mover
            return 1 if win == "W" else -1
        return 1 if wp else (-1 if bp else 0)
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def wins(W, B, ep, X, side):
        sgn = 1 if side == "W" else -1
        other = "B" if side == "W" else "W"
        for (W2, B2, e2) in T.pawn_moves(cfg, side, W, B, ep):
            d = decided(side, W2, B2, e2)
            if d == sgn: return True
            if d == -sgn: continue
            if not wins(W2, B2, e2, X, other): return True
        for X2 in (X[0] if side == "W" else X[1]):
            if not wins(W, B, ep, X2, other): return True
        return False
    return wins

W, B = T.parse("W: a2 c2 / B: b7 d7")
for aware in (False, True):
    cfg = T.Cfg(4, False, True, "count")
    wins = make(cfg, aware)
    for label, X in (("*2", T.STAR2), ("{2+-1|-2+-1}", H)):
        z = not wins(W, B, None, X, "W") and not wins(W, B, None, X, "B")
        print(f"flat4 count ep=on passed-test={'ep-aware' if aware else 'textbook'}: W a2 c2 / B b7 d7 == {label}: {z}")
