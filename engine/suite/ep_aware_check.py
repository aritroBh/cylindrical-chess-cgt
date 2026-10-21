#!/usr/bin/env python3
"""Do the suite's CGT predictions survive the adopted e.p.-aware passed-pawn test?

The suite (results.json, both EPD files) was built with cylcgt's textbook passed test: a pawn that
double-steps past an enemy pawn counts as passed before the e.p. capture. The project has since
adopted the e.p.-aware test (RESULTS.md, "Conventions"). The main checkout's cylcgt still runs the
textbook test, so this script recomputes every prediction with the *independent* move generator and
passer test of sumtest/sumsolver.py (ep_aware=True), and canonical forms from cylcgt.cgt.

For each of the 275 probed positions and each race rule it computes the predicted winning pawn moves
(king moves always lose in the model) and compares them with the stored textbook-test prediction and
with the tablebase.

Run from the project root (offline, a few seconds):
    PYTHONPATH=. .venv/bin/python engine/suite/ep_aware_check.py
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from cylcgt import cgt
from sumtest.sumsolver import Geometry, Rules

HERE = Path(__file__).resolve().parent
BIG = 256
FILES = "abcd"


def make_val(rules):
    @lru_cache(maxsize=None)
    def val(st):
        if st == "L":
            return cgt.integer(BIG)
        if st == "R":
            return cgt.integer(-BIG)
        W, B, e = st
        kids = {}
        for white in (True, False):
            out = []
            for c in rules.moves(W, B, e, white):
                res = rules.resolve(*c, white)
                out.append(val(res if res else c))
            kids[white] = out
        return cgt.make(kids[True], kids[False])
    return val


def uci(geo, before, after):
    frm = before & ~after
    to = after & ~before
    assert bin(frm).count("1") == 1 and bin(to).count("1") == 1
    f, t = frm.bit_length() - 1, to.bit_length() - 1
    return f"{FILES[geo.fileof[f]]}{geo.rankof[f]}{FILES[geo.fileof[t]]}{geo.rankof[t]}"


def predicted_wins(geo, rules, val, component, white_to_move):
    W, B = geo.parse(component)
    wins = set()
    for c in rules.moves(W, B, -1, white_to_move):
        res = rules.resolve(*c, white_to_move)
        g = val(res if res else c)
        o = cgt.outcome(g)
        mover_wins = o in ("L", "P") if white_to_move else o in ("R", "P")
        mine_before, mine_after = (W, c[0]) if white_to_move else (B, c[1])
        if mover_wins:
            wins.add(uci(geo, mine_before, mine_after))
    return wins


def main():
    recs = json.loads((HERE / "results.json").read_text())
    geo = Geometry(4, False)
    in_epd = {}
    for name in ("cgt_verified.epd", "cgt_disagree.epd"):
        for line in open(HERE / name):
            if 'id "' in line:
                in_epd[line.split('id "')[1].split('"')[0]] = name
    print("positions:", len(recs), "| in EPD files:", len(in_epd))
    for rule in ("count", "mover", "opponent"):
        rules = Rules(geo, ep=True, ep_aware=True, race_rule=rule)
        val = make_val(rules)
        changed, tb_pawn_agree_old, tb_pawn_agree_new, epd_changed = [], 0, 0, []
        for r in recs:
            new = predicted_wins(geo, rules, val, r["component"], r["stm"] == "W")
            old = set(r["rules"][rule]["pred_win"])
            kings = set(r["king_moves"])
            tb_pawn = {m for m, v in r["tb_moves"].items() if v == "win" and m not in kings}
            tb_pawn_agree_old += old == tb_pawn
            tb_pawn_agree_new += new == tb_pawn
            if new != old:
                changed.append((r["id"], r["component"], sorted(old), sorted(new), sorted(tb_pawn)))
                if r["id"] in in_epd:
                    epd_changed.append(r["id"])
        print(f"\n[{rule}] predicted winning-pawn-move sets that change under the e.p.-aware test: "
              f"{len(changed)} of {len(recs)} (in the EPD files: {len(epd_changed)})")
        print(f"[{rule}] pawn-move set equals the tablebase's: textbook {tb_pawn_agree_old}/{len(recs)}, "
              f"e.p.-aware {tb_pawn_agree_new}/{len(recs)}")
        for c in changed[:20]:
            print("   ", c[0], c[1], "textbook", c[2], "-> e.p.-aware", c[3], "| tablebase", c[4])


if __name__ == "__main__":
    main()
