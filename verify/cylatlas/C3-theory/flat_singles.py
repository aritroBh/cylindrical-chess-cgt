"""Collect W-free values of single flat components (w+b<=5) from the atlas, with the simplest witness."""
import json, re
idx = {}
for line in open("atlas/cylinder/value_index.jsonl"):
    d = json.loads(line); idx[d["vid"]] = d
def span(pos):
    fs = {"abcdefgh".index(t[0]) for t in re.findall(r"[a-h]\d", pos)}
    return max(fs) - min(fs) + 1
best = {}
allflat = set()
for line in open("atlas/cylinder/values.jsonl"):
    r = json.loads(line)
    if r["board"] != "flat": continue
    if idx[r["vid"]]["big"]: continue
    allflat.add(r["vid"])
    if r["ncomp"] != 1: continue
    s = (r["w"] + r["b"], span(r["pos"]), r["pos"])
    if r["vid"] not in best or s < best[r["vid"]][0]:
        best[r["vid"]] = (s, r["pos"], r["n"])
print("flat W-free values (all positions):", len(allflat), " of which from single components:", len(best))
json.dump({v: {"pawns": s[0], "span": s[1], "pos": p, "show": idx[v]["show"], "key": idx[v]["key"]} for v, (s, p, n) in best.items()},
          open("verify/cylatlas/C3-theory/flat_singles.json", "w"), indent=0, ensure_ascii=False)
# also W-free value counts per board
cyl = set()
for line in open("atlas/cylinder/values.jsonl"):
    r = json.loads(line)
    if r["board"] == "cyl" and not idx[r["vid"]]["big"]: cyl.add(r["vid"])
print("cyl W-free values:", len(cyl), " cyl-only W-free:", len(cyl - allflat), " flat-only W-free:", len(allflat - cyl))
print("total W-free values in index:", sum(1 for d in idx.values() if not d["big"]))
