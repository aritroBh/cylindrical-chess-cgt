"""Independent pawn-level solver for Dawson's chess on 3 x n boards (flat or cylinder).
Real pawn moves: one step forward to an empty square, diagonal-forward capture of an enemy pawn.
Captures compulsory. Normal play: side with no legal move loses. Any move onto the last rank
(promotion) is counted in PROMO and would be reported. Imports no worker code.
"""
import sys, itertools
from functools import lru_cache
sys.setrecursionlimit(100000)
PROMO = [0]

def make_solver(n, wrap):
    def cell(r, f): return r * n + f
    def nb(f):
        out = []
        for d in (-1, 1):
            g = f + d
            if wrap: g %= n
            if 0 <= g < n and g != f: out.append(g)
        return sorted(set(out))
    NB = [nb(f) for f in range(n)]
    def moves(b, side):          # side 1 = White (moves to higher rank), 2 = Black
        dr = 1 if side == 1 else -1
        enemy = 3 - side
        caps, pushes = [], []
        for r in range(3):
            for f in range(n):
                if b[cell(r, f)] != side: continue
                r2 = r + dr
                if not (0 <= r2 < 3): continue
                for g in NB[f]:
                    if b[cell(r2, g)] == enemy: caps.append((cell(r, f), cell(r2, g), r2))
                if b[cell(r2, f)] == 0: pushes.append((cell(r, f), cell(r2, f), r2))
        return caps if caps else pushes
    @lru_cache(maxsize=None)
    def win(b, side):            # True iff side to move wins
        for s, t, r2 in moves(b, side):
            if (side == 1 and r2 == 2) or (side == 2 and r2 == 0): PROMO[0] += 1
            nbd = list(b); nbd[t] = side; nbd[s] = 0
            if not win(tuple(nbd), 3 - side): return True
        return False
    return win

def start(layout):               # layout: string of 'x' (pawn file) and '.' (empty file)
    n = len(layout)
    b = [0] * (3 * n)
    for f, c in enumerate(layout):
        if c == 'x': b[f] = 1; b[2 * n + f] = 2
    return tuple(b)

def g137(N):
    def mex(s):
        m = 0
        while m in s: m += 1
        return m
    g = []
    for n in range(N + 1):
        g.append(mex({g[max(i - 1, 0)] ^ g[n - min(i + 2, n)] for i in range(n)}))
    return g

if __name__ == "__main__":
    W = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    G = g137(64)
    bad = 0; tested = 0
    # flat boards: every layout of strips separated by single empty files, width <= W
    for width in range(1, W + 1):
        solver = make_solver(width, False)
        for k in range(1, 4):                       # 1, 2 or 3 strips
            for parts in itertools.product(range(1, width + 1), repeat=k):
                if sum(parts) + (k - 1) != width: continue
                lay = '.'.join('x' * p for p in parts)
                pred_N = 0
                for p in parts: pred_N ^= G[p]
                for side in (1, 2):
                    got = solver(start(lay), side)
                    tested += 1
                    if got != (pred_N != 0):
                        bad += 1; print("MISMATCH flat", parts, "side", side, got, pred_N)
        print(f"flat width {width}: cumulative tests {tested}, mismatches {bad}, promotions {PROMO[0]}", flush=True)
    # cylinders: full ring of n files
    for n in range(3, W + 2):
        solver = make_solver(n, True)
        res = [solver(start('x' * n), s) for s in (1, 2)]
        pred = (G[n - 3] == 0)
        tested += 2
        if res != [pred, pred]:
            bad += 1; print("MISMATCH ring", n, res, pred)
        print(f"ring n={n}: first player wins = {res}, predicted g(n-3)==0 -> {pred}", flush=True)
    print(f"TOTAL tests {tested}, mismatches {bad}, promotions {PROMO[0]}")
