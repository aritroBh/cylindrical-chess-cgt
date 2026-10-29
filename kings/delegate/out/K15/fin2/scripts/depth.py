#!/usr/bin/env python3
"""K15 fin2: for each of the 26 non-shuttle moves of Z_B (flat 7x6, 8 roots) the least number of plies d such that the
opponent forces a promotion within d plies counted from the position AFTER the move (model P, first promotion wins,
checkmate = loss for the mated side, stalemate = draw, no e.p. possible here), found by iterative deepening with a memo.
Own generator: oneply.py (written for this task, independent of kpsolve).  Prints one line per move."""
import sys, functools
sys.path.insert(0, '.')
import oneply as O
g = O.G(7, 6, True)
def opp(s): return 'B' if s == 'W' else 'W'
@functools.lru_cache(maxsize=None)
def wins(pos, stm, who, d):
    """can `who` force a promotion within d plies (d>=1 counts the next ply) with `stm` to move at pos?"""
    if d <= 0: return False
    mv = g.moves(pos, stm)
    if stm == who:
        for m, npos in mv:
            if npos is None: return True            # promotion
            if wins(npos, opp(stm), who, d - 1): return True
        return False
    if not mv:
        return O.in_check(g, pos, stm)              # mated side loses; stalemate is a draw
    for m, npos in mv:
        if npos is None: return False               # the defender promotes (never happens here)
        if not wins(npos, opp(stm), who, d - 1): return False
    return True
roots = [l.strip() for l in open(sys.argv[1]) if l.strip()]
gf = {0, 1, 2}
allmax = 0; rows = []
for r in roots:
    pos = O.parse(r); side = r.split()[-2].upper()
    for m, npos, kind in O.analyse(g, pos, gf, side):
        if npos is None: print('promotion at root?', r); continue
        o = opp(side); res = None
        for d in range(1, 16):
            if wins(npos, o, o, d): res = d; break
        name = ('P' if m[0] == 'P' else 'K') + O.nm(m[1]) + O.nm(m[2])
        rows.append((r, name, res, kind))
for r, name, res, kind in rows:
    print('%-32s %-8s opponent forces promotion within %s plies after the move (one-ply kind: %s)' % (r, name, res if res else '>15 (not forced)', kind))
lose = [x for x in rows if x[2]]
print('moves %d, forced losses %d, max depth %d, depth histogram %s' % (len(rows), len(lose), max(x[2] for x in lose),
      {d: sum(1 for x in lose if x[2] == d) for d in sorted({x[2] for x in lose})}))
