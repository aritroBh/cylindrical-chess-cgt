"""Root options of G = W a2 c2 / B b7 d7 (4 files, flat) and the key line, under
textbook vs e.p.-aware passer tests, using indep2.Model + cylcgt.cgt for naming.
  PYTHONPATH=. .venv/bin/python verify/sumtest/C3-reproduce/run2/options.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep2 import Model, canonical, FN
from cylcgt import cgt

def nm(pos):
    if pos in ("L", "R"):
        return {"L": "+BIG", "R": "-BIG"}[pos]
    W, B, ep = pos
    s = lambda S: " ".join(FN[f] + str(r) for f, r in sorted(S))
    return f"W: {s(W)} / B: {s(B)}" + (f" [ep {ep[0]} may take on {FN[ep[1][0]]}{ep[1][1]}]" if ep else "")

for race in ("count", "mover"):
  for conv in ("textbook", "aware"):
    m = Model(4, False, True, conv, race, "local")
    g0 = m.parse("W: a2 c2 / B: b7 d7")
    print(f"=== race={race} conv={conv}: G = {cgt.show(canonical(m, g0))}")
    for col in ("W", "B"):
        for c in m.child(g0, col):
            print(f"   {col} -> {nm(c):40s} value {cgt.show(canonical(m, c))}")
    # key line X = W a2 c2 / B b4 d7, White to move a2-a4
    X = m.parse("W: a2 c2 / B: b4 d7")
    print("   X = W a2 c2 / B b4 d7 :", cgt.show(canonical(m, X)))
    for c in m.child(X, "W"):
        print(f"      W -> {nm(c):40s} value {cgt.show(canonical(m, c))}")
