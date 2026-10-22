#!/usr/bin/env python3
"""check_parts_codex.py K [LO HI]: for the connected parts with K pawns (parts_k{K}.tsv, rows LO..HI) compare the cylcgt value with the
value computed by the independent Codex solver (verify_ext/codex/solver.py PawnGame(width,'count',True,'aware')), as short games
(Codex Game -> cylcgt canonical form -> identity)."""
import sys, os, time
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "verify_ext", "codex"))
import solver as cx
from common import *
K = int(sys.argv[1]); rows = [l.rstrip("\n").split("\t") for l in open(f"parts_k{K}.tsv") if not l.startswith("#")]
LO, HI = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, len(rows))
memo = {}
def conv(g):
    r = memo.get(g)
    if r is None: r = memo[g] = cgt.make([conv(x) for x in g.left], [conv(x) for x in g.right])
    return r
games = {}; n = bad = 0; t0 = time.time()
for text, width, nw, nb, o, nim, shown in rows[LO:HI]:
    width = int(width)
    pg = games.setdefault(width, cx.PawnGame(width, "count", True, "aware"))
    c = conv(pg.value(*cx.parse_position(text.replace(":", ""), width)))
    W, B = parse_pos(text)
    g = value_of_part(width, W, B)
    n += 1
    if c is not g:
        bad += 1; print("DIFFER", text, cgt.show(g)[:60], "codex:", cgt.show(c)[:60])
    if n % 500 == 0: print(f"  ..{n} done {time.time()-t0:.0f}s", file=sys.stderr, flush=True)
print(f"k={K} rows {LO}..{HI}: compared={n} DIFFER={bad} elapsed={time.time()-t0:.0f}s")
