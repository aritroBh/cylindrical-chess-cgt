"""Validation ONLY (not the decisive check): compare my independent oS / oW
(indep.py, no project imports) with the project's implementations on random
positions, to make sure indep.py models the same games.

  my oS  vs  cgt.outcome(cylcgt.pawns.value)            (the sum model S)
  my oW  vs  crosscheck/minimax.outcome_class           (8 ranks, count rule)
  my oW  vs  lemmas.common.alt_outcome                  (all boards, all rules)

Also prints pawns.sum_safe and the project values for the 9 listed cases.

Run from the project root:
  PYTHONPATH=.:verify/lemmas/L2.2-sum_safe-counterexample-refute \
    .venv/bin/python verify/lemmas/L2.2-sum_safe-counterexample-refute/validate_vs_worker.py --n 600 --seed 5
"""
import argparse
import random
from collections import Counter

import indep as I
from cylcgt import cgt, pawns
from crosscheck import minimax as mm
from lemmas import common

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=600)
ap.add_argument("--seed", type=int, default=5)
a = ap.parse_args()


def proj_S(b, x, rule):
    if pawns.RACE_RULE != rule:
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
    return cgt.outcome(pawns.value(b, x))


print("== the 9 listed cases (project code) ==")
for (n, m, wrap, ep, text, rule, cs, cw) in I.CASES:
    b = pawns.Board(n, m, wrap, ep)
    x = pawns.Pos.parse(text)
    s = proj_S(b, x, rule)
    xc = (mm.outcome_class(mm.Board(n, m, wrap, ep), mm.Position(x.white, x.black, None))
          if (m == 8 and rule == "count") else None)
    alt = common.alt_outcome(b, x, rule)
    print(f"{n}x{m} wrap={wrap} ep={ep} {text} {rule}: ncomp={len(pawns.components(b, x))} "
          f"sum_safe={pawns.sum_safe(b, x)} o(pawns.value)={s} alt={alt} crosscheck={xc}")

print("== random validation ==")
rng = random.Random(a.seed)
st = Counter()
bad = []
done = 0
while done < a.n:
    n = rng.choice([4, 5, 6, 7, 8])
    m = rng.choice([6, 7, 8])
    wrap = rng.random() < 0.6
    ep = rng.random() < 0.5
    rule = rng.choice(["count", "mover", "opponent"])
    b = pawns.Board(n, m, wrap, ep)
    B = I.Bd(n, m, wrap, ep)
    nw, nb = rng.randint(1, 4), rng.randint(1, 4)
    x = common.random_position(rng, b, nw, nb)
    if common.terminal(b, x) is not None:
        continue
    try:
        ps = proj_S(b, x, rule)
        pa = common.alt_outcome(b, x, rule)
    except pawns.RaceError:
        st["race_error_skipped"] += 1
        continue
    done += 1
    ms, mw = I.oS(B, x.white, x.black, rule), I.oW(B, x.white, x.black, rule)
    I.clear()
    st["S_agree" if ms == ps else "S_DIS"] += 1
    st["W_agree_alt" if mw == pa else "W_DIS_alt"] += 1
    if m == 8 and rule == "count":
        xc = mm.outcome_class(mm.Board(n, m, wrap, ep), mm.Position(x.white, x.black, None))
        st["W_agree_xc" if mw == xc else "W_DIS_xc"] += 1
    st["multi" if len(pawns.components(b, x)) > 1 else "single"] += 1
    st["S!=W"] += (ms != mw)
    if ms != ps or mw != pa:
        bad.append((str(b), str(x), rule, ms, ps, mw, pa))
print(dict(st))
for t in bad[:10]:
    print("DISAGREE", t)
print("disagreements:", len(bad))
