"""Independent recomputation of the disagreement taxonomy behind claim C2.

No worker code imported. Uses recount.py's structural classification
(re-implemented helpers imported from this directory), the project's cylcgt
(read-only) for the CGT(count) winning pawn moves, and the raw Lichess cache.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/engines/C2-refute/taxonomy.py
"""
import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import recount as R  # noqa: E402  (this verifier's own helpers)
from cylcgt import cgt, pawns  # noqa: E402

FILES = "abcdefgh"


def sqi(n):
    return (FILES.index(n[0]), int(n[1]))


def child_of(pos, uci, side):
    """Apply a pawn move (uci) to a component Pos; mirror pawns.moves' e.p. bookkeeping."""
    fr, to = sqi(uci[:2]), sqi(uci[2:4])
    mine, theirs = (set(pos.white), set(pos.black)) if side == "W" else (set(pos.black), set(pos.white))
    assert fr in mine
    mine.discard(fr)
    mine.add(to)
    theirs.discard(to)
    ep = None
    if abs(to[1] - fr[1]) == 2:
        other = "B" if side == "W" else "W"
        ep = ((fr[0], (fr[1] + to[1]) // 2), to, other)
    w, b = (mine, theirs) if side == "W" else (theirs, mine)
    return pawns.Pos(frozenset(w), frozenset(b), ep)


def main():
    sel = json.load(open(os.path.join(R.ROOT, "engine", "suite", "selection.json"))) + \
        json.load(open(os.path.join(R.ROOT, "engine", "suite", "selection_ext.json")))
    selected = {s["fen"].split(" 0 1")[0] for s in sel}
    recs = [json.load(open(p)) for p in glob.glob(os.path.join(R.CACHE, "*", "*.json"))]
    rows = []
    for rec in recs:
        pcs, stm = R.parse(rec["fen"])
        lay = R.classify(pcs)
        if lay is None:
            continue
        in_sel = rec["fen"].split(" 0 1")[0] in selected
        S = stm.upper()
        d = rec["data"]
        w = frozenset(s for s, p in pcs.items() if p == "P" and s[0] <= 3)
        b = frozenset(s for s, p in pcs.items() if p == "p" and s[0] <= 3)
        pos = pawns.Pos(w, b, None)
        ksq = [s for s, p in pcs.items() if p == ("K" if stm == "w" else "k")][0]
        kname = FILES[ksq[0]] + str(ksq[1])
        res = {m["uci"]: R.MOVER[m["category"]] for m in d["moves"]}
        kmoves = {u for u in res if u[:2] == kname}
        pmoves = set(res) - kmoves
        kids = {u: child_of(pos, u, S) for u in pmoves}
        assert set(kids.values()) == set(pawns.moves(R.B4, pos, S)), rec["fen"]
        pred = {}
        for rule in ("count", "mover", "opponent"):
            pawns.RACE_RULE = rule
            pawns._value.cache_clear()
            pw = set()
            for u, ch in kids.items():
                v = R.child_value(ch, S, rule)
                if (cgt.le(R.ZERO, v) if S == "W" else cgt.le(v, R.ZERO)):
                    pw.add(u)
            pred[rule] = pw
        pawns.RACE_RULE = "count"
        pawns._value.cache_clear()
        v = pawns.value(R.B4, pos)
        tame = not R.has_big(v)
        rs = len({tuple(sorted(p)) for p in pred.values()}) > 1
        tbw = {u for u, x in res.items() if x in ("win", "cursed-win")}
        tbd = {u for u, x in res.items() if x == "draw"}
        rows.append(dict(fen=rec["fen"], lay=lay, stm=stm, in_sel=in_sel, tame=tame, rs=rs,
                         pred=pred["count"], tbw=tbw, tbd=tbd, kmoves=kmoves, pmoves=pmoves,
                         root=d["category"]))
    rows = [r for r in rows if r["in_sel"]]
    print("positions in the worker's 275-selection found in the cache:", len(rows))
    # disagreement set, as described in engine/suite/README.md
    dis = [r for r in rows if not (r["root"] == "win" and r["pred"] == r["tbw"])
           and (r["tbw"] or r["tbd"]) and not (r["pred"] == r["tbw"] and r["root"] == "loss")]
    print("disagreement positions:", len(dis), collections.Counter(r["root"] for r in dis))
    dropped = [r for r in rows if r["root"] == "loss" and r["pred"]]
    print("TB-loss roots where CGT(count) predicts a win (excluded from both EPD files):", len(dropped))
    for r in dropped:
        print("   ", r["fen"], "pred", sorted(r["pred"]))

    def cat(r):
        c = set()
        pred_root = "win" if r["pred"] else "loss"
        if pred_root != r["root"]:
            c.add("root")
        if r["pred"] - r["tbw"]:
            c.add("pred-pawn-not-win")
        if (r["tbw"] - r["pred"]) & r["pmoves"]:
            c.add("extra-pawn-win")
        if (r["tbw"] - r["pred"]) & r["kmoves"]:
            c.add("extra-king-win")
        return frozenset(c)

    cc = collections.Counter(cat(r) for r in dis)
    for k, n in cc.most_common():
        print(f"   {n:3d}  {sorted(k)}")
    only_king = [r for r in dis if cat(r) == {"extra-king-win"}]
    print("ONLY extra TB-winning king moves (root agrees, pawn win set agrees):", len(only_king))
    ok_with_kdraws = sum(bool(r["tbd"] & r["kmoves"]) for r in only_king)
    ok_with_pdraws = sum(bool(r["tbd"] & r["pmoves"]) for r in only_king)
    print("   of which also have drawing king moves:", ok_with_kdraws, "; drawing pawn moves:", ok_with_pdraws)
    print("   by group:", collections.Counter(("tame" if r["tame"] else "BIG") + ("/race-sens" if r["rs"] else "")
                                             + "/" + r["lay"][0] for r in only_king))
    any_root = sum("root" in cat(r) for r in dis)
    print("root differs:", any_root, "; pred pawn not win:", sum("pred-pawn-not-win" in cat(r) for r in dis),
          "; extra pawn win:", sum("extra-pawn-win" in cat(r) for r in dis),
          "; extra king win (any):", sum("extra-king-win" in cat(r) for r in dis))
    # how many of the 52 involve the king assumption at all (some king move does not lose)
    kfail = [r for r in dis if (r["tbw"] | r["tbd"]) & r["kmoves"]]
    print("disagreements with at least one non-losing king move:", len(kfail))
    kfail_only = [r for r in kfail if not (r["pred"] - r["tbw"]) and not ((r["tbw"] - r["pred"]) & r["pmoves"])
                  and not (r["tbd"] & r["pmoves"])]
    print("   ...whose pawn moves are all predicted exactly (win/loss, no pawn draws):", len(kfail_only))
    print("race-sensitive among the disagreements:", sum(r["rs"] for r in dis))
    # whole-sample: positions where the ONLY model error is on king moves
    allbad = [r for r in rows if (r["tbw"] | r["tbd"]) & r["kmoves"]]
    print("all 275: positions with a non-losing king move:", len(allbad))


if __name__ == "__main__":
    main()
