#!/usr/bin/env python3
"""diag_codex_diff.py "W: .. / B: .." WIDTH : walk the cylcgt game tree of a position and find the MINIMAL states (all children agree) where the cylcgt value and the
Codex solver value (verify_ext/codex/solver.py, same rules: count / e.p. / aware) differ as short games."""
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "verify_ext", "codex"))
import solver as cx
from common import *
text, width = sys.argv[1], int(sys.argv[2])
board = pawns.Board(width, 8, False, True); pg = cx.PawnGame(width, "count", True, "aware")
memo = {}
def conv(g):
    r = memo.get(g)
    if r is None: r = memo[g] = cgt.make([conv(x) for x in g.left], [conv(x) for x in g.right])
    return r
def cx_state(pos, mover):
    w = b = 0
    for f, r in pos.white: w |= 1 << ((r - 1) * width + f)
    for f, r in pos.black: b |= 1 << ((r - 1) * width + f)
    last = 0 if mover is None else (1 if mover == "W" else -1)
    if pos.ep:
        (tf, tr), (vf, vr), cap = pos.ep
        return w, b, (tr - 1) * width + tf, (-1 if cap == "W" else 1)
    return w, b, -1, last
seen = {}; minimal = []
def walk(pos, mover):
    key = (pos.white, pos.black, pos.ep, mover)
    if key in seen: return seen[key]
    anyp = pawns.passed(board, pos, "W") or pawns.passed(board, pos, "B")
    kids = []
    if not anyp:
        plain = pawns.Pos(pos.white, pos.black, None)
        lpos = plain if (pos.ep and pos.ep[2] != "W") else pos
        rpos = plain if (pos.ep and pos.ep[2] != "B") else pos
        kids = [(q, "W") for q in pawns.moves(board, lpos, "W")] + [(q, "B") for q in pawns.moves(board, rpos, "B")]
    ok_children = True
    for q, m in kids:
        if not walk(q, m): ok_children = False
    if anyp and mover is not None: g_cyl = pawns._child(board, pos, mover)
    elif anyp: g_cyl = pawns.value(board, pos)
    else: g_cyl = pawns._value(board, pos)
    g_cx = conv(pg._value(*cx_state(pos, mover)))
    same = (g_cyl is g_cx)
    seen[key] = same
    if not same and ok_children: minimal.append((pos, mover, g_cyl, g_cx))
    return same
root = pawns.Pos.parse(text)
walk(root, None)
print("states visited:", len(seen), " differing:", sum(1 for v in seen.values() if not v), " minimal differing states:", len(minimal))
for pos, mv, a, b in minimal[:6]:
    print("MINIMAL", pos, "ep=", pos.ep, "mover=", mv, "\n   cylcgt:", cgt.show(a)[:150], "\n   codex :", (cgt.show(b)[:150] if b else None))
