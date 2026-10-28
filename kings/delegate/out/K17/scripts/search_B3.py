"""Mechanism B, roots WITH a fresh e.p. right: X = (context, stm s, right owned by s), i.e. the other side has just
double-stepped next to a pawn of s. Compare D_whole (chess), D_fix (root components, rights persist across components)
and o(S) for the side s to move.  (E) is violated at the root whenever the root has >= 2 components, because the root
itself carries a usable right."""
import sys, itertools, json, time
from k17lib import *
from search_A import contexts

def with_rights(b, p):
    """yield (pos_with_ep, s): side s to move owns the right"""
    for s in "WB":
        o = other(s)
        mine = p.white if s == "W" else p.black
        theirs = p.black if s == "W" else p.white
        dest = 4 if o == "W" else b.ranks - 3
        r0 = 2 if o == "W" else b.ranks - 1
        r1 = 3 if o == "W" else b.ranks - 2
        occ = p.white | p.black
        for (f, r) in theirs:
            if r != dest: continue
            if (f, r1) in occ or (f, r0) in occ: continue
            if not any(((g is not None) and ((g, r) in mine)) for g in (b.nb(f, -1), b.nb(f, 1))): continue
            ep = ((f, r1), (f, r), s)
            yield Pos(p.white, p.black, ep), s

def res_of_class(o, s):
    if s == "W": return "W" if o in ("L", "N") else "L"
    return "W" if o in ("L", "P") else "L"

def main(spec, files, maxp, tag, kpmode=None):
    b = board_of(spec)
    t0 = time.time(); n = 0; nroots = 0; nmulti = 0; diffs = []; nhss = 0; nhss_multi = 0
    for p in contexts(b, files, maxp):
        n += 1
        for q, s in with_rights(b, p):
            if C.terminal(b, q) is not None: continue
            nroots += 1
            multi = len(pawns.components(b, q)) >= 2
            nmulti += multi
            dw = "W" if D_whole_win(b, q, s) == "W" else "L"
            comps = tuple(sorted(pawns.components(b, q), key=lambda x: sorted(x.white | x.black)))
            df = "W" if _dfix_(b, comps, s) == "W" else "L"
            rc = reach(b, q, s)
            hss = v4_hss_exact(b, q, s, rc)
            dS = None
            if hss:
                nhss += 1; nhss_multi += multi
                o = cgt.outcome(pawns.value(b, q)); dS = res_of_class(o, s)
            if df != dw or (dS is not None and dS != dw):
                diffs.append(dict(ctx=str(q), stm=s, D_whole=dw, D_fix=df, D_S=dS, hss=hss, multi=multi))
        if n % 20000 == 0: print(n, "t=%.0f" % (time.time() - t0), "roots", nroots, "diffs", len(diffs), flush=True)
    print(spec, files, maxp, "contexts", n, "roots with right", nroots, "multi-component", nmulti, "diffs", len(diffs), "hss roots", nhss, "hss multi-component roots", nhss_multi, "t=%.0f" % (time.time() - t0))
    json.dump(dict(spec=spec, files=files, maxp=maxp, nroots=nroots, nmulti=nmulti, nhss=nhss, nhss_multi=nhss_multi, diffs=diffs), open(f"../logs/B3_{tag}.json", "w"), indent=0)
    print("D_fix != D_whole:", sum(d["D_fix"] != d["D_whole"] for d in diffs),
          " D_S != D_whole (hss):", sum(d["D_S"] is not None and d["D_S"] != d["D_whole"] for d in diffs))
    for d in sorted(diffs, key=lambda d: len(d["ctx"]))[:12]: print(d)

from k17lib import _dfix as _dfix_
if __name__ == "__main__":
    main(sys.argv[1], [int(x) for x in sys.argv[2].split(",")], int(sys.argv[3]), sys.argv[4])
