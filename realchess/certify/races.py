"""Real-chess results of the race entries that decide a candidate's model
value (from tree_stats.py: single-flip-critical and pinning race entries).

A race entry is (terminal T, mover m): m's move produced T, so the OTHER side
is to move in the real position. The embedded 8x8 position (component on
a-d, trebuchet WK f5 Pg4 / BK h4 Pg5) is resolved by the Lichess tablebase
(<= 7 men: the position's own category; 8 men: realchess search with the
tablebase at every capture) and compared with the rules.

    PYTHONPATH=. .venv/bin/python -m realchess.certify.races --tree realchess/certify/results/<tag>_tree.json \
        --cap 1200 --max-new 20
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from cylcgt import pawns
from cylcgt.pawns import Pos

from realchess import component as C
from realchess import movegen as mg
from realchess.search import Searcher

from . import infra


def parse_term(s: str) -> Pos:
    """'W: a3 / B: c4 (ep c3)' -> Pos with the e.p. tuple cylcgt carries:
    (target square, square of the double-stepped pawn, side that may capture)."""
    ep = None
    if "(ep " in s:
        s, e = s.split("(ep ")
        f, r = pawns.sq(e.strip(") "))
        ep = ((f, r), (f, 4), "B") if r == 3 else ((f, r), (f, 5), "W")
    p = Pos.parse(s.strip())
    return Pos(p.white, p.black, ep)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--conv", default=None, help="textbook / ep_aware (default: both)")
    ap.add_argument("--cap", type=int, default=1200)
    ap.add_argument("--max-new", type=int, default=20)
    ap.add_argument("--ext", type=int, default=4)
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    sys.setrecursionlimit(100000)
    d = json.load(open(a.tree))
    from realchess.solve_candidate import RealOracle, OfflineOracle, deepen
    pr = infra.CertProber(a.cap, tag="certify-races", offline=a.offline)
    oracle = OfflineOracle(pr) if a.offline else RealOracle(pr, a.max_new)
    s = Searcher(oracle, cached=pr.cached, kb=infra.kb())
    entries = {}
    for conv, o in d.items():
        if a.conv and conv != a.conv:
            continue
        for e in o["single_flip_critical_race_entries"] + o["pinning_race_set"]:
            k = (e["terminal"], e["entered_by"])
            entries.setdefault(k, {"terminal": e["terminal"], "entered_by": e["entered_by"], "men": e["men"],
                                   "ref_winner": e["ref_winner"], "count_winner": e["count_winner"],
                                   "in": set()})["in"].add(conv)
    rows = []
    for (term, mover), e in sorted(entries.items(), key=lambda kv: (kv[1]["men"], kv[0])):
        t = parse_term(term)
        stm = "B" if mover == "W" else "W"
        pos = C.embed(t, stm)
        errs = mg.validity_errors(pos)
        if errs:
            res = "illegal: " + "; ".join(errs)
        else:
            iv = s.search(pos, 0) if pos.men() <= 7 else deepen(s, pos, a.ext)
            if iv[0] == iv[1]:
                w = iv[0] if pos.stm == mg.WHITE else -iv[0]
                res = {1: "White wins", 0: "draw", -1: "Black wins"}[w]
            else:
                res = "unresolved"
        e = dict(e, conventions=sorted(e.pop("in")), side_to_move=stm, fen=mg.normal_fen(pos), real=res,
                 real_matches_ref=(res == ("White wins" if e["ref_winner"] == "W" else "Black wins")),
                 real_matches_count=(res == ("White wins" if e["count_winner"] == "W" else "Black wins")))
        rows.append(e)
        print(json.dumps(e), flush=True)
    out = {"tree": os.path.basename(a.tree), "entries": rows, "new_requests": oracle.new_requests,
           "ledger_count": pr.ledger_count()}
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(out, fh, indent=1)
    print(json.dumps({"new_requests": oracle.new_requests, "ledger_count": pr.ledger_count()}))


if __name__ == "__main__":
    main()
