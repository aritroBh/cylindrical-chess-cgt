"""C3-theory checks (verifier scratch; imports cylcgt.cgt and sumtest read-only).

1. H = {2+-1 | -2+-1} built by hand from integers: canonical form, mean, temperature,
   H = -H, H + H = 0, H != *2, outcome vector against the 15 reference games.
2. Sensitivity of the e.p.-aware canonical value of G to the BIG constant.
3. Thermograph-free hand facts: stops of H.

  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/sumtest/C3-theory/theory_checks.py
"""
from cylcgt import cgt
import sumtest.aware_value as av
from sumtest.compare_cylcgt import ref_games
from sumtest.sumsolver import REF_NAMES

I = cgt.integer
pm21 = cgt.make([I(3)], [I(1)])
mpm21 = cgt.make([I(-1)], [I(-3)])
H = cgt.make([pm21], [mpm21])
print("H =", cgt.show(H), "| mean", cgt.mean(H), "| temp", cgt.temperature(H))
print("H == -H:", cgt.le(H, cgt.neg(H)) and cgt.le(cgt.neg(H), H))
print("outcome(H+H):", cgt.outcome(cgt.add(H, H)), "(P means H+H=0)")
S2 = cgt.nimber(2)
print("outcome(H + *2):", cgt.outcome(cgt.add(H, S2)))
R = ref_games()
print("H vector:", "".join(cgt.outcome(cgt.add(H, R[n])) for n in REF_NAMES))
print("*2 vector:", "".join(cgt.outcome(cgt.add(S2, R[n])) for n in REF_NAMES))
# H compared with small numbers: H is confused with every x in [-1, 1]
for x in [I(-2), I(-1), I(0), I(1), I(2)]:
    print(f"  outcome(H - ({cgt.show(x)})):", cgt.outcome(cgt.add(H, cgt.neg(x))))
print()
for big in (8, 16, 64, 256, 1024):
    av.BIG = big
    for rule in ("count", "mover", "opponent"):
        for aware in (True, False):
            v, brute, pred = av.value("W: a2 c2 / B: b7 d7", 4, False, ep=True, aware=aware, race_rule=rule)
            print(f"BIG={big:5d} rule={rule:8s} test={'aware' if aware else 'textbook'}: {cgt.show(v)}  "
                  f"(brute vector {'=' if brute == pred else '!='} cgt prediction)")
