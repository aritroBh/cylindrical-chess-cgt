"""Independent check of every row of notes/lemmas.md Counterexample 2.2 table (no project imports)."""
import sys, time
sys.path.insert(0, ".")
from indep import B, parse, make_solvers, reach, comps, threats, has_passer, gen, show

ROWS = [
    ((8, 8, True, False), "W: b2 d4 g3 h5 / B: a7 c7 f7 g4", "count", "R", "N"),
    ((8, 8, True, False), "W: b3 f4 g5 / B: a5 b6 f5 h6", "count", "N", "L"),
    ((8, 8, True, False), "W: b2 c5 d4 f3 / B: c7 d6 e7 g6", "count", "L", "N"),
    ((8, 8, True, True), "W: a2 c4 e4 h2 / B: a6 b5 d7 e7", "count", "R", "N"),
    ((8, 8, True, True), "W: a5 b6 d2 e2 / B: a7 c7 e7", "count", "L", "N"),
    ((8, 7, True, False), "W: c2 g2 h4 / B: a5 b6 f5 g6", "count", "R", "N"),
    ((7, 6, False, True), "W: b2 d3 f2 / B: c4 c5 e5 g5", "count", "N", "R"),
    ((8, 8, True, True), "W: a3 e2 e4 h6 / B: a4 a5 f5 g7", "opponent", "N", "L"),
    ((6, 8, False, False), "W: b2 d4 f4 / B: b7 c5 e5 e7", "opponent", "R", "N"),
]

def hss(bd, x):
    memo = {}
    for y in reach(bd, x):
        if has_passer(bd, y, "W") or has_passer(bd, y, "B"):
            continue
        cs = comps(bd, y)
        ts = [threats(bd, c, memo) for c in cs]
        for i, a in enumerate(ts):
            for j, b in enumerate(ts):
                if i != j and 1 in a and -1 in b:
                    return False
    return True

allok = True
for bk, text, rule, claimS, claimW in ROWS:
    bd = B(*bk)
    x = parse(text)
    nc = len(comps(bd, x))
    res = {}
    for BIG in (40, 64, 256):
        oW, oS, Wg, Sg = make_solvers(bd, rule, BIG)
        res[BIG] = (oS(x), oW(x))
    ruleW = {}
    for r in ("count", "mover", "opponent"):
        oW, oS, _, _ = make_solvers(bd, r, 256)
        ruleW[r] = (oS(x), oW(x))
    h = hss(bd, x)
    ok = nc == 1 and all(v == (claimS, claimW) for v in res.values()) and not h
    allok &= ok
    print(f"{'OK ' if ok else 'BAD'} {bk} {text} [{rule}] comps={nc} HSS={h} (o(S),o(W)) by BIG={res}  claimed=({claimS},{claimW})  all rules: {ruleW}", flush=True)
print("ALL ROWS AS CLAIMED:", allok)
