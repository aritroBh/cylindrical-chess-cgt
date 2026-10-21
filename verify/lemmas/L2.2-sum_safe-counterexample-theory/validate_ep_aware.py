"""Random validation of indep.py's S under EP_AWARE=True against the e.p.-aware branch's pawns.value.
  .venv/bin/python -I verify/lemmas/L2.2-sum_safe-counterexample-theory/validate_ep_aware.py <ep-wt root> [n] [seed]
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import indep as I  # noqa: E402
sys.path.insert(0, os.path.abspath(sys.argv[1]))
from cylcgt import cgt, pawns  # noqa: E402
assert pawns.PASSED_RESPECTS_EP
I.EP_AWARE = True
n = int(sys.argv[2]) if len(sys.argv) > 2 else 300
rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 9)
done = mis = multi = 0
while done < n:
    nf, nr = rng.choice([4, 5, 6, 7, 8]), rng.choice([6, 7, 8])
    bd = I.Bd(nf, nr, rng.random() < 0.6, True)
    rule = rng.choice(["count", "mover", "opponent"])
    nw, nb = rng.randint(1, 4), rng.randint(1, 4)
    # bias towards e.p. motifs: some pawns on start ranks
    sqs = [(f, r) for f in range(nf) for r in range(2, nr)]
    pick = rng.sample(sqs, nw + nb)
    p = (frozenset(pick[:nw]), frozenset(pick[nw:]), None)
    if I.term(bd, p) is not None:
        continue
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    b = pawns.Board(nf, nr, bd.wrap, True)
    try:
        ps = cgt.outcome(pawns.value(b, pawns.Pos(p[0], p[1], None)))
    except pawns.RaceError:
        continue
    done += 1
    multi += len(I.comps(bd, p)) > 1
    s = I.oS(bd, p, rule)
    if s != ps:
        mis += 1
        print("MISMATCH", bd.key(), I.show(p), rule, s, ps, flush=True)
print(f"EP_AWARE validation: {done} positions ({multi} multi-component), mismatches {mis}")
