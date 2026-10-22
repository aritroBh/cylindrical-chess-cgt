"""Independent check of paper Theorem 21 (ring rule) and the strip recurrence.
Written from the rules in the paper's Section XI only (does not import lemmas/ or cylcgt/).
Dawson's chess on a 3 x n board, flat or cylinder: white pawns on rank 1, black on rank 3,
one-step moves, diagonal captures (compulsory), no double step, no promotion,
a side with no legal move loses.  Usage: python3 dawson_ring_check.py [nmax]
"""
import sys
from functools import lru_cache
sys.setrecursionlimit(1000000)

def make(n, wrap):
    nb = lambda f, d: ((f + d) % n) if wrap else (f + d if 0 <= f + d < n else None)

    def moves(W, B, side):
        mine, theirs = (W, B) if side == 0 else (B, W)
        d = 1 if side == 0 else -1
        caps, pushes = [], []
        for (f, r) in mine:
            r1 = r + d
            if not (1 <= r1 <= 3):
                continue
            for df in (-1, 1):
                g = nb(f, df)
                if g is not None and (g, r1) in theirs:
                    caps.append((f, r, g, r1))
            if (f, r1) not in W and (f, r1) not in B:
                pushes.append((f, r, f, r1))
        lst = caps if caps else pushes          # captures are compulsory
        out = []
        for (f, r, g, r1) in lst:
            if (g, r1) in theirs:
                nm = (mine - {(f, r)}) | {(g, r1)}
                nt = theirs - {(g, r1)}
            else:
                nm = (mine - {(f, r)}) | {(g, r1)}
                nt = theirs
            out.append((nm, nt) if side == 0 else (nt, nm))
        return out

    @lru_cache(maxsize=None)
    def win(W, B, side):          # does the side to move win?
        for (w2, b2) in moves(W, B, side):
            if not win(w2, b2, 1 - side):
                return True
        return False
    start = (frozenset((f, 1) for f in range(n)), frozenset((f, 3) for f in range(n)))
    return win, start

def grundy(N):
    g = [0, 1]
    for n in range(2, N + 1):
        s = {g[n - 2]}
        for a in range(0, n - 2):
            b = n - 3 - a
            if b >= 0:
                s.add(g[a] ^ g[b])
        m = 0
        while m in s:
            m += 1
        g.append(m)
    return g

if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    g = grundy(300)
    bad = 0
    for n in range(1, nmax + 1):
        win, (W, B) = make(n, False)
        strip_first = win(W, B, 0)
        ok1 = (strip_first == (g[n] != 0))
        res = f"n={n:2d} strip: first-player-wins={strip_first} g={g[n]} {'ok' if ok1 else 'MISMATCH'}"
        if n >= 3:
            winc, (Wc, Bc) = make(n, True)
            ring_first = winc(Wc, Bc, 0)
            ok2 = (ring_first == (g[n - 3] == 0))
            res += f" | ring: first-player-wins={ring_first} g(n-3)={g[n-3]} {'ok' if ok2 else 'MISMATCH'}"
            bad += (not ok2)
        bad += (not ok1)
        print(res, flush=True)
    print("mismatches:", bad)
    zeros = [n + 3 for n in range(0, 80) if g[n] == 0]
    print("ring first-player wins (n<=82):", zeros)
    # period check of the recurrence out to 300
    per = [m for m in range(200, 300) if g[m] != g[m - 34]]
    print("g(m) != g(m-34) for m in [200,300):", per)
    exc = [m for m in range(34, 300) if g[m] != g[m - 34]]
    print("largest m<300 with g(m) != g(m-34):", max(exc))
