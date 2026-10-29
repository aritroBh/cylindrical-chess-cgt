#!/usr/bin/env python3
"""K26 own implementation of the D-model sum G (+) Z for a pawn-only context G and a reservoir Z (LOOPY 1.2, 3, 4).

G: pawns on a few files of a WxH board (no wrap needed: contexts stand on files at distance >= 2 from F_Z, or >= 2 files
from each other's wrap).  Moves: single step, double step from the start rank (sets an e.p. right only when an enemy
pawn could capture), captures, e.p. capture.  Any pawn move to the last rank (also a capture) is a decisive terminal
(P model: the first promotion wins for the promoter).  A Z-move resets the e.p. flag (a king move kills the right).
A player with no option anywhere loses (normal play).  Infinite play is a draw.  Results by least fixed point.

Reservoirs (Z nodes; L = White options, R = Black options):
  dud   : w0: L={w0}, R={w0}
  on    : w0: L={w0}, R={}
  off   : w0: L={},  R={w0}
  over  : w0: L={z}, R={w0};  z: no options        (White has the unique freezing move, Black passes)
  under : w0: L={w0}, R={z};  z: no options        (Black freezes, White passes)
"""
import itertools, collections

RES = {
    'dud': {'w0': ([ 'w0'], ['w0'])},
    'on': {'w0': (['w0'], [])},
    'off': {'w0': ([], ['w0'])},
    'over': {'w0': (['z'], ['w0']), 'z': ([], [])},
    'under': {'w0': (['w0'], ['z']), 'z': ([], [])},
    'none': {'z': ([], [])},     # no reservoir at all (G alone)
}


def g_moves(wp, bp, ep, stm, H):
    """yield (kind, wp', bp', ep') with kind 'S' (new position) or 'T' (decisive: the mover wins at once).
    wp, bp: frozensets of (file, rank); ep: None or (target, captured) valid for the side to move"""
    mine, theirs = (wp, bp) if stm == 0 else (bp, wp)
    d = 1 if stm == 0 else -1
    start = 2 if stm == 0 else H - 1
    last = H if stm == 0 else 1
    occ = wp | bp
    out = []
    for (f, r) in sorted(mine):
        r1 = r + d
        # step
        if (f, r1) not in occ:
            if r1 == last:
                out.append(('T',))
            else:
                nm = (mine - {(f, r)}) | {(f, r1)}
                out.append(('S', nm, theirs, None))
                if r == start and (f, r + 2 * d) not in occ:
                    nm2 = (mine - {(f, r)}) | {(f, r + 2 * d)}
                    cap_possible = any((f + df, r + 2 * d) in theirs for df in (-1, 1))
                    e = ((f, r1), (f, r + 2 * d)) if cap_possible else None
                    out.append(('S', nm2, theirs, e))
        # captures
        for df in (-1, 1):
            t = (f + df, r1)
            if t in theirs:
                if r1 == last:
                    out.append(('T',))
                else:
                    nm = (mine - {(f, r)}) | {t}
                    out.append(('S', nm, theirs - {t}, None))
            elif ep is not None and ep[0] == t:
                nm = (mine - {(f, r)}) | {t}
                out.append(('S', nm, theirs - {ep[1]}, None))
    res = []
    for o in out:
        if o[0] == 'T':
            res.append(('T',))
        else:
            _, nm, nt, e = o
            if stm == 0:
                res.append(('S', nm, nt, e))
            else:
                res.append(('S', nt, nm, e))
    return res


def solve(roots, reservoir, H):
    """roots: list of (wp, bp, ep, stm) with the reservoir at its first node.  Returns dict root -> 'W'/'D'/'L'
    (White's point of view)."""
    Z = RES[reservoir]
    z0 = 'w0' if 'w0' in Z else 'z'
    states = {}
    stack = []
    for (wp, bp, ep, stm) in roots:
        stack.append((wp, bp, ep, z0, stm))
    while stack:
        st = stack.pop()
        if st in states:
            continue
        wp, bp, ep, z, stm = st
        succ = []
        for m in g_moves(wp, bp, ep, stm, H):
            if m[0] == 'T':
                succ.append(('T', stm))
            else:
                ns = (m[1], m[2], m[3], z, 1 - stm)
                succ.append(('S', ns))
                stack.append(ns)
        zl, zr = Z[z]
        for zn in (zl if stm == 0 else zr):
            ns = (wp, bp, None, zn, 1 - stm)
            succ.append(('S', ns))
            stack.append(ns)
        states[st] = succ
    wins = {}
    for sigma in (0, 1):
        win = set()
        changed = True
        while changed:
            changed = False
            for st, succ in states.items():
                if st in win:
                    continue
                s = st[4]
                good = [(k == 'T' and x == sigma) or (k == 'S' and x in win) for (k, x) in succ]
                ok = any(good) if s == sigma else all(good)
                if ok:
                    win.add(st)
                    changed = True
        wins[sigma] = win
    out = {}
    for (wp, bp, ep, stm) in roots:
        st = (wp, bp, ep, z0, stm)
        out[(wp, bp, ep, stm)] = 'W' if st in wins[0] else ('L' if st in wins[1] else 'D')
    return out
