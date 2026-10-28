#!/usr/bin/env python3
"""summary of a ctx_exp2 table.  usage: analyze_E.py OUTDIR SORTIES.json [partial]"""
import json, sys, collections, os
out, selfn = sys.argv[1], sys.argv[2]
sel = json.load(open(selfn))
tab = json.load(open(f"{out}/table.json"))
conf = collections.Counter()
for r in tab: conf[(r["cls"], r["A"])] += 1
print("A = Y.m + G, Black to move; L = Black wins (the sortie is punished); X = sortie illegal in presence of G")
for cls in ("zero", "neg", "pos", "fuzzy"):
    print(" ", cls, {a: n for (c, a), n in sorted(conf.items()) if c == cls})
bad = [r for r in tab if r["cls"] in ("zero", "neg") and r["A"] not in ("L", "X")]
print("second-player-win contexts (zero, neg) in which the sortie is NOT punished:", len(bad), "of", sum(n for (c, a), n in conf.items() if c in ("zero", "neg") and a != "X"))
for r in bad[:30]:
    ctx = json.load(open(sys.argv[3] if len(sys.argv) > 3 else "logs/ctx8x6_efg_22_contexts.json"))[r["c"]]
    print("   sortie", r["s"], sel[r["s"]]["Y"], sel[r["s"]]["m"], "T", r["T"], "ctx W", ctx["w"], "B", ctx["b"], r["cls"], "->", r["A"], "dB", r["dB"], "dX", r["dX"], "promfree", r["promfree"])
# prediction of the pos/fuzzy classes: not punished?
for cls in ("pos", "fuzzy"):
    n = [r for r in tab if r["cls"] == cls and r["A"] != "X"]
    print(cls, "contexts:", len(n), "punished anyway:", sum(1 for r in n if r["A"] == "L"))
bys = collections.defaultdict(collections.Counter)
for r in tab:
    if r["cls"] in ("pos", "fuzzy") and r["A"] != "X": bys[r["s"]]["L" if r["A"] == "L" else "notL"] += 1
print("per sortie, pos/fuzzy contexts punished vs not:")
for s in sorted(bys): print("  ", s, sel[s]["kstar"], sel[s]["kvecP"][:4], dict(bys[s]))
