#!/usr/bin/env python3
"""pick (group, plain-only king sortie) pairs for the context experiments (stratified, fixed seed)."""
import json, sys, random, collections
sys.path.insert(0, "scripts")
import kit
kit.setboard("cyl:8x6", "0:3")
random.seed(18)
c = json.load(open("logs/search_c8x6_f3_22.Q.json"))
rows = []
for g in c:
    if g["flag"] != "NOESC": continue
    Y = kit.lg2.parse(g["Y"])
    np_ = (g["Y"].count(" P"), g["Y"].count(" p"))
    for m in g["moves"]:
        if m["cls"] != "PLAIN-ONLY" or not m["move"].startswith("K"): continue
        Ym = kit.apply_move(Y, m["move"])
        Q = kit.apply_move(Ym, m["Tplain_r"], confine=True)
        dst = Ym[2]
        rows.append({"Y": g["Y"], "m": m["move"], "r": m["Tplain_r"], "T": m["Tplain"], "Ym": kit.fmt(Ym), "Q": kit.fmt(Q),
                     "leaves": dst[0] not in kit.lg2.FZFILES, "dst": kit.sqn(dst), "pawns": np_, "nmoves": len(g["moves"])})
print(len(rows), "plain-only king sorties in", len({r['Y'] for r in rows}), "groups")
strata = collections.defaultdict(list)
for r in rows:
    tb = 0 if r["T"] <= 4 else 1 if r["T"] <= 6 else 2 if r["T"] <= 8 else 3
    strata[(tb, r["leaves"], r["pawns"])].append(r)
print({k: len(v) for k, v in sorted(strata.items(), key=str)})
sel = []
for k in sorted(strata, key=str):
    v = strata[k]; random.shuffle(v)
    sel += v[:2 if len(v) > 40 else 1]
json.dump(rows, open("logs/sorties_all.json", "w"))
json.dump(sel, open("logs/sorties_selected.json", "w"), indent=0)
print(len(sel), "selected")
for r in sel: print(r["Y"], r["m"], "T=", r["T"], "leaves" if r["leaves"] else "stays", r["pawns"])
