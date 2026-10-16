"""Root value of the candidate under several 'faithful' king-move models
(any K_L with a Right option -BIG, any K_R with a Left option +BIG), at EVERY
non-terminal node.  Project code used read-only (cgt.make, pawns.moves/passed).
Run: PYTHONPATH=. .venv/bin/python verify/lemmas/L3.4-candidate-all-models-theory/king_models.py"""
import sys
sys.setrecursionlimit(1_000_000)
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos, BIG
P, N = cgt.integer(BIG), cgt.integer(-BIG)
PM = cgt.make([P], [N])  # +-BIG

def race(b, c, mover, rule):
    o = "B" if mover == "W" else "W"
    if rule == "mover": w = mover
    elif rule == "opponent": w = o
    else: w = o if pawns.promote_distance(b, c, o) <= pawns.promote_distance(b, c, mover) else mover
    return P if w == "W" else N

def solve(b, x, rule, model):
    memo = {}
    def W(y):
        if y in memo: return memo[y]
        wp, bp = pawns.passed(b, y, "W"), pawns.passed(b, y, "B")
        assert not (wp and bp)
        if wp: g = P
        elif bp: g = N
        else:
            plain = Pos(y.white, y.black, None)
            lp = plain if (y.ep and y.ep[2] != "W") else y
            rp = plain if (y.ep and y.ep[2] != "B") else y
            def ch(c, m):
                a, d = pawns.passed(b, c, "W"), pawns.passed(b, c, "B")
                return race(b, c, m, rule) if (a and d) else W(c)
            L = [ch(c, "W") for c in pawns.moves(b, lp, "W")]
            R = [ch(c, "B") for c in pawns.moves(b, rp, "B")]
            g0 = cgt.make(L, R)
            if model == "none": pass
            elif model == "minusBIG": L, R = L + [N], R + [P]
            elif model == "pmBIG": L, R = L + [PM], R + [PM]
            elif model == "stepback": L, R = L + [cgt.make([g0], [N])], R + [cgt.make([P], [g0])]
            elif model == "zero_or_lose": L, R = L + [cgt.make([cgt.ZERO], [N])], R + [cgt.make([P], [cgt.ZERO])]
            g = cgt.make(L, R)
        memo[y] = g
        return g
    return W(x)

X = Pos.parse("W: a2 c2 / B: b7 d7")
for ep in (True, False):
    b = Board(4, 8, False, ep)
    for rule in ("count", "mover", "opponent"):
        vals = {m: cgt.show(solve(b, X, rule, m)) for m in ("none", "minusBIG", "pmBIG", "stepback", "zero_or_lose")}
        print(f"ep={ep!s:5s} rule={rule:8s} root value by king-move model: {vals}")
