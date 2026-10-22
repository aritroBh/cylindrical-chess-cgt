"""All *2 rings reachable by 2-insertions from the known C4/C5 rings (classes), then test every 1-insertion of those classes."""
import sys, time, json
sys.path.insert(0, "research/ring_family")
from ringlib import *
from closure import classes_of
from ins_search import SINGLES, insertions

def closure(start, stop):
    S = {start: classes_of(start)}
    for n in range(start, stop, 2):
        nxt = {}
        for base in S[n]:
            cands = insertions(base, 2)
            res = evaluate([c[2] for c in cands])
            for (slot, block, ring), r in zip(cands, res):
                if r[0] == "N" and r[1] == 2:
                    nxt.setdefault(canon(ring), (base, slot, block))
        S[n + 2] = list(nxt.keys())
        print(f"C{n} ({len(S[n])}) -> C{n+2}: {len(nxt)}", flush=True)
    return S

if __name__ == "__main__":
    allr = {}
    for start in (4, 5):
        S = closure(start, 10)
        for n, L in S.items(): allr.setdefault(n, set()).update(L)
    # also the known C3, C6, C7 classes
    for n in (3, 6, 7):
        allr.setdefault(n, set()).update(classes_of(n))
    json.dump({n: [cstr(r) for r in sorted(L)] for n, L in allr.items()}, open("research/ring_family/logs/closure_classes.json", "w"))
    hits = 0
    for n in sorted(allr):
        if n > 9: continue
        tot = 0; found = []
        for base in sorted(allr[n]):
            cands = insertions(base, 1)
            res = evaluate([c[2] for c in cands])
            for (slot, block, ring), r in zip(cands, res):
                if r[0] == "N" and r[1] == 2: found.append((base, slot, block, ring))
            tot += len(cands)
        print(f"1-insertions from C{n}: {len(allr[n])} classes, {tot} candidates, {len(found)} *2", flush=True)
        for base, slot, block, ring in found[:20]:
            print("    ", cstr(base), "+", cstr(block), "@", slot, "->", cstr(canon(ring)))
