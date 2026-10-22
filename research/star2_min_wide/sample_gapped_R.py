#!/usr/bin/env python3
"""sample_gapped_R.py MOD [CODEX] < scanner_tsv : for gapped rows with crc32(position) % MOD == 0 compare the scanner (whole-board, e.p. rights
persist per component) with the cylcgt WHOLE-BOARD game (pawns.components = lambda b,p:[p]; real-chess e.p. expiry) and,
with the 2nd argument CODEX, with the independent Codex whole-board solver.  (outcome, nimber) of each."""
import sys, os, zlib, time, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "verify_ext", "codex"))
import solver as cx
from common import *
MOD = int(sys.argv[1]); USE_CODEX = len(sys.argv) > 2
pawns.components = lambda b, p: [p]
memo = {}
def conv(g):
    r = memo.get(g)
    if r is None: r = memo[g] = cgt.make([conv(x) for x in g.left], [conv(x) for x in g.right])
    return r
cxgames = {}
n = bad_c = bad_x = bad_cx = 0; t0 = time.time(); conf = collections.Counter(); ex = []
for line in sys.stdin:
    if line.startswith("#"): continue
    pos, width, npaw, res = line.rstrip("\n").split("\t")
    W, B = parse_pos(pos)
    if len(occupied_groups(W, B)) < 2 or zlib.crc32(pos.encode()) % MOD: continue
    width = int(width)
    g = pawns.value(pawns.Board(width, 8, False, True), pawns.Pos(frozenset(W), frozenset(B)))
    oc = outcome_nim(g); sc = (res.split(",")[0], int(res.split(",")[1]))
    n += 1
    if oc != sc:
        bad_c += 1
        if len(ex) < 10: ex.append((pos, "scanner", sc, "cylcgt-whole", oc))
    if USE_CODEX:
        pg = cxgames.setdefault(width, cx.PawnGame(width, "count", True, "aware"))
        cg = conv(pg.value(*cx.parse_position(pos.replace(":", ""), width)))
        if cg is not g: bad_cx += 1; ex.append((pos, "cylcgt-whole vs codex differ", cgt.show(g)[:50], cgt.show(cg)[:50]))
    if n % 200 == 0:
        pawns._value.cache_clear(); cgt._le_memo.clear(); cgt._add_memo.clear(); cgt._neg_memo.clear()
        print(f"  ..{n} {time.time()-t0:.0f}s", file=sys.stderr, flush=True)
print(f"sampled gapped rows={n}  scanner!=cylcgt-whole-board: {bad_c}   cylcgt-whole!=codex: {bad_cx}  elapsed={time.time()-t0:.0f}s")
for e in ex: print("EXAMPLE", *e)
