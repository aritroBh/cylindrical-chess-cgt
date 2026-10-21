"""Two-component flat positions (w+b<=5) evaluated as WHOLE-BOARD games (first passer anywhere ends the game;
e.p. right expires after any move), with sumtest's generator (textbook test, count rule, e.p. on) + cylcgt.cgt.
Question: does any of the 53 cylinder-only W-free values occur as such a whole-board value?
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-theory/whole_pairs.py
"""
import itertools, json, sys, time
sys.setrecursionlimit(100000)
from functools import lru_cache
from cylcgt import cgt
from sumtest.sumsolver import Geometry, Rules
sys.path.insert(0, "verify/cylatlas/C3-theory")
from cgtkey import key
from ep_analyze_isbig import isbig

def comps(span, p):
    """oriented flat components with p pawns, span exactly `span`, no initial passer (as square lists)."""
    geo = Geometry(span, False); rules = Rules(geo, ep=True, ep_aware=False)
    sqs = [(f, r) for f in range(span) for r in range(2, 8)]
    out = []
    for w in range(1, p):
        for W in itertools.combinations(sqs, w):
            for B in itertools.combinations([s for s in sqs if s not in W], p - w):
                if len({f for f, _ in W + B}) != span: continue
                Wm = sum(1 << geo.sq(f, r) for f, r in W); Bm = sum(1 << geo.sq(f, r) for f, r in B)
                if rules.has_initial_passer(Wm, Bm): continue
                out.append((W, B))
    return out
C = {2: comps(1, 2) + comps(2, 2), 3: comps(1, 3) + comps(2, 3) + comps(3, 3)}
print("oriented comps:", {k: len(v) for k, v in C.items()}, flush=True)
only = json.load(open("verify/cylatlas/C3-theory/only_atlas.json"))
pairs = [(2, 2), (2, 3), (3, 2)]
geo = Geometry(8, False); rules = Rules(geo, ep=True, ep_aware=False, race_rule="count")
@lru_cache(maxsize=None)
def val(st):
    if st == "L": return cgt.integer(256)
    if st == "R": return cgt.integer(-256)
    W, B, e = st
    kids = {}
    for white in (True, False):
        kids[white] = [val(r if (r := rules.resolve(*c, white)) else c) for c in rules.moves(W, B, e, white)]
    return cgt.make(kids[True], kids[False])
found = {}; vals = set(); cnt = 0; t0 = time.time()
for pa, pb in pairs:
    for (WA, BA) in C[pa]:
        sa = max(f for f, _ in WA + BA) + 1
        for (WB, BB) in C[pb]:
            W = list(WA) + [(f + sa + 1, r) for f, r in WB]
            B = list(BA) + [(f + sa + 1, r) for f, r in BB]
            Wm = sum(1 << geo.sq(f, r) for f, r in W); Bm = sum(1 << geo.sq(f, r) for f, r in B)
            k = key(val((Wm, Bm, -1))); cnt += 1
            vals.add(k)
            if k in only and k not in found:
                found[k] = geo.show(Wm, Bm)
print(f"whole-board 2-component flat positions: {cnt}, distinct values {len(vals)}, W-free {sum(1 for k in vals if not isbig(k))}, {round(time.time()-t0)} s")
print("cylinder-only values hit:", len(found))
for k, p in found.items(): print("  ", cgt.show(__import__('cgtkey').parse(k)), p)
