"""Does the candidate behave as *2 in sums with small threat-free games H,
(a) with the CGT (stale-right) e.p. semantics and (b) with chess (global
expiry) e.p. semantics?  Reference: o(*2 + H) from explicit forms.
Run: python3 run_sums.py"""
import sys, itertools
sys.path.insert(0, ".")
from indep import *
from indep import _cls
from functools import lru_cache

def ex_wins(g, side):
    opts = g[0] if side == "W" else g[1]
    other = "B" if side == "W" else "W"
    return any(not ex_wins(o, other) for o in opts)
def ex_out(g):
    return _cls(ex_wins(g, "W"), ex_wins(g, "B"))

UPSTAR = add(UP, STAR)
DOWNSTAR = add(DOWN, STAR)
TINY = ((ZERO,), (((ZERO,), (MONE,)),))       # {0 || 0 | -1} = tiny-1
MINY = ((((ONE,), (ZERO,)),), (ZERO,))
SW = ((ONE,), (STAR,))                         # {1 | *}
basic = {"0": ZERO, "*": STAR, "*2": nim(2), "*3": nim(3), "up": UP, "down": DOWN,
         "up*": UPSTAR, "down*": DOWNSTAR, "1": ONE, "-1": MONE, "1/2": HALF,
         "+-1": PM1, "tiny1": TINY, "miny1": MINY, "{1|*}": SW}
Hs = dict(basic)
for (a, ga), (b, gb) in itertools.combinations(basic.items(), 2):
    if a in ("0",) or b in ("0",): continue
    Hs[a + "+" + b] = add(ga, gb)

X = parse("W: a2 c2 / B: b7 d7")
bad = {"local": 0, "global": 0}
n = 0
for ep in (True, False):
    bd = Bd(4, 8, False, ep)
    for rule in ("count", "mover"):
        for name, h in Hs.items():
            ref = ex_out(add(nim(2), h))
            for mode in ("local", "global"):
                o = outcome(bd, X, h, rule, False, mode)
                n += 1
                if o != ref:
                    bad[mode] += 1
                    print(f"MISMATCH ep={ep} rule={rule} mode={mode} H={name}: o(X+H)={o}, o(*2+H)={ref}")
print(f"{len(Hs)} games H x 2 e.p. x 2 rules x 2 modes = {n} checks; mismatches: {bad}")
