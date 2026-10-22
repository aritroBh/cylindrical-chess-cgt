"""Pawn-only games on flat, cylinder and Mobius boards (research/mobius, T35).

This is a fork of cylcgt/pawns.py. Its conventions are kept: normal play, passed pawn = +-BIG,
race rule RACE_RULE = "count", en passant respected, components split by empty files, and the same
canonical forms (cylcgt.cgt). The one change is the geometry, following research/mobius/RULES.md:

  * kind 'flat': no wrap.
  * kind 'cyl' : the a and last files are glued straight (cylcgt's cylinder).
  * kind 'mob' : the seam is glued with a half twist. Crossing it maps a rank r to 9 - r
                 (RULES.md 1.1), and a pawn whose CAPTURE crosses the seam flips its direction
                 flag (RULES.md 3). Other moves never cross the seam.

A pawn is a triple (file, rank, d). d = +1 moves toward rank 8 and d = -1 toward rank 1. White
pawns start with d = +1 and Black pawns with d = -1. The double step starts from rank 2 if d = +1
and from rank 7 if d = -1. A pawn promotes on rank 8 if d = +1 and on rank 1 if d = -1. Who moves
a pawn is decided by which set it sits in (White or Black), not by d.

Positions are stored in one fundamental chart (files 0..files-1, ranks 1..8), so a pawn's square
has a single coordinate pair. Adjacency across the seam is handled by shift().
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from cylcgt import cgt

BIG = 256
cgt.BIG_DISPLAY = BIG // 2
RACE_RULE = "count"
PASSED_RESPECTS_EP = True
H = 8  # ranks 1..8
race_count = 0  # number of race resolutions (diagnostic)


class RaceError(Exception):
    pass


@dataclass(frozen=True)
class Board:
    files: int = 8
    kind: str = "mob"  # 'flat' | 'cyl' | 'mob'
    ep: bool = True

    @property
    def wrap(self) -> bool:
        return self.kind != "flat"


def shift(board: Board, f: int, r: int, df: int, dr: int):
    """One step of df files and dr ranks from (f, r). Returns (g, r2, crossed), or None if off board.

    crossed is True iff the step passed the seam. On 'mob' the rank is then flipped, r2 -> 9 - r2."""
    g = f + df
    crossed = False
    if g < 0 or g >= board.files:
        if board.kind == "flat":
            return None
        g %= board.files
        crossed = True
    r2 = r + dr
    if crossed and board.kind == "mob":
        r2 = H + 1 - r2
    if not 1 <= r2 <= H:
        return None
    return g, r2, crossed


def _neighbour(board: Board, f: int, g: int) -> bool:
    if board.kind == "flat":
        return abs(f - g) == 1
    return (f - g) % board.files in (1, board.files - 1)


def _crosses(board: Board, f: int, g: int) -> bool:
    """True if the adjacency f-g goes through the seam (only possible on wrapped boards)."""
    return board.wrap and f != g and abs(f - g) == board.files - 1


@dataclass(frozen=True)
class Pos:
    white: frozenset  # of (file, rank, d)
    black: frozenset
    ep: tuple | None = None  # (target square, captured square, side allowed to capture); squares (f, r)

    @staticmethod
    def parse(text: str) -> "Pos":
        """'W: a2 c2 / B: b7 d7' (all pawns start with the default direction)."""
        w_part, b_part = text.split("/")
        w = frozenset((FILES.index(t[0]), int(t[1:]), 1) for t in w_part.split(":")[1].split())
        b = frozenset((FILES.index(t[0]), int(t[1:]), -1) for t in b_part.split(":")[1].split())
        return Pos(w, b)

    def __str__(self):
        w = " ".join(sorted("%s%d" % (FILES[f], r) + ("" if d == 1 else "*") for f, r, d in self.white))
        b = " ".join(sorted("%s%d" % (FILES[f], r) + ("" if d == -1 else "*") for f, r, d in self.black))
        return "W: %s / B: %s" % (w, b)


FILES = "abcdefghijklmnopqrstuvwxyz"


def _enemy_rank(board: Board, f: int, g: int, s: int) -> int:
    """Rank s of an enemy pawn on file g, expressed in the chart of a pawn on file f."""
    if g != f and _crosses(board, f, g) and board.kind == "mob":
        return H + 1 - s
    return s


def ep_capturable(board: Board, pos: Pos, side: str, square) -> bool:
    """True if the side's pawn on `square` (file, rank) may be taken en passant right now."""
    if not (PASSED_RESPECTS_EP and pos.ep and pos.ep[1] == square and pos.ep[2] != side):
        return False
    tf, tr = pos.ep[0]
    capturers = pos.black if side == "W" else pos.white
    for g, s, e in capturers:
        for df in (-1, 1):
            sh = shift(board, g, s, df, e)
            if sh is not None and sh[0] == tf and sh[1] == tr:
                return True
    return False


def passed(board: Board, pos: Pos, side: str) -> bool:
    mine, theirs = (pos.white, pos.black) if side == "W" else (pos.black, pos.white)
    for f, r, d in mine:
        blocked = False
        for g, s, _ in theirs:
            if g != f and not _neighbour(board, f, g):
                continue
            if (_enemy_rank(board, f, g, s) - r) * d > 0:
                blocked = True
                break
        if not blocked and not ep_capturable(board, pos, side, (f, r)):
            return True
    return False


