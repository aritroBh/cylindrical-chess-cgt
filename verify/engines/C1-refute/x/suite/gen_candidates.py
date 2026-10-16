"""Enumerate every queenside component with 2 or 3 pawns on files a-d (4-file flat
8-rank board, e.p. on) that has no passed pawn, plus every e.p.-right variant,
and record the CGT prediction under each promotion-race rule.

Output: engine/suite/candidates.json

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python engine/suite/gen_candidates.py
"""
from __future__ import annotations

import itertools
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cgtpos as C  # noqa: E402
from cylcgt import pawns  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "candidates.json")

WSQ = [(f, r) for f in range(4) for r in range(2, 7)]  # a white pawn on rank 7 is always passed
BSQ = [(f, r) for f in range(4) for r in range(3, 8)]  # a black pawn on rank 2 is always passed


def components_iter():
    for nw, nb in ((1, 1), (2, 1), (1, 2)):
        for ws in itertools.combinations(WSQ, nw):
            for bs in itertools.combinations(BSQ, nb):
                if set(ws) & set(bs):
                    continue
                p = pawns.Pos(frozenset(ws), frozenset(bs))
                if pawns.passed(C.B4, p, "W") or pawns.passed(C.B4, p, "B"):
                    continue
                if len(pawns.components(C.B4, p)) != 1:
                    continue  # >1 component would need a passer somewhere with <=3 pawns
                yield p, "W"
                yield p, "B"
                # e.p. variants: the opponent has just double-stepped next to one of our pawns
                for (f, r) in p.black:  # Black just played f7-f5, White to move
                    if r == 5 and (f, 6) not in p.white | p.black and (f, 7) not in p.white | p.black \
                            and any((g, 5) in p.white for g in (f - 1, f + 1)):
                        yield pawns.Pos(p.white, p.black, ((f, 6), (f, 5), "W")), "W"
                for (f, r) in p.white:  # White just played f2-f4, Black to move
                    if r == 4 and (f, 3) not in p.white | p.black and (f, 2) not in p.white | p.black \
                            and any((g, 4) in p.black for g in (f - 1, f + 1)):
                        yield pawns.Pos(p.white, p.black, ((f, 3), (f, 4), "B")), "B"


def main():
    t0 = time.time()
    rows = []
    for p, stm in components_iter():
        rec = {"pos": str(p), "white": sorted(C.sqn(s) for s in p.white),
               "black": sorted(C.sqn(s) for s in p.black),
               "ep": C.sqn(p.ep[0]) if p.ep else None, "stm": stm, "rules": {}}
        rows.append((p, stm, rec))
    for rule in C.RULES:
        for p, stm, rec in rows:
            a = C.analyse(p, stm, rule)
            rec["rules"][rule] = {
                "value": a["value"], "outcome": a["outcome"], "stm_wins": a["stm_wins"],
                "new_race_nodes": a["new_race_nodes"],
                "moves": [[m["uci"], m["san"], m["kind"], m["value"], m["wins"]] for m in a["moves"]],
            }
    out = [rec for _, _, rec in rows]
    with open(OUT, "w") as fh:
        json.dump(out, fh)
    print(f"{len(out)} component/side-to-move records -> {OUT} in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
