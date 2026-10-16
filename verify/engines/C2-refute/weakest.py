"""Is the king assumption the model's weakest point?  Compare per-move error rates of
king moves (model: always lose) with pawn moves (model: CGT(count)), by group.
No worker code imported.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/engines/C2-refute/weakest.py
"""
import collections, glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import recount as R, taxonomy as T
from cylcgt import cgt, pawns
sel = json.load(open(os.path.join(R.ROOT, "engine/suite/selection.json"))) + \
    json.load(open(os.path.join(R.ROOT, "engine/suite/selection_ext.json")))
selected = {s["fen"] for s in sel}
stats = collections.defaultdict(collections.Counter)
posstats = collections.defaultdict(collections.Counter)
for p in glob.glob(os.path.join(R.CACHE, "*", "*.json")):
    rec = json.load(open(p))
    if rec["fen"] not in selected:
        continue
    pcs, stm = R.parse(rec["fen"]); lay = R.classify(pcs); S = stm.upper()
    w = frozenset(s for s, q in pcs.items() if q == "P" and s[0] <= 3)
    b = frozenset(s for s, q in pcs.items() if q == "p" and s[0] <= 3)
    pos = pawns.Pos(w, b, None)
    ksq = [s for s, q in pcs.items() if q == ("K" if stm == "w" else "k")][0]
    kn = R.FILES[ksq[0]] + str(ksq[1])
    res = {m["uci"]: R.MOVER[m["category"]] for m in rec["data"]["moves"]}
    preds = {}
    for rule in ("count", "mover", "opponent"):
        pawns.RACE_RULE = rule; pawns._value.cache_clear()
        preds[rule] = {u: ("win" if (cgt.le(R.ZERO, v) if S == "W" else cgt.le(v, R.ZERO)) else "loss")
                       for u in res if u[:2] != kn
                       for v in [R.child_value(T.child_of(pos, u, S), S, rule)]}
    pawns.RACE_RULE = "count"; pawns._value.cache_clear()
    v = pawns.value(R.B4, pos); tame = not R.has_big(v)
    rs = len({tuple(sorted(d.items())) for d in preds.values()}) > 1
    g = ("tame" if tame else "BIG") + ("/race-sens" if rs else "") + "/" + lay[0]
    kerr = perr = 0
    for u, x in res.items():
        if u[:2] == kn:
            stats[g]["king"] += 1; stats[g]["king_wrong"] += x != "loss"; kerr += x != "loss"
        else:
            stats[g]["pawn"] += 1; stats[g]["pawn_wrong"] += x != preds["count"][u]; perr += x != preds["count"][u]
    posstats[g]["n"] += 1
    posstats[g]["only_king_errors"] += kerr > 0 and perr == 0
    posstats[g]["only_pawn_errors"] += perr > 0 and kerr == 0
    posstats[g]["both"] += kerr > 0 and perr > 0
    posstats[g]["exact"] += kerr == 0 and perr == 0
tot = collections.Counter(); ptot = collections.Counter()
for g in sorted(stats):
    s = stats[g]; tot.update(s); ptot.update(posstats[g])
    print(f"{g:22s} king moves wrong {s['king_wrong']:3d}/{s['king']:3d} ({100*s['king_wrong']/s['king']:4.1f}%)  "
          f"pawn moves wrong {s['pawn_wrong']:3d}/{s['pawn']:3d} ({100*s['pawn_wrong']/max(1,s['pawn']):4.1f}%)  positions {dict(posstats[g])}")
print(f"{'TOTAL':22s} king moves wrong {tot['king_wrong']}/{tot['king']}  pawn moves wrong {tot['pawn_wrong']}/{tot['pawn']}  positions {dict(ptot)}")
