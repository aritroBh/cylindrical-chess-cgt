"""Which terminal sides must be known for the real-chess oracle value to be
PINNED (G_lo == G_hi) at the value it takes when every unknown side is
filled by the model (one-sided terminal: the passer's owner wins; race: the
--race-rule verdict)?

Chunked greedy: free the filled terminals (most men first) while the
monotone sandwich of the treatment still pins the same value. The terminals
left are those the pinned value rests on; their filled sides are an
ASSUMPTION until resolved in real chess.

    PYTHONPATH=. .venv/bin/python -m realchess.certify.pinneed --component "W: a3 b2 c2 / B: a4 b6 c5" \
        --treatment "switch, draw = White win" --out ...
"""
from __future__ import annotations

import argparse
import json
from collections import Counter

from cylcgt import cgt
from cylcgt.pawns import Pos

from realchess import component as C
from realchess.oracle_value import TREATMENTS, Terminals, sandwich

from . import termdb
from .iterate import chunked_greedy
from .oracle10 import owner, passed_test, side_fens


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", required=True)
    ap.add_argument("--treatment", required=True, choices=list(TREATMENTS))
    ap.add_argument("--race-rule", default="count")
    ap.add_argument("--no-l8-rows", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    comp = Pos.parse(a.component)
    T = Terminals(comp)
    db = termdb.load()
    if a.no_l8_rows:
        db = {k: v for k, v in db.items() if not v.get("l8")}
    kind, d = TREATMENTS[a.treatment]
    open_raw, base = {}, {}
    filled = []
    for t in T.terms:
        f = side_fens(T, t)
        o = owner(T, t)
        vo, vb = [], []
        for s in "WB":
            r = db.get(f[s])
            if r is not None:
                vo.append(r["white"])
                vb.append(r["white"])
            else:
                vo.append(None)
                if o is not None:
                    vb.append(1 if o == "W" else -1)
                else:
                    vb.append(C.model_terminal_value(T.board, t, "B" if s == "W" else "W", a.race_rule))
        open_raw[t], base[t] = tuple(vo), tuple(vb)
        if open_raw[t] != base[t]:
            filled.append(t)
    g_lo, g_hi = sandwich(T, base, kind, d)
    out = {"component": a.component, "tree": passed_test(), "treatment": a.treatment, "race_rule_fill": a.race_rule,
           "no_l8_rows": a.no_l8_rows, "resolved_sides": sum(v is not None for t in T.terms for v in open_raw[t]),
           "filled_terminals": len(filled), "value_with_fill": cgt.show(g_lo), "fill_pinned": g_lo is g_hi}
    print(json.dumps(out), flush=True)
    if g_lo is g_hi:
        target = g_lo

        def ok(F):
            raw = {t: (open_raw[t] if t in F else base[t]) for t in T.terms}
            lo, hi = sandwich(T, raw, kind, d)
            return lo is target and hi is target

        order = sorted(filled, key=lambda t: (-T.men(t), str(t)))
        free = chunked_greedy(order, ok, chunk=32)
        need = [t for t in filled if t not in free]
        out["needed"] = len(need)
        out["needed_by_men"] = dict(sorted(Counter(T.men(t) for t in need).items()))
        out["needed_terminals"] = []
        for t in sorted(need, key=lambda t: (T.men(t), str(t))):
            f = side_fens(T, t)
            out["needed_terminals"].append({"terminal": str(t), "men": T.men(t), "race": owner(T, t) is None,
                                            "assumed_rw_rb": base[t], "known_rw_rb": open_raw[t],
                                            "fen_W": f["W"], "fen_B": f["B"]})
        print(json.dumps({k: v for k, v in out.items() if k != "needed_terminals"}), flush=True)
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
