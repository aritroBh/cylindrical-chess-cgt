#!/usr/bin/env python3
"""Z_B regression: for the 8 roots of Z_B on flat 7x6, join (a) the one-ply kind of every legal move (oneply.py)
with (b) the exact P value after the move (kpp --pmodel --moves, output in logs/zb_moves.txt).
usage: zb_regression.py logs/zb_moves.txt  [--cyl W]"""
import sys, re
sys.path.insert(0, '.')
import oneply as O
flat = '--cyl' not in sys.argv
W = int(sys.argv[sys.argv.index('--cyl') + 1]) if not flat else 7
g = O.G(W, 6, flat); gf = {0, 1, 2}
tot = {'one-ply suicide': 0, 'one-ply shuttle': 0, 'one-ply other': 0, 'one-ply promotion': 0}
rows = []
loser_shuttle = 0; nonshuttle_exact_loss = 0; nonshuttle = 0
for line in open(sys.argv[1]):
    if '|' not in line or line.startswith('['): continue
    pos, val, mv = [x.strip() for x in line.split('|')[:3]] if line.count('|') >= 2 else (None, None, None)
    if pos is None: continue
    side = pos.split()[-2].upper()
    P = O.parse(pos)
    kinds = {}
    for m, npos, kind in O.analyse(g, P, gf, side):
        key = O.nm(m[1]) + O.nm(m[2])
        kinds[('P' if m[0] == 'P' else 'K') + key] = kind
    for tok in mv.split():
        name, v = tok.split(':')
        k = kinds.get(name[0] + name[1:3] + name[3:5] if False else name[0] + name[1:], None)
        if k is None:
            # kpp names like Kb2b1, Pb4b5 : from,to
            k = kinds.get(name[0] + name[1:5], '?')
        rows.append((pos, name, v, k))
shut_exact = {}
print('%-34s %-8s %-6s %s' % ('root', 'move', 'exact', 'one-ply kind'))
for pos, name, v, k in rows:
    print('%-34s %-8s %-6s %s' % (pos, name, v, k))
# summary: exact = the move loses for the mover (L when White moves, W when Black moves)
def loses(pos, v):
    side = pos.split()[-2]
    return (side == 'w' and v == 'L') or (side == 'b' and v == 'W')
nl = [r for r in rows if loses(r[0], r[2])]
print()
print('moves listed: %d ; exact-P losing moves: %d ; exact-P drawing (shuttle) moves: %d' % (len(rows), len(nl), sum(1 for r in rows if r[2] == 'D')))
for kind in ('suicide', 'shuttle', 'other', 'promotion', '?'):
    a = sum(1 for r in nl if r[3] == kind)
    b = sum(1 for r in rows if r[2] == 'D' and r[3] == kind)
    print('  among exact-losing moves, one-ply kind %-9s : %d     among exact-drawing moves: %d' % (kind, a, b))
