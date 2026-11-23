"""Concrete positions in the T83 report. Run from the project root."""
import sys

import chess

from cylcgt import cgt, pawns

sys.path.insert(0, "notes/proof_audit2/checks")
import indep_sum_model as minimax


def legal(board):
    return {board.san(move) for move in board.legal_moves}


def corollary_example():
    for turn in ("b", "w"):
        board = chess.Board(f"k7/2P5/1K6/p7/8/8/8/8 {turn} - - 0 1")
        assert board.is_valid() and not board.is_check()
        if turn == "b":
            assert legal(board) == {"a4"}
            board.push_san("a4")
        assert legal(board) == {
            "Ka5" if turn == "b" else "Kxa5", "Ka6", "Kb5", "Kc5", "Kc6",
            "c8=Q#", "c8=R#", "c8=B", "c8=N",
        }
        board.push_san("c8=Q#")
        assert board.is_checkmate()


def mate_on_reply():
    board = chess.Board("k7/pP2p3/KP1P4/8/8/8/8/8 b - - 0 1")
    assert board.is_valid() and board.is_check()
    assert legal(board) == {"Kb8"}
    board.push_san("Kb8")
    board.push_san("bxa7#")
    assert board.is_checkmate()
    for square in (chess.D6, chess.E7):
        board.remove_piece_at(square)
    assert board.is_check() and legal(board) == {"Kc7"}
    board.push_san("Kc7")
    assert "a8=Q" in legal(board)


def race_settings():
    position = "W: b2 d4 g3 h5 / B: a7 c7 f7 g4"
    for rule, expected in (("count", "R"), ("mover", "N"), ("opponent", "R")):
        minimax.configure(8, 8, True, False, rule, True, big=256)
        root = minimax.parse(position)
        assert minimax.W_outcome(*root) == "N"
        assert minimax.S_outcome(*root) == expected
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        value = pawns.value(pawns.Board(8, 8, True, False), pawns.Pos.parse(position))
        assert cgt.outcome(value) == expected


if __name__ == "__main__":
    corollary_example()
    mate_on_reply()
    race_settings()
    print("A.13, A.14 and the A.16 timing counterexample agree with the report.")
