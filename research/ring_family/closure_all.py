"""Closure of *2 rings (n+3 pawns, default setting) under 1- and 2-file insertions of single-pawn files, up to width NMAX."""
import sys, json, time
sys.path.insert(0, "research/ring_family")
from ringlib import *
from closure import classes_of
from ins_search import insertions
NMAX = int(sys.argv[1])
S = {n: set(classes_of(n)) for n in (3, 4, 5, 6)}
# drop the non-*2 entries
for n in S:
    S[n] = {r for r in S[n] if evaluate([r])[0][:2] == ("N", 2)}
prov = {}
for n in range(7, NMAX + 1):
    S[n] = set()
    for k in (1, 2):
        if n - k in S:
            for base in sorted(S[n - k]):
                cands = insertions(base, k)
                res = evaluate([c[2] for c in cands])
                for (slot, block, ring), r in zip(cands, res):
                    if r[0] == "N" and r[1] == 2:
                        c = canon(ring)
                        if c not in S[n]: S[n].add(c); prov[c] = (n - k, cstr(base), slot, cstr(block))
    print(f"C{n}: {len(S[n])} classes ({sum(1 for c in S[n] if prov[c][0]==n-1)} via 1-insertion, {sum(1 for c in S[n] if prov[c][0]==n-2)} via 2-insertion)", flush=True)
json.dump({n: [cstr(r) for r in sorted(L)] for n, L in S.items()}, open("research/ring_family/closure_all.json", "w"), indent=0)
