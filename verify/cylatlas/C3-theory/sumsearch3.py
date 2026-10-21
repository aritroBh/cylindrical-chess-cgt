"""Textbook test: X = A + B with A, B ANY W-free flat values of the atlas (w+b<=5 each; A or B may itself be a
two-component sum), minimal flat widths wA + wB + 1 <= 8.  Covers sums of up to 4 flat components on <= 8 files.
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-theory/sumsearch3.py
"""
import json, re, sys
sys.path.insert(0, "verify/cylatlas/C3-theory")
from cgtkey import parse, key
from cylcgt import cgt
idx = {}
for line in open("atlas/cylinder/value_index.jsonl"):
    d = json.loads(line); idx[d["vid"]] = d
def width(pos):
    fs = {"abcdefgh".index(t[0]) for t in re.findall(r"[a-h]\d", pos)}
    return max(fs) - min(fs) + 1
F = {}
for line in open("atlas/cylinder/values.jsonl"):
    r = json.loads(line)
    if r["board"] != "flat" or idx[r["vid"]]["big"]: continue
    k = idx[r["vid"]]["key"]; c = (width(r["pos"]), r["w"] + r["b"], r["pos"])
    if k not in F or c < F[k]: F[k] = c
only = json.load(open("verify/cylatlas/C3-theory/only_atlas.json"))
hits = 0
for kx, (n, pos) in sorted(only.items(), key=lambda kv: kv[1]):
    X = parse(kx); best = None
    for ka, (wa, pa, posa) in F.items():
        kd = key(cgt.add(X, cgt.neg(parse(ka))))
        if kd in F:
            wb, pb, posb = F[kd]
            if wa + wb + 1 <= 8:
                c = (pa + pb, wa + wb + 1, posa, posb)
                best = c if best is None or c < best else best
    hits += best is not None
    print(n, pos, cgt.show(X), "->", best, flush=True)
print(f"{hits} of {len(only)} cylinder-only W-free values are A+B with A, B W-free flat values (<=5 pawns each) fitting on 8 files")
