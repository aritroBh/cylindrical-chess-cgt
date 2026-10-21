"""C3 REFUTE-lens, version 2: octal 0.137 values, ring outcome sequence, periodicity,
and a raw forced-line lemma check on large rings. Stdlib only; imports nothing from the
project.  Run: python3 v2_octal.py [NMAX]"""
import sys

def octal(code, nmax):
    digits = [int(c) for c in code.split('.')[1]]       # d_1, d_2, ...
    g = [0] * (nmax + 1)
    for n in range(1, nmax + 1):
        opts = set()
        for k, d in enumerate(digits, start=1):
            if k > n:
                break
            r = n - k
            if (d & 1) and r == 0:
                opts.add(0)
            if (d & 2) and r > 0:
                opts.add(g[r])
            if (d & 4) and r >= 2:
                for a in range(1, r // 2 + 1):
                    opts.add(g[a] ^ g[r - a])
        m = 0
        while m in opts:
            m += 1
        g[n] = m
    return g

def lemma_ring(n, f0):
    """Raw rules on a 3 x n ring: White pushes file f0, then every forced capture line.
    Returns list of (plies, resulting board) at the first quiet position."""
    E, W, B = 0, 1, 2
    start = tuple((W, E, B) for _ in range(n))
    def nb(f):
        return {(f - 1) % n, (f + 1) % n}
    def caps(b, s):
        out = []
        dr = 1 if s == W else -1
        opp = B if s == W else W
        for f in range(n):
            for r in range(3):
                if b[f][r] != s:
                    continue
                r2 = r + dr
                if not 0 <= r2 < 3:
                    continue
                for g2 in nb(f):
                    if b[g2][r2] == opp:
                        nbd = [list(x) for x in b]
                        nbd[f][r] = E
                        nbd[g2][r2] = s
                        out.append(tuple(tuple(x) for x in nbd))
        return out
    b = [list(x) for x in start]
    b[f0][0] = E; b[f0][1] = W
    b = tuple(tuple(x) for x in b)
    res = []
    stack = [(b, B, 1)]
    while stack:
        bb, s, ply = stack.pop()
        c = caps(bb, s)
        if not c:
            res.append((ply, s, bb))
            continue
        for x in c:
            stack.append((x, W if s == B else B, ply + 1))
    return res

def main():
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    g = octal('0.137', NMAX)
    g07 = octal('0.07', NMAX + 1)
    print('0.137 vs 0.07 shifted: equal for n<=%d:' % NMAX, all(g[n] == g07[n + 1] for n in range(NMAX + 1)))
    print('g(0..33):', ' '.join(map(str, g[:34])))
    print('max g up to %d:' % NMAX, max(g))
    exc = [n for n in range(NMAX - 34 + 1) if g[n] != g[n + 34]]
    print('n with g(n)!=g(n+34), n<=%d:' % (NMAX - 34), exc)
    n0, p, k = 52, 34, 3
    print('periodicity theorem hypothesis g(n+34)=g(n) for 52<=n<%d:' % (2 * n0 + p + k),
          all(g[n + p] == g[n] for n in range(n0, 2 * n0 + p + k)))
    R = {n: 1 if g[n - 3] == 0 else 0 for n in range(3, NMAX + 4)}
    wins = [n for n in range(3, 201) if R[n]]
    print('ring first-player wins n<=200:', wins)
    claimed = [3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57]
    print('claimed prefix matches:', [n for n in range(3, 58) if R[n]] == claimed)
    rexc = [n for n in range(3, NMAX + 4 - 34) if R[n] != R[n + 34]]
    print('n with R(n)!=R(n+34):', rexc)
    top = NMAX + 3
    for q in range(1, 35):
        bad = [n for n in range(38, top - q + 1) if R[n] != R[n + q]]
        if q in (1, 2, 17, 34) or not bad:
            print('  period %d on n>=38: %s' % (q, 'holds' if not bad else 'fails, first at n=%d' % bad[0]))
    # proof of R-periodicity on the tail: m=n-3>=52 from g-periodicity, 35<=m<=51 by direct check
    print('direct check [g(m)=0]==[g(m+34)=0] for 35<=m<=51:', all((g[m] == 0) == (g[m + 34] == 0) for m in range(35, 52)))
    print('R(37), R(71):', R[37], R[71], ' g(34), g(68):', g[34], g[68])
    # lemma on large rings: every forced line from a push gives one blocked file with empty neighbours
    allok = True
    for n in list(range(3, 61)) + [100, 150, 200, 250, 300]:
        fs = range(n) if n <= 60 else [0, n // 2, n - 1]
        for f0 in fs:
            for ply, s, bb in lemma_ring(n, f0):
                ok = (ply == 5 and s == 2)
                for f in range(n):
                    if f == f0:
                        ok &= bb[f] == (0, 1, 2)
                    elif f in ((f0 - 1) % n, (f0 + 1) % n):
                        ok &= bb[f] == (0, 0, 0)
                    else:
                        ok &= bb[f] == (1, 0, 2)
                if not ok:
                    allok = False
                    print('  LEMMA FAIL n=%d f0=%d ply=%d' % (n, f0, ply))
    print('raw forced-line lemma (White first; Black by colour symmetry) n=3..60 all files, 100..300 three files:', allok)

main()
