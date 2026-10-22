import sys, json, itertools, time
sys.path.insert(0, "research/ring_family")
from ringlib import *
from known import KNOWN
from ins_search import SINGLES, insertions

def classes_of(n):
    seen = []; s = set()
    for t in KNOWN[n]:
        r = canon(to_ring(t, n))
        if r not in s: s.add(r); seen.append(r)
    return seen

if __name__ == "__main__":
    start = int(sys.argv[1]); stop = int(sys.argv[2])
    S = {start: classes_of(start)}
    prov = {}
    for n in range(start, stop, 2):
        nxt = {}
        for base in S[n]:
            cands = insertions(base, 2)
            t0 = time.time()
            res = evaluate([c[2] for c in cands], max_entries=1 << 24)
            for (slot, block, ring), r in zip(cands, res):
                if r[0] == "N" and r[1] == 2:
                    c = canon(ring)
                    nxt.setdefault(c, (base, slot, block))
        S[n + 2] = list(nxt.keys())
        prov.update({c: v for c, v in nxt.items()})
        print(f"C{n} ({len(S[n])} classes) -> C{n+2}: {len(nxt)} classes via 2-insertion", flush=True)
    for n in sorted(S):
        print(f"--- C{n}: {len(S[n])}")
        for c in S[n]:
            print("   ", cstr(c), "<-" , (cstr(prov[c][0]) + f" @ {prov[c][1]} + [{cstr(prov[c][2])}]") if c in prov else "(known)")
