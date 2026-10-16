"""Pawn-level spot check that the 0.137 values are the Grundy values of Dawson's chess
(adversarial verifier C4). Independent code; imports nothing from dawson/ or cylcgt/.
3 x W flat board; W pawns on rank 1, B pawns on rank 3, except files listed as empty.
Rules: pawn moves one square forward to empty square, or diagonally forward to capture;
captures compulsory; side with no legal move loses (normal play). Promotion would raise.
Test: board = strip n1 | empty file | strip n2. Mover loses iff g(n1) == g(n2).
Usage: python pawn_sum_check.py MAXW
"""
import sys
from functools import lru_cache
sys.setrecursionlimit(100000)

def mex(s):
    m = 0
    while m in s: m += 1
    return m

def g0137(N):
    g = [0] * (N + 1)
    for n in range(1, N + 1):
        g[n] = mex({g[max(i-1,0)] ^ g[max(n-2-i,0)] for i in range(n)})
    return g

def solve_width(W):
    @lru_cache(maxsize=None)
    def mover_wins(cells, white):  # cells: tuple of 3*W chars '.', 'W', 'B'; row r file f at r*W+f
        me, opp, d = ('W', 'B', 1) if white else ('B', 'W', -1)
        caps, pushes = [], []
        for r in range(3):
            for f in range(W):
                if cells[r*W+f] != me: continue
                r2 = r + d
                if not 0 <= r2 < 3: continue
                for f2 in (f-1, f+1):
                    if 0 <= f2 < W and cells[r2*W+f2] == opp:
                        caps.append((r*W+f, r2*W+f2, r2))
                if cells[r2*W+f] == '.':
                    pushes.append((r*W+f, r2*W+f, r2))
        moves = caps if caps else pushes
        for a, b, r2 in moves:
            if (white and r2 == 2) or ((not white) and r2 == 0):
                raise RuntimeError("promotion reached")
            c = list(cells); c[b] = c[a]; c[a] = '.'
            if not mover_wins(tuple(c), not white):
                return True
        return False
    return mover_wins

def start(W, empty):
    c = []
    for r, ch in ((0, 'W'), (1, '.'), (2, 'B')):
        for f in range(W):
            c.append('.' if (f in empty or ch == '.') else ch)
    return tuple(c)

def main(MAXW):
    g = g0137(MAXW)
    tested = bad = 0
    for W in range(1, MAXW + 1):
        mw = solve_width(W)
        # single strip
        for white in (True, False):
            res = mw(start(W, set()), white)
            tested += 1
            if res != (g[W] != 0):
                bad += 1; print("MISMATCH single", W, white, res, g[W])
        for n1 in range(1, W - 1):
            n2 = W - 1 - n1
            if n2 < 1: continue
            for white in (True, False):
                res = mw(start(W, {n1}), white)
                tested += 1
                if res != ((g[n1] ^ g[n2]) != 0):
                    bad += 1; print("MISMATCH sum", n1, n2, white, res, g[n1], g[n2])
        print(f"W={W}: cache {mw.cache_info().currsize}", flush=True)
    print(f"tested {tested} start positions (single strips and strip|empty|strip, both movers), mismatches {bad}")

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 12)
