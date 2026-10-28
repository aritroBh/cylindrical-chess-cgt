"""Mechanism A with REAL kings (kp_p --pmodel: first promotion wins, kings move).
X: Black to move, in check from the White Z-pawn at (a,r) (locked by pa(r+1)); Black king on b(r+1).
Looks for X with P_real = White wins (so every legal Black move, all Z-moves, is punished: V3 at X) while
D(Black to move) = Black wins in every D model."""
import sys, os, itertools, json
from k17lib import *
from search_A import contexts

def main(spec, files, maxp):
    b = board_of(spec)
    FZ = {0, 1}
    zsq = [f"{'ab'[f]}{r}" for f in (0, 1) for r in range(1, b.ranks + 1)]
    cands = []
    ctxs = [p for p in contexts(b, files, maxp)]
    dres = {p: D_whole(b, p) for p in ctxs}
    ctxs = [p for p in ctxs if dres[p][1] == "L"]
    qs = []; meta = []
    for r in range(2, b.ranks - 1):
        wz = f"a{r}"; bz = f"a{r+1}"; bk = f"b{r+1}"
        for wk in zsq:
            if wk in (wz, bz, bk): continue
            # kings not adjacent
            if abs(ord(wk[0]) - ord(bk[0])) <= 1 and abs(int(wk[1:]) - int(bk[1:])) <= 1: continue
            Z = dict(wk=wk, bk=bk, wz=[wz], bz=[bz], FZ=FZ)
            for p in ctxs:
                qs.append(chess_str(p, "B", Z)); meta.append((p, Z))
    print(spec, "contexts", len(ctxs), "queries", len(qs), flush=True)
    res, err = run_kp(KPP, spec, qs, flags=("--pmodel", "--moves"), heavy=(os.environ.get("HEAVY","1")=="1"))
    print(err.strip())
    hits = []
    for (p, Z), q in zip(meta, qs):
        A, B_, toks = res[q]
        if A == "X": continue
        if A == "W":
            hits.append(dict(pos=q, ctx=str(p), Z=Z, P=A, D="L", moves=toks, DS=D_S(b, p)[0][1], Dfix=D_fix(b, p)[1]))
    print("real-P hits (P=W, D=Black wins):", len(hits))
    json.dump(dict(spec=spec, hits=hits), open(f"../logs/Areal_{spec.replace(':','_')}.json", "w"), indent=0, default=list)
    hits.sort(key=lambda h: (len(h["ctx"]), h["pos"]))
    for h in hits[:10]: print(h["pos"], h["moves"], h["DS"], h["Dfix"])

if __name__ == "__main__":
    main(sys.argv[1], [int(x) for x in sys.argv[2].split(",")], int(sys.argv[3]))
