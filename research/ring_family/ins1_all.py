import sys, json
sys.path.insert(0, "research/ring_family")
from ringlib import *
from closure import classes_of
from ins_search import insertions
from closure1 import closure
allr = {}
for start in (4, 5):
    S = closure(start, 9)
    for n, L in S.items(): allr.setdefault(n, set()).update(L)
for n in (3, 6, 7):
    allr.setdefault(n, set()).update(classes_of(n))
# drop non-*2 (the *3 ring is listed in KNOWN[7])
for n in list(allr):
    keep = set()
    for r in allr[n]:
        res = evaluate([r])[0]
        if res[0] == "N" and res[1] == 2: keep.add(r)
    allr[n] = keep
json.dump({n: [cstr(r) for r in sorted(L)] for n, L in allr.items()}, open("research/ring_family/closure_classes.json", "w"), indent=0)
tot_bases = 0
for n in sorted(allr):
    if n > 9: continue
    found = []; ncand = 0
    for base in sorted(allr[n]):
        cands = insertions(base, 1); ncand += len(cands)
        res = evaluate([c[2] for c in cands])
        for (slot, block, ring), r in zip(cands, res):
            if r[0] == "N" and r[1] == 2: found.append((base, slot, block, ring))
    tot_bases += len(allr[n])
    print(f"1-insertions from C{n}: {len(allr[n])} *2 classes, {ncand} candidates, {len(found)} give *2", flush=True)
    for base, slot, block, ring in found[:10]: print("   ", cstr(base), "+", cstr(block), "@", slot, "->", cstr(canon(ring)))
print("total bases", tot_bases)
