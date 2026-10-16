"""Matched A-vs-B comparison: same component under an A-trebuchet and a B-trebuchet (same rank),
White to move. King-move results from raw cache only (no worker code, no cylcgt needed).

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/engines/C2-refute/matched.py
"""
import collections, glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import recount as R
sel = json.load(open(os.path.join(R.ROOT, "engine/suite/selection.json"))) + \
    json.load(open(os.path.join(R.ROOT, "engine/suite/selection_ext.json")))
selected = {s["fen"] for s in sel}
by = {}
for p in glob.glob(os.path.join(R.CACHE, "*", "*.json")):
    rec = json.load(open(p))
    if rec["fen"] not in selected:
        continue
    pcs, stm = R.parse(rec["fen"]); lay = R.classify(pcs)
    comp = tuple(sorted((s, q) for s, q in pcs.items() if s[0] <= 3))
    ksq = [s for s, q in pcs.items() if q == ("K" if stm == "w" else "k")][0]
    kn = R.FILES[ksq[0]] + str(ksq[1])
    km = collections.Counter(R.MOVER[m["category"]] for m in rec["data"]["moves"] if m["uci"][:2] == kn)
    by[(comp, stm, lay)] = (km, rec["fen"])
pairs = 0; A = collections.Counter(); B = collections.Counter(); nA = nB = 0
for (comp, stm, lay), (km, fen) in by.items():
    if lay[0] != "A" or stm != "w":
        continue
    other = by.get((comp, stm, ("B", lay[1])))
    if other is None:
        continue
    pairs += 1; A.update(km); B.update(other[0])
    nA += any(k != "loss" for k in km.elements()); nB += any(k != "loss" for k in other[0].elements())
    if any(k != "loss" for k in km.elements()) or any(k != "loss" for k in other[0].elements()):
        print(f"  {fen:38s} A{lay[1]} {dict(km)}   ->   B{lay[1]} {dict(other[0])}")
print(f"matched pairs (same component, same rank, White to move): {pairs}")
print(f"  A king moves {dict(A)}; positions with a non-losing king move {nA}")
print(f"  B king moves {dict(B)}; positions with a non-losing king move {nB}")
