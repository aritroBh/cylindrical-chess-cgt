"""Sensitivity probes for C3 (verifier scratch). Imports only the verifier's own c3_indep.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3_indep import Model, REF, STAR2, H, ZERO, sw, integer, pure_outcome, gsum

POS = "W: a2 c2 / B: b7 d7"
for race in ("count", "mover"):
    for rd in (True, False):
        for scope in ("local", "global"):
            m = Model(4, False, ep=True, aware=True, race=race, scope=scope, race_double=rd)
            out = m.solver(); g = m.parse(POS)
            vec = "".join(out(g, x) for _, x in REF)
            print(f"aware race={race} race_double={rd} scope={scope}: vec={vec} G+*2={out(g, STAR2)} G+H={out(g, H)}")

# First options of G under aware/count/local, tested against small candidate values
m = Model(4, False, ep=True, aware=True, race="count", scope="local")
out = m.solver(); g = m.parse(POS)
cands = {"0": ZERO, "*": REF[1][1], "*2": STAR2, "2+-1": sw(3, 1), "-2+-1": sw(-1, -3),
         "1": integer(1), "-1": integer(-1), "3": integer(3), "-3": integer(-3)}
from c3_indep import gneg
def name(st):
    if isinstance(st, str):
        return "+BIG" if st == "L" else "-BIG"
    for k, v in cands.items():
        if out(st, gneg(v)) == "P":
            return k
    return "?"
def show(st):
    if isinstance(st, str): return st
    W, B, ep = st
    f = lambda s: " ".join(sorted("abcdefgh"[a] + str(b) for a, b in s))
    return f"W {f(W)} / B {f(B)}" + (f" ep={ep}" if ep else "")
for white in (True, False):
    for c in m.children(g, white):
        print(("L" if white else "R") + "-option:", show(c), "=", name(c))
