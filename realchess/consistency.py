"""Cross-check two pipelines (offline, no network):
  (a) the CGT value of every internal node rebuilt from REAL terminal
      classes (oracle_value, model classes for unexamined terminals), and
  (b) the direct real-chess search results of the node stage.
For a node position with side X to move, (a) predicts "X wins moving first"
iff the CGT game is a first-player win for X; (b) is the searched result.

    PYTHONPATH=. .venv/bin/python -m realchess.consistency
"""
from __future__ import annotations

import json
import os
from collections import Counter

from cylcgt import cgt
from cylcgt.pawns import Pos

from . import component as C
from . import movegen as mg
from .oracle_value import Terminals, classes_under, game_for
from .solve_candidate import Model, RESULTS, tag_of, write_json


def all_values(T, assign):
    memo = {}

    def val(p):
        g = memo.get(p)
        if g is None:
            L = [kid(q, "W") for q in C.options(T.board, p, "W")]
            R = [kid(q, "B") for q in C.options(T.board, p, "B")]
            g = memo[p] = cgt.make(L, R)
        return g

    def kid(q, mover):
        return assign(q) if C.is_terminal(T.board, q) else val(q)
    val(T.comp)
    return memo


def first_player_wins(g, side):
    o = cgt.outcome(g)
    return o == "N" or o == ("L" if side == "W" else "R")


def main(component="W: a2 c2 / B: b7 d7"):
    comp = Pos.parse(component)
    T = Terminals(comp)
    tag = tag_of(comp)
    o = json.load(open(os.path.join(RESULTS, f"{tag}_oracle_pure.json")))
    byname = {str(t): t for t in T.terms}
    raw = {byname[r["terminal"]]: (r["real_W_first"], r["real_B_first"]) for r in o["terminals"]
           if r["how_W"] or r["how_B"]}
    prior = {t: ("L" if C.model_terminal_value(T.board, t, next(iter(T.movers[t])), "count") > 0 else "R")
             for t in T.terms}
    model = Model()
    fens = set()
    for name in (f"{tag}_nodes_pure.json", f"{tag}_roots_pure.json"):
        p = os.path.join(RESULTS, name)
        if os.path.exists(p):
            d = json.load(open(p))
            for r in d.get("nodes", d.get("model_nodes", [])):
                for side in "WB":
                    if r.get(side + "_fen") and r.get(side) and r[side][0] == r[side][1]:
                        fens.add((r[side + "_fen"], r[side][0]))
    out = {"component": component, "positions_compared": len(fens)}
    for d, name in ((-1, "draw=Black win"), (+1, "draw=White win")):
        known = classes_under(raw, d)
        for t, (rw, rb) in raw.items():  # partials: model completion (value-independent, see REPORT)
            if t not in known:
                v = 1 if prior[t] == "L" else -1
                f = lambda x: x if x != 0 else d
                from .oracle_value import class_of
                known[t] = class_of(f(rw if rw is not None else v), f(rb if rb is not None else v))
        vals = all_values(T, lambda t: game_for(known.get(t) or prior[t], True))
        tally, bad = Counter(), []
        for fen, real in sorted(fens):
            pos = mg.parse_fen(fen)
            side = "W" if pos.stm == mg.WHITE else "B"
            p = model.comp(pos)
            g = vals.get(p) or vals.get(Pos(p.white, p.black, None))
            if g is None:
                tally["not in tree"] += 1
                continue
            pred = first_player_wins(g, side)
            if real == 0:
                tally["real draw"] += 1
            elif (real == 1) == pred:
                tally["agree"] += 1
            else:
                tally["DISAGREE"] += 1
                bad.append({"fen": fen, "real_for_stm": real, "cgt_predicts_stm_wins": pred})
        out[name] = {"tally": dict(tally), "disagreements": bad}
    write_json(os.path.join(RESULTS, f"{tag}_consistency.json"), out)
    print(json.dumps({k: (v if not isinstance(v, dict) else v["tally"]) for k, v in out.items()}, indent=1))


if __name__ == "__main__":
    main()
