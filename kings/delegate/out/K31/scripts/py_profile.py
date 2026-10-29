#!/usr/bin/env python3
# K31: Python (lk_py) leads Lw, Fw, Lb, Fb for every root, to compare with `tempo profile` (C++, built on lk.cpp).
import sys, json; sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31/scripts')
from lk_py import *
import collections
cyl = sys.argv[1] == 'cyl'; W = int(sys.argv[2]); H = int(sys.argv[3]); N = int(sys.argv[4])
pairs = [(ord(p[0]) - 97, int(p[1:])) for p in sys.argv[5].split(',')]
lk = LK(W, H, cyl, pairs)
opts, S_, win = solve(lk, N)
def w(st, p): return win[p].get(st)
hist = collections.Counter()
for x in lk.nodes():
    Lw = Fw = Lb = Fb = -1
    for n in range(0, N + 1):
        if w((x, -n, 1), 0) is not None: Lw = n
        if w((x, -n, 0), 0) is not None: Fw = n
        if w((x, n, 0), 1) is not None: Lb = n
        if w((x, n, 1), 1) is not None: Fb = n
    hist['Lw=%d Fw=%d Lb=%d Fb=%d' % (Lw, Fw, Lb, Fb)] += 1
print('PYPROFILE', sys.argv[1:], 'roots', sum(hist.values()))
for k, v in sorted(hist.items()): print('  %-34s %8d' % (k, v))
