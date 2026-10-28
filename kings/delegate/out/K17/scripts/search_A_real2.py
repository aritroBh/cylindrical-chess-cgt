"""Second stage of the real-kings search: for the hits of search_A_real, check X exactly and the twin."""
import sys, os, json
from k17lib import *

def twin_bks(b, Z, r):
    out = []
    for rr in (r + 2, r):
        if 1 <= rr <= b.ranks:
            out.append(f"b{rr}")
    return out

def main(spec):
    b = board_of(spec)
    hits = json.load(open(f"../logs/Areal_{spec.replace(':','_')}.json"))["hits"]
    rows = []
    qs = set(); items = []
    for h in hits:
        p = Pos.parse(h["ctx"]) if False else None
    # rebuild contexts from the position string
    def ctx_of(q):
        toks = q.split()[:-2]
        zw = {"K" + h["Z"]["wk"], "k" + h["Z"]["bk"]} 
        return toks
    for h in hits:
        Z = h["Z"]; r = int(Z["wz"][0][1:])
        toks = h["pos"].split()[:-2]
        w = frozenset(sq(t[1:]) for t in toks if t[0] == "P" and t[1:] not in Z["wz"])
        bl = frozenset(sq(t[1:]) for t in toks if t[0] == "p" and t[1:] not in Z["bz"])
        p = Pos(w, bl)
        Z = dict(Z, FZ=set(Z["FZ"]))
        h["_p"] = p; h["_Z"] = Z
        tw = []
        for bk in twin_bks(b, Z, r):
            ZT = dict(Z, bk=bk); tw.append(ZT)
        h["_tw"] = tw
        for ZT in tw:
            for s in "WB":
                qs.update(all_queries(b, p, s, ZT))
        qs.add(chess_str(p, "B", Z))
    qs = sorted(qs); print("twin queries", len(qs), flush=True)
    res, err = run_kp(KPP, spec, qs, flags=("--pmodel", "--moves"), heavy=(os.environ.get("HEAVY","1")=="1"))
    print(err.strip())
    out = []
    for h in hits:
        p, Z = h["_p"], h["_Z"]
        okX, notesX = verify(b, spec, p, "B", Z, res, rc={(p, "B"): reach(b, p, "B")[(p, "B")]}, model="real")
        # X: chess-reachable set is {X} only (all legal moves are Z-moves)
        row = dict(pos=h["pos"], X_V3=okX["V3"], X_V1b=okX["V1b"], X_V1a_moves=okX["V1a_moves"], X_V2=okX["V2"],
                   hss=v4_hss_exact(b, p, "B"), strong=v4_strong(b, p), tempo=tempo_ok(b, p),
                   D_whole=D_whole(b, p), D_fix=D_fix(b, p), D_S=D_S(b, p)[0], P=res[chess_str(p, "B", Z)][:2])
        row["twin"] = []
        for ZT in h["_tw"]:
            t = {}
            legal = res[chess_str(p, "B", ZT)][0] != "X" and res[chess_str(p, "W", ZT)][0] != "X"
            t["bk"] = ZT["bk"]; t["legal"] = legal
            if legal:
                good = True
                for s in "WB":
                    ok, notes = verify(b, spec, p, s, ZT, res, model="real")
                    Pr = res[chess_str(p, s, ZT)][0]; Dw = D_whole(b, p)[0 if s == "W" else 1]
                    t[s] = dict(ok=ok, P=Pr, D=Dw)
                    good &= all(ok.values()) and Pr == Dw
                t["clean"] = good
            row["twin"].append(t)
        out.append(row)
    nX = sum(1 for r in out if r["X_V3"] and r["X_V1b"] and r["hss"] and r["tempo"] and not r["X_V1a_moves"])
    ntw = sum(1 for r in out if any(t.get("clean") for t in r["twin"]))
    print("hits", len(out), "X with V1b,V3,V4 holding and V1a failing:", nX, " with a real-P-clean twin:", ntw)
    json.dump(out, open(f"../logs/Areal2_{spec.replace(':','_')}.json", "w"), indent=0, default=list)
    for r in out:
        if any(t.get("clean") for t in r["twin"]): print("CLEAN TWIN", r["pos"]); break
    for r in out[:3]: print(r)

if __name__ == "__main__":
    main(sys.argv[1])
