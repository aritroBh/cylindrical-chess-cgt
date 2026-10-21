"""Calibration of indep2 against the code under test on random positions:
indep2.oS vs cgt.outcome(pawns.value), and indep2.oW vs crosscheck (8 ranks, count).
Also counts single components with sum_safe True and oS != oW.

Run from the project root:
  PYTHONPATH=.:verify/lemmas/L2.2-sum_safe-counterexample-refute/run2 \
    .venv/bin/python verify/lemmas/L2.2-sum_safe-counterexample-refute/run2/compare_random.py --n 300 --seed 777 --tmax 900
"""
import argparse
import random
import time

import indep2 as I
from cylcgt import cgt, pawns
from crosscheck import minimax as mm

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=300)
ap.add_argument("--seed", type=int, default=777)
ap.add_argument("--tmax", type=float, default=900)
a = ap.parse_args()
rng = random.Random(a.seed)
t0 = time.time()
stats = {"tried": 0, "S_agree": 0, "S_disagree": 0, "W_xc_agree": 0, "W_xc_disagree": 0,
         "single": 0, "multi": 0, "single_SneW": 0, "multi_SneW": 0}
bad = []
while stats["tried"] < a.n and time.time() - t0 < a.tmax:
    files = rng.choice([5, 6, 7, 8])
    ranks = rng.choice([6, 7, 8])
    wrap = rng.random() < 0.6
    ep = rng.random() < 0.5
    nw, nb = rng.randint(1, 4), rng.randint(1, 4)
    sqs = [(f, r) for f in range(files) for r in range(2, ranks)]
    pick = rng.sample(sqs, nw + nb)
    w, k = frozenset(pick[:nw]), frozenset(pick[nw:])
    Bd = I.Board(files, ranks, wrap, ep)
    if I.has_passer(Bd, w, k, "W") or I.has_passer(Bd, w, k, "B"):
        continue
    rule = rng.choice(["count", "mover", "opponent"])
    stats["tried"] += 1
    s_mine, w_mine = I.oS(Bd, (w, k), rule), I.oW(Bd, (w, k), rule)
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    pb = pawns.Board(files, ranks, wrap, ep)
    px = pawns.Pos(w, k)
    s_proj = cgt.outcome(pawns.value(pb, px))
    single = len(pawns.components(pb, px)) == 1
    stats["single" if single else "multi"] += 1
    if s_mine == s_proj:
        stats["S_agree"] += 1
    else:
        stats["S_disagree"] += 1
        bad.append(("S", repr(Bd), I.fmt(w, k), rule, s_mine, s_proj))
    if s_mine != w_mine:
        stats["single_SneW" if single else "multi_SneW"] += 1
    if ranks == 8 and rule == "count":
        xc = mm.outcome_class(mm.Board(files, ranks, wrap, ep), mm.Position(w, k, None))
        if xc == w_mine:
            stats["W_xc_agree"] += 1
        else:
            stats["W_xc_disagree"] += 1
            bad.append(("W", repr(Bd), I.fmt(w, k), rule, w_mine, xc))
pawns.RACE_RULE = "count"
print(stats, f"{time.time() - t0:.0f}s")
for b in bad:
    print("DISAGREE", b)
