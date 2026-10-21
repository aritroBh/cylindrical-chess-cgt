"""Third e.p.-aware variant V3 (verifier's own; cylcgt.cgt used read-only for canonical forms):
at a decided child whose double-stepped pawn can be taken e.p. at once, the entitled
side s gets, besides the convention score ("the passer stands", standing for any
other move), the extra option of each e.p. capture (scored normally). The other side's
option there is also "stands". Everything else is the convention W of indep.py.
Run: PYTHONPATH=. .venv/bin/python verify/lemmas/L3.4-candidate-all-models-reproduce/ep_variant_v3.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cylcgt import cgt
import indep as I
from ep_passer import contested
PB, NB = cgt.integer(I.BIG), cgt.integer(-I.BIG)

def model(board, rule):
    memo = {}
    def score(c, mover):
        if contested(board, c):
            return node(c)
        r = I.child_result(board, c, mover, rule)
        return node(c) if r is None else (PB if r == "W" else NB)
    def node(x):
        if x in memo:
            return memo[x]
        t = I.term(board, x)
        if t is not None:
            s = x[2][2]
            stands = (PB if t == 1 else NB) if t != 0 else \
                (PB if I.race_win(board, x, "B" if s == "W" else "W", rule) == "W" else NB)
            victim = x[2][1]
            caps = [score(c, s) for c in I.gen(board, x, s)
                    if victim not in (c[0] | c[1])]
            g = cgt.make([stands] + caps, [stands]) if s == "W" else cgt.make([stands], [stands] + caps)
        else:
            ls = x if (x[2] is None or x[2][2] == "W") else (x[0], x[1], None)
            rs = x if (x[2] is None or x[2][2] == "B") else (x[0], x[1], None)
            g = cgt.make([score(c, "W") for c in I.gen(board, ls, "W")],
                         [score(c, "B") for c in I.gen(board, rs, "B")])
        memo[x] = g
        return g
    return node

for files, root in ((4, I.mkpos("a2 c2", "b7 d7")), (8, I.mkpos("a2 c2 g4", "b7 d7 g5"))):
    for rule in ("count", "mover", "opponent"):
        g = model((files, 8, True), rule)(root)
        print(f"V3 files={files} rule={rule:8s}: value {cgt.show(g)}  outcome {cgt.outcome(g)}")
