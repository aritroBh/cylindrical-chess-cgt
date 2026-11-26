"""Tiny executable checks for the independent whole-position solver."""

from crosscheck.minimax import Board, Position, legal_moves, outcome_class


def check():
    # A unique starting passer wins regardless of who would otherwise move.
    assert outcome_class(Board(), Position(frozenset({(0, 2)}), frozenset())) == "L"

    # Both pawns are blocked, so the player to move loses: second player wins.
    blocked = Position(frozenset({(0, 7)}), frozenset({(0, 8)}))
    assert outcome_class(Board(), blocked) == "P"

    # Only White may use this one-ply en-passant right; any Black move expires it.
    ep_pos = Position(
        frozenset({(0, 4), (2, 5)}),
        frozenset({(1, 5), (3, 6)}),
        ((1, 6), (1, 5), "W"),
    )
    ep_moves = legal_moves(Board(), ep_pos, "W")
    assert any((1, 6) in child.white and (1, 5) not in child.black for child in ep_moves)
    black_moves = legal_moves(Board(), ep_pos, "B")
    assert black_moves and all(child.ep is None for child in black_moves)
    assert all(not ((1, 6) in child.white and (1, 5) not in child.black)
               for child in legal_moves(Board(ep=False), ep_pos, "W"))

    # Black's double step starts from the rank below the top one, whatever the height.
    for ranks in (5, 6, 7, 9):
        board = Board(files=3, ranks=ranks, wrap=False)
        lone = Position(frozenset({(0, 2)}), frozenset({(2, ranks - 1)}))
        targets = {next(iter(child.black))[1] for child in legal_moves(board, lone, "B")}
        assert targets == {ranks - 2, ranks - 3}, (ranks, targets)


if __name__ == "__main__":
    check()
    print("minimax checks passed")
