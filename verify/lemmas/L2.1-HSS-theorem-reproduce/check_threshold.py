"""Validate the threshold solver of indep_l21.o_S against an explicit minimax over F-states
(live components, frozen integer n, side to move) on the first 300 seed-1 samples, BIG' = max(M)+1."""
import sys
sys.path.insert(0, "verify/lemmas/L2.1-HSS-theorem-reproduce")
import indep_l21 as IL
memo = {}
def win(bd, live, n, tomove, rule, BIG):
    k = (bd, live, n, tomove, rule, BIG)
    if k in memo: return memo[k]
    other = "B" if tomove == "W" else "W"
    res = other
    opts = []
    if tomove == "W" and n >= 1: opts.append((live, n - 1))
    if tomove == "B" and n <= -1: opts.append((live, n + 1))
    for nl, d in IL.f_moves(bd, live, tomove, rule, BIG): opts.append((nl, n + d))
    for nl, nn in opts:
        if win(bd, nl, nn, other, rule, BIG) == tomove: res = tomove; break
    memo[k] = res
    return res
bad = 0; n = 0
for i, (bd, x, rule) in enumerate(IL.samples(1500, 1)):
    if i >= 300: break
    mw, mb = IL.mbound(bd, x); BIG = max(mw, mb) + 1
    live = frozenset(IL.comps(bd, x))
    o = IL.cls(win(bd, live, 0, "W", rule, BIG) == "W", win(bd, live, 0, "B", rule, BIG) == "W")
    t = IL.o_S(bd, x, rule, BIG)
    n += 1; bad += (o != t)
    if o != t: print("MISMATCH", bd, IL.show(x), rule, o, t)
    memo.clear()
print("checked", n, "mismatches", bad)
