"""Pawn-only chess positions on Möbius strip boards, evaluated as exact combinatorial games.

Conventions (following cylcgt.pawns / Elkies 1996):
- Normal play: side with no legal move loses.
- Passed pawn = ±BIG (BIG = 256). Race rule for double passers.
- En passant respected: a pawn that can be taken e.p. is not passed.
- Components separated by empty files are independent summands.
- On Möbius strip: file wrap with rank flip (h↔a, r→9-r).
- Pawn crossing the seam via capture FLIPS its forward direction.
- Promotion occurs on the rank matching the pawn's current direction flag.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from functools import lru_cache
from typing import Optional

from cylcgt import cgt

BIG = 256
cgt.BIG_DISPLAY = BIG // 2


class RaceError(Exception):
    pass


# Race rule: "count" (opponent moves first in race, fewer moves to promote wins, ties to opponent)
RACE_RULE = "count"
race_hits: list[str] = []

# En passant awareness
PASSED_RESPECTS_EP = True


def promote_distance(board: "Board", pos: "Pos", side: str) -> int:
    """Minimum moves to promote for a passed pawn of `side`."""
    best = None
    mine = pos.white if side == "W" else pos.black
    occ = pos.white | pos.black
    for f, r, d in mine:
        # Check if this pawn is passed (not blocked, not e.p. capturable)
        if not passed(board, Pos(frozenset([(f, r, d)]) if side == "W" else pos.white,
                                 pos.black if side == "W" else frozenset([(f, r, d)])), side):
            continue
        if ep_capturable(board, pos, side, (f, r, d)):
            continue
        # Must be the frontmost pawn of its file for this side
        if side == "W":
            if any((f, s, dd) in occ for s in range(r + 1, board.ranks + 1) for dd in (1, -1)):
                continue
            # Distance depends on direction flag
            if d == 1:
                dist = board.ranks - r - (1 if r == 2 else 0)
            else:  # d == -1, moving toward rank 1
                dist = r - 1 - (1 if r == board.ranks - 1 else 0)
        else:  # Black
            if any((f, s, dd) in occ for s in range(1, r) for dd in (1, -1)):
                continue
            if d == -1:
                dist = r - 1 - (1 if r == board.ranks - 1 else 0)
            else:  # d == 1, moving toward rank 8
                dist = board.ranks - r - (1 if r == 2 else 0)
        best = dist if best is None else min(best, dist)
    return best if best is not None else 10**6


@dataclass(frozen=True)
class Board:
    files: int = 8
    ranks: int = 8
    ep: bool = True

    def nb(self, f: int, df: int) -> tuple[int, bool]:
        """Neighbour file: returns (file, wrapped) where wrapped=True if crossed seam."""
        g = f + df
        if 0 <= g < self.files:
            return g, False
        # Wrap with flip
        g = (g + self.files) % self.files
        return g, True


FILES = "abcdefghijklmnopqrstuvwxyz"


def sq(name: str) -> tuple[int, int]:
    return (FILES.index(name[0]), int(name[1:]))


def name(s: tuple[int, int, int]) -> str:
    return f"{FILES[s[0]]}{s[1]}"


@dataclass(frozen=True)
class Pos:
    white: frozenset[tuple[int, int, int]]  # (file, rank, dir) dir=+1 (toward 8) or -1 (toward 1)
    black: frozenset[tuple[int, int, int]]
    ep: tuple[tuple[int, int, int], tuple[int, int, int], str] | None = None
    # ep = (target_square, captured_square, side_that_may_capture)
    # target and captured are (f, r, d) where d is the capturer's direction

    @staticmethod
    def parse(text: str) -> "Pos":
        """'W: a2 c2 / B: b7 d7' -- all pawns start with default direction."""
        w_part, b_part = text.split("/")
        w = frozenset((sq(t)[0], sq(t)[1], 1) for t in w_part.split(":")[1].split())
        b = frozenset((sq(t)[0], sq(t)[1], -1) for t in b_part.split(":")[1].split())
        return Pos(w, b)

    def __str__(self):
        w = " ".join(sorted(f"{FILES[f]}{r}" for f, r, d in self.white))
        b = " ".join(sorted(f"{FILES[f]}{r}" for f, r, d in self.black))
        return f"W: {w} / B: {b}" + (f" (ep {FILES[self.ep[0][0]]}{self.ep[0][1]})" if self.ep else "")


def ep_capturable(board: Board, pos: Pos, side: str, square: tuple[int, int, int]) -> bool:
    """True if `side`'s pawn on `square` may be taken en passant right now."""
    if not (PASSED_RESPECTS_EP and pos.ep and pos.ep[1] == square and pos.ep[2] != side):
        return False
    f, r, d = square
    theirs = pos.black if side == "W" else pos.white
    # Enemy pawn must be on adjacent file, same rank
    for df in (-1, 1):
        g, _ = board.nb(f, df)
        if any((g, r, dd) in theirs for dd in (1, -1)):
            return True
    return False


def passed(board: Board, pos: Pos, side: str) -> bool:
    mine, theirs = (pos.white, pos.black) if side == "W" else (pos.black, pos.white)
    for f, r, d in mine:
        # Check files: own file and adjacent files (with wrap)
        files = {f}
        for df in (-1, 1):
            g, _ = board.nb(f, df)
            files.add(g)
        if side == "W":
            # Blocked if enemy pawn ahead on any of these files
            blocked = any(g in files and s > r for g, s, dd in theirs)
        else:
            blocked = any(g in files and s < r for g, s, dd in theirs)
        if not blocked and not ep_capturable(board, pos, side, (f, r, d)):
            return True
    return False


