"""Independent theory-lens check of claim C2 (Dawson section 8 of the 2025 paper).

Written from scratch; imports nothing from dawson/ or cylcgt/.

1. g(n): Grundy values of Node Kayles on a path P_n (choose a vertex, delete it and its
   neighbours), computed by brute force over bitmask positions for n <= 22, and by the
   0.137 recurrence for n <= 300. Node Kayles on P_n is the standard formulation of 0.137.
2. G(n): the paper's recurrence, literally: G(n) = mex{G(a) xor G(b) : a,b >= 0, a+b = n-3}.
   This is the recurrence of octal game 0.007 (remove exactly 3 contiguous), checked by
   brute force on bitmasks too.
3. Literal paper rule: full row, remove a pawn only if both neighbours (if any) are empty.
4. A pawn-level solver for the 3 x n board (flat and cylinder), compulsory capture,
   normal play, flags any promotion; compares outcomes to g / G predictions.

Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python \
     verify/dawson/C2-theory/check_c2.py
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)


def mex(s):
    m = 0
    while m in s:
        m += 1
    return m


# ---------- 1. g via brute-force Node Kayles on a path (bitmask of live vertices) ----------
def node_kayles_path_grundy(n):
    @lru_cache(maxsize=None)
    def gr(mask):
        opts = set()
        for i in range(n):
            if mask >> i & 1:
                kill = (1 << i) | ((1 << (i - 1)) if i > 0 else 0) | ((1 << (i + 1)) if i + 1 < n else 0)
                opts.add(gr(mask & ~kill))
        return mex(opts)
    return gr((1 << n) - 1)


def g_recurrence(N):
    g = [0] * (N + 1)
    for n in range(1, N + 1):
        opts = set()
        if n == 1:
            opts.add(0)
        if n >= 2:
            opts.add(g[n - 2])                      # end vertex: kills 2
        for a in range(0, n - 2):                   # interior vertex: kills 3, a + b = n - 3
            opts.add(g[a] ^ g[n - 3 - a])
        g[n] = mex(opts)
    return g


def G_paper(N):
    G = [0] * (N + 1)
    for n in range(N + 1):
        G[n] = mex({G[a] ^ G[n - 3 - a] for a in range(0, n - 2)}) if n >= 3 else 0
    return G


def octal_0007_bruteforce(n):
    """Remove exactly 3 contiguous tokens from a row (bitmask)."""
    @lru_cache(maxsize=None)
    def gr(mask):
        opts = set()
        for i in range(n - 2):
            t = 0b111 << i
            if mask & t == t:
                opts.add(gr(mask & ~t))
        return mex(opts)
    return gr((1 << n) - 1)


def literal_rule_moves(n):
    """Full row of n pawns: a pawn may be removed only if its neighbours (if any) are empty."""
    row = [1] * n
    return [i for i in range(n) if row[i] and (i == 0 or not row[i - 1]) and (i == n - 1 or not row[i + 1])]


# ---------- 4. pawn-level 3 x n solver ----------
def pawn_outcome(n, wrap):
    """Return (first player wins?, promotion_seen) for the start position, White to move.
    Board squares: ranks 1..3. White pawns move +1, Black -1. Compulsory capture.
    A pawn reaching its last rank is recorded (promotion_seen) and treated as... we only flag."""
    promo = [False]

    def nb(f):
        out = []
        for d in (-1, 1):
            h = f + d
            if wrap:
                h %= n
            if 0 <= h < n and h != f:
                out.append(h)
        return sorted(set(out))

    NB = [nb(f) for f in range(n)]

    def moves(state, white):
        # state: tuple of length 3n; cell (rank r in 0..2, file f) -> state[r*n+f] in {0,'W','B'}
        me, op, dr = ('W', 'B', 1) if white else ('B', 'W', -1)
        caps, quiet = [], []
        for r in range(3):
            for f in range(n):
                if state[r * n + f] != me:
                    continue
                r2 = r + dr
                if not (0 <= r2 < 3):
                    continue
                for h in NB[f]:
                    if state[r2 * n + h] == op:
                        s = list(state); s[r * n + f] = 0; s[r2 * n + h] = me
                        if (white and r2 == 2) or (not white and r2 == 0):
                            promo[0] = True
                        caps.append(tuple(s))
                if state[r2 * n + f] == 0:
                    s = list(state); s[r * n + f] = 0; s[r2 * n + f] = me
                    if (white and r2 == 2) or (not white and r2 == 0):
                        promo[0] = True
                    quiet.append(tuple(s))
        return caps if caps else quiet

    @lru_cache(maxsize=None)
    def win(state, white):  # side to move wins?
        return any(not win(s, not white) for s in moves(state, white))

    start = tuple(['W'] * n + [0] * n + ['B'] * n)
    res = win(start, True)
    resB = win(start, False)
    assert res == resB, "colour asymmetry?"
    return res, promo[0]


def main():
    N = 300
    g = g_recurrence(N)
    G = G_paper(N)

    # brute-force cross-checks
    for n in range(0, 23):
        assert node_kayles_path_grundy(n) == g[n], ("node kayles", n)
        assert octal_0007_bruteforce(n) == G[n], ("0.007", n)
    print("Node-Kayles-on-path brute force == 0.137 recurrence g(n) for n <= 22: OK")
    print("octal 0.007 (remove exactly 3 contiguous) brute force == paper G(n) for n <= 22: OK")

    print("g(0..40) =", g[:41])
    print("G(0..40) =", G[:41])
    agree = [n for n in range(N + 1) if g[n] == G[n]]
    print(f"n in 0..{N} with G(n) == g(n): {len(agree)} of {N+1}: {agree}")
    flat_out = [n for n in range(N + 1) if (g[n] == 0) != (G[n] == 0)]
    print(f"flat outcome (zero vs nonzero) mismatches n <= {N}: {len(flat_out)}; first {flat_out[:12]}")
    ring = [n for n in range(3, N + 1) if (g[n - 3] == 0) != (G[n - 3] == 0)]
    print(f"ring outcome mismatches 3 <= n <= {N}: {len(ring)}; first {ring[:12]}")
    print("paper predicts 3x4 cylinder first-player win:", G[1] == 0, "; correct:", g[1] == 0)

    for n in range(0, 8):
        print(f"literal paper rule, full row n={n}: legal removals at {literal_rule_moves(n)}")

    print("pawn-level 3 x n solver (independent), compulsory capture, normal play:")
    bad_flat, bad_ring = [], []
    for n in range(1, 10):
        w, p = pawn_outcome(n, False)
        ok = (w == (g[n] != 0)); paper_ok = (w == (G[n] != 0))
        if not ok:
            bad_flat.append(n)
        print(f"  flat n={n}: first player wins={w}  g-pred ok={ok}  paper-G-pred ok={paper_ok}  promo={p}")
    for n in range(3, 10):
        w, p = pawn_outcome(n, True)
        ok = (w == (g[n - 3] == 0)); paper_ok = (w == (G[n - 3] == 0))
        if not ok:
            bad_ring.append(n)
        print(f"  ring n={n}: first player wins={w}  g-pred ok={ok}  paper-G-pred ok={paper_ok}  promo={p}")
    print("pawn-level mismatches vs g:", bad_flat, bad_ring)


if __name__ == "__main__":
    main()
