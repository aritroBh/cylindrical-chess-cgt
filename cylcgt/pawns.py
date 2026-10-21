"""Pawn-only chess positions on W-file x H-rank boards, flat or cylindrical,
evaluated as exact combinatorial games (White = Left, Black = Right).

Conventions (Elkies 1996, and the cylinder paper):
  * normal play: a side with no legal move loses;
  * a position in which exactly one side has a passed pawn is a decisive win
    for that side, modelled as the number +BIG / -BIG;
  * a position where both sides have passed pawns is a race and is rejected.

Fact used for decomposition: pawns only change file by capturing, so an empty
file stays empty forever and pawn groups separated by an empty file are
independent summands. On a cylinder a group may wrap around the a/h seam;
with no empty file at all it forms a single "ring" component.

En passant: a double step leaves an e.p. right for the opponent that is only
usable as the opponent's very next move *in this component*. That is the
standard short-game approximation (exact when the component is played alone).
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from . import cgt

BIG = 256  # value of a won (passed-pawn) position; must dominate all tempo counts
cgt.BIG_DISPLAY = BIG // 2


class RaceError(Exception):
    pass


# How to score a move that gives BOTH sides a passed pawn (a promotion race).
#   "count": the opponent of the mover moves first in the race; whoever needs
#            fewer moves to promote wins (opponent wins ties). Ignores queen
#            checks / a new queen stopping the other pawn.
#   "mover": the mover wins.   "opponent": the mover loses.
RACE_RULE = "count"
race_hits: list[str] = []  # positions where the race rule was invoked

# A pawn that has just double-stepped and can still be taken en passant is not
# yet passed: the opponent's e.p. capture comes first. False restores the
# textbook test, under which W a2 c2 / B b7 d7 is *2 (see RESULTS.md section 1).
PASSED_RESPECTS_EP = True


def promote_distance(board: "Board", pos: "Pos", side: str) -> int:
    best = None
    mine = pos.white if side == "W" else pos.black
    occ = pos.white | pos.black
    for f, r in mine:
        if not passed(board, Pos(frozenset([(f, r)]) if side == "W" else pos.white,
                                 pos.black if side == "W" else frozenset([(f, r)])), side):
            continue
        if ep_capturable(board, pos, side, (f, r)):
            continue
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, board.ranks + 1)):
                continue  # not the front pawn of its file
            d = board.ranks - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            d = r - 1 - (1 if r == board.ranks - 1 else 0)
        best = d if best is None else min(best, d)
    return best if best is not None else 10**6


@dataclass(frozen=True)
class Board:
    files: int = 8
    ranks: int = 8
    wrap: bool = True
    ep: bool = True

    def nb(self, f: int, df: int):
        g = f + df
        if self.wrap:
            return g % self.files
        return g if 0 <= g < self.files else None


CYL8 = Board(8, 8, True, True)
FLAT8 = Board(8, 8, False, True)

FILES = "abcdefghijklmnopqrstuvwxyz"


def sq(name: str):
    return (FILES.index(name[0]), int(name[1:]))


def name(s):
    return f"{FILES[s[0]]}{s[1]}"


@dataclass(frozen=True)
class Pos:
    white: frozenset
    black: frozenset
    ep: tuple | None = None  # (target_square, captured_square, side_that_may_capture)

    @staticmethod
    def parse(text: str) -> "Pos":
        """'W: a4 h2 h4 / B: a5 a6 a7 h3'"""
        w_part, b_part = text.split("/")
        w = frozenset(sq(t) for t in w_part.split(":")[1].split())
        b = frozenset(sq(t) for t in b_part.split(":")[1].split())
        return Pos(w, b)

    def __str__(self):
        w = " ".join(sorted(map(name, self.white)))
        b = " ".join(sorted(map(name, self.black)))
        return f"W: {w} / B: {b}" + (f" (ep {name(self.ep[0])})" if self.ep else "")


def ep_capturable(board: Board, pos: Pos, side: str, square) -> bool:
    """True if `side`'s pawn on `square` may be taken en passant right now."""
    if not (PASSED_RESPECTS_EP and pos.ep and pos.ep[1] == square and pos.ep[2] != side):
        return False
    f, r = square
    theirs = pos.black if side == "W" else pos.white
    return any((g, r) in theirs for g in (board.nb(f, -1), board.nb(f, 1)) if g is not None)


