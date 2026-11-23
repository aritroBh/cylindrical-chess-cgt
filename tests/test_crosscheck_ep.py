"""Whole-board minimax versus the CGT engine, in both passed-pawn settings."""
from dataclasses import replace

import pytest

from crosscheck.minimax import Board, Position, outcome_class, parse_position
from cylcgt import cgt, pawns


@pytest.fixture(autouse=True)
def restore_engine_flag():
    saved = pawns.PASSED_RESPECTS_EP
    yield
    pawns.PASSED_RESPECTS_EP = saved
    pawns._value.cache_clear()


def _sq(name):
    return "abcdefgh".index(name[0]), int(name[1:])


def _pos(text, ep_target, captured, side):
    pos = parse_position(text)
    return Position(pos.white, pos.black, (_sq(ep_target), _sq(captured), side))


# (wrap, position, expected class with the e.p.-aware test, expected class with the textbook test)
DIFFERENT = [
    (False, _pos("W: e4 g5 / B: f6 h5", "h6", "h5", "W"), "N", "R"),
    (True, _pos("W: a5 a6 / B: b7 h5", "h6", "h5", "W"), "N", "R"),
    (True, _pos("W: b2 d4 / B: a4 c4", "d3", "d4", "B"), "N", "L"),
    (True, _pos("W: c5 c6 / B: b5 b7", "b6", "b5", "W"), "N", "R"),
    (False, _pos("W: a4 c3 / B: b4 d6", "a3", "a4", "B"), "N", "L"),
    (False, _pos("W: d4 f2 / B: e4 g6", "d3", "d4", "B"), "N", "L"),
]
SAME = [
    (True, parse_position("W: a2 c2 / B: b7 d7")),
    (False, parse_position("W: a2 c2 / B: b7 d7")),
    (True, parse_position("W: a7 / B: a8")),
    (True, parse_position("W: a2 b3 / B: a6 b7")),
    (False, parse_position("W: b2 c3 / B: c7 d6")),
]


def _engine_outcome(wrap, pos, ep_aware):
    pawns.PASSED_RESPECTS_EP = ep_aware
    pawns._value.cache_clear()
    board = pawns.Board(8, 8, wrap, True)
    engine_pos = pawns.Pos(pos.white, pos.black, pos.ep)
    assert len(pawns.components(board, engine_pos)) == 1
    return cgt.outcome(pawns.value(board, engine_pos))


def _minimax_outcome(wrap, pos, ep_aware):
    return outcome_class(Board(8, 8, wrap, True, ep_passed=ep_aware), pos)


@pytest.mark.parametrize("wrap,pos,aware,textbook", DIFFERENT)
def test_settings_differ_and_both_solvers_follow_each(wrap, pos, aware, textbook):
    assert _minimax_outcome(wrap, pos, True) == _engine_outcome(wrap, pos, True) == aware
    assert _minimax_outcome(wrap, pos, False) == _engine_outcome(wrap, pos, False) == textbook
    assert aware != textbook


@pytest.mark.parametrize("wrap,pos", SAME)
@pytest.mark.parametrize("ep_aware", [True, False])
def test_single_components_agree(wrap, pos, ep_aware):
    assert _minimax_outcome(wrap, pos, ep_aware) == _engine_outcome(wrap, pos, ep_aware)


def test_minimax_setting_is_part_of_the_board():
    assert Board().ep_passed and replace(Board(), ep_passed=False) != Board()
