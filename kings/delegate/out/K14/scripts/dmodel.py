#!/usr/bin/env python3
"""K14: independent D-model solver for G (+) dud_D  (Theorem 3.4(a), here by plain least-fixed-point retrograde
analysis on the product graph, NOT by the closed recursion), for a pawn-only context G on a flat WxH board.

G is the pawn-only game of SPEC.md without kings: push, double push from the second rank, captures, en passant
(optional), promotion = decisive event for the mover (terminal, the P-model).  The pass of dud_D is a move
that changes nothing except that it clears an e.p. right (a pass is a king shuttle in chess).

Also solves G (+) on_D, G (+) off_D and G alone (normal play: a side with no move loses) for cross-checks.

State = (white pawn squares, black pawn squares, ep target or -1, side to move).  Square = rank*W + file.
"""
import sys
from functools import lru_cache


class Ctx:
    def __init__(self, W, H, ep=True):
        self.W, self.H, self.ep = W, H, ep

    def moves(self, wp, bp, ep, side):
        """yield ('win', None) for a promotion, or ('mv', (wp', bp', ep')) for an ordinary pawn move."""
        W, H = self.W, self.H
        mine, theirs = (wp, bp) if side == 0 else (bp, wp)
        d = 1 if side == 0 else -1
        start = 1 if side == 0 else H - 2
        last = H - 1 if side == 0 else 0
        occ = wp | bp
        for p in sorted(mine):
            f, r = p % W, p // W
            t = p + d * W
            if t not in occ:
                if t // W == last:
                    yield ('win', None)
                else:
                    yield ('mv', self.mk(side, mine - {p} | {t}, theirs, -1))
                    if r == start and (t + d * W) not in occ:
                        t2 = t + d * W
                        e = t if self.ep else -1
                        yield ('mv', self.mk(side, mine - {p} | {t2}, theirs, e))
            for df in (-1, 1):
                if not (0 <= f + df < W): continue
                c = (r + d) * W + f + df
                if c in theirs:
                    if c // W == last:
                        yield ('win', None)
                    else:
                        yield ('mv', self.mk(side, mine - {p} | {c}, theirs - {c}, -1))
                elif c == ep and self.ep:
                    cap = c - d * W  # the double-stepped pawn stands behind the target
                    if cap in theirs:
                        yield ('mv', self.mk(side, mine - {p} | {c}, theirs - {cap}, -1))

    @staticmethod
    def mk(side, mine, theirs, ep):
        return (frozenset(mine), frozenset(theirs), ep) if side == 0 else (frozenset(theirs), frozenset(mine), ep)


def solve(ctx, wp0, bp0, ep0, mode):
    """mode: 'dud' | 'on' | 'off' | 'none'.  returns dict state->('W'|'D'|'L') for reachable states (x,side).
    Passes: 'dud' both, 'on' White only, 'off' Black only, 'none' neither (normal play: no move = loss)."""
    start = [((frozenset(wp0), frozenset(bp0), ep0), s) for s in (0, 1)]
    opts = {}
    stack = list(start)
    while stack:
        st = stack.pop()
        if st in opts: continue
        (wp, bp, ep), s = st
        o = []
        for kind, nx in ctx.moves(wp, bp, ep, s):
            if kind == 'win': o.append(('T', s))
            else: o.append(('S', (nx, 1 - s)))
        if mode == 'dud' or (mode == 'on' and s == 0) or (mode == 'off' and s == 1):
            o.append(('S', ((wp, bp, -1), 1 - s)))
        opts[st] = o
        for k, v in o:
            if k == 'S': stack.append(v)
    win = {0: set(), 1: set()}
    for sigma in (0, 1):
        Wn = win[sigma]
        changed = True
        while changed:
            changed = False
            for st, o in opts.items():
                if st in Wn: continue
                s = st[1]
                if s == sigma:
                    ok = any((k == 'T' and v == sigma) or (k == 'S' and v in Wn) for k, v in o)
                else:
                    # sigma-bar to move: no option loses (normal play); an own terminal refutes
                    ok = all((k == 'S' and v in Wn) for k, v in o) if o else True
                    # a sigma-bar terminal in o has k=='T' and v!=sigma -> all() fails, correct.
                if ok:
                    Wn.add(st); changed = True
    res = {}
    for st in opts:
        res[st] = 'W' if st in win[0] else ('L' if st in win[1] else 'D')
    return {s: res[(start[s][0], s)] for s in (0, 1)}


def sqs(names, W):
    out = set()
    for n in names:
        out.add((int(n[1:]) - 1) * W + (ord(n[0]) - 97))
    return out


if __name__ == '__main__':
    W, H = 7, 6
    ctx = Ctx(W, H, True)
    for desc in sys.argv[1:]:
        wn, bn = desc.split('/')
        wp, bp = sqs(wn.split(), W), sqs(bn.split(), W)
        print(desc, {m: solve(ctx, wp, bp, -1, m) for m in ('dud', 'on', 'none')})
