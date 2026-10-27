import time
from lib import *
ev = Evaluator("results.tsv")
X2 = R("W5 B7 W4 W4B7 B6 W3B6")
QC = R("W3B6 W3 W2B5 B5 W2 B4 W4 B7")
X3 = R("W5 B7 W4 W4B7 B6 W3B6 W2 B5")
def show(name, ring):
    t=time.time(); s=ev.sig(ring); print(f"{name:40s} n={len(ring):2d} {s} {nimber(s)}  {time.time()-t:.2f}s  nodes={ev.cache[canon(ring)][1]}", flush=True)
for f in "WB":
    for L in range(1,7):
        show(f"X2 + wall({L},{f})", X2+wall(L,f))
for f in "WB":
    for L in range(1,7):
        show(f"QC + wall({L},{f})", QC+wall(L,f))
for f in "WB":
    for L in (2,4):
        show(f"X3 + wall({L},{f})", X3+wall(L,f))
