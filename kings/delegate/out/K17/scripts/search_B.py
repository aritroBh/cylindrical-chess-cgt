"""Mechanism B: e.p. across components (violation of (E) of L1.6 in notes/lemmas.md).
Pure-Python stage: contexts with >=2 components, D_whole (chess e.p.) vs D_fix (component-local persistent rights) vs D_S (cylcgt).
Z = bare kings on file a (F_Z={a}); buffer b (and the last file on a cylinder); context on c,d,e,f..."""
import sys, itertools, json, time
from k17lib import *
from search_A import contexts

def main(spec, files, maxp):
    b = board_of(spec)
    t0 = time.time(); n = 0; rows = []
    for p in contexts(b, files, maxp):
        comps = pawns.components(b, p)
        if len(comps) < 2: continue
        n += 1
        dw = D_whole(b, p); df = D_fix(b, p)
        if dw != df:
            ds = D_S(b, p)
            rows.append(dict(ctx=str(p), D_whole=dw, D_fix=df, D_S=ds[0], oS=ds[1]))
    print(spec, files, "maxp", maxp, "multi-component contexts", n, "D_whole != D_fix:", len(rows), "t=%.1f" % (time.time() - t0))
    json.dump(dict(spec=spec, files=files, maxp=maxp, n=n, rows=rows), open(f"../logs/B1_{spec.replace(':','_')}_{maxp}.json", "w"), indent=0)
    rows.sort(key=lambda r: (len(r["ctx"]), r["ctx"]))
    for r in rows[:10]: print(r)

if __name__ == "__main__":
    main(sys.argv[1], [int(x) for x in sys.argv[2].split(",")], int(sys.argv[3]))
