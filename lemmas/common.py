"""Shared helpers for the lemma falsification tests (workstream A1).

Three game models of a pawn position X on a board (all use cylcgt.cgt):

  S(X)   the project's sum model, i.e. cylcgt.pawns.value: a global passer
         check at the root, then the sum of the component values, recursively
         (a component that gets a passer is frozen into +-BIG while play
         continues in the other components).
  W(X)   the whole-board convention game: no splitting at all; a position
         in which exactly one side has a passed pawn is terminal (+-BIG);
         a move that creates passers for both sides is scored by the race
         rule; e.p. rights are global (they expire after any other move).
  WF(X)  W(X) plus one extra option for each side at every non-terminal
         node: a "king move" that loses at once (-BIG for White, +BIG for
         Black). This is the frozen-trebuchet model of lemma L3.

Also: the "pure" game (no passer convention at all; pawns that reach the last
rank simply stop), threat sets, and random position generators.

Run everything from the project root with PYTHONPATH=. .venv/bin/python ...
"""
from __future__ import annotations

import random
import sys
from functools import lru_cache

sys.setrecursionlimit(1_000_000)

from cylcgt import cgt, pawns
from cylcgt.pawns import BIG, Board, Pos

PBIG = cgt.integer(BIG)
NBIG = cgt.integer(-BIG)
RULES = ("count", "mover", "opponent")


# ---------------------------------------------------------------------------
# race resolution (identical to pawns._child, but with the rule as a parameter)
# ---------------------------------------------------------------------------

def race_winner(board: Board, pos: Pos, mover: str, rule: str) -> str:
    if rule == "mover":
        return mover
    other = "B" if mover == "W" else "W"
    if rule == "opponent":
        return other
    assert rule == "count"
    d_other = pawns.promote_distance(board, pos, other)
    d_mover = pawns.promote_distance(board, pos, mover)
    return other if d_other <= d_mover else mover


def terminal(board: Board, pos: Pos):
    """+1 / -1 if exactly one side has a passer, 0 if both, None if neither."""
    wp, bp = pawns.passed(board, pos, "W"), pawns.passed(board, pos, "B")
    if wp and bp:
        return 0
    if wp:
        return 1
    if bp:
        return -1
    return None


def split_ep(pos: Pos):
    """Positions from which Left / Right generate moves (pawns._value logic):
    a right belonging to the other side expires when this side moves."""
    plain = Pos(pos.white, pos.black, None)
    lpos = plain if (pos.ep and pos.ep[2] != "W") else pos
    rpos = plain if (pos.ep and pos.ep[2] != "B") else pos
    return lpos, rpos


# ---------------------------------------------------------------------------
# S: the project's sum model
# ---------------------------------------------------------------------------

def S(board: Board, pos: Pos, rule: str = "count") -> cgt.Game:
    if pawns.RACE_RULE != rule:
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
    return pawns.value(board, pos)


# ---------------------------------------------------------------------------
# W and WF: whole-board convention games
# ---------------------------------------------------------------------------

_W_memo: dict = {}


def W(board: Board, pos: Pos, rule: str = "count", kings: bool = False) -> cgt.Game:
    key = (board, pos, rule, kings)
    g = _W_memo.get(key)
    if g is not None:
        return g
    t = terminal(board, pos)
    if t == 0:
        raise pawns.RaceError(str(pos))
    if t == 1:
        g = PBIG
    elif t == -1:
        g = NBIG
    else:
        lpos, rpos = split_ep(pos)
        L = [_W_child(board, c, "W", rule, kings) for c in pawns.moves(board, lpos, "W")]
        R = [_W_child(board, c, "B", rule, kings) for c in pawns.moves(board, rpos, "B")]
        if kings:
            L.append(NBIG)
            R.append(PBIG)
        g = cgt.make(L, R)
    _W_memo[key] = g
    return g


def _W_child(board, pos, mover, rule, kings):
    if terminal(board, pos) == 0:
        return PBIG if race_winner(board, pos, mover, rule) == "W" else NBIG
    return W(board, pos, rule, kings)


def WF(board: Board, pos: Pos, rule: str = "count") -> cgt.Game:
    return W(board, pos, rule, kings=True)


# ---------------------------------------------------------------------------
# alternating-play winner of the whole-board convention game (plain minimax,
# no CGT): used as a third, CGT-free reference for outcomes.
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def alt_winner(board: Board, pos: Pos, to_move: str, rule: str = "count", kings: bool = False) -> str:
    t = terminal(board, pos)
    if t == 1:
        return "W"
    if t == -1:
        return "B"
    if t == 0:
        raise pawns.RaceError(str(pos))
    other = "B" if to_move == "W" else "W"
    lpos, rpos = split_ep(pos)
    src = lpos if to_move == "W" else rpos
    for c in pawns.moves(board, src, to_move):
        tc = terminal(board, c)
        if tc == 0:
            res = race_winner(board, c, to_move, rule)
        elif tc is not None:
            res = "W" if tc == 1 else "B"
        else:
            # the opponent's e.p. right (if any) stays only for the next move
            res = alt_winner(board, c, other, rule, kings)
        if res == to_move:
            return to_move
    # with kings, the side to move always has a (losing) king move; without
    # kings, having no move loses. Either way the opponent wins.
    return other