def passed(board: Board, pos: Pos, side: str) -> bool:
    mine, theirs = (pos.white, pos.black) if side == "W" else (pos.black, pos.white)
    for f, r in mine:
        files = {f} | {g for g in (board.nb(f, -1), board.nb(f, 1)) if g is not None}
        if side == "W":
            blocked = any(g in files and s > r for g, s in theirs)
        else:
            blocked = any(g in files and s < r for g, s in theirs)
        if not blocked and not ep_capturable(board, pos, side, (f, r)):
            return True
    return False


def moves(board: Board, pos: Pos, side: str):
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

    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if not (1 <= r1 <= board.ranks):
            continue
        if (f, r1) not in occ:
            emit(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= board.ranks and (f, r2) not in occ:
                ep = None
                if board.ep:
                    other = "B" if side == "W" else "W"
                    ep = ((f, r1), (f, r2), other)
                emit(rest | {(f, r2)}, theirs, ep)
        for df in (-1, 1):
            g = board.nb(f, df)
            if g is None:
                continue
            t = (g, r1)
            if t in theirs:
                emit(rest | {t}, theirs - {t})
            elif ep_target and ep_target[0] == t:
                emit(rest | {t}, theirs - {ep_target[1]})
    # de-duplicate (two pawns may reach identical positions)
    return list(dict.fromkeys(out))


def components(board: Board, pos: Pos):
    """Split a position into independent sub-positions separated by empty files."""
    occ_files = sorted({f for f, _ in pos.white | pos.black})
    if not occ_files:
        return []
    groups: list[list[int]] = []
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


def is_ring(board: Board, pos: Pos) -> bool:
    return board.wrap and len({f for f, _ in pos.white | pos.black}) == board.files


def value(board: Board, pos: Pos) -> cgt.Game:
    # A passed pawn ends the whole game, so check before splitting: otherwise
    # +BIG in one component could be cancelled by a -BIG threat in another.
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
    # an e.p. right only survives if the opponent moves here immediately
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


def sum_safe(board: Board, pos: Pos) -> bool:
    """False if passed-pawn threats of opposite colour live in different
    components; then the disjunctive-sum value may differ from real play
    (in chess the first passer ends the game; in a sum +BIG and -BIG cancel).

    A heuristic, not a certificate: it looks only at the top-level split, so
    it misses cancellation in sums that appear later in the tree (e.g. W: b2
    d4 g3 h5 / B: a7 c7 f7 g4 on CYL8 with e.p. off is True here, yet the sum
    model gets the outcome wrong). The proved test is "hereditarily sum-safe",
    lemmas.common.hereditarily_safe; see notes/lemmas.md section 2."""
    signs = []
    for c in components(board, pos):
        g = _value(board, c)
        seen, stack, s = set(), [g], set()
        while stack:
            x = stack.pop()
            if x.id in seen:
                continue
            seen.add(x.id)
            if x.num is not None and abs(x.num) >= BIG // 2:
                s.add(1 if x.num > 0 else -1)
            stack.extend(x.L + x.R)
        signs.append(s)
    pos_c = sum(1 for s in signs if 1 in s)
    neg_c = sum(1 for s in signs if -1 in s)
    return not (pos_c and neg_c and len(signs) > 1 and
                any((1 in a and -1 in b) for i, a in enumerate(signs) for j, b in enumerate(signs) if i != j))


def describe(board: Board, pos: Pos) -> dict:
    g = value(board, pos)
    info = {"position": str(pos), "value": cgt.show(g), "outcome": cgt.outcome(g),
            "components": [str(c) for c in components(board, pos)],
            "ring": is_ring(board, pos), "sum_safe": sum_safe(board, pos)}
    try:
        info["mean"] = str(cgt.mean(g))
        t = cgt.temperature(g)
        info["temperature"] = "number" if t is None else str(t)
    except AssertionError as e:  # pragma: no cover
        info["thermo_error"] = str(e)
    return info
