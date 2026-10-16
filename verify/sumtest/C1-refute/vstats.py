"""Non-vacuity statistics of the verifier's outcome vectors.
  cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/sumtest/C1-refute/vstats.py
"""
import gzip, json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
B = ["flat3", "flat4", "cyl3", "cyl4", "cyl5"]; R = ["count", "mover", "opponent"]
def load(p):
    with gzip.open(p, "rt") as fh: return json.load(fh)["outcomes"]
allL, allR = "L" * 15, "R" * 15
vecs = Counter(); trivial = 0; total = 0; varying = 0; distinct_cases = 0
ep_changes = 0; rule_changes = 0
for b in B:
    d = {(r, e): load(os.path.join(OUT, f"v__{b}__{r}__{e}__P.json.gz")) for r in R for e in ("ep", "noep")}
    for k in d[("count", "noep")]:
        vs = [d[(r, e)][k] for r in R for e in ("ep", "noep")]
        for v in vs:
            vecs[v] += 1; total += 1
            trivial += v in (allL, allR)
        distinct_cases += len(set(vs))
        varying += len(set(vs)) > 1
        ep_changes += sum(d[(r, "ep")][k] != d[(r, "noep")][k] for r in R)
        rule_changes += sum(len({d[(r, e)][k] for r in R}) > 1 for e in ("ep", "noep"))
print("cases (position,rule,ep):", total)
print("distinct outcome vectors overall:", len(vecs))
print("cases with all-L or all-R vector (decided by BIG-type value):", trivial)
print("positions whose vector varies across the 6 (rule,ep) settings:", varying)
print("sum over positions of #distinct vectors across the 6 settings:", distinct_cases)
print("(position,rule) cases where ep on/off changes the vector:", ep_changes)
print("(position,ep) cases where the race rule changes the vector:", rule_changes)
print("most common vectors:", vecs.most_common(8))
