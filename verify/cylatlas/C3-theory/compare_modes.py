"""Compare the cylinder-only W-free sets: atlas (textbook) vs own-enumeration textbook control vs e.p.-aware.
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-theory/compare_modes.py
"""
import json, os, sys
sys.path.insert(0, "verify/cylatlas/C3-theory")
from cgtkey import parse
from cylcgt import cgt
D = "verify/cylatlas/C3-theory/"
A = json.load(open(D + "only_atlas.json"))
E = json.load(open(D + "only_aware.json"))
T = json.load(open(D + "only_tb.json")) if os.path.exists(D + "only_tb.json") else None
if T is not None:
    print("own-enumeration textbook control == atlas set:", set(T) == set(A), len(T))
c53 = {r["pos"]: r for r in json.load(open(D + "check53_out.json"))}
kept = [k for k in A if k in E]
print(f"atlas cylinder-only W-free: {len(A)}; e.p.-aware: {len(E)}; same value still cylinder-only: {len(kept)}")
lost = [k for k in A if k not in E]
print("\nLost under e.p.-aware (value no longer cylinder-only):")
flatE = set(json.load(open(D + "flatW_aware.json")))
for k in lost:
    n, pos = A[k]
    r = c53.get(pos)
    why = "now also on a flat strip" if k in flatE else "witness value changed / value no longer on any ring"
    print(f"  {n} {pos:32s} {cgt.show(parse(k)):28s} -> e.p.-aware witness value {r['d_epaware_show'] if r else '?':28s} ({why})")
print("\nNew under e.p.-aware:")
for k in E:
    if k not in A:
        n, pos = E[k]
        print(f"  {n} {pos:32s} {cgt.show(parse(k))}")
# the headline examples
for pos, n in (("W: a2 b4 / B: b7 c6", 3), ("W: a2 b3 / B: a5 c7", 3), ("W: a2 b2 / B: c5 c6", 3), ("W: a2 c2 / B: b7 d7", 4)):
    r = c53[pos]
    print(f"headline {n}-file {pos}: textbook {r['a_show']}, e.p.-aware {r['d_epaware_show']}, e.p.-aware value cylinder-only: {r['d_epaware_key'] in E}")
print("\nunchanged under all six textbook settings:", [(r["pos"], r["a_show"]) for r in c53.values() if r["e_all_same"]])
