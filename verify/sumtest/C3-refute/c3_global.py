"""C3 refute lens: outcome vectors of G + X when the e.p. right expires on ANY move
("global" scope, as in chess), by direct minimax over the pair (G-state, X-node).

Under global scope G is not a disjunctive summand (a move in X changes G), so the
vector may depend on which tree represents X.  We test two representations:
  canon : canonical forms of X (from c3_canon's engine)
  expl  : explicit, unsimplified trees (up* = up + *, dup* = up + up + *, etc.)
Imports only the verifier's own c3_canon.py.
Run:  .venv/bin/python -I verify/sumtest/C3-refute/c3_global.py
"""
import os, sys
from functools import lru_cache
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c3_canon as C

sys.setrecursionlimit(100000)
POS = "W: a2 c2 / B: b7 d7"


@lru_cache(maxsize=None)
def xadd(a, b):            # explicit (unsimplified) sum
    L = [xadd(x, b) for x in C.GL[a]] + [xadd(a, y) for y in C.GL[b]]
    R = [xadd(x, b) for x in C.GR[a]] + [xadd(a, y) for y in C.GR[b]]
    return C.mk(L, R)


mk = C.mk
Z = mk((), ())
S = mk([Z], [Z])
S2 = mk([Z, S], [Z, S])
S3 = mk([Z, S, S2], [Z, S, S2])
UPx = mk([Z], [S])
DNx = mk([S], [Z])
ONEx = mk([Z], [])
MONEx = mk([], [Z])
EXPL = [("0", Z), ("*", S), ("*2", S2), ("*3", S3), ("up", UPx), ("down", DNx),
        ("up*", xadd(UPx, S)), ("dup*", xadd(xadd(UPx, UPx), S)),
        ("1/2", mk([Z], [ONEx])), ("-1/2", mk([MONEx], [Z])), ("1", ONEx), ("-1", MONEx),
        ("{1|0}", mk([ONEx], [Z])), ("+-1", mk([ONEx], [MONEx])),
        ("tiny1", mk([Z], [mk([Z], [MONEx])]))]


def solver(m, scope):
    def after_x(g, mover_white):
        if scope == "local" or g[2] is None:
            return g
        return m.resolve((g[0], g[1], None), mover_white)

    @lru_cache(maxsize=None)
    def lw(g, x):
        if g == "L":
            return True
        if g == "R":
            return False
        if any(not rw(m.resolve(c, True), x) for c in m.gen(g, True)):
            return True
        g2 = after_x(g, True)
        return any(not rw(g2, xl) for xl in C.GL[x])

    @lru_cache(maxsize=None)
    def rw(g, x):
        if g == "R":
            return True
        if g == "L":
            return False
        if any(not lw(m.resolve(c, False), x) for c in m.gen(g, False)):
            return True
        g2 = after_x(g, False)
        return any(not lw(g2, xr) for xr in C.GR[x])

    def out(g, x):
        return {(True, False): "L", (False, True): "R", (True, True): "N", (False, False): "P"}[(lw(g, x), rw(g, x))]
    return out


for files, wrap in ((4, False), (8, False), (8, True)):
    for race in ("count", "mover", "opponent"):
        for ep, aware in ((True, False), (True, True)):
            for scope in ("local", "global"):
                m = C.Pawns(files, wrap, ep=ep, aware=aware, race=race)
                out = solver(m, scope)
                g = m.parse(POS)
                vc = "".join(out(g, x) for _, x in C.REF)
                ve = "".join(out(g, x) for _, x in EXPL)
                print(f"{files}{'cyl' if wrap else 'flat'} {race:8s} {'aware' if aware else 'plain'} {scope:6s} "
                      f"canonX={vc} explX={ve} G+H={out(g, C.H)} G+*2={out(g, C.STAR2)}")
