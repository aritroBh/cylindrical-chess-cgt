"""Self-checks for the cylinder atlas (symmetries and the cut lemma).

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python -m pytest -q atlas/cylinder/test_atlas.py
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from cylcgt import cgt, pawns  # noqa: E402
from cylcgt.pawns import Board, Pos  # noqa: E402
from enumerate import canon_positions, group  # noqa: E402


def _val(board, W, B):
    return pawns.value(board, Pos(frozenset(W), frozenset(B)))


def _colour_swap(W, B):
    return [(f, 9 - r) for f, r in B], [(f, 9 - r) for f, r in W]


def test_colour_reversal_negates():
    pawns.RACE_RULE = "count"
    pawns._value.cache_clear()
    for n, wrap in ((3, True), (4, True), (4, False), (5, True)):
        board = Board(n, 8, wrap, True)
        for w, b in ((1, 1), (1, 2), (2, 1), (2, 2), (1, 3)):
            for W, B in canon_positions(n, wrap, w, b):
                g = _val(board, W, B)
                W2, B2 = _colour_swap(W, B)
                assert _val(board, W2, B2) is cgt.neg(g), (n, wrap, W, B)


def test_dihedral_invariance():
    rng = random.Random(1)
    for n, wrap in ((4, True), (5, True), (6, True), (5, False)):
        board = Board(n, 8, wrap, True)
        pos = list(canon_positions(n, wrap, 2, 3))
        for W, B in rng.sample(pos, min(150, len(pos))):
            g = _val(board, W, B)
            for gmap in group(n, wrap):
                W2 = [(gmap[f], r) for f, r in W]
                B2 = [(gmap[f], r) for f, r in B]
                assert _val(board, W2, B2) is g


def test_cut_lemma():
    """A cylinder position with an empty file equals the flat position obtained
    by cutting the cylinder at that file."""
    rng = random.Random(2)
    for n in (4, 5, 6, 7):
        cyl = Board(n, 8, True, True)
        flat = Board(n - 1, 8, False, True)
        pos = [p for p in canon_positions(n, True, 2, 3)
               if len({f for f, _ in p[0]} | {f for f, _ in p[1]}) < n]
        for W, B in rng.sample(pos, min(200, len(pos))):
            occ = {f for f, _ in W} | {f for f, _ in B}
            e = min(f for f in range(n) if f not in occ)
            # flat file j <- cylinder file e+1+j
            m = {(e + 1 + j) % n: j for j in range(n - 1)}
            W2 = [(m[f], r) for f, r in W]
            B2 = [(m[f], r) for f, r in B]
            assert _val(cyl, W, B) is _val(flat, W2, B2), (n, W, B)


def test_star2_candidate():
    pawns.RACE_RULE = "count"
    pawns._value.cache_clear()
    g = pawns.value(Board(4, 8, False, True), Pos.parse("W: a2 c2 / B: b7 d7"))
    assert g is cgt.nimber(2)
