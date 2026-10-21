"""Canonical-form-free check: G == *k  iff  G + *k is a second-player win.
Plain minimax over (pawn position, nim heap, side to move); a passer (or a race,
scored by the rule) ends the game, since +-BIG dominates any nim heap.
Uses pg.gen / pg.has_passer / pg.race_winner only (no cg canonical forms).

Run: ../../../.venv/bin/python nimtest.py
"""
import sys
from functools import lru_cache

import pg

sys.setrecursionlimit(100000)


def terminal(kind, n, W, B, ep, mover):
    wp = pg.has_passer(kind, n, W, B, ep, "W")
    bp = pg.has_passer(kind, n, W, B, ep, "B")
    if wp and bp:
        return pg.race_winner(kind, n, W, B, ep, mover)
    if wp:
        return "W"
    if bp:
        return "B"
    return None


def solve(kind, n, W0, B0):
    @lru_cache(maxsize=None)
    def win(W, B, ep, k, side):
        other = "B" if side == "W" else "W"
        for (w, b, e) in pg.gen(kind, n, W, B, ep, side):
            t = terminal(kind, n, w, b, e, side)
            if t == side:
                return True
            if t is None and not win(w, b, e, k, other):
                return True
        for j in range(k):
            if not win(W, B, ep, j, other):
                return True
        return False

    res = {}
    for k in range(0, 5):
        lw = win(W0, B0, None, k, "W")
        rw = win(W0, B0, None, k, "B")
        res[k] = {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(lw, rw)]
    return res


if __name__ == "__main__":
    pg.EPAWARE = False
    for rule, ep, kind, n, text in (("count", True, "F", 4, "W: a2 c2 / B: b7 d7"),
                                    ("mover", True, "F", 4, "W: a2 c2 / B: b7 d7"),
                                    ("opponent", True, "F", 4, "W: a2 c2 / B: b7 d7"),
                                    ("count", False, "F", 4, "W: a2 c2 / B: b7 d7"),
                                    ("opponent", True, "C", 3, "W: a2 b3 / B: a5 c5"),
                                    ("count", True, "C", 4, "W: a2 c2 / B: b7 d7")):
        pg.RULE, pg.EP = rule, ep
        W, B = pg.parse(text)
        r = solve(kind, n, W, B)
        print(f"{rule:8s} ep={ep} {kind}{n} {text}: outcome of G + *k for k=0..4: {r}")
    pg.RULE, pg.EP, pg.EPAWARE = "count", True, True
    W, B = pg.parse("W: a2 c2 / B: b7 d7")
    print("count ep-aware F4 W: a2 c2 / B: b7 d7:", solve("F", 4, W, B))
