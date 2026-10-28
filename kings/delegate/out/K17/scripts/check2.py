"""CHECKED-2 driver: verify chosen examples with BOTH kpsolve (kp / kp_p) and the independent refp.py."""
import sys, json
from k17lib import *
import refp

def parse_ctx(txt):
    return Pos.parse(txt)

def full_report(spec, ctx, Z, twin_bk, mode):
    ctx_txt = ctx
    b = board_of(spec); p = parse_ctx(ctx_txt)
    W_, H_ = b.files, b.ranks; wrap = b.wrap
    Zx = dict(Z, FZ=set(Z["FZ"])); Zt = dict(Zx, bk=twin_bk)
    out = dict(spec=spec, ctx=ctx_txt, Z=Z, twin_bk=twin_bk, mode=mode)
    rcB = reach(b, p, "B"); rcW = reach(b, p, "W")
    qX = chess_str(p, "B", Zx)
    qT = sorted(set(all_queries(b, p, "B", Zt, rcB)) | set(all_queries(b, p, "W", Zt, rcW)))
    flags = ("--frozen", "--moves") if mode == "frozen" else ("--pmodel", "--moves")
    binary = KP if mode == "frozen" else KPP
    kpres, _ = run_kp(binary, spec, [qX] + qT, flags=flags)
    rmode = "frozen" if mode == "frozen" else "P"
    rres, nst = refp.solve_many([qX] + qT, W_, H_, wrap, rmode)
    out["refp_states"] = nst
    # raw agreement of result and move lists on every query
    agree = all(kpres[q][0] == rres[q][0] and sorted(kpres[q][2]) == sorted(t.upper() if False else t for t in rres[q][2]) or
                (kpres[q][0] == rres[q][0] and sorted(m[0].upper() + m[1:] for m in kpres[q][2]) == sorted(m[0].upper() + m[1:] for m in rres[q][2]))
                for q in [qX] + qT)
    out["kp_vs_refp_agree_on_all_%d_positions" % (len(qT) + 1)] = bool(agree)
    for name_, res in (("kp", kpres), ("refp", rres)):
        okX, notesX = verify(b, spec, p, "B", Zx, res, rc={(p, "B"): rcB[(p, "B")]}, model="real" if mode != "frozen" else "frozen")
        # NOTE: at X the chess-reachable set is {X} because every legal move of Black is a Z-move (check)
        r = dict(X_P=res[qX][0], X_moves=res[qX][2], X_checks=okX, X_notes=notesX)
        tw = {}
        for s, rc in (("W", rcW), ("B", rcB)):
            ok, notes = verify(b, spec, p, s, Zt, res, rc=rc, model="real" if mode != "frozen" else "frozen")
            tw[s] = dict(ok=ok, P=res[chess_str(p, s, Zt)][0], notes=notes[:3], n_positions=len(rc))
        r["twin"] = tw
        out[name_] = r
    out["D_whole"] = D_whole(b, p); out["D_fix"] = D_fix(b, p); out["D_S"] = D_S(b, p)
    out["V4_X_hss_exact"] = v4_hss_exact(b, p, "B"); out["V4_strong"] = v4_strong(b, p); out["tempo_ok"] = tempo_ok(b, p)
    out["E_violated"] = str(E_violated(b, p, "B")) if E_violated(b, p, "B") else None
    return out

if __name__ == "__main__":
    ex = json.load(open(sys.argv[1]))
    res = [full_report(**e) for e in ex]
    json.dump(res, open(sys.argv[2], "w"), indent=1, default=str)
    for r in res:
        print(r["spec"], r["ctx"], r["mode"], "agree:", [v for k, v in r.items() if k.startswith("kp_vs")][0])
        for nm in ("kp", "refp"):
            print(" ", nm, "X:", r[nm]["X_P"], r[nm]["X_moves"], r[nm]["X_checks"], "| twin:", {s: (t["P"], all(t["ok"].values())) for s, t in r[nm]["twin"].items()})
        print("  D_whole", r["D_whole"], "D_fix", r["D_fix"], "D_S", r["D_S"], "HSS", r["V4_X_hss_exact"], r["V4_strong"], "tempo", r["tempo_ok"])
