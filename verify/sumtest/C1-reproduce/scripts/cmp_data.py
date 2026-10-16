"""Compare freshly recomputed data files with the worker's stored ones (outcomes + info)."""
import gzip, json, os, sys
W = "/Users/aritro/Downloads/Research/Chessendgames/sumtest/data"
F = "/Users/aritro/Downloads/Research/Chessendgames/verify/sumtest/C1-reproduce/pkg/sumtest/data"
names = sorted(n for n in os.listdir(W) if n.endswith(".json.gz"))
assert sorted(n for n in os.listdir(F) if n.endswith(".json.gz")) == names, "file sets differ"
bad = 0
for n in names:
    a = json.load(gzip.open(os.path.join(W, n), "rt")); b = json.load(gzip.open(os.path.join(F, n), "rt"))
    same = a["outcomes"] == b["outcomes"] and a.get("info") == b.get("info")
    ma = {k: v for k, v in a["meta"].items() if k != "seconds"}; mb = {k: v for k, v in b["meta"].items() if k != "seconds"}
    if not same or ma != mb:
        bad += 1; print("DIFF", n, ma, mb)
print(len(names), "files compared;", bad, "differ")
