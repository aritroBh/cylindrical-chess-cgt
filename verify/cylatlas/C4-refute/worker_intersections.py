"""Re-slice the WORKER's own w+b<=4 sensitivity data (parts_sens_all) to compute
intersections of cylinder-only (non-W) value sets over subsets of the six settings.
Reads only JSON files; does not import worker code.
  cd verify/cylatlas/C4-refute && python3 worker_intersections.py
"""
import glob, json, re, itertools
from collections import defaultdict
D = "worker_data/parts_sens_all"
vals = {}
for vf in glob.glob(D + "/*.vals"):
    for line in open(vf):
        d = json.loads(line); vals.setdefault(d["vid"], d)
sets = defaultdict(lambda: defaultdict(set))
wit = defaultdict(dict)
for pf in glob.glob(D + "/*.jsonl"):
    m = re.search(r"(cyl|flat)(\d)_w\db\d_(count|mover|opponent)_ep(\d)_", pf)
    board, n, rule, ep = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    combo = f"{rule}/ep{'on' if ep == '1' else 'off'}"
    for line in open(pf):
        r = json.loads(line)
        sets[combo][board].add(r["vid"])
        if board == "cyl":
            wit[(combo, r["vid"])].setdefault(n, r["pos"])
combos = ["count/epon", "mover/epon", "opponent/epon", "count/epoff", "mover/epoff", "opponent/epoff"]
only = {}
for c in combos:
    only[c] = {v for v in sets[c]["cyl"] - sets[c]["flat"] if not vals[v]["big"]}
    print(c, len(only[c]))
def show(v): return vals[v]["show"]
for sub in [combos[:3], combos[3:], ["count/epon","count/epoff"], ["mover/epon","mover/epoff"], ["opponent/epon","opponent/epoff"], combos]:
    I = set.intersection(*(only[c] for c in sub))
    print("\nINTERSECTION over", sub, "->", len(I))
    for v in sorted(I, key=show):
        print("   ", show(v), {c: wit[(c, v)] for c in sub})
