#!/usr/bin/env python3
"""module contexts: private tempo reservoirs (a for White = s, b for Black = sbar) on files e and g.  Refined tempo prediction:
sortie punished iff Delta = a - b <= 0, or the finite-budget local game (P variant) is won for budget Delta."""
import json, sys, collections
out = sys.argv[1]; sel = json.load(open(sys.argv[2])); ctx = json.load(open("logs/ctxmod_contexts.json"))
AB = {"W1(e)+B1(g) zero": (1, 1), "B1(e)+W1(g) zero": (1, 1), "W1(e)": (1, 0), "W1(g)": (1, 0), "B1(e)": (0, 1), "B1(g)": (0, 1), "W1(e)+W1(g)": (2, 0), "B1(e)+B1(g)": (0, 2)}
rows = []
for i, s in enumerate(sel):
    rout = None
    for d in (out, out + "b"):
        try:
            r_ = [l.rstrip() for l in open(f"{d}/out_{i}.txt") if " | " in l]
        except OSError: continue
        if len(r_) == 2 * len(ctx): rout = r_; break
    if rout is None: continue
    for j, c in enumerate(ctx):
        a = rout[2 * j].split(" | ")[1].split(); b = rout[2 * j + 1].split(" | ")[1].split()
        A = a[0] if a[0] == a[1] else a[0] + a[1]; B = b[0] if b[0] == b[1] else b[0] + b[1]
        na, nb = AB[c["name"]]; d = na - nb
        pred = True if d <= 0 else (s["kvecP"][d] is not None)
        rows.append({"s": i, "ctx": c["name"], "delta": d, "A": A, "B": B, "pred": pred, "kstar": s["kstar"], "T": s["T"], "leaves": s["leaves"], "kvecP": s["kvecP"][:4]})
json.dump(rows, open(f"{out}/table.json", "w"))
cnt = collections.Counter(); bad = []
for r in rows:
    if r["A"] in ("X", "XX"): cnt[("illegal", r["delta"])] += 1; continue
    got = r["A"] == "L"
    cnt[(r["delta"], "pred punished" if r["pred"] else "pred not punished", "punished" if got else "NOT punished (%s)" % r["A"])] += 1
    if got != r["pred"]: bad.append(r)
for k in sorted(cnt, key=str): print(k, cnt[k])
print("mismatches with the refined prediction:", len(bad))
for r in bad[:40]: print("  ", r["s"], sel[r["s"]]["Y"], sel[r["s"]]["m"], "T", r["T"], "ctx", r["ctx"], "delta", r["delta"], "A", r["A"], "kvecP", r["kvecP"])
