"""Extension of indep.py to w+b <= 5 (verifier C4-refute): flat single components
(widths 1..5), sums of a 2-pawn and a 2- or 3-pawn component, rings on C3/C4 (<=5 pawns)
and C5 (5 pawns). Same independent engine (imports only indep.py from this folder).
  ../../../.venv/bin/python indep5.py RULE EP OUTFILE
"""
import json, sys, threading, time
sys.path.insert(0, ".")
import indep
from indep import Model, components_enum, vkey, has_big, add, txt, show

def run(rule, ep, outfile):
    t0 = time.time()
    m = Model(rule, ep)
    out = {"flat_single": {}, "flat_pair": {}, "ring": {}}
    by_tot = {2: {}, 3: {}}
    for w in range(1, 6):
        for tot in range(max(2, w), 6):
            for W, B in components_enum(w, False, tot, m):
                g = m.whole(w, False, W, B, None)
                out["flat_single"].setdefault(vkey(g), [txt(W, B), w, has_big(g)])
                if tot in by_tot:
                    by_tot[tot][g.id] = g
        print(f"flat width {w} done {time.time()-t0:.0f}s", flush=True)
    two, three = list(by_tot[2].values()), list(by_tot[3].values())
    for i, a in enumerate(two):
        for b in two[i:] + three:
            g = add(a, b)
            out["flat_pair"].setdefault(vkey(g), [vkey(a), vkey(b), has_big(g)])
    print(f"pairs done {time.time()-t0:.0f}s", flush=True)
    for n, tots in ((3, (3, 4, 5)), (4, (4, 5)), (5, (5,))):
        for tot in tots:
            for W, B in components_enum(n, True, tot, m):
                g = m.whole(n, True, W, B, None)
                out["ring"].setdefault(vkey(g), [f"C{n} " + txt(W, B), n, has_big(g), show(g)])
        print(f"ring C{n} done {time.time()-t0:.0f}s", flush=True)
    json.dump(out, open(outfile, "w"), ensure_ascii=False)
    print(f"wrote {outfile} {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    threading.stack_size(1 << 29)
    th = threading.Thread(target=run, args=(sys.argv[1], sys.argv[2] == "1", sys.argv[3])); th.start(); th.join()
