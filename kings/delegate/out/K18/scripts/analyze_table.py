#!/usr/bin/env python3
"""summarise a ctx_exp table: frozen class of G vs kpp (P model) result after the sortie (A) / of the whole position (B)."""
import json, sys, collections
tab = json.load(open(sys.argv[1]))
ctxfn = sys.argv[2] if len(sys.argv) > 2 else None
def fc(f):
    return {("L", "W"): "zero", ("L", "L"): "neg", ("W", "W"): "pos", ("W", "L"): "fuzzy"}.get(tuple(f), str(f))
conf = collections.Counter(); confB = collections.Counter()
for r in tab:
    if r["A"] in ("XX", "X"): conf[(fc(r["frozen"]), "X")] += 1; continue
    conf[(fc(r["frozen"]), r["A"])] += 1
    confB[(fc(r["frozen"]), r["B"])] += 1
print("A = Y.m + G, Black to move (is the sortie punished? L = yes)")
for k in sorted(conf): print("  ", k, conf[k])
print("B = Y + G, White to move (L = Black wins)")
for k in sorted(confB): print("  ", k, confB[k])
# deviations from the tempo-matching prediction
dev = [r for r in tab if r["A"] not in ("XX", "X") and ((r["frozen"][0] == "L") != (r["A"] == "L"))]
print("deviations of A from 'punished iff frozen G is a second-player win for Black':", len(dev))
sub = [r for r in dev if r["frozen"][0] == "L"]
print("  of which G is a second-player win for Black but the sortie is NOT punished:", len(sub))
byr = collections.Counter((fc(r["frozen"]), "reach" if r["dB"] <= r["T"] else "far", "promfree" if r["promfree"] else "race", r["A"]) for r in sub)
for k in sorted(byr): print("    ", k, byr[k])
sup = [r for r in dev if r["frozen"][0] == "W"]
print("  of which G is not a second-player win but the sortie IS punished:", len(sup))
byr = collections.Counter((fc(r["frozen"]), "reach" if r["dB"] <= r["T"] else "far") for r in sup)
for k in sorted(byr): print("    ", k, byr[k])
json.dump({"dev_not_punished": [(r["s"], r["c"]) for r in sub], "dev_punished": [(r["s"], r["c"]) for r in sup]}, open(sys.argv[1].replace("table.json", "dev.json"), "w"))
