"""Which promotion-race rule matches real chess? (offline; uses cached probes only)

Every probed root lists the tablebase result of every legal move. When a pawn
move creates a position in which BOTH sides have a passed pawn (a "race node",
where cylcgt applies RACE_RULE), the tablebase result of that move is ground
truth for the race. We compare it with the three rules.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python engine/suite/race_nodes.py
"""
from __future__ import annotations

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_suite as BS  # noqa: E402
import cgtpos as C  # noqa: E402
import tb  # noqa: E402
from cylcgt import pawns  # noqa: E402


def main():
    sel = BS.all_selected()
    cands = {(r["pos"], r["stm"]): r for r in json.load(open(BS.CANDS))}
    rows, seen = [], set()
    for c in sel:
        rec = tb.lookup(c["fen"], allow_network=False)
        if rec is None or rec.get("status") != 200:
            continue
        s = tb.summarize(rec)
        comp = BS.rec_pos(cands[(c["component"], c["stm"])])
        mover = c["stm"]
        other = "B" if mover == "W" else "W"
        for uci, san, kind, child in C.labeled_moves(C.B4, comp, mover):
            if not (pawns.passed(C.B4, child, "W") and pawns.passed(C.B4, child, "B")):
                continue
            key = (c["fen"], uci)
            if key in seen:
                continue
            seen.add(key)
            res = s["moves"][uci][1]
            truth = "win" if res in BS.WINS else "loss" if res in BS.LOSSES else res
            dm = pawns.promote_distance(C.B4, child, mover)
            do = pawns.promote_distance(C.B4, child, other)
            pred = {"mover": "win", "opponent": "loss",
                    "count": "loss" if do <= dm else "win"}
            rows.append({"fen": c["fen"], "treb": c["treb"], "move": san, "mover": mover,
                         "child": str(child), "d_mover": dm, "d_opp": do, "tb": truth, "pred": pred})
    print(f"{len(rows)} distinct race nodes at depth 1 (tablebase result known)")
    tally = collections.Counter(r["tb"] for r in rows)
    print("tablebase result for the mover:", dict(tally))
    for rule in C.RULES:
        ok = sum(r["pred"][rule] == r["tb"] for r in rows)
        print(f"  rule {rule:9s}: correct {ok}/{len(rows)}")
    print("\nby (mover distance - opponent distance):")
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        by[r["d_mover"] - r["d_opp"]][r["tb"]] += 1
    for k in sorted(by):
        print(f"  d_mover - d_opp = {k:+d}: {dict(by[k])}")
    print("\nby trebuchet:")
    byt = collections.defaultdict(collections.Counter)
    for r in rows:
        byt[r["treb"]][(r["tb"], r["pred"]["count"] == r["tb"])] += 1
    for k in sorted(byt):
        print(f"  {k}: {dict(byt[k])}")
    json.dump(rows, open(os.path.join(HERE, "race_nodes.json"), "w"), indent=1)
    print("\nmisses of the count rule:")
    for r in rows:
        if r["pred"]["count"] != r["tb"]:
            print(f"  {r['fen']}  {r['move']:6s} -> {r['child']:28s} d_mover={r['d_mover']} "
                  f"d_opp={r['d_opp']} tb={r['tb']}")


if __name__ == "__main__":
    main()
