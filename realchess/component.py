"""The a-d pawn component, its CGT game tree, and its 8x8 embedding.

Uses cylcgt.pawns for the model rules (read-only import). The component lives
on a 4-file flat board with 8 ranks (files a-d of the real board; file e is
empty, so on the real board it is an independent summand next to the
g-file trebuchet).

Terminology:
  * internal node: a component position in which neither side has a passed
    pawn;
  * terminal: a position reached by a move in which some side has a passed
    pawn (the model scores it +BIG/-BIG, races by RACE_RULE).
A terminal is identified by (white squares, black squares, ep) where ep is
the cylcgt ep tuple (only present when the move into it was a double step).
"""
from __future__ import annotations

from functools import lru_cache

from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos

from . import movegen

BOARD4 = Board(4, 8, False, True)          # files a-d, flat, e.p. on
BOARD4_NOEP = Board(4, 8, False, False)
BIG = pawns.BIG

# The trebuchet used by the proposed embedding (squares in movegen indexing).
TREBUCHET = {"f5": "K", "g4": "P", "h4": "k", "g5": "p"}


def is_terminal(board: Board, p: Pos) -> bool:
    return pawns.passed(board, p, "W") or pawns.passed(board, p, "B")


def options(board: Board, p: Pos, side: str):
    """Children of internal node p for `side` (cylcgt semantics: an e.p. right
    belongs only to the side it was granted to)."""
    plain = Pos(p.white, p.black, None)
    use = p if (p.ep and p.ep[2] == side) else plain
    return pawns.moves(board, use, side)


def enumerate_tree(board: Board, root: Pos):
    """All internal nodes and terminals reachable in the CGT game tree
    (moves by either side in any order). Returns (internal, terminals, edges)
    with edges[(node, side)] = list of children."""
    internal, terminals, edges = set(), set(), {}
    stack = [root]
    seen = set()
    while stack:
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)
        if is_terminal(board, p):
            terminals.add(p)
            continue
        internal.add(p)
        for side in "WB":
            kids = options(board, p, side)
            edges[(p, side)] = kids
            stack.extend(kids)
    return internal, terminals, edges


def model_terminal_value(board: Board, t: Pos, mover: str, rule: str) -> int:
    """+1 / -1 for the model's verdict on terminal t entered by `mover`."""
    wp, bp = pawns.passed(board, t, "W"), pawns.passed(board, t, "B")
    if wp and bp:
        if rule == "mover":
            win = mover
        elif rule == "opponent":
            win = "B" if mover == "W" else "W"
        else:
            other = "B" if mover == "W" else "W"
            win = other if pawns.promote_distance(board, t, other) <= \
                pawns.promote_distance(board, t, mover) else mover
        return 1 if win == "W" else -1
    return 1 if wp else -1


def value_with(board: Board, root: Pos, term_value):
    """Canonical CGT value of `root` where every terminal child is replaced by
    term_value(terminal, mover) -> cgt.Game."""
    memo = {}

    def val(p):
        g = memo.get(p)
        if g is not None:
            return g
        L = [kid(q, "W") for q in options(board, p, "W")]
        R = [kid(q, "B") for q in options(board, p, "B")]
        g = cgt.make(L, R)
        memo[p] = g
        return g

    def kid(q, mover):
        if is_terminal(board, q):
            return term_value(q, mover)
        return val(q)

    if is_terminal(board, root):
        raise ValueError("root is already terminal")
    return val(root)


# ------------------------------------------------------------- embedding
def embed(p: Pos, stm: str, trebuchet=TREBUCHET, keep_ep: bool = True) -> movegen.Position:
    """8x8 position: component pawns on files a-d (cylcgt ranks are 1-based),
    plus the trebuchet. stm in {'W','B'}. The e.p. right is kept only if it
    belongs to stm."""
    b = [movegen.EMPTY] * 64
    for f, r in p.white:
        b[8 * (r - 1) + f] = "P"
    for f, r in p.black:
        b[8 * (r - 1) + f] = "p"
    for s, pc in trebuchet.items():
        i = movegen.sq(s)
        assert b[i] == movegen.EMPTY, "trebuchet overlaps the component"
        b[i] = pc
    ep = None
    if keep_ep and p.ep is not None and p.ep[2] == stm:
        (f, r), _, _ = p.ep
        ep = 8 * (r - 1) + f
    return movegen.Position(tuple(b), movegen.WHITE if stm == "W" else movegen.BLACK, ep, 0, 1)


def component_of(pos: movegen.Position, files=range(4)) -> Pos:
    """Inverse of embed for the pawns on `files` (ep dropped)."""
    w, bl = set(), set()
    for s, pc in enumerate(pos.board):
        f, r = s % 8, s // 8 + 1
        if f in files:
            if pc == "P":
                w.add((f, r))
            elif pc == "p":
                bl.add((f, r))
    return Pos(frozenset(w), frozenset(bl))


def trebuchet_intact(pos: movegen.Position, trebuchet=TREBUCHET) -> bool:
    return all(pos.board[movegen.sq(s)] == pc for s, pc in trebuchet.items())


def only_component_and_trebuchet(pos: movegen.Position, trebuchet=TREBUCHET, files=range(4)) -> bool:
    """True if every man is either a pawn on files a-d or a trebuchet man in place."""
    treb = {movegen.sq(s) for s in trebuchet}
    for s, pc in enumerate(pos.board):
        if pc == movegen.EMPTY:
            continue
        if s in treb:
            continue
        if s % 8 in files and pc in "Pp":
            continue
        return False
    return trebuchet_intact(pos, trebuchet)


@lru_cache(maxsize=None)
def model_outcome(board: Board, p: Pos, rule: str) -> str:
    """cylcgt outcome class of component p (as a game) under `rule`."""
    old = pawns.RACE_RULE
    try:
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        return cgt.outcome(pawns.value(board, p))
    finally:
        pawns.RACE_RULE = old
        pawns._value.cache_clear()
