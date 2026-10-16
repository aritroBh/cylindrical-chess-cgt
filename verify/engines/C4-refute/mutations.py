"""Sensitivity check: how many of the 181 verified lines would fail under mutated models.
    cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/engines/C4-refute/mutations.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import refute_c4 as R

cache = R.load_cache()
ver = [R.parse_epd(l) for l in open(os.path.join(R.SUITE, "cgt_verified.epd")) if l.strip()]
orig_terminal, orig_moves = R.terminal, R.comp_moves


def run(name):
    R.winner.cache_clear()
    bad = 0
    for fen4, ops in ver:
        b, stm, _, _ = R.parse_fen(fen4 + " 0 1")
        W, B = R.comp_of(b)
        pred = R.predicted_wins(W, B, "W" if stm == "w" else "B")
        if pred != set(" ".join(ops["c2"]).split()):
            bad += 1
    print(f"{name:40s} verified lines whose bm != prediction: {bad}/181")


def race(rule):
    def t(W, B, mover):
        wp, bp = R.passed(W, B, "W"), R.passed(W, B, "B")
        other = "B" if mover == "W" else "W"
        if wp and bp:
            if rule == "mover":
                return mover
            if rule == "opponent":
                return other
            if rule == "count-tie-mover":
                return other if R.dist(W, B, other) < R.dist(W, B, mover) else mover
            if rule == "count-no-double":
                def d(side):
                    mine, theirs = (W, B) if side == "W" else (B, W)
                    best = 10**6
                    for f, r in mine:
                        if any(abs(g - f) <= 1 and ((s > r) if side == "W" else (s < r)) for g, s in theirs):
                            continue
                        best = min(best, (8 - r) if side == "W" else (r - 1))
                    return best
                return other if d(other) <= d(mover) else mover
        return orig_terminal(W, B, mover)
    return t


R.terminal = orig_terminal
run("baseline count rule")
for rule in ("mover", "opponent", "count-tie-mover", "count-no-double"):
    R.terminal = race(rule)
    run("race rule " + rule)
R.terminal = orig_terminal


def no_ep(W, B, ep, side):
    return [m for m in orig_moves(W, B, ep, side) if m[1] != "ep"]


R.comp_moves = no_ep
run("en passant off")
R.comp_moves = orig_moves


def no_double(W, B, ep, side):
    return [m for m in orig_moves(W, B, ep, side) if m[1] != "double"]


R.comp_moves = no_double
run("no double steps")
R.comp_moves = orig_moves
