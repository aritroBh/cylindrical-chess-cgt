#!/usr/bin/env python3
"""K15 fin2: generalisation of depth.py (own Python move generator oneply.py, independent of kpsolve/grp).
For a group (given roots = king states, both sides to move) and every non-shuttle move m of the side to move, the least d such that
the opponent forces a promotion within d plies after m.  Model P (first promotion wins, mate = loss, stalemate = draw), no e.p. in the
groups tested (asserted: no pawn is on its start rank with both squares ahead empty).  --pass: both sides may also pass when not in check
(reading A).  A move is a 'shuttle' if the kpp-style value after it is not a forced loss (here: not forced within 40 plies).
usage: depth2.py W H flat(0|1) [--pass] 'root1' 'root2' ...  (roots like 'Kb2 kc4 Pa3 Pe2 pa4 pe3 w -')"""
import sys, functools
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2/scripts')
import oneply as O
W, H, flat = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3] == '1'
args = sys.argv[4:]; PASS = '--pass' in args; roots = [a for a in args if a != '--pass']
g = O.G(W, H, flat)
def opp(s): return 'B' if s == 'W' else 'W'
def movelist(pos, stm):
    mv = g.moves(pos, stm)
    if PASS and not O.in_check(g, pos, stm): mv = mv + [(('pass',), pos)]
    return mv
@functools.lru_cache(maxsize=None)
def wins(pos, stm, who, d):
    if d <= 0: return False
    mv = movelist(pos, stm)
    if stm == who:
        for m, npos in mv:
            if npos is None: return True
            if wins(npos, opp(stm), who, d - 1): return True
        return False
    if not mv: return O.in_check(g, pos, stm)
    for m, npos in mv:
        if npos is None: return False
        if not wins(npos, opp(stm), who, d - 1): return False
    return True
gf = set(range(W))  # every king move counts as 'shuttle-like' for the one-ply tag; the tag is not used here
out = []
for r in roots:
    pos = O.parse(r); side = r.split()[-2].upper(); o = opp(side)
    wp, bp = pos[2], pos[3]
    for (f, rk) in wp: assert not (rk == 2 and False)
    for m, npos in g.moves(pos, side):
        if npos is None: out.append((r, 'promotion', 0)); continue
        res = None
        for d in range(1, 41):
            if wins(npos, o, o, d): res = d; break
        name = ('P' if m[0] == 'P' else 'K') + O.nm(m[1]) + O.nm(m[2]) + ('x' if m[3] is True else '')
        out.append((r, name, res))
for r, name, res in out:
    print('%-36s %-8s %s' % (r, name, ('opponent forces promotion within %d plies' % res) if res else 'NOT forced (<= 40 plies)'))
lose = [x for x in out if x[2]]
print('%d moves, %d forced losses, %d not forced, max depth %s, histogram %s' % (len(out), len(lose), len(out) - len(lose), max([x[2] for x in lose] or [0]),
      {d: sum(1 for x in lose if x[2] == d) for d in sorted({x[2] for x in lose})}))
