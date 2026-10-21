import json, sys
from collections import Counter
D = "/Users/aritro/Downloads/Research/Chessendgames/verify/bench/C3-reproduce"
meta = json.load(open(f"{D}/jobs_all.meta.json"))
def load(b):
    out = []
    import glob
    for c in "abcd":
        out += [tuple(l.split()) for l in open(f"{D}/out_{b}_chunk_{c}.txt").read().splitlines()]
    if b != "ab_mine":
        pre = "restd_" if b == "abx1" else "restd0_"
        for f in sorted(glob.glob(f"{D}/out_{b}_{pre}?.txt")):
            out += [tuple(l.split()) for l in open(f).read().splitlines()]
    return out
A = {b: load(b) for b in ("ab_mine", "abx0", "abx1")}
n = len(meta)
for b, v in A.items():
    print(b, len(v), "of", n)
assert all(len(v) == n for v in A.values())
c = Counter()
capped_rows = set()
res = {}
for i, (rid, side, oc, k) in enumerate(meta):
    a, x0, x1 = A["ab_mine"][i], A["abx0"][i], A["abx1"][i]
    c["ab ep_events>0"] += int(a[3]) > 0
    c["abx1 ep_events>0"] += int(x1[3]) > 0
    for nm, x in (("abx0", x0), ("abx1", x1)):
        if a[0] == "0" or x[0] == "0":
            c[f"{nm} capped (either)"] += 1
            continue
        c[f"{nm} result same"] += a[0] == x[0]
        c[f"{nm} nodes same"] += a[1] == x[1]
        c[f"{nm} compared"] += 1
    if a[0] == "0":
        capped_rows.add(rid)
    res.setdefault(rid, {})[side] = (int(a[0]), oc, k)
agree = Counter()
for rid, d in res.items():
    vw, oc, k = d[1]; vb = d[0][0]
    if vw == 0 or vb == 0:
        agree["capped"] += 1; continue
    a, cc = vw == 1, vb == 1
    o = "L" if a and not cc else "R" if cc and not a else "N" if a else "P"
    agree["agree" if o == oc else "DISAGREE"] += 1
print(dict(c)); print(dict(agree)); print("capped rows:", sorted(capped_rows))
