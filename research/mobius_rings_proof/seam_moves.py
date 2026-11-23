"""seam_moves.py FAM m -- what the seam does: for the root of FAM(m), every move of a pawn on files n-2, n-1, 0, 1,
its class (T/L/P/K) on the strip and on the cylinder, and the first winning reply of the opponent for P-moves.
Then, over all nodes of the reduced strip graph, the classes of moves of pawns on those four files."""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgame import Board, parse_ring, fmt
from rgraph import FAM, reduced

def cls_move(B, ch, side):
    c = B.classify(ch, side)
    if c > 0: return 'T', None
    if c < 0: return 'L', None
    for d, g in B.moves(ch, 1 - side):
        if B.classify(g, 1 - side) > 0: return 'P', d
    return 'K', None

def name(d):
    f0, r0, k, f1, r1 = d
    return '%d.%d%s%d.%d' % (f0, r0, {'s': '-', 'd': '=', 'x': 'x', 'e': 'xep'}[k], f1, r1)

fam, m = sys.argv[1], int(sys.argv[2]); ring = FAM[fam](m); root = parse_ring(ring); n = len(root[0])
files = [n - 2, n - 1, 0, 1]
print('# %s(%d) n=%d: %s   (moves as file.rank; files 0..n-1; seam between %d and 0)' % (fam, m, n, ring, n - 1))
for twist in (True, False):
    B = Board(n, twist)
    print('## %s' % ('STRIP' if twist else 'CYLINDER'))
    for side in (0, 1):
        for d, ch in B.moves(root, side):
            if d[0] not in files: continue
            c, rep = cls_move(B, ch, side)
            print('  %s %-12s %s%s' % ('White' if side == 0 else 'Black', name(d), c,
                                       ('  (reply %s)' % name(rep)) if rep else ''))
B, root, nodes = reduced(ring, True)
cnt = collections.Counter()
for p in nodes:
    for side in (0, 1):
        for d, ch in B.moves(p, side):
            if d[0] in files: cnt[(d[0], cls_move(B, ch, side)[0])] += 1
print('## all %d nodes of the reduced strip graph: (file, class) -> number of moves' % len(nodes))
for k in sorted(cnt): print('  file %d class %s: %d' % (k[0], k[1], cnt[k]))
