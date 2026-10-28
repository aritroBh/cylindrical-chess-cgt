#!/usr/bin/env python3
"""classify plain-only king sorties by their finite-pass threshold k* (Q variant) and pick a stratified sample."""
import json, sys, random, collections
sys.path.insert(0, "scripts"); import kit
kit.setboard("cyl:8x6", "0:3")
random.seed(1801)
c = json.load(open("logs/searchk_c8x6_f3_22.Q.json"))
KMAX = 6
rows = []
for g in c:
    if g["flag"] != "NOESC": continue
    Y = kit.lg2.parse(g["Y"]); np_ = (g["Y"].count(" P"), g["Y"].count(" p"))
    for m in g["moves"]:
        if m["cls"] != "PLAIN-ONLY" or not m["move"].startswith("K"): continue
        kv = m["kvec"]                       # T_0..T_6, T_inf  (None = no win)
        fin = [k for k in range(KMAX + 1) if kv[k] is not None]
        kstar = max(fin) if fin else -1
        contiguous = fin == list(range(len(fin)))
        Ym = kit.apply_move(Y, m["move"]); Q = kit.apply_move(Ym, m["Tplain_r"], confine=True)
        rows.append({"Y": g["Y"], "m": m["move"], "r": m["Tplain_r"], "T": m["Tplain"], "kvec": kv, "kstar": kstar, "contig": contiguous,
                     "Ym": kit.fmt(Ym), "Q": kit.fmt(Q), "leaves": Ym[2][0] not in kit.lg2.FZFILES, "dst": kit.sqn(Ym[2]), "pawns": np_})
cnt = collections.Counter((r["kstar"] if r["kstar"] < KMAX else "patient>=6") for r in rows)
print("plain-only king sorties:", len(rows), " by k*:", sorted(cnt.items(), key=str))
print("non-contiguous finite-budget sets:", sum(1 for r in rows if not r["contig"]))
grow = collections.Counter()
for r in rows:
    kv = r["kvec"][:KMAX + 1]
    if all(x is not None for x in kv): grow[tuple(kv[i + 1] - kv[i] for i in range(KMAX))] += 1
print("T_k increments for the patient ones:", grow.most_common(6))
json.dump(rows, open("logs/sorties_k_all.json", "w"))
strata = collections.defaultdict(list)
for r in rows:
    kc = r["kstar"] if r["kstar"] < KMAX else 99
    strata[(kc, r["leaves"])].append(r)
sel = []
for k in sorted(strata):
    v = strata[k]; random.shuffle(v)
    take = 4 if k[0] in (0, 1) else 2 if k[0] < 99 else 4
    sel += v[:take]
json.dump(sel, open("logs/sorties_k_selected.json", "w"))
print(len(sel), "selected"); 
for r in sel: print(r["Y"], r["m"], "T=", r["T"], "kvec=", r["kvec"], "k*=", r["kstar"], "leaves" if r["leaves"] else "stays")
