"""Discriminating power of the family test, from the verifier's own brute force outputs."""
import gzip, json, os
from collections import Counter
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
B = ["flat3", "flat4", "cyl3", "cyl4", "cyl5"]
def load(b, r, e, s="pcomp"):
    with gzip.open(os.path.join(OUT, f"bf__{b}__{r}__{e}__{s}.json.gz"), "rt") as fh:
        return json.load(fh)["outcomes"]
tot = Counter()
for e in ("noep", "ep"):
    for r in ("count", "mover", "opponent"):
        for b in B:
            o = load(b, r, e)
            for k, v in o.items():
                tot[(e, "pos")] += 1
                if v in ("L" * 15, "R" * 15):
                    tot[(e, "trivial")] += 1
                else:
                    tot[(e, "nontrivial")] += 1
                    tot[(e, "nontrivial_pairs")] += 15
            tot[(e, "distinct")] += len(set(o.values()))
print({k: v for k, v in sorted(tot.items())})
# sensitivity: rule vs rule, ep vs noep, scope vs scope
for b in B:
    c, m, op = load(b, "count", "noep"), load(b, "mover", "noep"), load(b, "opponent", "noep")
    ce = load(b, "count", "ep")
    cg, cgl = load(b, "count", "ep", "G"), load(b, "count", "ep", "global")
    d = lambda x, y: sum(x[k] != y[k] for k in x)
    print(b, "count!=mover", d(c, m), "count!=opponent", d(c, op), "mover!=opponent", d(m, op),
          "| count ep!=noep", d(c, ce), "| count ep pcomp!=G", d(ce, cg), "pcomp!=global", d(ce, cgl))
