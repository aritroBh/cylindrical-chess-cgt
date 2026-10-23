# value-level comparison: my G+*h outcome (flag persists across heap moves) vs cylcgt whole-board value, random small positions
import sys, random
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
sys.setrecursionlimit(1000000)
from cylcgt import pawns, cgt
pawns.components = lambda b, p: [p]
from eng import *
from lem1 import rand_small
def to_cyl(pos):
    n = len(pos)
    W = frozenset((f, r) for f in range(n) for r in range(1, 9) if pos[f][0] >> (r - 1) & 1)
    B = frozenset((f, r) for f in range(n) for r in range(1, 9) if pos[f][1] >> (r - 1) & 1)
    return pawns.Pos(W, B, None)
rng = random.Random(int(sys.argv[2])); N = int(sys.argv[1]); ok = bad = 0
while ok + bad < N:
    pos = rand_small(rng)
    if passed_ranks(pos, None, 'W') or passed_ranks(pos, None, 'B'): continue
    n = len(pos); board = pawns.Board(n, 8, True, True)
    try:
        g = pawns.value(board, to_cyl(pos))
    except pawns.RaceError:
        continue
    s = Solver(); mine = []; theirs = []
    for h in range(4):
        a = s.win(pos, None, h, 'W'); b = s.win(pos, None, h, 'B')
        mine.append({(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)])
        o = cgt.outcome(cgt.add(g, cgt.nimber(h)))
        theirs.append(o)
    mine = ''.join(mine); theirs = ''.join(theirs)
    if mine == theirs: ok += 1
    else: bad += 1; print('MISMATCH', pos, mine, theirs)
print('value-level G+*h: agree', ok, 'disagree', bad)
