"""Check, two ways, a one-sided exclusion certificate of *2 for the real-chess
oracle value of a component, and extract its minimal support.

Treatment "free": a terminal is FIXED only if both of its sides are resolved
in real chess with the same decisive result (class L -> +BIG, class R ->
-BIG); every other terminal (N, P, draw, partly or wholly unresolved) is free
in [-2BIG, +2BIG]. With G_lo (free at -2BIG) and G_hi (free at +2BIG):

  lower test: not (G_lo <= *2)  <=>  Left (White) moving first wins G_lo + *2
  upper test: not (*2 <= G_hi)  <=>  Right (Black) moving first wins G_hi + *2

(1) CGT: cylcgt canonical forms (oracle_value.Terminals.value).
(2) Direct: an explicit win/loss minimax over states (component node, nim
    heap 0..2, player to move) of the SUM game; a terminal child is a nonzero
    integer, so it decides the sum by its sign. This shares only the model's
    move rules (realchess.component.options) with (1), not the canonical-form
    code.
If either test holds, every admissible oracle value G (G_lo <= G <= G_hi)
differs from *2: the target is excluded whatever the free terminals are.

Support: a greedy minimal subset of the fixed (L/R) terminals that keeps the
test true with all other terminals free; its sides are listed with FENs.

    PYTHONPATH=. .venv/bin/python -m realchess.certify.certify_check --component "W: a3 b3 c2 / B: b5 b7 c6" \
        --out realchess/certify/results/<tag>_cert_textbook.json [--no-l8-rows]
"""
from __future__ import annotations

import argparse
import json
import sys
from functools import lru_cache

from cylcgt import cgt
from cylcgt.pawns import Pos

from realchess import component as C
from realchess.oracle_value import G_BIG, G_BIG2, G_NBIG, G_NBIG2, Terminals

from . import termdb
from .oracle10 import passed_test, side_fens


def classes(T, db):
    out = {}
    for t in T.terms:
        f = side_fens(T, t)
        rw, rb = db.get(f["W"]), db.get(f["B"])
        if rw is not None and rb is not None and rw["white"] == rb["white"] and rw["white"] != 0:
            out[t] = "L" if rw["white"] == 1 else "R"
    return out


def cgt_test(T, fixed, test, target):
    if test == "lower":
        g = T.value(lambda t: G_BIG if fixed.get(t) == "L" else (G_NBIG if fixed.get(t) == "R" else G_NBIG2))
        return not cgt.le(g, target), g
    g = T.value(lambda t: G_BIG if fixed.get(t) == "L" else (G_NBIG if fixed.get(t) == "R" else G_BIG2))
    return not cgt.le(target, g), g


def direct_test(T, fixed, test, heap=2, first=None):
    """Left first (lower) / Right first (upper) wins comp + *heap ?
    first='W'/'B' overrides who moves first (the question is then whether
    that player wins)."""
    board = T.board
    free_val = -2 if test == "lower" else 2
    tval = {t: (1 if fixed.get(t) == "L" else (-1 if fixed.get(t) == "R" else free_val)) for t in T.terms}
    sys.setrecursionlimit(1000000)

    @lru_cache(maxsize=None)
    def win(p, k, side):
        """True if `side` to move wins (comp p) + *k."""
        other = "B" if side == "W" else "W"
        for q in C.options(board, p, side):
            if q in T.terms:
                v = tval[q]
                if (v > 0) == (side == "W"):
                    return True
                continue
            if not win(q, k, other):
                return True
        for k2 in range(k):
            if not win(p, k2, other):
                return True
        return False

    r = win(T.comp, heap, first or ("W" if test == "lower" else "B"))
    win.cache_clear()
    return r


