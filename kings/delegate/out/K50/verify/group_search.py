"""K50 referee: random king groups whose bare data make the (V2) Proposition 2.11 route possible for some
beneficiary beta: (H2) at beta's king, (H3) at omega's king, omega has no Z-pawn move, and every omega king move has a
strict local certificate. Also records groups with every Z-move of one side strictly certified (V3 route).
Run from the project root: python3 .../group_search.py <board> <fzfiles> <ctxpair> <n> <seed>"""
import json
import os
import random
import sys

sys.path.insert(0, os.getcwd())
from kings.embed_check import Board, Checker, FILES  # noqa: E402

bd, fzs, ctxpair, n, seed = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
kind, size = bd.split(":")
W, H = map(int, size.split("x"))
B = Board(W, H, kind == "cyl")
fzf = [FILES.index(c) for c in fzs]
rnd = random.Random(seed)
ch = Checker(B, 6, 300000, False, 20)
seen = set()
for it in range(n):
    sqs = [(f, r) for f in fzf for r in range(1, H + 1)]
    wk, bk = rnd.sample(sqs, 2)
    if B.kdist(wk, bk) <= 1:
        continue
    occ = {wk, bk}
    wp, bp = [], []
    for _ in range(rnd.randint(0, 4)):
        s = (rnd.choice(fzf), rnd.randint(2, H - 1))
        if s in occ:
            continue
        occ.add(s)
        (wp if rnd.random() < 0.5 else bp).append(s)
    grp = " ".join([f"K{FILES[wk[0]]}{wk[1]}"] + [f"P{FILES[p[0]]}{p[1]}" for p in wp] + [f"k{FILES[bk[0]]}{bk[1]}"]
                   + [f"p{FILES[p[0]]}{p[1]}" for p in bp])
    if grp in seen:
        continue
    seen.add(grp)
    for stm in "wb":
        txt = f"{grp} {ctxpair} {stm} -"
        try:
            r = ch.run(txt, fzs and ",".join(fzs))
        except Exception as e:  # noqa: BLE001
            print(json.dumps({"grp": grp, "err": repr(e)}))
            continue
        if r["separation"]["verdict"] != "PASS" or "sorties" not in json.dumps(r["V3"]):
            continue
        st = {}
        for beta in ("W", "B"):
            omega_white = beta == "B"
            kb, kw = (ch.wk, ch.bk) if beta == "W" else (ch.bk, ch.wk)
            zall = ch.zw | ch.zb
            h2 = not any(p[0] in {B.nb(kb[0], -1), B.nb(kb[0], 1)} for p in zall)
            rows = ch.sortie_T[omega_white]
            zp = any(rw["move"][0] in "Pp" for rw in rows)
            kT = [0 if rw.get("T") == 0 else rw.get("T_strict") for rw in rows if rw["move"][0] in "Kk"]
            st[beta] = h2 and not zp and kT and all(t is not None for t in kT)
        v3 = {s: r["V3"][s]["verdict"] for s in ("white", "black")}
        if st["W"] or st["B"] or "CERTIFIED" in v3.values():
            print(json.dumps({"grp": grp, "stm": stm, "v2route": st, "V3": v3, "verdict": r["verdict"],
                              "V2": r["V2"]["passer_and_race_terminals"]["verdict"]}), flush=True)
