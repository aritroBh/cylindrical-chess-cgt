import sys, time
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
sys.setrecursionlimit(1000000)
from cylcgt import pawns, cgt
from eng import ring
def to_cyl(pos, ep):
    n = len(pos)
    W = frozenset((f, r) for f in range(n) for r in range(1, 9) if pos[f][0] >> (r - 1) & 1)
    B = frozenset((f, r) for f in range(n) for r in range(1, 9) if pos[f][1] >> (r - 1) & 1)
    return pawns.Pos(W, B, None)
pawns.components = lambda b, p: [p]
pawns.RACE_RULE = 'count'; pawns.PASSED_RESPECTS_EP = True
pawns._value.cache_clear()
for spec in sys.argv[1:]:
    kind, n = spec[0], int(spec[1:])
    pos = to_cyl(ring(kind, n), None)
    t = time.time()
    g = pawns.value(pawns.Board(n, 8, True, True), pos)
    print(kind, n, 'pawns', len(pos.white) + len(pos.black), 'whole-board cylcgt value', cgt.show(g), 'outcome', cgt.outcome(g), '%.1fs' % (time.time() - t), flush=True)
