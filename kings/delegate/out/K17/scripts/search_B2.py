"""Mechanism B, full stage: all contexts (<= maxp pawns per side, ranks 2..H-1, no passer at the root) on the given
context files, roots without an e.p. right (both sides to move). For each root:
   dw = D_whole (chess e.p.), df = D_fix (fixed root components, persistent local rights), dS = o(cylcgt S)
   E  = (E) of L1.6 violated at some chess-reachable position (for the stm in question)
   hss = V4 hereditary sum-safety (exact, alternating reachability) -- needed for S to be meaningful.
Report: counts, and every root with dS != dw or df != dw (in particular with hss True)."""
import sys, itertools, json, time
from k17lib import *
from search_A import contexts

def main(spec, files, maxp, tag):
    b = board_of(spec)
    t0 = time.time(); n = 0; nE = 0; nsplit = 0
    diffs = []
    nhss = 0
    for p in contexts(b, files, maxp):
        n += 1
        e_flags = []
        for s in "WB":
            rc = reach(b, p, s)
            e_flags.append(E_violated(b, p, s, rc) is not None)
        if not any(e_flags):
            continue
        nE += 1
        dw = D_whole(b, p)
        df = D_fix(b, p)
        hss = [v4_hss_exact(b, p, s) for s in "WB"]
        if all(hss):
            nhss += 1
            dS = D_S(b, p)
        else:
            dS = None
        if df != dw or (dS is not None and dS[0] != dw):
            diffs.append(dict(ctx=str(p), D_whole=dw, D_fix=df, D_S=dS[0] if dS else None, E=e_flags, hss=hss,
                              strong=v4_strong(b, p), ncomp=len(pawns.components(b, p))))
        if n % 20000 == 0: print(n, "t=%.0f" % (time.time() - t0), "diffs", len(diffs), "E-violating", nE, flush=True)
    print("(E)-violating roots with hss for both stm:", nhss)
    print(spec, files, maxp, "contexts", n, "(E)-violating roots:", nE, "diffs:", len(diffs), "t=%.0f" % (time.time() - t0), flush=True)
    json.dump(dict(spec=spec, files=files, maxp=maxp, n=n, nE=nE, diffs=diffs), open(f"../logs/B2_{tag}.json", "w"), indent=0)
    print("diffs with D_whole != D_fix:", sum(1 for d in diffs if d["D_fix"] != d["D_whole"]))
    print("diffs with D_S != D_whole:", sum(1 for d in diffs if d["D_S"] is not None and d["D_S"] != d["D_whole"]))
    print("diffs with D_S != D_whole and hss for both stm:", sum(1 for d in diffs if d["D_S"] is not None and d["D_S"] != d["D_whole"] and all(d["hss"])))
    for d in sorted(diffs, key=lambda d: len(d["ctx"]))[:12]: print(d)

if __name__ == "__main__":
    main(sys.argv[1], [int(x) for x in sys.argv[2].split(",")], int(sys.argv[3]), sys.argv[4])
