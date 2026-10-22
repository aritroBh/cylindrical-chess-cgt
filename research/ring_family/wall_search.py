"""For a fixed window (list of file contents), search all frozen-language walls w (paths in the 5-gram automaton of the
frozen cyclic words of period <= 7, any first/last symbols) of length 1..LMAX, and list those with window+wall = *2."""
import sys, itertools, json, subprocess
sys.path.insert(0, "research/ring_family")
from ringlib import *
from frozen_walls import SYMS, run
import frozen_walls

def frozen_ngrams(n=5, maxp=7):
    res, words = run(maxp)
    grams = set()
    for w in res:
        p = len(w)
        for i in range(p):
            grams.add(tuple(w[(i + j) % p] for j in range(n)))
    return grams

def walls(grams, L, n=5):
    if L < n:
        yield from itertools.product(range(10), repeat=L); return
    # extend along automaton
    pref = {}
    for g in grams: pref.setdefault(g[:n - 1], []).append(g[-1])
    cur = [tuple(g) for g in grams]
    for _ in range(L - n):
        nxt = []
        for w in cur:
            for c in pref.get(w[-(n - 1):], []): nxt.append(w + (c,))
        cur = nxt
    yield from cur

def evaluate_batch(rings):
    out = []
    B = 4000
    for i in range(0, len(rings), B):
        out += evaluate(rings[i:i + B], max_entries=1 << 21)
    return out

if __name__ == "__main__":
    window = from_cstr(sys.argv[1]); LMAX = int(sys.argv[2]); Lmin = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    grams = frozen_ngrams()
    print("frozen 5-grams:", len(grams), flush=True)
    for L in range(Lmin, LMAX + 1):
        ws = list(walls(grams, L))
        rings = [window + tuple(SYMS[i] for i in w) for w in ws]
        res = evaluate_batch(rings)
        hits = [(w, r) for w, r in zip(ws, res) if r[0] == "N" and r[1] == 2]
        print(f"L={L} (ring width {len(window)+L}, pawns {nparts(window)+L}): {len(ws)} walls, {len(hits)} give *2", flush=True)
        for w, r in hits[:12]:
            print("     wall", " ".join(cstr((SYMS[i],)) for i in w))