def sanity(T, n, seed=1):
    """Random terminal assignments in {+-BIG, +-2BIG}: the direct minimax must
    agree with cylcgt on who wins G + *2 for each first player."""
    import random
    rnd = random.Random(seed)
    board = T.board
    bad = 0
    for _ in range(n):
        vals = {t: rnd.choice((1, -1, 2, -2)) for t in T.terms}
        game = {1: G_BIG, -1: G_NBIG, 2: G_BIG2, -2: G_NBIG2}
        g = cgt.add(T.value(lambda t: game[vals[t]]), cgt.nimber(2))
        o = cgt.outcome(g)
        sys.setrecursionlimit(1000000)

        @lru_cache(maxsize=None)
        def win(p, k, side):
            other = "B" if side == "W" else "W"
            for q in C.options(board, p, side):
                if q in T.terms:
                    if (vals[q] > 0) == (side == "W"):
                        return True
                    continue
                if not win(q, k, other):
                    return True
            for k2 in range(k):
                if not win(p, k2, other):
                    return True
            return False
        lw, rw = win(T.comp, 2, "W"), win(T.comp, 2, "B")
        want = {"L": (True, False), "R": (False, True), "N": (True, True), "P": (False, False)}[o]
        if (lw, rw) != want:
            bad += 1
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", required=True)
    ap.add_argument("--no-l8-rows", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--oracleall", default=None, help="take real results from an oracle-all JSON instead of realdb")
    ap.add_argument("--sanity", type=int, default=0, help="random cross-checks of the direct solver")
    a = ap.parse_args()
    comp = Pos.parse(a.component)
    T = Terminals(comp)
    db = termdb.load()
    if a.no_l8_rows:
        db = {k: v for k, v in db.items() if not v.get("l8")}
    if a.oracleall:
        # results of `solve_candidate oracle-all` (e.g. the A2-realchess files, read-only)
        oa = json.load(open(a.oracleall))
        db = {}
        for r in oa["terminals"]:
            for s, key in (("W", "real_W_first"), ("B", "real_B_first")):
                if r[key] is not None:
                    db[r["fen_" + s]] = {"white": r[key], "how": r.get("how_" + s)}
    fixed = classes(T, db)
    target = cgt.nimber(2)
    out = {"component": a.component, "tree": passed_test(), "no_l8_rows": a.no_l8_rows,
           "terminals": len(T.terms), "internal_nodes": len(T.internal),
           "fixed_LR_terminals": len(fixed), "tests": {}}
    if a.sanity:
        out["sanity_random_assignments"] = a.sanity
        out["sanity_disagreements"] = sanity(T, a.sanity)
        print("sanity disagreements:", out["sanity_disagreements"], "of", a.sanity, flush=True)
    for test in ("lower", "upper"):
        ok_cgt, g = cgt_test(T, fixed, test, target)
        ok_dir = direct_test(T, fixed, test)
        res = {"cgt": ok_cgt, "direct_minimax": ok_dir, "bound": cgt.show(g),
               "bound_outcome_cgt": cgt.outcome(g),
               "bound_outcome_direct": {"White first wins": direct_test(T, fixed, test, heap=0, first="W"),
                                        "Black first wins": direct_test(T, fixed, test, heap=0, first="B")}}
        if test == "lower" and cgt.outcome(g) == "L":
            res["meaning"] = "G_lo > 0: every admissible oracle value is positive (White wins the pawn tree whoever starts)"
        if test == "upper" and cgt.outcome(g) == "R":
            res["meaning"] = "G_hi < 0: every admissible oracle value is negative (Black wins the pawn tree whoever starts)"
        if ok_cgt and ok_dir:
            items = sorted(fixed, key=lambda t: (-T.men(t), str(t)))
            keep = dict(fixed)
            for t in items:
                trial = dict(keep)
                del trial[t]
                if cgt_test(T, trial, test, target)[0]:
                    keep = trial
            res["support_size"] = len(keep)
            res["support_cgt"] = cgt_test(T, keep, test, target)[0]
            res["support_direct"] = direct_test(T, keep, test)
            res["support"] = []
            for t in sorted(keep, key=lambda t: (T.men(t), str(t))):
                f = side_fens(T, t)
                res["support"].append({"terminal": str(t), "men": T.men(t), "class": keep[t],
                                       "fen_W": f["W"], "how_W": db[f["W"]]["how"],
                                       "fen_B": f["B"], "how_B": db[f["B"]]["how"]})
        out["tests"][test] = res
        print(test, json.dumps({k: v for k, v in res.items() if k != "support"}), flush=True)
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
