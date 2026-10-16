"""Independent re-check of claim C2 (verifier scratch; does not import dawson/ or cylcgt/).

1. Grundy values of the pin model of Dawson's chess, written directly from the
   physical description (a run of n untouched files; a push on file i removes i and
   its untouched neighbours inside the run), with no octal-code parsing.
2. The claimed corrected recurrence g(0)=0, g(1)=1, g(n)=mex({g(n-2)} u {g(a)^g(b): a+b=n-3}).
3. The 2025 paper's recurrence G(n)=mex{G(a)^G(b): a+b=n-3, a,b>=0} (empty set for n<3).
4. Counts: agreements G==g on 0..N, ring-prediction mismatches on 3..N.
5. Whether the paper's G is merely a shifted copy of g (G(n)=g(n+s) eventually).

Run:  cd <root> && .venv/bin/python verify/dawson/C2-reproduce/indep.py 300
"""
import sys


def mex(s):
    m = 0
    while m in s:
        m += 1
    return m


def pin_model(N):
    g = [0] * (N + 1)
    for n in range(1, N + 1):
        opts = set()
        for i in range(1, n + 1):          # push on file i of a run 1..n
            left = max(i - 2, 0)           # files 1..i-2 survive
            right = max(n - i - 1, 0)      # files i+2..n survive
            opts.add(g[left] ^ g[right])
        g[n] = mex(opts)
    return g


def claimed_recurrence(N):
    g = [0] * (N + 1)
    if N >= 1:
        g[1] = 1
    for n in range(2, N + 1):
        opts = {g[n - 2]}
        for a in range(0, n - 2):          # a + b = n - 3, a,b >= 0
            opts.add(g[a] ^ g[n - 3 - a])
        g[n] = mex(opts)
    return g


def paper_recurrence(N):
    G = [0] * (N + 1)
    for n in range(N + 1):
        opts = set()
        if n >= 3:
            for a in range(0, n - 2):
                opts.add(G[a] ^ G[n - 3 - a])
        G[n] = mex(opts)
    return G


def main(N):
    g = pin_model(N)
    g2 = claimed_recurrence(N)
    G = paper_recurrence(N)
    print("pin model == claimed recurrence on 0..N:", g == g2)
    print("g(0..40):", g[:41])
    print("G(0..40):", G[:41])
    agree = [n for n in range(N + 1) if g[n] == G[n]]
    print(f"G==g at {len(agree)} of {N+1} values; they are {agree}")
    Rg = {n: int(g[n - 3] == 0) for n in range(3, N + 1)}
    RG = {n: int(G[n - 3] == 0) for n in range(3, N + 1)}
    mism = [n for n in range(3, N + 1) if Rg[n] != RG[n]]
    print(f"ring mismatches on 3..{N}: {len(mism)}; {mism}")
    print("paper predicts ring first-player win (n<=100):", [n for n in range(3, 101) if RG[n]])
    print("correct ring first-player win (n<=100):", [n for n in range(3, 101) if Rg[n]])
    # shift test on the tail
    best = None
    for s in range(-60, 61):
        lo = max(60, -s)
        ok = all(G[n] == g[n + s] for n in range(lo, N + 1) if 0 <= n + s <= N)
        if ok:
            best = s
            print("paper G(n) == g(n+s) for all tested n>=60 with s =", s)
    if best is None:
        print("no shift s in [-60,60] makes G(n)==g(n+s) on n>=60")
    # period of G for info
    for p in range(1, 120):
        last = max([n for n in range(N - p + 1) if G[n] != G[n + p]], default=-1)
        if last < N - 2 * p - 10:
            print(f"paper G looks periodic: period {p}, last exception {last}")
            break


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 300)
