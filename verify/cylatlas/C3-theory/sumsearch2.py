"""sumsearch for either convention, singles from this directory's own runs (tb = textbook, ep = e.p.-aware).
  PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-theory/sumsearch2.py tb|ep
Counts the cylinder-only W-free values X (only_tb.json / only_aware.json) with X = A + B, A and B W-free values of
single flat components (w+b<=5 each) whose spans satisfy spanA + spanB + 1 <= 8 (so A, empty file, B fits on 8 files)."""
import glob, json, re, sys
sys.path.insert(0, "verify/cylatlas/C3-theory")
from cgtkey import parse, key
from cylcgt import cgt
from ep_analyze_isbig import isbig
mode = sys.argv[1]
D = "verify/cylatlas/C3-theory/"
F = {}
for f in glob.glob(D + mode + "/flat*.jsonl"):
    for line in open(f):
        r = json.loads(line)
        if isbig(r["key"]): continue
        p = r["w"] + r["b"]
        if r["key"] not in F or (p, r["n"]) < F[r["key"]][:2]:
            F[r["key"]] = (p, r["n"], r["pos"])
only = json.load(open(D + ("only_tb.json" if mode == "tb" else "only_aware.json")))
hits = 0
for kx, (n, pos) in sorted(only.items(), key=lambda kv: kv[1]):
    X = parse(kx); best = None
    for ka, (pa, sa, posa) in F.items():
        kd = key(cgt.add(X, cgt.neg(parse(ka))))
        if kd in F:
            pb, sb, posb = F[kd]
            if sa + sb + 1 <= 8:
                c = (pa + pb, sa + sb + 1, posa, posb)
                best = c if best is None or c < best else best
    hits += best is not None
    print(n, pos, cgt.show(X), "->", best)
print(f"mode={mode}: {hits} of {len(only)} cylinder-only W-free values are sums of two W-free flat single components")
