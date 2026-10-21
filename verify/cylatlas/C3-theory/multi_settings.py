"""Cylinder-only W-free values (w+b<=5, union of widths 3..8) under one setting, with the independent sumtest
generator (whole-board trees for single components and rings; two-component flat values by CGT addition).
  PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-theory/multi_settings.py <race> <ep 0|1> <aware 0|1>
Writes verify/cylatlas/C3-theory/multi/only_<race>_ep<ep>_aw<aware>.json"""
import json, os, sys, time
sys.setrecursionlimit(100000)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from functools import lru_cache
from cylcgt import cgt
from sumtest.sumsolver import Geometry, Rules
from enum_own import positions
from cgtkey import key, parse
from ep_analyze_isbig import isbig
race, ep, aware = sys.argv[1], bool(int(sys.argv[2])), bool(int(sys.argv[3]))
t0 = time.time()
def evaluate(n, wrap):
    geo = Geometry(n, wrap); rules = Rules(geo, ep=ep, ep_aware=aware, race_rule=race)
    @lru_cache(maxsize=None)
    def val(st):
        if st == "L": return cgt.integer(256)
        if st == "R": return cgt.integer(-256)
        W, B, e = st
        kids = {}
        for white in (True, False):
            kids[white] = [val(r if (r := rules.resolve(*c, white)) else c) for c in rules.moves(W, B, e, white)]
        return cgt.make(kids[True], kids[False])
    out = []
    for w, b, pos in positions(n, wrap, 5):
        W, B = geo.parse(str(pos))
        out.append((w + b, str(pos), key(val((W, B, -1)))))
    return out
singles = {}
for span in range(1, 6):
    for p, pos, k in evaluate(span, False):
        singles.setdefault(p, {}).setdefault(k, pos)
rings = {}
for n in (3, 4, 5):
    for p, pos, k in evaluate(n, True):
        rings.setdefault(k, (n, pos))
flat = set()
for p in singles: flat |= set(singles[p])
for p1 in singles:
    for p2 in singles:
        if p1 <= p2 and p1 + p2 <= 5:
            for k1 in singles[p1]:
                g1 = parse(k1)
                for k2 in singles[p2]:
                    flat.add(key(cgt.add(g1, parse(k2))))
only = {k: v for k, v in rings.items() if k not in flat and not isbig(k)}
os.makedirs("verify/cylatlas/C3-theory/multi", exist_ok=True)
json.dump(only, open(f"verify/cylatlas/C3-theory/multi/only_{race}_ep{int(ep)}_aw{int(aware)}.json", "w"))
print(race, int(ep), int(aware), "cylinder-only W-free:", len(only), "flat W-free:", sum(1 for k in flat if not isbig(k)), round(time.time() - t0), "s", flush=True)
