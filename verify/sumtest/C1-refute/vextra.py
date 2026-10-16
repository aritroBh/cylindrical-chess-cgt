"""Out-of-family probe (not part of claim C1): random 3v3 / 3v2 / 2v3 positions on flat4 and cyl4,
verifier solver vs cylcgt, all rules, e.p. on/off.  Seeded.
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/sumtest/C1-refute/vextra.py
"""
import os, random, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from vsolve import Board, Solver, build_refs, key, outcome_letter
from vcylcgt import xs
from cylcgt import cgt, pawns
rng = random.Random(20261015)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 150
tot = diff = 0; t0 = time.time(); ex = []
for files, wrap in ((4, False), (4, True)):
    vb = Board(files, wrap, False, "count")
    sqs = [vb.sq(f, r) for f in range(files) for r in range(2, 8)]
    poss = []
    while len(poss) < N:
        nw, nb = rng.choice([(3, 3), (3, 2), (2, 3)])
        s = rng.sample(sqs, nw + nb)
        W = sum(1 << q for q in s[:nw]); B = sum(1 << q for q in s[nw:])
        if vb.passed_pawns(W, B, "W") or vb.passed_pawns(W, B, "B"):
            continue
        poss.append((W, B))
    for rule in ("count", "mover", "opponent"):
        for ep in (False, True):
            U, refs = build_refs(); b = Board(files, wrap, ep, rule, "P"); sv = Solver(b, U)
            pawns.RACE_RULE = rule; pawns._value.cache_clear()
            cb = pawns.Board(files, 8, wrap, ep); X = xs(cgt)
            for W, B in poss:
                k = key(files, W, B)
                mine = "".join(outcome_letter(*sv.solve((W, B, None)), x) for x in refs)
                p = pawns.Pos.parse(k)
                v = pawns.value(cb, p)
                cy = "".join(cgt.outcome(cgt.add(v, x)) for x in X)
                tot += 15; d = sum(a != c for a, c in zip(mine, cy)); diff += d
                if d and len(ex) < 10:
                    ex.append((files, wrap, rule, ep, k, mine, cy, cgt.show(v), pawns.sum_safe(cb, p)))
print(f"pairs compared {tot}, differing {diff}, seconds {time.time()-t0:.0f}")
for e in ex: print(e)
