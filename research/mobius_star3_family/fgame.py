"""fgame.py -- faster drop-in for mgame.Board (research/mobius_rings_proof): same rules, passers() computed from
per-file seen-rank extremes, classify() and moves() memoised.  Checked equal to mgame.Board on random positions
(fgame_test.py)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mobius_rings_proof'))
from mgame import Board, col, dirn
class FBoard(Board):
    def __init__(self, n, twist=True):
        super().__init__(n, twist); self._cl = {}; self._mv = {}
    def passers(self, pos, side):
        cells, ep = pos; n = self.n
        # per file and colour: (min rank, max rank) of that colour's pawns
        ext = []
        for f in range(n):
            mn = [9, 9]; mx = [0, 0]
            for r in range(1, 9):
                c = cells[f][r - 1]
                if c:
                    k = col(c)
                    if r < mn[k]: mn[k] = r
                    if r > mx[k]: mx[k] = r
            ext.append((mn, mx))
        enemy = 1 - side; out = []
        prot = {(ep[0], ep[1])} if ep else set()
        for f in range(n):
            lo, hi = 9, 0       # extremes of enemy ranks seen from file f (seam neighbours mirrored)
            for df in (-1, 0, 1):
                g = f + df; x = False
                if g < 0 or g >= n:
                    if not self.twist: g %= n
                    else: g %= n; x = True
                mn, mx = ext[g]
                if mx[enemy] == 0: continue
                a, b = mn[enemy], mx[enemy]
                if x: a, b = 9 - b, 9 - a
                if a < lo: lo = a
                if b > hi: hi = b
            for r in range(1, 9):
                c = cells[f][r - 1]
                if c and col(c) == side and (f, r) not in prot:
                    if dirn(c) > 0: bl = hi > r
                    else: bl = lo < r
                    if not bl: out.append((f, r))
        return out
    def classify(self, pos, mover):
        k = (pos, mover); v = self._cl.get(k)
        if v is None:
            v = Board.classify(self, pos, mover)
            if len(self._cl) > 1500000: self._cl.clear()
            self._cl[k] = v
        return v
    def moves(self, pos, side):
        k = (pos, side); v = self._mv.get(k)
        if v is None:
            v = Board.moves(self, pos, side)
            if len(self._mv) > 60000: self._mv.clear()
            self._mv[k] = v
        return v
