"""Normal-play Grundy values for Dawson's chess as an octal game.

Independent of cylcgt: a generic octal-game evaluator (any code 0.d1d2...dk),
applied to 0.137 (Dawson's chess, one pin per file of a 3 x n board) and to
0.07 (Dawson's Kayles), plus the ring values and the 2025 paper's recurrence.

Run from the project root:
    PYTHONPATH=. .venv/bin/python -m dawson.octal            # summary, N = 300
    PYTHONPATH=. .venv/bin/python -m dawson.octal 1000       # larger N
"""
import sys


def octal_options(code: str):
    """Parse '0.137' into a move list [(k, bits)] where bits has
    1 = may remove k leaving nothing, 2 = leaving one heap, 4 = leaving two heaps."""
    assert code.startswith("0.")
    return [(k, int(d)) for k, d in enumerate(code[2:], start=1) if int(d)]


def heap_moves(code_moves, n):
    """All ways to move in a single heap of size n: list of tuples of remaining heaps
    (each remaining heap has size >= 1)."""
    out = []
    for k, bits in code_moves:
        r = n - k
        if r < 0:
            continue
        if r == 0 and bits & 1:
            out.append(())
        if r >= 1 and bits & 2:
            out.append((r,))
        if r >= 2 and bits & 4:
            for a in range(1, r // 2 + 1):
                out.append((a, r - a))
    return out


def grundy(code: str, N: int):
    mv = octal_options(code)
    g = [0] * (N + 1)
    for n in range(1, N + 1):
        opts = set()
        for rest in heap_moves(mv, n):
            x = 0
            for h in rest:
                x ^= g[h]
            opts.add(x)
        m = 0
        while m in opts:
            m += 1
        g[n] = m
    return g


def find_period(g, k):
    """Smallest period p and preperiod n0 such that g(n+p) = g(n) for all n0 <= n
    with n+p <= len(g)-1, choosing the smallest p for which the Guy-Smith
    certificate range n0 <= n < 2*n0 + p + k lies inside the data.
    Returns (p, n0, last_exception) or None."""
    N = len(g) - 1
    for p in range(1, N // 2):
        # last n with g(n) != g(n+p)
        last = -1
        for n in range(0, N - p + 1):
            if g[n] != g[n + p]:
                last = n
        n0 = last + 1
        if 2 * n0 + p + k - 1 + p <= N:  # every n < 2 n0 + p + k is checked (n + p <= N)
            return p, n0, last
    return None


def ring_values(g, N):
    """R_n for a 3 x n cylinder, n >= 3: the only first move opens the ring into a strip
    of n - 3 files, so R_n = mex{ g(n-3) }."""
    R = {}
    for n in range(3, N + 1):
        R[n] = 1 if g[n - 3] == 0 else 0
    return R


def paper_recurrence(N):
    """The 2025 paper's recurrence G(n) = mex{G(a) xor G(b) : a + b = n - 3} (omits end moves)."""
    G = [0] * (N + 1)
    for n in range(N + 1):
        opts = {G[a] ^ G[n - 3 - a] for a in range(0, n - 2)} if n >= 3 else set()
        m = 0
        while m in opts:
            m += 1
        G[n] = m
    return G


def main(N=300):
    g = grundy("0.137", N)
    gk = grundy("0.07", N + 1)
    shift_ok = all(g[n] == gk[n + 1] for n in range(N + 1))
    print(f"0.137 Grundy values g(0..{N}):")
    for s in range(0, N + 1, 34):
        print(f"  n={s:3d}..{min(s+33, N):3d}: " + "".join(f"{v:x}" if v < 16 else f"({v})" for v in g[s:s + 34]))
    print(f"max g(n) for n <= {N}: {max(g)}")
    print(f"g_0.137(n) == g_0.07(n+1) for all n <= {N}: {shift_ok}")
    per = find_period(g, k=3)
    print(f"period search (Guy-Smith certificate, k=3): p, n0, last exception = {per}")
    if per:
        p, n0, last = per
        print(f"  checked g(n+{p}) = g(n) for {n0} <= n <= {N-p}; certificate needs n < {2*n0+p+3}")
        exc = [n for n in range(0, N - p + 1) if g[n] != g[n + p]]
        print(f"  all n with g(n) != g(n+{p}): {exc}")
    perk = find_period(gk, k=2)
    print(f"0.07 (Dawson's Kayles) period: {perk}")
    R = ring_values(g, N)
    rs = "".join(str(R[n]) for n in range(3, N + 1))
    print(f"ring values R_n, n = 3..{N}:")
    for s in range(3, N + 1, 68):
        print(f"  n={s:3d}..{min(s+67, N):3d}: " + "".join(str(R[n]) for n in range(s, min(s + 68, N + 1))))
    ones = [n for n in range(3, N + 1) if R[n] == 1]
    print(f"R_n = 1 (first player wins the ring) for n in {ones[:40]} ...")
    print(f"  ring outcome period: R_(n+34) == R_n for all 3+52 <= n <= {N-34}: "
          f"{all(R[n] == R[n + 34] for n in range(55, N - 33))}")
    print(f"  last n with R_n != R_(n+34): {max([n for n in range(3, N - 33) if R[n] != R[n + 34]], default=None)}")
    zeros = [n for n in range(N + 1) if g[n] == 0]
    print(f"g(n) = 0 for n in {zeros[:30]} ...")
    G = paper_recurrence(N)
    diff = [n for n in range(N + 1) if G[n] != g[n]]
    print(f"paper recurrence G(0..40): {G[:41]}")
    print(f"correct  0.137   g(0..40): {g[:41]}")
    print(f"n <= {N} where paper G(n) != g(n): {len(diff)} values, first few {diff[:12]}")
    pr = {n: (1 if G[n - 3] == 0 else 0) for n in range(3, N + 1)}
    rdiff = [n for n in range(3, N + 1) if pr[n] != R[n]]
    print(f"n <= {N} where paper Ring(n) != correct R_n: {len(rdiff)} values, first few {rdiff[:12]}")
    return g, R


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 300)
