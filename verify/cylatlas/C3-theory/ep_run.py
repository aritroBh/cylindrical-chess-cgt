"""Evaluate flat single components / rings (w+b<=5) under a chosen passed test, count rule, e.p. on.
  PYTHONPATH=<ep-wt>:. .venv/bin/python verify/cylatlas/C3-theory/ep_run.py <flat|ring> <n> <minp> <maxp> <out.jsonl>
With PYTHONPATH starting at the ep-aware-passed checkout, cylcgt.pawns.PASSED_RESPECTS_EP is True."""
import json, sys, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from enum_own import positions

def key(g, memo={}):
    if g.id in memo: return memo[g.id]
    if g.num is not None:
        x = g.num; r = str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    elif g.nim is not None:
        r = f"*{g.nim}"
    else:
        r = "{" + ",".join(sorted(key(x) for x in g.L)) + "|" + ",".join(sorted(key(x) for x in g.R)) + "}"
    memo[g.id] = r; return r

kind, n, minp, maxp, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
print("PASSED_RESPECTS_EP =", getattr(pawns, "PASSED_RESPECTS_EP", "absent (textbook)"), "file", pawns.__file__, flush=True)
wrap = kind == "ring"
board = Board(n, 8, wrap, True)
t0 = time.time(); c = 0
with open(out, "w") as fh:
    for w, b, pos in positions(n, wrap, maxp):
        if w + b < minp: continue
        g = pawns.value(board, pos)
        fh.write(json.dumps({"kind": kind, "n": n, "w": w, "b": b, "pos": str(pos), "key": key(g)}) + "\n")
        c += 1
        if c % 1000 == 0: print(c, round(time.time() - t0), flush=True)
print("done", c, round(time.time() - t0), flush=True)
