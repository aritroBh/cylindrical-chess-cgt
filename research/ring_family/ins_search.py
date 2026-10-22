import sys, itertools
sys.path.insert(0, "research/ring_family")
from ringlib import *
from known import KNOWN

WR = [((r,), ()) for r in range(2, 7)]
BR = [((), (r,)) for r in range(3, 8)]
SINGLES = WR + BR

def insertions(ring, k):
    """all rings obtained by inserting k single-pawn files at each slot (slot i = before file i)"""
    n = len(ring)
    out = []
    for slot in range(n):
        for block in itertools.product(SINGLES, repeat=k):
            out.append((slot, block, ring[:slot] + tuple(block) + ring[slot:]))
    return out

if __name__ == "__main__":
    n = int(sys.argv[1]); k = int(sys.argv[2])
    seen = set(); bases = []
    for t in KNOWN[n]:
        r = canon(to_ring(t, n))
        if r not in seen: seen.add(r); bases.append(r)
    for base in bases:
        cands = insertions(base, k)
        res = evaluate([c[2] for c in cands])
        hits = [(c, r) for c, r in zip(cands, res) if r[0] == "N" and r[1] == 2]
        print(f"base C{n} {cstr(base)}: {len(cands)} insertions, {len(hits)} are *2")
        classes = {}
        for (slot, block, ring), r in hits:
            classes.setdefault(canon(ring), []).append((slot, cstr(block)))
        for c, lst in classes.items():
            print("    ", cstr(c), "  via", lst[:3])
