from dataclasses import replace

import pytest

from cylcgt import cgt, pawns
from cylcgt.pawns import FLAT8, Board, Pos, passed, sq, value


@pytest.fixture(autouse=True)
def default_conventions():
    saved = pawns.PASSED_RESPECTS_EP, pawns.RACE_RULE
    pawns._value.cache_clear()
    yield
    pawns.PASSED_RESPECTS_EP, pawns.RACE_RULE = saved
    pawns._value.cache_clear()


def test_pawn_that_can_be_taken_en_passant_is_not_passed():
    # after a2-a4 with a black pawn on b4, b4xa3 e.p. is legal
    pos = Pos(frozenset({sq("a4")}), frozenset({sq("b4")}), (sq("a3"), sq("a4"), "B"))
    assert not passed(FLAT8, pos, "W")
    pawns.PASSED_RESPECTS_EP = False
    assert passed(FLAT8, pos, "W")


def test_en_passant_right_without_a_capturer_does_not_block():
    # the right is recorded on every double step; with no pawn beside a4 it is empty
    pos = Pos(frozenset({sq("a4")}), frozenset({sq("d7")}), (sq("a3"), sq("a4"), "B"))
    assert passed(FLAT8, pos, "W")


def test_star2_candidate_needs_the_textbook_passed_test():
    pos = Pos.parse("W: a2 c2 / B: b7 d7")
    four = Board(4, 8, False, True)
    assert cgt.show(value(four, pos)) == "{2±1 | -2±1}"
    assert value(replace(four, ep=False), pos) is cgt.nimber(2)
    pawns.PASSED_RESPECTS_EP = False
    pawns._value.cache_clear()
    assert value(four, pos) is cgt.nimber(2)