def alt_outcome(board, pos, rule="count", kings=False) -> str:
    w_first = alt_winner(board, pos, "W", rule, kings) == "W"
    w_second = alt_winner(board, pos, "B", rule, kings) == "W"
    if w_first and w_second:
        return "L"
    if not w_first and not w_second:
        return "R"
    return "N" if w_first else "P"


# ---------------------------------------------------------------------------
# the pure game: no passer convention; normal play only
# ---------------------------------------------------------------------------

_P_memo: dict = {}


def pure(board: Board, pos: Pos) -> cgt.Game:
    """Whole-board pure pawn game (no passer rule). Pawns on the last rank have
    no moves. E.p. rights are global, as in W."""
    key = (board, pos)
    g = _P_memo.get(key)
    if g is None:
        lpos, rpos = split_ep(pos)
        L = [pure(board, c) for c in pawns.moves(board, lpos, "W")]
        R = [pure(board, c) for c in pawns.moves(board, rpos, "B")]
        g = cgt.make(L, R)
        _P_memo[key] = g
    return g


_PL_memo: dict = {}


def pure_local(board: Board, pos: Pos) -> cgt.Game:
    """Pure game of ONE component with local e.p. (the sum model's convention):
    identical to pure() on a single component; the difference appears only when
    pure_local values of several components are added."""
    return pure(board, pos)


def pure_sum(board: Board, pos: Pos) -> cgt.Game:
    """Sum of the pure values of the components of pos (local e.p.)."""
    return cgt.total(pure(board, c) for c in pawns.components(board, pos))


# ---------------------------------------------------------------------------
# reachability and threat sets
# ---------------------------------------------------------------------------

def reachable(board: Board, pos: Pos, stop_at_terminal: bool = True):
    """All positions reachable from pos by any sequence of moves of either side
    (not necessarily alternating). With stop_at_terminal, positions where some
    side has a passer are included but not expanded."""
    seen = {pos}
    stack = [pos]
    while stack:
        x = stack.pop()
        if stop_at_terminal and terminal(board, x) is not None:
            continue
        lpos, rpos = split_ep(x)
        for side, src in (("W", lpos), ("B", rpos)):
            for c in pawns.moves(board, src, side):
                if c not in seen:
                    seen.add(c)
                    stack.append(c)
    return seen


_T_memo: dict = {}


def threats(board: Board, pos: Pos) -> frozenset:
    """tau(X): the set of signs s in {+1,-1} such that some position reachable
    from X (by moves of either side, in any order, not continuing past the
    first passer) has a passer for that side. Computed by memoised recursion
    over the (acyclic) move graph:
        tau(X) = {signs of passers in X}          if X has a passer,
        tau(X) = union of tau(X') over all moves X -> X'   otherwise.
    """
    key = (board, pos)
    r = _T_memo.get(key)
    if r is not None:
        return r
    out = set()
    if pawns.passed(board, pos, "W"):
        out.add(1)
    if pawns.passed(board, pos, "B"):
        out.add(-1)
    if not out:
        lpos, rpos = split_ep(pos)
        for side, src in (("W", lpos), ("B", rpos)):
            for c in pawns.moves(board, src, side):
                out |= threats(board, c)
    r = frozenset(out)
    _T_memo[key] = r
    return r


def pairwise_safe(board: Board, pos: Pos) -> bool:
    """No two distinct components with opposite threat signs."""
    ts = [threats(board, c) for c in pawns.components(board, pos)]
    for i, a in enumerate(ts):
        for j, b in enumerate(ts):
            if i != j and 1 in a and -1 in b:
                return False
    return True


def hereditarily_safe(board: Board, pos: Pos) -> bool:
    """HSS: every non-terminal position reachable from pos is pairwise safe."""
    for y in reachable(board, pos):
        if terminal(board, y) is None and not pairwise_safe(board, y):
            return False
    return True


# ---------------------------------------------------------------------------
# geometry helpers
# ---------------------------------------------------------------------------

def occupied_files(pos: Pos):
    return {f for f, _ in pos.white | pos.black}


def relabel(pos: Pos, fmap) -> Pos:
    ep = None
    if pos.ep:
        (tf, tr), (cf, cr), s = pos.ep
        ep = ((fmap[tf], tr), (fmap[cf], cr), s)
    return Pos(frozenset((fmap[f], r) for f, r in pos.white),
               frozenset((fmap[f], r) for f, r in pos.black), ep)


def colour_reverse(board: Board, pos: Pos) -> Pos:
    """Swap colours and flip ranks r -> ranks+1-r."""
    m = board.ranks
    flip = lambda s: (s[0], m + 1 - s[1])
    ep = None
    if pos.ep:
        t, c, s = pos.ep
        ep = (flip(t), flip(c), "B" if s == "W" else "W")
    return Pos(frozenset(map(flip, pos.black)), frozenset(map(flip, pos.white)), ep)


def random_position(rng: random.Random, board: Board, n_white: int, n_black: int,
                    files=None, legal_ranks: bool = True) -> Pos:
    """Random pawn placement. With legal_ranks, pawns avoid their own back rank
    and the promotion rank (White ranks 2..m-1, Black ranks 2..m-1)."""
    files = list(range(board.files)) if files is None else list(files)
    lo, hi = (2, board.ranks - 1) if legal_ranks else (1, board.ranks)
    squares = [(f, r) for f in files for r in range(lo, hi + 1)]
    pick = rng.sample(squares, n_white + n_black)
    return Pos(frozenset(pick[:n_white]), frozenset(pick[n_white:]))


def name_pos(pos: Pos) -> str:
    return str(pos)
