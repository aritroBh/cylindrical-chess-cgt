"""Mechanism A: pawn check on a king by a Z-pawn. cyl:6x6 / cyl:7x6 / flat:6x6, F_Z = {a,b}.
Z = locked pair Pa3/pa4 (no legal Z-pawn move), Ka1; X has Black king on b4 (attacked by Pa3), twin has it on b5.
For every context on the context files (ranks 2..5, <=3 pawns per side, no passer at the root):
  twin: V1a(moves), V1b, V2, V3, V4 exact + P_frozen == D for both sides to move
  X   : Black to move in check; D(Black to move) vs kp --frozen.
"""
import sys, os, itertools, json, time
from k17lib import *

def contexts(b, files, maxp=3, ranks=None):
    ranks = ranks or range(2, b.ranks)
    sqs = [(f, r) for f in files for r in ranks]
    for w in range(0, maxp + 1):
        for ws in itertools.combinations(sqs, w):
            rest = [s for s in sqs if s not in ws]
            for bl in range(0, maxp + 1):
                for bs in itertools.combinations(rest, bl):
                    if not ws or not bs: continue
                    pos = Pos(frozenset(ws), frozenset(bs))
                    if C.terminal(b, pos) is not None: continue
                    yield pos

def main(spec, files, maxp):
    b = board_of(spec)
    FZ = {0, 1}
    ZT = dict(wk="a1", bk="b5", wz=["a3"], bz=["a4"], FZ=FZ)   # twin
    ZX = dict(ZT, bk="b4")                                      # X: Black king in check from Pa3
    t0 = time.time()
    ctxs = list(contexts(b, files, maxp))
    print(spec, "contexts", len(ctxs), flush=True)
    dres = {}
    for p in ctxs:
        dres[p] = (D_whole(b, p))
    cand = [p for p in ctxs if dres[p][1] == "L"]       # Black (to move) wins the context in D
    print("D(Black to move)=Black wins:", len(cand), "t", time.time() - t0, flush=True)
    # kp queries for twin of every candidate (both stm) + X (Black to move)
    rcs = {}
    qs = set()
    for p in cand:
        for s in "WB":
            rc = reach(b, p, s); rcs[(p, s)] = rc
            qs.update(all_queries(b, p, s, ZT, rc))
        qs.add(chess_str(p, "B", ZX))
    qs = sorted(qs); print("kp queries", len(qs), flush=True)
    kpres, err = run_kp(KP, spec, qs, heavy=(os.environ.get("HEAVY","1")=="1"))
    print(err.strip(), flush=True)
    rows = []
    for p in cand:
        row = dict(ctx=str(p))
        twin_ok = True
        for s in "WB":
            ok, notes = verify(b, spec, p, s, ZT, kpres, rcs[(p, s)])
            key = chess_str(p, s, ZT)
            Pres = kpres[key][0]
            Dw = dres[p][0 if s == "W" else 1]
            row["twin_" + s] = dict(ok=ok, P=Pres, D=Dw, hss=v4_hss_exact(b, p, s, rcs[(p, s)]), strong=v4_strong(b, p))
            twin_ok &= all(ok.values()) and Pres == Dw and row["twin_" + s]["hss"]
        row["twin_clean"] = bool(twin_ok)
        kx = kpres[chess_str(p, "B", ZX)]
        row["X"] = dict(P=kx[0], D=dres[p][1], moves=kx[2],
                        Dfix=D_fix(b, p)[1], DS=D_S(b, p)[0][1])
        row["X"]["mismatch"] = kx[0] != dres[p][1]
        rows.append(row)
    good = [r for r in rows if r["twin_clean"] and r["X"]["mismatch"]]
    print("twin clean:", sum(r["twin_clean"] for r in rows), " X mismatch among twin clean:", len(good))
    print("X mismatches overall:", sum(r["X"]["mismatch"] for r in rows), "of", len(rows))
    json.dump(dict(spec=spec, files=files, maxp=maxp, n_ctx=len(ctxs), n_cand=len(cand), rows=rows),
              open(f"../logs/A_{spec.replace(':','_')}.json", "w"))
    good.sort(key=lambda r: len(r["ctx"]))
    for r in good[:8]: print(r["ctx"], r["X"])

if __name__ == "__main__":
    spec = sys.argv[1]; files = [int(x) for x in sys.argv[2].split(",")]; maxp = int(sys.argv[3])
    main(spec, files, maxp)
