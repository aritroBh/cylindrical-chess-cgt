"""Theory-lens checks for claim L2.2 (sum_safe counterexample).

Part A validates indep.py against the project code on random positions (so that
indep.py can count as a second implementation of o(S) and o(W)).
Part B examines the headline position with indep.py only (plus pawns.sum_safe,
which is the object under test).

Run from the project root:
  PYTHONPATH=. .venv/bin/python verify/lemmas/L2.2-sum_safe-counterexample-theory/analyse.py [--n 400] [--seed 7]
"""
import argparse
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep as I  # noqa: E402

from cylcgt import cgt, pawns  # noqa: E402
from crosscheck import minimax as mm  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=400)
ap.add_argument("--seed", type=int, default=7)
a = ap.parse_args()


def proj_S(bd, p, rule):
    if pawns.RACE_RULE != rule:
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
    return cgt.outcome(pawns.value(pawns.Board(bd.nf, bd.nr, bd.wrap, bd.ep), pawns.Pos(p[0], p[1], p[2])))


def to_proj(p):
    return pawns.Pos(p[0], p[1], p[2])


# ---------------------------------------------------------------- Part A
rng = random.Random(a.seed)
t0 = time.time()
stats = dict(n=0, multi=0, s_mis=0, w_mis=0, xc=0, xc_mis=0, sw_diff=0, race=0)
while stats['n'] < a.n:
    nf = rng.choice([4, 5, 6, 7, 8])
    nr = rng.choice([6, 7, 8])
    bd = I.Bd(nf, nr, rng.random() < 0.6, rng.random() < 0.5)
    rule = rng.choice(["count", "mover", "opponent"])
    nw, nb = rng.randint(1, 4), rng.randint(1, 4)
    sqs = [(f, r) for f in range(nf) for r in range(2, nr)]
    pick = rng.sample(sqs, nw + nb)
    p = (frozenset(pick[:nw]), frozenset(pick[nw:]), None)
    if I.term(bd, p) is not None:
        continue
    try:
        ps = proj_S(bd, p, rule)
    except pawns.RaceError:
        stats["race"] += 1
        continue
    stats["n"] += 1
    stats["multi"] += len(I.comps(bd, p)) > 1
    s = I.oS(bd, p, rule)
    w = I.oW(bd, p, rule)
    if s != ps:
        stats["s_mis"] += 1
        print("S MISMATCH", bd.key(), I.show(p), rule, s, ps)
    import lemmas.common as C
    cw = C.alt_outcome(pawns.Board(bd.nf, bd.nr, bd.wrap, bd.ep), to_proj(p), rule)
    if w != cw:
        stats["w_mis"] += 1
        print("W MISMATCH", bd.key(), I.show(p), rule, w, cw)
    if nr == 8 and rule == "count":
        stats["xc"] += 1
        xc = mm.outcome_class(mm.Board(nf, nr, bd.wrap, bd.ep), mm.Position(p[0], p[1], None))
        if xc != w:
            stats["xc_mis"] += 1
            print("XC MISMATCH", bd.key(), I.show(p), rule, w, xc)
    stats["sw_diff"] += s != w
print("Part A (indep vs project):", stats, f"{time.time()-t0:.0f}s", flush=True)

# ---------------------------------------------------------------- Part B
bd = I.Bd(8, 8, True, False)
X = I.parse("W: b2 d4 g3 h5 / B: a7 c7 f7 g4")
I._BD[bd.key()] = bd
print("\nPart B: headline", I.show(X))
print("  components:", [I.show(c) for c in I.comps(bd, X)])
print("  pawns.sum_safe:", pawns.sum_safe(pawns.Board(8, 8, True, False), to_proj(X)))
for rule in ("count", "mover", "opponent"):
    print(f"  rule {rule:8s}: indep o(S)={I.oS(bd, X, rule)}  indep o(W)={I.oW(bd, X, rule)}")
bad = I.unsafe_nodes(bd, X)
print("  reachable non-terminal non-pairwise-safe nodes (so HSS fails):", len(bad))
M = I.parse("W: b5 d4 g3 / B: c6 f6 g4 h6")
R = I.reach(bd, X)
print("  mechanism node", I.show(M), "reachable:", M in R,
      "comps+threats:", [(I.show(c), sorted(I.tau(bd.key(), c))) for c in I.comps(bd, M)],
      "o(S)=", I.oS(bd, M, "count"), "o(W)=", I.oW(bd, M, "count"))
for side in ("W", "B"):
    ch = I.gen(bd, X, side)
    diff = [c for c in ch if I.term(bd, c) is None and I.oS(bd, c) != I.oW(bd, c)]
    print(f"  {side} has {len(ch)} moves; children with o(S)!=o(W): {len(diff)}")

# BIG sensitivity (move bound M_W=%d, M_B=%d)
mw = sum(8 - r for _, r in X[0])
mb = sum(r - 1 for _, r in X[1])
for big in (60, 100, 256, 1000):
    I.BIG = big
    I.s_win.cache_clear()
    I.w_win.cache_clear()
    print(f"  BIG={big} (M_W={mw}, M_B={mb}): o(S)={I.oS(bd, X, 'count')} o(W)={I.oW(bd, X, 'count')}")
I.BIG = 256
I.s_win.cache_clear()
I.w_win.cache_clear()

# the same position is an arc, i.e. a flat 7-file strip (Lemma 1.4): f..d -> a..g
fmap = {5: 0, 6: 1, 7: 2, 0: 3, 1: 4, 2: 5, 3: 6}
Xf = (frozenset((fmap[f], r) for f, r in X[0]), frozenset((fmap[f], r) for f, r in X[1]), None)
bf = I.Bd(7, 8, False, False)
I._BD[bf.key()] = bf
print("\n  flat 7x8 relabelling:", I.show(Xf), "sum_safe:",
      pawns.sum_safe(pawns.Board(7, 8, False, False), to_proj(Xf)),
      "o(S)=", I.oS(bf, Xf), "o(W)=", I.oW(bf, Xf),
      "crosscheck=", mm.outcome_class(mm.Board(7, 8, False, False), mm.Position(Xf[0], Xf[1], None)))
# with e.p. on
be = I.Bd(8, 8, True, True)
I._BD[be.key()] = be
print("  headline with e.p. ON: o(S)=", I.oS(be, X), "o(S_glob)=", I.oS(be, X, glob=True), "o(W)=", I.oW(be, X))
