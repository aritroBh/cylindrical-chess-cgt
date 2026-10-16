"""Brute-force (no canonical forms) outcome tests for claim C4.

G = H is checked as: G + (-H) is a second-player win (P), by plain minimax over
the explicit game tree of the pawn position plus an explicit tree for -H.
Integers (the +-256 leaves and plain numbers) are kept as explicit integer games:
Left may move n -> n-1 when n > 0, Right n -> n+1 when n < 0 (no number avoidance).
Only my own pawn model (c4check.Model) is used; no canonical simplification.

Run:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/sumtest/C4-refute/c4brute.py
"""
import os
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.setrecursionlimit(5_000_000)
from c4check import Model, parse  # noqa: E402  (own code; c4check's CGT is not used here)

# explicit small games as nested tuples ("g", Ltuple, Rtuple) or ints
def G(L, R):
    return ("g", tuple(L), tuple(R))


def pm(x):           # {x | -x} for integer x
    return G([x], [-x])


def sw(a, b):
    return G([a], [b])


def negate(h):
    if isinstance(h, int):
        return -h
    _, L, R = h
    return G([negate(x) for x in R], [negate(x) for x in L])


STAR = G([0], [0])
STAR2 = G([0, STAR], [0, STAR])


class SumSolver:
    def __init__(self, model):
        self.m = model
        self.memo = {}

    def pawn_opts(self, st, side):
        out = []
        for c in self.m.moves(*st, side):
            r = self.m.resolve(c, side)
            out.append(r if r is not None else c)  # int or state
        return out

    # a state of the sum: (pawn part: state or None, h part: tuple or None, n: int)
    def norm(self, p, h, n):
        if isinstance(p, int):
            n += p
            p = None
        if isinstance(h, int):
            n += h
            h = None
        return (p, h, n)

    def wins(self, S, left):
        """True if the side `left` (True=Left) moving first in S wins"""
        key = (S, left)
        v = self.memo.get(key)
        if v is not None:
            return v
        p, h, n = S
        side = "W" if left else "B"
        kids = []
        if p is not None:
            for c in self.pawn_opts(p, side):
                kids.append(self.norm(c, h, n))
        if h is not None:
            for c in (h[1] if left else h[2]):
                kids.append(self.norm(p, c, n))
        if left and n > 0:
            kids.append((p, h, n - 1))
        if (not left) and n < 0:
            kids.append((p, h, n + 1))
        v = any(not self.wins(k, not left) for k in kids)
        self.memo[key] = v
        return v

    def outcome(self, pos_text, h):
        W, B = parse(pos_text)
        S = self.norm((W, B, None), h, 0)
        lw, rw = self.wins(S, True), self.wins(S, False)
        return {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(lw, rw)]


def main():
    X = "W: a2 c2 / B: b4 d7"
    B5 = "W: a2 c2 / B: b5 d7"
    Gr = "W: a2 c2 / B: b7 d7"
    T_text = G([256], [pm(256)])
    claims = [
        # (position, test, claimed value H, label)
        (X, False, T_text, "X textbook = {256 | +-256}"),
        (X, True, -3, "X aware = -3"),
        (B5, False, 0, "B5 textbook = 0"),
        (B5, True, sw(-1, -3), "B5 aware = -2+-1"),
        (Gr, False, STAR2, "G textbook = *2"),
        (Gr, True, G([sw(3, 1)], [sw(-1, -3)]), "G aware = {2+-1 | -2+-1}"),
    ]
    # near-miss alternatives that must NOT be equal (sanity: test has power)
    alts = [
        (X, True, -2, "X aware = -2 (should fail)"),
        (X, True, -4, "X aware = -4 (should fail)"),
        (X, False, 256, "X textbook = 256 (should fail)"),
        (X, False, pm(256), "X textbook = +-256 (should fail)"),
        (B5, True, -2, "B5 aware = -2 (should fail)"),
        (B5, True, sw(-1, -2), "B5 aware = {-1|-2} (should fail)"),
        (B5, False, STAR, "B5 textbook = * (should fail)"),
    ]
    for race in ("count", "mover", "opponent"):
        for ep in (True, False):
            for aware in (False, True):
                if aware and not ep:
                    continue
                m = Model(4, 8, False, ep=ep, aware=aware, race=race)
                s = SumSolver(m)
                for pos, a, H, label in claims + alts:
                    if a != aware:
                        continue
                    o = s.outcome(pos, negate(H))
                    print(f"race={race:8s} ep={'on ' if ep else 'off'} {label:40s} "
                          f"outcome(G - H) = {o}  -> {'EQUAL' if o == 'P' else 'not equal'}")


if __name__ == "__main__":
    threading.stack_size(1 << 30)
    t = threading.Thread(target=main)
    t.start()
    t.join()