def promote_distance(board: Board, pos: Pos, side: str) -> int:
    best = None
    mine = pos.white if side == "W" else pos.black
    occ = {(f, r) for f, r, _ in pos.white | pos.black}
    for f, r, d in mine:
        one = Pos(frozenset([(f, r, d)]) if side == "W" else pos.white,
                  pos.black if side == "W" else frozenset([(f, r, d)]))
        if not passed(board, one, side):
            continue
        if ep_capturable(board, pos, side, (f, r)):
            continue
        ahead = range(r + 1, H + 1) if d == 1 else range(1, r)
        if any((f, s) in occ for s in ahead):
            continue  # not the front pawn of its file
        if d == 1:
            dist = H - r - (1 if r == 2 else 0)
        else:
            dist = r - 1 - (1 if r == H - 1 else 0)
        best = dist if best is None else min(best, dist)
    return best if best is not None else 10 ** 6


def components(board: Board, pos: Pos):
    """Split a position into independent sub-positions separated by empty files."""
    occ_files = sorted({f for f, _, _ in pos.white | pos.black})
    if not occ_files:
        return []
    groups = []
    for f in occ_files:
        if groups and f == groups[-1][-1] + 1:
            groups[-1].append(f)
        else:
            groups.append([f])
    if board.wrap and len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == board.files - 1:
        groups[0] = groups.pop() + groups[0]
    comps = []
    for gfiles in groups:
        fs = set(gfiles)
        ep = pos.ep if (pos.ep and pos.ep[0][0] in fs) else None
        comps.append(Pos(frozenset(p for p in pos.white if p[0] in fs),
                         frozenset(p for p in pos.black if p[0] in fs), ep))
    return comps


def moves(board: Board, pos: Pos, side: str):
    mine, theirs = (pos.white, pos.black) if side == "W" else (pos.black, pos.white)
    occ = {(f, r) for f, r, _ in pos.white | pos.black}
    ep_target = pos.ep if (pos.ep and pos.ep[2] == side) else None
    out = []

    def emit(new_mine, new_theirs, ep=None):
        if side == "W":
            out.append(Pos(frozenset(new_mine), frozenset(new_theirs), ep))
        else:
            out.append(Pos(frozenset(new_theirs), frozenset(new_mine), ep))

    def without_square(pieces, sq):
        return frozenset(p for p in pieces if (p[0], p[1]) != sq)

    for (f, r, d) in mine:
        rest = mine - {(f, r, d)}
        r1 = r + d
        if not 1 <= r1 <= H:
            continue
        if (f, r1) not in occ:
            emit(rest | {(f, r1, d)}, theirs)
            r2 = r + 2 * d
            start = 2 if d == 1 else H - 1
            if r == start and 1 <= r2 <= H and (f, r2) not in occ:
                ep = None
                if board.ep:
                    other = "B" if side == "W" else "W"
                    ep = ((f, r1), (f, r2), other)
                emit(rest | {(f, r2, d)}, theirs, ep)
        for df in (-1, 1):
            sh = shift(board, f, r, df, d)
            if sh is None:
                continue
            g, t_r, crossed = sh
            nd = -d if (crossed and board.kind == "mob") else d
            tgt = (g, t_r)
            if any((p[0], p[1]) == tgt for p in theirs):
                emit(rest | {(g, t_r, nd)}, without_square(theirs, tgt))
            elif ep_target and ep_target[0] == tgt:
                emit(rest | {(g, t_r, nd)}, without_square(theirs, ep_target[1]))
    return list(dict.fromkeys(out))


def value(board: Board, pos: Pos) -> cgt.Game:
    wp, bp = passed(board, pos, "W"), passed(board, pos, "B")
    if wp != bp:
        return cgt.integer(BIG if wp else -BIG)
    comps = components(board, pos)
    if len(comps) > 1:
        return cgt.total(_value(board, c) for c in comps)
    return _value(board, pos)


@lru_cache(maxsize=None)
def _value(board: Board, pos: Pos) -> cgt.Game:
    wp, bp = passed(board, pos, "W"), passed(board, pos, "B")
    if wp and bp:
        raise RaceError(str(pos))
    if wp:
        return cgt.integer(BIG)
    if bp:
        return cgt.integer(-BIG)
    plain = Pos(pos.white, pos.black, None)
    lpos = plain if (pos.ep and pos.ep[2] != "W") else pos
    rpos = plain if (pos.ep and pos.ep[2] != "B") else pos
    L = [_child(board, p, "W") for p in moves(board, lpos, "W")]
    R = [_child(board, p, "B") for p in moves(board, rpos, "B")]
    return cgt.make(L, R)


def _child(board: Board, pos: Pos, mover: str) -> cgt.Game:
    global race_count
    if passed(board, pos, "W") and passed(board, pos, "B"):
        race_count += 1
        other = "B" if mover == "W" else "W"
        if RACE_RULE == "mover":
            winner = mover
        elif RACE_RULE == "opponent":
            winner = other
        else:
            winner = other if promote_distance(board, pos, other) <= promote_distance(board, pos, mover) else mover
        return cgt.integer(BIG if winner == "W" else -BIG)
    return value(board, pos)
