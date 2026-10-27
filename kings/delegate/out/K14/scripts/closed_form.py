#!/usr/bin/env python3
"""K14: third implementation: the closed recursion of Theorem 3.4(a) for pawn-only contexts (a pass resets the e.p.
flag, as a king move does), compared with the least-fixed-point solver of dmodel.py on every context of <= 2+2 pawns on
files e..g (flat 7x6; 4579 contexts).  Prints the number of contexts and disagreements."""
import itertools, sys
from functools import lru_cache
sys.path.insert(0, 'scripts')
from dmodel import Ctx, solve
W, H = 7, 6
ctx = Ctx(W, H, True)

@lru_cache(None)
def LamL(wp, bp, ep):   # White to move, White forces a decisive event against a passing opponent
    for kind, nx in ctx.moves(wp, bp, ep, 0):
        if kind == 'win' or LamR(*nx): return True
    return False

@lru_cache(None)
def LamR(wp, bp, ep):   # Black to move, White wins
    if not LamL(wp, bp, -1): return False          # Black passes (e.p. flag reset)
    for kind, nx in ctx.moves(wp, bp, ep, 1):
        if kind == 'win' or not LamL(*nx): return False
    return True

@lru_cache(None)
def RhoR(wp, bp, ep):   # Black to move, Black wins
    for kind, nx in ctx.moves(wp, bp, ep, 1):
        if kind == 'win' or RhoL(*nx): return True
    return False

@lru_cache(None)
def RhoL(wp, bp, ep):   # White to move, Black wins
    if not RhoR(wp, bp, -1): return False          # White passes
    for kind, nx in ctx.moves(wp, bp, ep, 0):
        if kind == 'win' or not RhoR(*nx): return False
    return True

sqn = [chr(97 + f) + str(r + 1) for f in (4, 5, 6) for r in range(1, 5)]
def S(ns): return frozenset((int(n[1:]) - 1) * W + ord(n[0]) - 97 for n in ns)
n = bad = 0
for kw in range(3):
    for kb in range(3):
        for wn in itertools.combinations(sqn, kw):
            for bn in itertools.combinations(sqn, kb):
                if set(wn) & set(bn): continue
                wp, bp = S(wn), S(bn)
                d = solve(ctx, wp, bp, -1, 'dud')
                cf = ('W' if LamL(wp, bp, -1) else 'L' if RhoL(wp, bp, -1) else 'D',
                      'W' if LamR(wp, bp, -1) else 'L' if RhoR(wp, bp, -1) else 'D')
                n += 1
                if (d[0], d[1]) != cf:
                    bad += 1
                    if bad < 5: print('DISAGREE', wn, bn, d, cf)
print('contexts', n, 'disagreements', bad)
