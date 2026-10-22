#!/usr/bin/env python3
"""Symmetry check for mob_pawns (T35): the one-file shift of the Mobius strip is an automorphism.

phi(f, r, d) = (f + 1, r, d) for f < W-1, and phi(W-1, r, d) = (0, 9 - r, -d) (seam crossing: rank flip,
direction flip). A correct Mobius pawn game must have value(P) == value(phi(P)) for every position P.
usage: PYTHONPATH=. .venv/bin/python research/mobius/check_mob_symmetry.py WIDTH MAXP
"""
import sys
from research.mobius.pawn_values_mobius import enum_positions
from research.mobius import mob_pawns as mp
from cylcgt import cgt


def phi(p, W):
    f, r, d = p
    return (0, 9 - r, -d) if f == W - 1 else (f + 1, r, d)


def phi_pos(pos, W):
    return mp.Pos(frozenset(phi(p, W) for p in pos.white), frozenset(phi(p, W) for p in pos.black), None)


def show(fn):
    try:
        return cgt.show(fn())
    except mp.RaceError:
        return None


if __name__ == "__main__":
    W, M = int(sys.argv[1]), int(sys.argv[2])
    b = mp.Board(W, "mob")
    n = bad = races = 0
    for wsq, bsq in enum_positions(W, M):
        pos = mp.Pos(frozenset((f, r, 1) for f, r in wsq), frozenset((f, r, -1) for f, r in bsq))
        a = show(lambda: mp.value(b, pos))
        c = show(lambda: mp.value(b, phi_pos(pos, W)))
        n += 1
        if a is None or c is None:
            races += 1
            continue
        if a != c:
            bad += 1
            if bad <= 5:
                print("ASYMMETRY", pos, "->", phi_pos(pos, W), a, c)
    print("Mobius shift symmetry, width %d, <=%d pawns: positions %d, race-excluded %d, asymmetric %d" % (W, M, n, races, bad))
