import time
from lib import *
ev = Evaluator("results_two.tsv", tbits=24, nodelim=20000000)
X2 = R("W5 B7 W4 W4B7 B6 W3B6")
X3 = R("W5 B7 W4 W4B7 B6 W3B6 W2 B5")
QC = R("W3B6 W3 W2B5 B5 W2 B4 W4 B7")
P1 = R("W4B6")   # *1
P2 = R("B7 W4")  # *1 (type W even/odd, B even)
def show(name, ring):
    t=time.time(); s=ev.sig(ring); print(f"{name:40s} n={len(ring):2d} {s} {nimber(s)}  {time.time()-t:.2f}s  nodes={ev.cache[canon(ring)][1]}", flush=True)
for L1,L2 in ((2,2),(2,4),(4,4)):
    show(f"X2+W{L1}+W4B6+W{L2}", X2+wall(L1,'W')+P1+wall(L2,'W'))
for L1,L2 in ((2,2),(2,4)):
    show(f"X2+W{L1}+(B7 W4)+W{L2}", X2+wall(L1,'W')+P2+wall(L2,'W'))
for L1,L2 in ((2,2),(2,4),(4,4)):
    show(f"X2+W{L1}+X2+W{L2}", X2+wall(L1,'W')+X2+wall(L2,'W'))
for L1,L2 in ((2,2),):
    show(f"X2+W{L1}+X3+W{L2}", X2+wall(L1,'W')+X3+wall(L2,'W'))
    show(f"X2+W{L1}+QC+W{L2}", X2+wall(L1,'W')+QC+wall(L2,'B'))
