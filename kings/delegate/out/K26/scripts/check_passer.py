#!/usr/bin/env python3
"""cross-check the passer flags of k26lib.Geo.configs against cylcgt.pawns.passed (PASSED_RESPECTS_EP = True) on all configs."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k26lib import Geo
from cylcgt.pawns import Board, Pos, passed, PASSED_RESPECTS_EP
print('PASSED_RESPECTS_EP =', PASSED_RESPECTS_EP)
for (W, H, wrap) in ((7, 6, False), (7, 6, True), (8, 6, True), (7, 7, False)):
    g = Geo(H)
    cfgs = g.configs(2, 2)
    b = Board(W, H, wrap, True)
    bad = 0
    for (wp, bp, occ, wa, ba, pw, pb, s) in cfgs:
        pos = Pos(frozenset((g.f[i] - 1, g.r[i]) for i in wp), frozenset((g.f[i] - 1, g.r[i]) for i in bp))
        if passed(b, pos, 'W') != pw or passed(b, pos, 'B') != pb:
            bad += 1
    print('board', W, H, 'wrap' if wrap else 'flat', 'configs', len(cfgs), 'mismatches', bad)
