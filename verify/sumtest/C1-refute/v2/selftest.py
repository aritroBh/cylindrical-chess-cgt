"""Sanity checks of bf.py (no cylcgt)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bf

# family sizes
for b,(F,w) in bf.BOARDS.items():
    print(b, len(bf.family(F, w)[1]))

def mk(geo, text):
    wp, bp = text.split("/")
    W = sum(1 << geo.sq("abcdefgh".index(t[0]), int(t[1:])) for t in wp.split(":")[1].split())
    B = sum(1 << geo.sq("abcdefgh".index(t[0]), int(t[1:])) for t in bp.split(":")[1].split())
    return W, B

def vec(F, wrap, ep, rule, text, scope="pcomp"):
    s = bf.Solver(F, wrap, ep, rule, scope)
    W, B = mk(s.geo, text)
    return "".join(s.outcome(W, B, bf.REF[n]) for n in bf.REF_NAMES)

# X alone: G = blocked 1-file position (no moves for anyone, no passer) == 0
print("X alone   ", vec(1, False, True, "count", "W: a4 / B: a5"), "(expect PNNNLRNLLRLRNNL)")
print("1-file a4/a6 (= *)  ", vec(1, False, True, "count", "W: a4 / B: a6"))
print("1-file a2/a5 (= up?)", vec(1, False, True, "count", "W: a2 / B: a5"))
# candidate on flat 4
for rule in ("count", "mover", "opponent"):
    for ep in (False, True):
        print("cand", rule, ep, vec(4, False, ep, rule, "W: a2 c2 / B: b7 d7"))
