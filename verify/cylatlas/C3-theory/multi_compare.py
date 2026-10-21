"""Intersections of the cylinder-only W-free sets over the 9 settings (3 race rules x {e.p. on textbook, e.p. on aware, e.p. off}).
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-theory/multi_compare.py"""
import glob, json, os, sys
sys.path.insert(0, "verify/cylatlas/C3-theory")
from cgtkey import parse
from cylcgt import cgt
D = "verify/cylatlas/C3-theory/"
S = {os.path.basename(f)[5:-5]: json.load(open(f)) for f in sorted(glob.glob(D + "multi/only_*.json"))}
atlas = json.load(open(D + "only_atlas.json")); aware = json.load(open(D + "only_aware.json"))
print("sumtest count_ep1_aw0 == atlas 53:", set(S["count_ep1_aw0"]) == set(atlas))
print("sumtest count_ep1_aw1 == cylcgt(ep-aware branch) 54:", set(S["count_ep1_aw1"]) == set(aware))
allk = set.intersection(*(set(v) for v in S.values()))
print("cylinder-only under all 9 settings:", len(allk), [cgt.show(parse(k)) for k in allk])
cnt = set.intersection(*(set(v) for k, v in S.items() if k.startswith("count")))
print("cylinder-only under all 3 count-rule settings:", len(cnt))
a53 = set(atlas)
for k, v in S.items():
    print(f"  {k:16s} size {len(v):4d}   of the atlas's 53 still cylinder-only: {len(a53 & set(v))}")
print("atlas values cylinder-only in every setting:", [cgt.show(parse(k)) for k in a53 & allk])
