# targeted value-level comparison: positions rich in double steps / e.p. rights
import sys, random
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
sys.setrecursionlimit(1000000)
from cylcgt import pawns, cgt
pawns.components = lambda b, p: [p]
from eng import *
def to_cyl(pos):
    n = len(pos)
    W = frozenset((f, r) for f in range(n) for r in range(1, 9) if pos[f][0] >> (r - 1) & 1)
    B = frozenset((f, r) for f in range(n) for r in range(1, 9) if pos[f][1] >> (r - 1) & 1)
    return pawns.Pos(W, B, None)
rng = random.Random(int(sys.argv[2])); N = int(sys.argv[1]); ok = bad = 0; epnodes = 0
def gen():
    n = rng.randint(5, 6); w = [0]*n; b = [0]*n
    for _ in range(rng.randint(3, 6)):
        f = rng.randrange(n)
        if rng.random() < .5:
            r = rng.choice((2, 2, 4, 5, 3)); w[f] |= 1 << (r-1)
        else:
            r = rng.choice((7, 7, 5, 4, 6)); b[f] |= 1 << (r-1)
    for f in range(n):
        x = w[f] & b[f]; w[f] &= ~x
    return tuple(zip(w, b))
while ok + bad < N:
    pos = gen()
    if passed_ranks(pos, None, 'W') or passed_ranks(pos, None, 'B'): continue
    n = len(pos); board = pawns.Board(n, 8, True, True)
    try: g = pawns.value(board, to_cyl(pos))
    except pawns.RaceError: continue
    s = Solver(); mine = ''; theirs = ''
    for h in range(4):
        a = s.win(pos, None, h, 'W'); b = s.win(pos, None, h, 'B')
        mine += {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)]
        theirs += cgt.outcome(cgt.add(g, cgt.nimber(h)))
    epnodes += sum(1 for k in s.memo if k[1] is not None)
    if mine == theirs: ok += 1
    else: bad += 1; print('MISMATCH', pos, mine, theirs)
print('targeted value-level: agree', ok, 'disagree', bad, 'flagged solver states visited', epnodes)
