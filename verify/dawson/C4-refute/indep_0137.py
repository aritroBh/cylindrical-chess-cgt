"""Independent check of claim C4 (adversarial verifier, lens REFUTE).
Does NOT import dawson/ or cylcgt/. Stdlib only.

Three independent formulations of the game tree:
 (A) pin row (Dawson's chess macro-moves): choose pin i of a run of n, remove it and its
     present neighbours; left run max(i-1,0), right run max(n-2-i,0).
 (B) Dawson's Kayles 0.07: remove two adjacent pins from a run of m; then g(n) := h(n+1).
 (C) bitmask brute force of the pin-row game on ALL subsets of a row of length <= L,
     no decomposition assumed (Grundy of whole configuration by mex).
Then: exceptions, least period, Guy-Smith certificate re-derived here (see verdict).
Usage: python indep_0137.py N
"""
import sys
from functools import lru_cache

def mex(s):
    m = 0
    while m in s:
        m += 1
    return m

def pinrow(N):
    g = [0] * (N + 1)
    for n in range(1, N + 1):
        opts = set()
        for i in range(n):
            L = max(i - 1, 0)
            R = max(n - 2 - i, 0)
            opts.add(g[L] ^ g[R])
        g[n] = mex(opts)
    return g

def kayles07(M):
    h = [0] * (M + 1)
    for m in range(2, M + 1):
        h[m] = mex({h[i] ^ h[m - 2 - i] for i in range(m - 1)})
    return h

def bitmask_check(L):
    """Grundy of every subset of a length-L row under the pin-row rule; returns dict mask->G."""
    G = {}
    for mask in range(1 << L):
        # options: choose a present pin i, remove bits i-1,i,i+1 (those present)
        opts = set()
        for i in range(L):
            if mask >> i & 1:
                rm = (1 << i) | ((1 << (i - 1)) if i > 0 else 0) | ((1 << (i + 1)) if i + 1 < L else 0)
                opts.add(G[mask & ~rm])  # smaller mask -> already computed
        G[mask] = mex(opts)
    return G

def runs(mask, L):
    out, c = [], 0
    for i in range(L):
        if mask >> i & 1:
            c += 1
        else:
            if c: out.append(c)
            c = 0
    if c: out.append(c)
    return out

def main(N):
    gA = pinrow(N)
    h = kayles07(N + 1)
    gB = [h[n + 1] for n in range(N + 1)]
    print("A == B (pin row vs 0.07 shifted) for n <=", N, ":", gA == gB)
    L = 16
    G = bitmask_check(L)
    ok_full = all(G[(1 << n) - 1] == gA[n] for n in range(L + 1))
    bad = 0
    for mask in range(1 << L):
        x = 0
        for r in runs(mask, L):
            x ^= gA[r]
        if x != G[mask]:
            bad += 1
    print(f"C: bitmask full rows n<={L} match A: {ok_full}; subsets with G != xor of runs: {bad} of {1<<L}")
    g = gA
    print("g(0..33)  :", " ".join(map(str, g[0:34])))
    print("g(52..85) :", " ".join(map(str, g[52:86])))
    print("max g(n<=300):", max(g[:301]), " max g(n<=N):", max(g))
    print("zeros n<=200:", [n for n in range(201) if g[n] == 0])
    p = 34
    exc = [n for n in range(N - p + 1) if g[n] != g[n + p]]
    print(f"n <= {N-p} with g(n) != g(n+34):", exc)
    # standard ('Winning Ways') exceptional values: differ from the eventual periodic value
    ev = {r: g[1000 + ((r - 1000) % p)] for r in range(p)} if N >= 1100 else None
    if ev:
        std = [n for n in range(200) if g[n] != g[n + 34 * 30]]
        print("standard exceptional values (g(n) != g(n+34*30)), n<200:", std)
    # least period with preperiod tail inside data
    for q in range(1, 35):
        last = max([n for n in range(N - q + 1) if g[n] != g[n + q]], default=-1)
        if last < N - q - 200:  # periodic over at least 200 checked values
            print(f"least eventual period found: {q}, last n with g(n)!=g(n+{q}): {last}")
            break
    for q in range(1, 34):
        hits = [n for n in range(52, N - q + 1) if g[n] != g[n + q]]
        assert hits, q
    print("every q < 34 has a mismatch g(n) != g(n+q) with n >= 52: True")
    n0, k = 52, 3
    hi = 2 * n0 + p + k
    print(f"certificate range n0={n0}<=n<{hi}: all agree: {all(g[n]==g[n+p] for n in range(n0, hi))}; needs g up to n={hi-1+p}")
    # one-off sanity: tighter-than-needed check that n0=51 fails
    print("g(51), g(85):", g[51], g[85])

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3000)
