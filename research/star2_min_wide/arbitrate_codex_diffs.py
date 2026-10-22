#!/usr/bin/env python3
"""arbitrate_codex_diffs.py FILE... : for every 'DIFFER <position>' line in the given check_parts_codex output files
(a) walk the game tree and list the MINIMAL states where cylcgt and the Codex canonical forms differ,
(b) arbitrate each such state with the naive definition of equality on the RAW game {children|children} (children = values both programs agree on),
(c) compare (outcome, nimber) of the whole position by cylcgt, by the Codex canonical form and by Codex's own bitmask test (_outcome_masks, no canonicalisation)."""
import sys, os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "verify_ext", "codex")); sys.path.insert(0, os.path.dirname(__file__))
import solver as cx
from common import *
class Raw:
    def __init__(self, L, R): self.L, self.R = tuple(L), tuple(R)
def LE(a, b):
    if isinstance(a, cgt.Game) and isinstance(b, cgt.Game): return cgt.le(a, b)
    return all(not LE(b, al) for al in a.L) and all(not LE(br, a) for br in b.R)
memo = {}
def conv(g):
    r = memo.get(g)
    if r is None: r = memo[g] = cgt.make([conv(x) for x in g.left], [conv(x) for x in g.right])
    return r
def width_of(pos): return max(f for f, _ in pos.white | pos.black) + 1
def masks_class(pg, state):
    lm, rm = pg._outcome_masks(*state)
    lf, rf = bool(lm & 1), bool(rm & 1)
    o = "N" if lf and rf else "L" if lf else "R" if rf else "P"
    k = next((k for k in range(300) if not ((lm >> k) & 1) and not ((rm >> k) & 1)), -1)
    return o, (k if k < 3 else -1)
total = bad_cyl = 0
for fn in sys.argv[1:]:
    for line in open(fn):
        if not line.startswith("DIFFER"): continue
        text = re.match(r"DIFFER (W: .*? / B: [a-z0-9 ]+?) \{", line).group(1)
        pos0 = pawns.Pos.parse(text); width = width_of(pos0)
        board = pawns.Board(width, 8, False, True); pg = cx.PawnGame(width, "count", True, "aware")
        def cxs(pos, mover):
            w = b = 0
            for f, r in pos.white: w |= 1 << ((r - 1) * width + f)
            for f, r in pos.black: b |= 1 << ((r - 1) * width + f)
            last = 0 if mover is None else (1 if mover == "W" else -1)
            if pos.ep:
                (tf, tr), _, cap = pos.ep
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
            okc = all([walk(q, m) for q, m in kids])
            gc = pawns._child(board, pos, mover) if (anyp and mover) else pawns.value(board, pos) if anyp else pawns._value(board, pos)
            gx = conv(pg._value(*cxs(pos, mover)))
            same = gc is gx; seen[key] = same
            if not same and okc: minimal.append((pos, mover, gc, gx))
            return same
        walk(pos0, None)
        res = []
        for pos, mover, gc, gx in minimal:
            plain = pawns.Pos(pos.white, pos.black, None)
            lpos = plain if (pos.ep and pos.ep[2] != "W") else pos
            rpos = plain if (pos.ep and pos.ep[2] != "B") else pos
            raw = Raw([pawns._child(board, q, "W") for q in pawns.moves(board, lpos, "W")], [pawns._child(board, q, "B") for q in pawns.moves(board, rpos, "B")])
            res.append((str(pos), LE(raw, gc) and LE(gc, raw), LE(raw, gx) and LE(gx, raw)))
        gc0, gx0 = pawns.value(board, pos0), conv(pg.value(*cxs(pos0, None)[:2]))
        cls_c = outcome_nim(gc0); cls_x = outcome_nim(gx0); cls_m = masks_class(pg, cxs(pos0, None))
        total += 1; bad_cyl += any(not r[1] for r in res)
        print(f"{text}: minimal differing states={len(res)}  cylcgt==raw: {[r[1] for r in res]}  codex==raw: {[r[2] for r in res]}  "
              f"(outcome,nim): cylcgt {cls_c} codex-form {cls_x} codex-bitmask {cls_m}", flush=True)
print(f"parts arbitrated={total}; parts where cylcgt disagreed with the raw-game definition: {bad_cyl}")
