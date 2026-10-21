"""Freeze test for W a2 c2 / B b7 d7 with en passant OFF (the setting in which the
4-file *2 survives under the adopted e.p.-aware test), using myfreeze with double
steps kept but no e.p. capture; also split terminal / non-terminal failures.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/cylatlas/C7-theory/freeze_epoff.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import myfreeze as M
_gen = M.gen
def gen_noep(W, B, ep, side, w):
    return [(a, b, None) for a, b, _ in _gen(W, B, None, side, w)]
M.gen = gen_noep
for t in ["W: a2 c2 / B: b7 d7"]:
    res = M.run(t, verbose=True)
    det = res["cyl8"][2]
    print("  cyl8 placements failing at a non-terminal node:", sum(1 for d in det if d[4] is not None and d[5]),
          " failing only at terminal nodes:", sum(1 for d in det if d[4] is not None and not d[5]))
    detf = res["flat8"][2]
    print("  flat8 placements failing at a non-terminal node:", sum(1 for d in detf if d[4] is not None and d[5]),
          " failing only at terminal nodes:", sum(1 for d in detf if d[4] is not None and not d[5]))
M.gen = _gen
res = M.run("W: a2 c2 / B: b7 d7", verbose=False)
detf = res["flat8"][2]
print("e.p. ON flat8: non-terminal failures", sum(1 for d in detf if d[4] is not None and d[5]),
      " terminal-only failures", sum(1 for d in detf if d[4] is not None and not d[5]))
