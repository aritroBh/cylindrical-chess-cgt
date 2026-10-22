"""Sanity: all legal KPK positions (either side to move) vs. those reachable from quiet placements."""
import sys
import vgraph

board = sys.argv[1]
G = vgraph.build(board)
s = G.solver
g = s.g
allk = []
for wk in range(g.N):
    for bk in range(g.N):
        if wk == bk or (g.king_mask[wk] >> bk) & 1:
            continue
        for p in range(g.N):
            if p in (wk, bk) or g.rank[p] in (0, g.H - 1):
                continue
            for stm in (0, 1):
                pos = (stm, wk, bk, (), 1 << p, 0, -1)
                if s.in_check(pos, 1 - stm):
                    continue
                allk.append(pos)
reach = {p for p in G.pos if p[4]}
sall = set(allk)
miss = [p for p in allk if p not in reach]
extra = [p for p in reach if p not in sall]
print(board, 'legal KPK', len(allk), 'reachable', len(reach), 'unreachable', len(miss), 'extra', len(extra))
for p in miss[:6]:
    print('  unreachable stm', p[0], 'K', g.sqname(p[1]), 'k', g.sqname(p[2]), 'P', [g.sqname(i) for i in range(g.N) if p[4] >> i & 1],
          'bk in check by pawn' if s.in_check(p, 1) else '')
