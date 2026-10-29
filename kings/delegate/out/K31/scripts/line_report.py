#!/usr/bin/env python3
# K31 task 4: option tables and principal variations of a +1 root with reserves 0, -1 (Black has one spare move), +1.
# usage: line_report.py cyl|flat W H a2[,c4] "Kc3 ka4 Pa2 pa3 Pc4 pc5"
import sys; sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31/scripts')
from lk_py import *
cyl = sys.argv[1] == 'cyl'; W = int(sys.argv[2]); H = int(sys.argv[3])
pairs = [(ord(p[0]) - 97, int(p[1:])) for p in sys.argv[4].split(',')]
lk = LK(W, H, cyl, pairs); N = 2
opts, S_, win = solve(lk, N)
x = parse(lk, sys.argv[5])
def outcome(st):
    w = win[0].get(st); b = win[1].get(st)
    return ('W', w) if w is not None else (('L', b) if b is not None else ('D', None))
def fmt(o): return o[0] + ('' if o[1] is None else str(o[1]))
def mvname(st, nxt):
    (S0, w0, b0), c0, s0 = st; (S1, w1, b1), c1, s1 = nxt
    if (w0, b0) == (w1, b1): return 'pass'
    return ('K' + name(w1)) if s0 == 0 else ('k' + name(b1))
def options(st):
    rows = []
    for k, v in S_[st]:
        if k == 'T': rows.append('capture(event %s)' % ('+' if v == 1 else '-'))
        else: rows.append('%s -> %s' % (mvname(st, v), fmt(outcome(v))))
    return rows
def pv(st, maxply=60):
    o = outcome(st)
    if o[0] == 'D': return []
    player = 0 if o[0] == 'W' else 1
    dist = win[player]; winT = 1 if player == 0 else -1
    line = []
    for _ in range(maxply):
        x_, c, s = st
        cands = []
        for k, v in S_[st]:
            if k == 'T':
                if v == winT and s == player: cands.append((1, None))
            elif v in dist: cands.append((dist[v], v))
        if not cands: break
        best = min(cands, key=lambda t: t[0]) if s == player else max(cands, key=lambda t: t[0])
        if best[1] is None:
            line.append('x(event %s)' % ('+' if player == 0 else '-')); break
        line.append(('W:' if s == 0 else 'B:') + mvname(st, best[1])); st = best[1]
    return line
print('root', sys.argv[5], 'board', sys.argv[1] + ':%dx%d' % (W, H), 'pairs', sys.argv[4])
print('integer contexts (reserve c: c>0 White spare moves, c<0 Black spare moves); outcome with White to move / Black to move; Wk = White forces the event in k plies, Lk = Black does:')
for c in (-2, -1, 0, 1, 2): print('  c=%+d  White to move %s   Black to move %s' % (c, fmt(outcome((x, c, 0))), fmt(outcome((x, c, 1)))))
for c, s in [(0, 1), (0, 0), (-1, 0), (-1, 1), (1, 0)]:
    st = (x, c, s)
    print('node reserve %+d, %s to move: %s' % (c, 'White' if s == 0 else 'Black', fmt(outcome(st))))
    print('   options:', '; '.join(options(st)))
    print('   principal variation:', ' '.join(pv(st)))
