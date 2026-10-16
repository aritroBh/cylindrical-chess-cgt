"""Exact memoized win/loss search for pawn-only chess positions.

Run the small contract check with ``.venv/bin/python -m crosscheck.test_minimax``.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import inf

Square = tuple[int, int]
EnPassant = tuple[Square, Square, str]  # target, captured pawn, entitled side
FILES = "abcdefghijklmnopqrstuvwxyz"


@dataclass(frozen=True)
class Board:
    files: int = 8
    ranks: int = 8
    wrap: bool = True
    ep: bool = True

    def __post_init__(self):
        if self.files < 1 or self.ranks < 1:
            raise ValueError("board dimensions must be positive")

    def neighbor(self, file: int, delta: int) -> int | None:
        f = file + delta
        if self.wrap:
            return f % self.files
        return f if 0 <= f < self.files else None


@dataclass(frozen=True)
class Position:
    white: frozenset[Square]
    black: frozenset[Square]
    ep: EnPassant | None = None

    def __post_init__(self):
        if self.white & self.black:
            raise ValueError("two pawns cannot occupy the same square")
        if self.ep and self.ep[2] not in ("W", "B"):
            raise ValueError("en-passant side must be W or B")


def parse_position(text: str, ep: EnPassant | None = None) -> Position:
    """Parse ``W: a4 h2 / B: a5`` notation without project dependencies."""
    try:
        white_part, black_part = text.split("/")
        white = frozenset(_parse_square(s) for s in white_part.split(":", 1)[1].split())
        black = frozenset(_parse_square(s) for s in black_part.split(":", 1)[1].split())
    except (ValueError, IndexError) as exc:
        raise ValueError(f"invalid position: {text!r}") from exc
    return Position(white, black, ep)


def _parse_square(name: str) -> Square:
    if len(name) < 2 or name[0] not in FILES:
        raise ValueError(f"invalid square: {name!r}")
    rank = int(name[1:])
    if rank < 1:
        raise ValueError(f"invalid square: {name!r}")
    return FILES.index(name[0]), rank


def format_position(pos: Position) -> str:
    def names(squares):
        return " ".join(f"{FILES[f]}{r}" for f, r in sorted(squares))

    result = f"W: {names(pos.white)} / B: {names(pos.black)}"
    if pos.ep:
        result += f" (ep {FILES[pos.ep[0][0]]}{pos.ep[0][1]} for {pos.ep[2]})"
    return result


def legal_moves(board: Board, pos: Position, side: str) -> tuple[Position, ...]:
    """Return every one-pawn move; any old en-passant right expires here."""
    if side not in ("W", "B"):
        raise ValueError("side must be W or B")
    mine = pos.white if side == "W" else pos.black
    theirs = pos.black if side == "W" else pos.white
    occupied = pos.white | pos.black
    direction = 1 if side == "W" else -1
    start_rank = 2 if side == "W" else 7
    en_passant = pos.ep if board.ep and pos.ep and pos.ep[2] == side else None
    out = []

    def emit(new_mine, new_theirs, new_ep=None):
        if side == "W":
            out.append(Position(frozenset(new_mine), frozenset(new_theirs), new_ep))
        else:
            out.append(Position(frozenset(new_theirs), frozenset(new_mine), new_ep))

    for file, rank in sorted(mine):
        next_rank = rank + direction
        if not 1 <= next_rank <= board.ranks:
            continue
        rest = mine - {(file, rank)}
        forward = (file, next_rank)
        if forward not in occupied:
            emit(rest | {forward}, theirs)
            double_rank = rank + 2 * direction
            if (rank == start_rank and 1 <= double_rank <= board.ranks
                    and (file, double_rank) not in occupied):
                next_ep = ((file, next_rank), (file, double_rank), "B" if side == "W" else "W")
                emit(rest | {(file, double_rank)}, theirs, next_ep if board.ep else None)

        for delta in (-1, 1):
            target_file = board.neighbor(file, delta)
            if target_file is None:
                continue
            target = (target_file, next_rank)
            if target in theirs:
                emit(rest | {target}, theirs - {target})
            elif (en_passant and target == en_passant[0]
                  and en_passant[1] in theirs and target not in occupied):
                emit(rest | {target}, theirs - {en_passant[1]})
    return tuple(dict.fromkeys(out))


def _pawn_is_passed(board: Board, pos: Position, side: str, pawn: Square) -> bool:
    _, rank = pawn
    enemy = pos.black if side == "W" else pos.white
    files = {pawn[0], board.neighbor(pawn[0], -1), board.neighbor(pawn[0], 1)} - {None}
    if side == "W":
        return not any(file in files and enemy_rank > rank for file, enemy_rank in enemy)
    return not any(file in files and enemy_rank < rank for file, enemy_rank in enemy)


def _has_passed(board: Board, pos: Position, side: str) -> bool:
    mine = pos.white if side == "W" else pos.black
    return any(_pawn_is_passed(board, pos, side, pawn) for pawn in mine)


def passed_flags(board: Board, pos: Position) -> tuple[bool, bool]:
    """Return whether White and Black respectively have a passed pawn."""
    return _has_passed(board, pos, "W"), _has_passed(board, pos, "B")


def _promotion_distance(board: Board, pos: Position, side: str) -> int | float:
    mine = pos.white if side == "W" else pos.black
    distances = []
    for file, rank in mine:
        pawn = (file, rank)
        if not _pawn_is_passed(board, pos, side, pawn):
            continue
        frontmost = not any(
            f == file and (r > rank if side == "W" else r < rank)
            for f, r in mine
        )
        if frontmost:
            if side == "W":
                distances.append(board.ranks - rank - (rank == 2))
            else:
                distances.append(rank - 1 - (rank == 7))
    return min(distances, default=inf)


def _winner_after_move(board: Board, pos: Position, mover: str) -> str | None:
    white_passed = _has_passed(board, pos, "W")
    black_passed = _has_passed(board, pos, "B")
    if white_passed != black_passed:
        return "W" if white_passed else "B"
    if white_passed:
        other = "B" if mover == "W" else "W"
        return other if _promotion_distance(board, pos, other) <= _promotion_distance(board, pos, mover) else mover
    return None


def winner(board: Board, pos: Position, side: str) -> str:
    """Return the winning color when ``side`` moves next."""
    if side not in ("W", "B"):
        raise ValueError("side must be W or B")
    return _winner(board, pos, side)


@lru_cache(maxsize=None)
def _winner(board: Board, pos: Position, side: str) -> str:
    white_passed = _has_passed(board, pos, "W")
    black_passed = _has_passed(board, pos, "B")
    if white_passed != black_passed:
        return "W" if white_passed else "B"
    if white_passed:
        raise ValueError("both sides already have passers in the starting position")

    other = "B" if side == "W" else "W"
    for child in legal_moves(board, pos, side):
        result = _winner_after_move(board, child, side)
        if result is None:
            result = _winner(board, child, other)
        if result == side:
            return side
    return other


def outcome_class(board: Board, pos: Position) -> str:
    """Return CGT outcome class L/R/N/P from both side-to-move results."""
    white_wins_with_white_to_move = winner(board, pos, "W") == "W"
    white_wins_with_black_to_move = winner(board, pos, "B") == "W"
    if white_wins_with_white_to_move and white_wins_with_black_to_move:
        return "L"
    if not white_wins_with_white_to_move and not white_wins_with_black_to_move:
        return "R"
    if white_wins_with_white_to_move:
        return "N"
    return "P"
