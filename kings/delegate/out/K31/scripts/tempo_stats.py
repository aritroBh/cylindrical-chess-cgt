#!/usr/bin/env python3
# K31 task 4: for every +1 root (named by the leads Lw=1, Fw=0, Lb=-1, Fb=-1) of a configuration print, per root, the plies with
# which White forces the event with White / Black to move (reserve 0), and with Black to move / White to move (reserve -1),
# and how many legal moves the side to move has.  Written with lk_py (independent of lk.cpp).
import sys; sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31/scripts')
from lk_py import *
cyl = sys.argv[1] == 'cyl'; W = int(sys.argv[2]); H = int(sys.argv[3])
pairs = [(ord(p[0]) - 97, int(p[1:])) for p in sys.argv[4].split(',')]
lk = LK(W, H, cyl, pairs); N = 2
opts, S_, win = solve(lk, N)
def d(st):
    w = win[0].get(st); b = win[1].get(st)
    return ('W%d' % w) if w is not None else (('L%d' % b) if b is not None else 'D')
rows = []
for x in lk.nodes():
    # +1 test: reserves -2..2, both movers: (L,L) at -2; (L,W) at -1; (W,W) at 0, 1, 2
    o = {(c, s): d((x, c, s))[0] for c in (-2, -1, 0, 1, 2) for s in (0, 1)}
    if all(o[(-2, s)] == 'L' for s in (0, 1)) and o[(-1, 0)] == 'L' and o[(-1, 1)] == 'W' and all(o[(c, s)] == 'W' for c in (0, 1, 2) for s in (0, 1)):
        nW = len(opts[x][0]); nB = len(opts[x][1])
        rows.append((x, d((x, 0, 0)), d((x, 0, 1)), d((x, -1, 0)), d((x, -1, 1)), nW, nB))
print('config', sys.argv[1:5], 'roots with (L,L),(L,W),(W,W),(W,W),(W,W) against reserves -2..2:', len(rows))
slower = sum(1 for r in rows if int(r[1][1:]) > int(r[2][1:]))
print('White-to-move win slower than Black-to-move win (reserve 0):', slower, 'of', len(rows))
for x, a, b, c, e, nW, nB in rows[:int(sys.argv[5]) if len(sys.argv) > 5 else 12]:
    S, wk, bk = x
    print('  K%s k%s : alone WtM %s BtM %s | reserve -1: WtM %s BtM %s | #White moves %d #Black moves %d' % (name(wk), name(bk), a, b, c, e, nW, nB))
