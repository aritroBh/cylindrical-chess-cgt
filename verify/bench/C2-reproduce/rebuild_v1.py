"""Rebuild library v1 (filters 1-5, no filter 5') with the main (textbook) cylcgt,
using the bench code itself with filter 5' disabled (as conventions.positive_control does).
Also report the filter-5' status of every v1 component. Writes v1_positions.txt."""
import sys, json
from cylcgt import pawns
import bench.components as C
print("cylcgt:", pawns.__file__, "has flag:", hasattr(pawns, "PASSED_RESPECTS_EP"))
orig = C.ep_relevant
C.ep_relevant = lambda w, p, at_terminals=False: False if at_terminals else orig(w, p)
v1, st = C.build(verbose=False)
C.ep_relevant = orig
print("v1 stats:", dict(st))
out = sys.argv[1]
with open(out, "w") as fh:
    for r in v1:
        fh.write(f"{r['width']}|{r['position']}\n")
f5 = [r for r in v1 if C.ep_relevant(r["width"], r["_pos"], at_terminals=True)]
print("v1:", len(v1), "filter 5' hits:", len(f5))
cur = [json.loads(x) for x in open(sys.argv[2])]
curset = {(c["width"], c["position"]) for c in cur}
rest = {(r["width"], r["position"]) for r in v1 if r not in f5}
print("v1 minus filter-5' hits == data/components.jsonl positions:", rest == curset, len(rest), len(curset))
# do the stored values in components.jsonl match the v1 rebuild values?
v1map = {(r["width"], r["position"]): (r["value_ascii"], [m["value"] for m in r["moves"]]) for r in v1}
mism = [c["comp_id"] for c in cur if v1map.get((c["width"], c["position"])) != (c["value_ascii"], [m["value"] for m in c["moves"]])]
print("library values/children equal the v1 rebuild values:", not mism, mism[:5])
