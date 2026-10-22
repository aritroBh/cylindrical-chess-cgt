import sys, time
from common import *
n = 0; t0 = time.time(); cnt = 0
for line in sys.stdin:
    W, B = parse_pos(line.strip()); width = max(f for f, _ in W + B) + 1
    g = pawns.value(pawns.Board(width, 8, False, True), pawns.Pos(frozenset(W), frozenset(B)))
    n += 1
    if n % 10 == 0: print(n, f"{(time.time()-t0)/n:.3f}s/root", cgt.outcome(g), g.nim, flush=True)
print(n, (time.time()-t0)/n, "s/root")
