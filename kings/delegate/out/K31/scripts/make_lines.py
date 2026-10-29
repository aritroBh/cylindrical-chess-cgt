#!/usr/bin/env python3
# K31 task 4: write the principal variations of lk_py (minimum-distance winner, maximum-distance loser) as state files for bin/linechk.
# usage: make_lines.py cyl|flat W H pairs "root text" outdir tag
import sys; sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31/scripts')
from lk_py import *
cyl = sys.argv[1] == 'cyl'; W = int(sys.argv[2]); H = int(sys.argv[3])
pairs = [(ord(p[0]) - 97, int(p[1:])) for p in sys.argv[4].split(',')]
lk = LK(W, H, cyl, pairs); N = 2
opts, S_, win = solve(lk, N)
x0 = parse(lk, sys.argv[5]); outdir = sys.argv[6]; tag = sys.argv[7]
def outcome(st):
    w = win[0].get(st); b = win[1].get(st)
    return ('W', w) if w is not None else (('L', b) if b is not None else ('D', None))
def text(x):
    S, wk, bk = x
    return 'K%s k%s ' % (name(wk), name(bk)) + ' '.join(('%s%s' % (c, name((f, r)))) for (c, f, r) in sorted(S, key=lambda q: (q[0] != 'P', q[2], q[1])))
def pv(st, maxply=80):
    o = outcome(st); states = [st]; ev = None
    if o[0] == 'D': return states, None
    player = 0 if o[0] == 'W' else 1; dist = win[player]; winT = 1 if player == 0 else -1
    for _ in range(maxply):
        x_, c, s = st; cands = []
        for k, v in S_[st]:
            if k == 'T':
                if v == winT and s == player: cands.append((1, None))
            elif v in dist: cands.append((dist[v], v))
        if not cands: break
        best = min(cands, key=lambda t: t[0]) if s == player else max(cands, key=lambda t: t[0])
        if best[1] is None: ev = '+' if player == 0 else '-'; break
        st = best[1]; states.append(st)
    return states, ev
for c, s in [(0, 1), (0, 0), (-1, 0), (-1, 1), (1, 0)]:
    states, ev = pv((x0, c, s))
    fn = '%s/line_%s_c%+d_%s.txt' % (outdir, tag, c, 'B' if s else 'W')
    with open(fn, 'w') as f:
        for (x, cc, ss) in states: f.write('%s|%d|%d\n' % (text(x), cc, ss))
        if ev: f.write('EVENT|%s\n' % ev)
    print(fn, len(states), ev)
