"""Sanity checks of indep.py on hand-known one-file values, plus embedding variants."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep import Cfg, make_solver, outcome, parse, refs, add, neg, REF_ORDER
R = refs()
def vec(pos, **kw):
    W, B = parse(pos)
    win, _ = make_solver(Cfg(**kw))
    return {n: outcome(win, W, B, R[n]) for n in ["0", "*", "*2", "*3", "up", "down"]}
# W a4 / B a6 one file: expected *  -> G+* = P
print("a4/a6 1-file:", vec("W: a4 / B: a6", files=1, ep=False))
# W a2 / B a5 one file: expected up -> G+down = P
print("a2/a5 1-file:", vec("W: a2 / B: a5", files=1, ep=False))
# W a4 / B a5: 0
print("a4/a5 1-file:", vec("W: a4 / B: a5", files=1, ep=False))
# W a2 / B b3 2-file flat: W can capture b3 ... expect +-BIG-ish (N)
print("a2/b3 2-file:", vec("W: a2 / B: b3", files=2, ep=False))
# embedding variants for the candidate under count / textbook
for files, wrap in ((8, False), (5, True), (8, True)):
    for ep in (False, True):
        print(f"candidate files={files} wrap={wrap} ep={ep}:",
              vec("W: a2 c2 / B: b7 d7", files=files, wrap=wrap, ep=ep, race="count"))
