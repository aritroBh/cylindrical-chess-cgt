import sys
sys.path.insert(0, "research/ring_family")
from ringlib import *
from known import KNOWN

def reductions(ring, k):
    n = len(ring); out = []
    for s in range(n):
        idx = [(s + j) % n for j in range(k)]
        removed = tuple(ring[i] for i in idx)
        if any(len(a) + len(b) != 1 for a, b in removed):  # single-pawn files only
            continue
        keep = [i for i in range(n) if i not in idx]
        # rotate so ring order is preserved starting after the block
        order = [(s + k + j) % n for j in range(n - k)]
        out.append((s, removed, tuple(ring[i] for i in order)))
    return out

if __name__ == "__main__":
    n = int(sys.argv[1]); ks = [int(x) for x in sys.argv[2:]]
    seen = set(); bases = []
    for t in KNOWN[n]:
        r = canon(to_ring(t, n))
        if r not in seen: seen.add(r); bases.append(r)
    for base in bases:
        line = []
        for k in ks:
            if n - k < 3: continue
            reds = reductions(base, k)
            if not reds: continue
            res = evaluate([r[2] for r in reds])
            for (s, removed, small), r in zip(reds, res):
                if r[0] == "N" and r[1] == 2:
                    line.append(f"k={k} remove[{cstr(removed)}] at {s} -> C{n-k}: {cstr(canon(small))}")
        print(f"C{n} {cstr(base)}:" + ("" if line else " (no *2 reduction)"))
        for l in line: print("     ", l)
