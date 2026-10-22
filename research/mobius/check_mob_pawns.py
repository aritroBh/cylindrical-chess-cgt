#!/usr/bin/env python3
"""Checks for research/mobius/mob_pawns.py (run from the project root with PYTHONPATH=.).

1. Seam geometry (RULES.md 1.1): shift() on the Mobius board.
2. Agreement with cylcgt.pawns on flat and cylinder boards, for every position of the T9 enumeration
   with up to MAXP pawns on WIDTH files (value strings and race errors must match exactly).
3. On positions whose pawns never touch a seam file, the Mobius value equals the flat value.
usage: .venv/bin/python research/mobius/check_mob_pawns.py WIDTH MAXP
"""
import sys
from itertools import combinations

from cylcgt import pawns as cyl
from cylcgt import cgt
from research.mobius import mob_pawns as mp


def squares(width):
    return [(f, r) for f in range(width) for r in range(1, 9)]


def enum_positions(width, maxp):
    """Every (white squares, black squares) with 1..maxp pawns: the T9 enumeration, each once."""
    sq = squares(width)
    for total in range(1, maxp + 1):
        for wc in range(total + 1):
            for wsq in combinations(sq, wc):
                rem = [s for s in sq if s not in wsq]
                for bsq in combinations(rem, total - wc):
                    yield wsq, bsq


def to_mob(wsq, bsq):
    return mp.Pos(frozenset((f, r, 1) for f, r in wsq), frozenset((f, r, -1) for f, r in bsq))


def to_cyl(wsq, bsq):
    return cyl.Pos(frozenset(wsq), frozenset(bsq))


def val_str(fn):
    try:
        return cgt.show(fn())
    except mp.RaceError:
        return "RACE"
    except cyl.RaceError:
        return "RACE"


def seam_tests():
    b = mp.Board(8, "mob")
    assert mp.shift(b, 7, 2, 1, 1) == (0, 6, True), mp.shift(b, 7, 2, 1, 1)   # h2 up-right -> a6
    assert mp.shift(b, 0, 5, -1, 0) == (7, 4, True)                          # a5 left -> h4
    assert mp.shift(b, 7, 8, 1, 0) == (0, 1, True)                           # h8 right -> a1
    assert mp.shift(b, 7, 1, 1, 1) == (0, 7, True)                           # h1 up-right -> a7 (seam flip)
    assert mp.shift(b, 3, 8, 0, 1) is None                                   # off the top rank
    assert mp.shift(b, 3, 4, 1, 1) == (4, 5, False)                          # ordinary step
    c = mp.Board(8, "cyl")
    assert mp.shift(c, 7, 2, 1, 1) == (0, 3, True)                           # cylinder: no flip
    print("seam geometry: OK")


def compare_cylinder_flat(width, maxp):
    checked = 0
    for kind in ("flat", "cyl"):
        mb = mp.Board(width, kind)
        cb = cyl.Board(width, 8, kind == "cyl", True)
        mism = []
        for wsq, bsq in enum_positions(width, maxp):
            a = val_str(lambda: mp.value(mb, to_mob(wsq, bsq)))
            c = val_str(lambda: cyl.value(cb, to_cyl(wsq, bsq)))
            checked += 1
            if a != c:
                mism.append((wsq, bsq, a, c))
        print("%s width %d maxp %d: positions %d, mismatches vs cylcgt %d" % (kind, width, maxp, checked, len(mism)))
        for m in mism[:5]:
            print("  MISMATCH", m)
        assert not mism, "fork disagrees with cylcgt on %s" % kind
        checked = 0
    print("cylcgt agreement: OK")


def mobius_vs_flat_away_from_seam(width, maxp):
    mb = mp.Board(width, "mob")
    fb = mp.Board(width, "flat")
    n = same = 0
    for wsq, bsq in enum_positions(width, maxp):
        files = {f for f, _ in wsq} | {f for f, _ in bsq}
        if files & {0, width - 1}:
            continue  # the seam files
        n += 1
        if val_str(lambda: mp.value(mb, to_mob(wsq, bsq))) == val_str(lambda: mp.value(fb, to_mob(wsq, bsq))):
            same += 1
    print("Mobius vs flat, pawns off the seam files: %d positions, equal %d" % (n, same))
    assert n == same, "Mobius differs from flat away from the seam"
    print("away-from-seam agreement: OK")


if __name__ == "__main__":
    W = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    M = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    seam_tests()
    compare_cylinder_flat(W, M)
    mobius_vs_flat_away_from_seam(W + 1 if W < 4 else W, M)