def moves(board: Board, pos: Pos, side: str) -> list[Pos]:
    """Positions reachable by one move of `side` ('W' or 'B')."""
    mine, theirs = (pos.white, pos.black) if side == "W" else (pos.black, pos.white)
    occ = pos.white | pos.black
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else board.ranks - 1
    ep_target = pos.ep if (pos.ep and pos.ep[2] == side) else None
    out = []

    def emit(new_mine, new_theirs, ep=None):
        if side == "W":
            out.append(Pos(frozenset(new_mine), frozenset(new_theirs), ep))
        else:
            out.append(Pos(frozenset(new_theirs), frozenset(new_mine), ep))

    for (f, r, pawn_dir) in mine:
        rest = mine - {(f, r, pawn_dir)}
        # Single step forward (in pawn's current direction)
        r1 = r + pawn_dir
        if 1 <= r1 <= board.ranks:
            if (f, r1, pawn_dir) not in occ and (f, r1, -pawn_dir) not in occ:
                emit(rest | {(f, r1, pawn_dir)}, theirs)
                # Double step from starting rank
                r2 = r + 2 * pawn_dir
                if r == start and 1 <= r2 <= board.ranks:
                    if (f, r2, pawn_dir) not in occ and (f, r2, -pawn_dir) not in occ:
                        ep = None
                        if board.ep:
                            other = "B" if side == "W" else "W"
                            # EP target is the skipped square with the mover's direction
                            ep = ((f, r1, pawn_dir), (f, r2, pawn_dir), other)
                        emit(rest | {(f, r2, pawn_dir)}, theirs, ep)
        # Captures: diagonally forward in pawn's current direction
        for df in (-1, 1):
            g, wrapped = board.nb(f, df)
            r1 = r + pawn_dir
            if not (1 <= r1 <= board.ranks):
                continue
            t = (g, r1, -pawn_dir if wrapped else pawn_dir)  # FLIP direction if crossed seam
            if t in theirs:
                emit(rest | {t}, theirs - {t})
            elif ep_target and ep_target[0][:2] == (g, r1):
                # En passant capture: target square matches, captured pawn is on ep_target[1]
                # The capturing pawn's direction flips if the capture crosses the seam
                cap_sq = ep_target[1]
                new_dir = -pawn_dir if wrapped else pawn_dir
                emit(rest | {(g, r1, new_dir)}, theirs - {cap_sq})
    # De-duplicate
    return list(dict.fromkeys(out))


def components(board: Board, pos: Pos) -> list[Pos]:
    """Split a position into independent sub-positions separated by empty files."""
    occ_files = sorted({f for f, _, _ in pos.white | pos.black})
    if not occ_files:
        return []
    groups: list[list[int]] = []
    for f in occ_files:
        if groups and f == groups[-1][-1] + 1:
            groups[-1].append(f)
        else:
            groups.append([f])
    # Check for wrap-around group (files 0 and files-1 both occupied)
    if len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == board.files - 1:
        groups[0] = groups.pop() + groups[0]
    comps = []
    for gfiles in groups:
        fs = set(gfiles)
        ep = pos.ep if (pos.ep and pos.ep[0][0] in fs) else None
        comps.append(Pos(frozenset(p for p in pos.white if p[0] in fs),
                         frozenset(p for p in pos.black if p[0] in fs), ep))
    return comps


def is_ring(board: Board, pos: Pos) -> bool:
    return len({f for f, _, _ in pos.white | pos.black}) == board.files


@lru_cache(maxsize=None)
def _value(board: Board, pos: Pos) -> cgt.Game:
    wp, bp = passed(board, pos, "W"), passed(board, pos, "B")
    if wp and bp:
        raise RaceError(str(pos))
    if wp:
        return cgt.integer(BIG)
    if bp:
        return cgt.integer(-BIG)
    # E.p. right only survives if opponent moves here immediately
    plain = Pos(pos.white, pos.black, None)
    lpos = plain if (pos.ep and pos.ep[2] != "W") else pos
    rpos = plain if (pos.ep and pos.ep[2] != "B") else pos
    L = [_child(board, p, "W") for p in moves(board, lpos, "W")]
    R = [_child(board, p, "B") for p in moves(board, rpos, "B")]
    return cgt.make(L, R)


def _child(board: Board, pos: Pos, mover: str) -> cgt.Game:
    if passed(board, pos, "W") and passed(board, pos, "B"):
        race_hits.append(f"{pos} after {mover}")
        if RACE_RULE == "mover":
            winner = mover
        elif RACE_RULE == "opponent":
            winner = "B" if mover == "W" else "W"
        else:
            other = "B" if mover == "W" else "W"
            winner = other if promote_distance(board, pos, other) <= promote_distance(board, pos, mover) else mover
        return cgt.integer(BIG if winner == "W" else -BIG)
    return value(board, pos)


def value(board: Board, pos: Pos) -> cgt.Game:
    wp, bp = passed(board, pos, "W"), passed(board, pos, "B")
    if wp != bp:
        return cgt.integer(BIG if wp else -BIG)
    comps = components(board, pos)
    if len(comps) > 1:
        return cgt.total(_value(board, c) for c in comps)
    return _value(board, pos)


def describe(board: Board, pos: Pos) -> dict:
    g = value(board, pos)
    info = {"position": str(pos), "value": cgt.show(g), "outcome": cgt.outcome(g),
            "components": [str(c) for c in components(board, pos)],
            "ring": is_ring(board, pos)}
    try:
        info["mean"] = str(cgt.mean(g))
        t = cgt.temperature(g)
        info["temperature"] = "number" if t is None else str(t)
    except AssertionError as e:
        info["thermo_error"] = str(e)
    return info


# Convenience board constructors
def mobius_board(files: int, ranks: int = 8) -> Board:
    return Board(files=files, ranks=ranks, ep=True)