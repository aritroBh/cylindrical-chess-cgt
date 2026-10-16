"""Mechanism checks for the headline counterexample (independent code only)."""
import sys
sys.path.insert(0, ".")
from indep import B, parse, make_solvers, reach, comps, threats, has_passer, gen, show

bd = B(8, 8, True, False)
x = parse("W: b2 d4 g3 h5 / B: a7 c7 f7 g4")
oW, oS, Wg, Sg = make_solvers(bd, "count", 256)

def o_child(c):
    wp, bp = has_passer(bd, c, "W"), has_passer(bd, c, "B")
    if wp and bp:
        return "race", "race"
    if wp or bp:
        return ("L", "L") if wp else ("R", "R")
    return oS(c), oW(c)

for side in ("W", "B"):
    kids = sorted(gen(bd, x, side), key=show)
    print(f"{side} has {len(kids)} moves")
    nd = 0
    for c in kids:
        s, w = o_child(c)
        nd += s != w
        print(f"   {show(c):45s} comps={len(comps(bd, c))} o(S)={s} o(W)={w}{'   <-- differ' if s != w else ''}")
    print(f"   children where o(S) != o(W): {nd}")

y = parse("W: b5 d4 g3 / B: c6 f6 g4 h6")
R = reach(bd, x)
print("mechanism node reachable from X:", y in R)
memo = {}
print("mechanism node components and threat sets:", [(show(c), sorted(threats(bd, c, memo))) for c in comps(bd, y)])
print("mechanism node o(S) =", oS(y), " o(W) =", oW(y))

# how many reachable non-terminal multi-component nodes with opposite threats in different comps, and S/W disagreement there
bad = dis = 0
for z in R:
    if has_passer(bd, z, "W") or has_passer(bd, z, "B"):
        continue
    cs = comps(bd, z)
    if len(cs) < 2:
        continue
    ts = [threats(bd, c, memo) for c in cs]
    if any(i != j and 1 in a and -1 in b for i, a in enumerate(ts) for j, b in enumerate(ts)):
        bad += 1
        dis += oS(z) != oW(z)
print("reachable non-pairwise-safe split nodes:", bad, " of which o(S) != o(W):", dis)
