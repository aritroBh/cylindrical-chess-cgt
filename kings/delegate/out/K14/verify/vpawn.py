#!/usr/bin/env python3
"""Referee's own pawn-only D-game generator + solver for G (+) dud_D on a flat W x H board (written from SPEC.md).
Terminal = a promotion (P model).  A pass (king shuttle) resets the e.p. right.
State: (white pawns tuple, black pawns tuple, ep square or None, side).  Square = (file, rank), ranks 1..H.
Computes (1) retrograde LFP with stage numbers on the product, (2) Lemma B check (some entering option is a
G-move at stage <= n-1), (3) the closed recursion of Theorem 3.4(a), and compares.
"""
import sys, itertools
from collections import defaultdict, deque

W, H = 7, 6


def children(wp, bp, ep, side):
    """list of ('T',) for a promotion, or ('S', (wp', bp', ep')) ."""
    out = []
    mine, theirs = (wp, bp) if side == 0 else (bp, wp)
    dr = 1 if side == 0 else -1
    start = 2 if side == 0 else H - 1
    last = H if side == 0 else 1
    occ = set(wp) | set(bp)
    def make(newmine, newtheirs, newep):
        return ((tuple(sorted(newmine)), tuple(sorted(newtheirs))) if side == 0
                else (tuple(sorted(newtheirs)), tuple(sorted(newmine)))) + (newep,)
    for (f, r) in mine:
        # forward
        t = (f, r + dr)
        if t not in occ:
            if t[1] == last:
                out.append(('T',))
            else:
                out.append(('S', make([p for p in mine if p != (f, r)] + [t], theirs, None)))
                t2 = (f, r + 2 * dr)
                if r == start and t2 not in occ:
                    out.append(('S', make([p for p in mine if p != (f, r)] + [t2], theirs, t)))
        for df in (-1, 1):
            c = (f + df, r + dr)
            if not (1 <= c[0] <= W):
                continue
            if c in theirs:
                if c[1] == last:
                    out.append(('T',))
                else:
                    out.append(('S', make([p for p in mine if p != (f, r)] + [c], [p for p in theirs if p != c], None)))
            elif ep is not None and c == ep:
                victim = (c[0], c[1] - dr)
                if victim in theirs:
                    out.append(('S', make([p for p in mine if p != (f, r)] + [c], [p for p in theirs if p != victim], None)))
    return out


def solve(root_x):
    """root_x = (wp, bp, ep). Explore states (x, side) reachable from both sides to move. Return dict of stages
    and results."""
    O = {}
    stack = [(root_x, 0), (root_x, 1)]
    while stack:
        st = stack.pop()
        if st in O: continue
        (wp, bp, ep), s = st
        opts = []
        for ch in children(wp, bp, ep, s):
            opts.append(('T', s) if ch[0] == 'T' else ('S', (ch[1], 1 - s)))
        opts.append(('S', ((wp, bp, None), 1 - s, 'pass')))  # pass: marked
        # normalise pass target
        opts[-1] = ('P', ((wp, bp, None), 1 - s))
        O[st] = opts
        for k, v in opts:
            if k in ('S', 'P'): stack.append(v)
    stage = {0: {}, 1: {}}  # sigma -> state -> stage
    for sigma in (0, 1):
        st_map = stage[sigma]
        n = 0
        while True:
            n += 1
            new = []
            for st, opts in O.items():
                if st in st_map: continue
                s = st[1]
                if s == sigma:
                    ok = any((k == 'T' and v == sigma) or (k in 'SP' and v in st_map and st_map[v] <= n - 1) for k, v in opts)
                else:
                    ok = all((k in 'SP' and v in st_map and st_map[v] <= n - 1) for k, v in opts)
                if ok: new.append(st)
            if not new: break
            for st in new: st_map[st] = n
    return O, stage


def res_of(stage, st):
    return 'W' if st in stage[0] else ('L' if st in stage[1] else 'D')


def lemmaB_check(O, stage):
    bad = 0; tot = 0
    for sigma in (0, 1):
        for st, n in stage[sigma].items():
            if st[1] != sigma: continue
            tot += 1
            good = False
            for k, v in O[st]:
                if k == 'T' and v == sigma: good = True
                elif k == 'S' and v in stage[sigma] and stage[sigma][v] <= n - 1: good = True
            if not good: bad += 1
    return tot, bad


# closed recursion of Theorem 3.4(a)
from functools import lru_cache

@lru_cache(None)
def LamL(x):
    wp, bp, ep = x
    return any(c[0] == 'T' or LamR(c[1]) for c in children(wp, bp, ep, 0))

@lru_cache(None)
def LamR(x):
    wp, bp, ep = x
    if not LamL((wp, bp, None)): return False
    return all(c[0] != 'T' and LamL(c[1]) for c in children(wp, bp, ep, 1))

@lru_cache(None)
def RhoR(x):
    wp, bp, ep = x
    return any(c[0] == 'T' or RhoL(c[1]) for c in children(wp, bp, ep, 1))

@lru_cache(None)
def RhoL(x):
    wp, bp, ep = x
    if not RhoR((wp, bp, None)): return False
    return all(c[0] != 'T' and RhoR(c[1]) for c in children(wp, bp, ep, 0))


def closed(x):
    return (('W' if LamL(x) else 'L' if RhoL(x) else 'D'), ('W' if LamR(x) else 'L' if RhoR(x) else 'D'))


def sq(name):
    return (ord(name[0]) - 96, int(name[1:]))


def contexts(files, maxw, maxb):
    squares = [(f, r) for f in files for r in range(2, H)]  # ranks 2..H-1
    for kw in range(maxw + 1):
        for kb in range(maxb + 1):
            for wn in itertools.combinations(squares, kw):
                for bn in itertools.combinations(squares, kb):
                    if set(wn) & set(bn): continue
                    yield tuple(sorted(wn)), tuple(sorted(bn))


if __name__ == '__main__':
    files = [5, 6, 7]
    n = bad = 0
    lb_tot = lb_bad = 0
    for wn, bn in contexts(files, 2, 2):
        x = (wn, bn, None)
        O, stage = solve(x)
        r = (res_of(stage, (x, 0)), res_of(stage, (x, 1)))
        c = closed(x)
        n += 1
        if r != c:
            bad += 1
            if bad < 4: print('DISAGREE', wn, bn, r, c)
        t, b = lemmaB_check(O, stage)
        lb_tot += t; lb_bad += b
    print('contexts', n, 'LFP-vs-closed disagreements', bad, '| Lemma B on', lb_tot, 'winning nodes, violations', lb_bad)
