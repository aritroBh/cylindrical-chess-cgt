#!/usr/bin/env python3
"""diag_canon.py: decide who is right when cylcgt and the Codex solver give different canonical forms for the same position
(state W: a2 a4 d2 / B: b5 c3, White just moved, 4 files).  The raw game {Left-children | Right-children} (children = canonical values both programs
agree on) is compared with each candidate by the NAIVE recursive definition A<=B iff no A^L>=B and no B^R<=A (raw game never simplified)."""
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "verify_ext", "codex")); sys.path.insert(0, os.path.dirname(__file__))
import solver as cx
from common import *
class Raw:
    def __init__(self, L, R): self.L, self.R = tuple(L), tuple(R)
def LE(a, b):
    if isinstance(a, cgt.Game) and isinstance(b, cgt.Game): return cgt.le(a, b)
    return all(not LE(b, al) for al in a.L) and all(not LE(br, a) for br in b.R)
width = 4; board = pawns.Board(width, 8, False, True); pg = cx.PawnGame(width, "count", True, "aware")
memo = {}
def conv(g):
    r = memo.get(g)
    if r is None: r = memo[g] = cgt.make([conv(x) for x in g.left], [conv(x) for x in g.right])
    return r
pos = pawns.Pos.parse(sys.argv[1] if len(sys.argv) > 1 else "W: a2 a4 d2 / B: b5 c3")
kidsL = [pawns._child(board, q, "W") for q in pawns.moves(board, pos, "W")]
kidsR = [pawns._child(board, q, "B") for q in pawns.moves(board, pos, "B")]
raw = Raw(kidsL, kidsR)
cyl = pawns._value(board, pos)
w = b = 0
for f, r in pos.white: w |= 1 << ((r - 1) * width + f)
for f, r in pos.black: b |= 1 << ((r - 1) * width + f)
cxg = conv(pg._value(w, b, -1, 1))
print("cylcgt canonical :", cgt.show(cyl))
print("codex  (conv'd)  :", cgt.show(cxg))
for name, cand in (("cylcgt", cyl), ("codex", cxg)):
    print(f"raw game == {name} form ?  raw<=cand: {LE(raw, cand)}  cand<=raw: {LE(cand, raw)}")
print("cylcgt == codex as games:", cgt.le(cyl, cxg) and cgt.le(cxg, cyl))
