"""Independent value check of the *2 candidate (no project code).
G = *k  <=>  G + *k is P.  Run: python3 run_values.py"""
import sys, time
sys.path.insert(0, ".")
from indep import *

X4 = parse("W: a2 c2 / B: b7 d7")
X8 = parse("W: a2 c2 g4 / B: b7 d7 g5")
t0 = time.time()
for ep in (True, False):
    for files, X in ((4, X4), (8, X8)):
        bd = Bd(files, 8, False, ep)
        for rule in ("count", "mover", "opponent"):
            row = {f"*{k}": outcome(bd, X, nim(k), rule) for k in range(4)}
            eq = [k for k in range(4) if row[f"*{k}"] == "P"]
            print(f"ep={ep!s:5} files={files} rule={rule:8} o(G+*k) for k=0..3: {row}  => G = *{eq[0]}" if eq else
                  f"ep={ep!s:5} files={files} rule={rule:8} o(G+*k): {row}  => G is no nimber *0..*3")
# reachable tree / split check on the 4-file strip
for ep in (True, False):
    bd = Bd(4, 8, False, ep)
    R = reachable(bd, X4)
    nt = [y for y in R if term(bd, y) is None]
    split = [y for y in nt if n_components(bd, y) > 1]
    print(f"ep={ep}: reachable {len(R)}, non-terminal {len(nt)}, non-terminal with >=2 components: {len(split)}")
    # 8x8: the root already has two components (a-d and g)
    bd8 = Bd(8, 8, False, ep)
    print(f"   8x8 root components: {n_components(bd8, X8)}")
print("time %.1fs" % (time.time() - t0))
