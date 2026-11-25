"""K63 question 2: compare F2's P graph on flat 8x7 and flat 8x8 (kref63 dump outputs: '<position> | <W/L/D>', White's view).
usage: python3 cmp_boards.py DUMP87 DUMP88   Prints counts, the positions present on both boards whose values differ
(grouped), and a sample."""
import sys
from collections import Counter

def load(fn):
    d = {}
    for line in open(fn):
        p, v = line.rstrip('\n').split(' | ')
        d[p] = v
    return d

a, b = load(sys.argv[1]), load(sys.argv[2])
common = set(a) & set(b)
diff = sorted(p for p in common if a[p] != b[p])
print('nodes 8x7 %d, 8x8 %d, common %d, only 8x7 %d, only 8x8 %d' % (len(a), len(b), len(common), len(set(a) - set(b)), len(set(b) - set(a))))
print('value tally 8x7', dict(Counter(a.values())), ' 8x8', dict(Counter(b.values())))
print('common positions with different P values: %d' % len(diff))
print('  (8x7 -> 8x8) transitions:', dict(Counter((a[p], b[p]) for p in diff)))
def npawns(p):
    t = p.split()
    return sum(1 for x in t if x[0] == 'P'), sum(1 for x in t if x[0] == 'p')
print('  by pawn counts (White, Black):', dict(Counter(npawns(p) for p in diff)))
def rank7(p):
    return any(x[0] == 'P' and x[2] == '6' for x in p.split())
print('  with a White pawn on rank 6 (one step from promotion on 8x7):', sum(1 for p in diff if rank7(p)))
for p in diff[:40]:
    print('  %s : 8x7 %s, 8x8 %s' % (p, a[p], b[p]))
