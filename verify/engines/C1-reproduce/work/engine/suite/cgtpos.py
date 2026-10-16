"""CGT model of "trebuchet + queenside pawn component" positions on the real 8x8 board.

A queenside component G lives on files a-d (file e empty). It is evaluated with
cylcgt on the 4-file flat 8-rank board, en passant on (real chess). A trebuchet
freezes both kings on files f-h, so (in the model) any king move loses: it drops
that side's g-pawn. The model therefore predicts

    White to move wins  <=>  not (G <= 0)
    a White move G -> G' wins  <=>  G' >= 0       (king moves: always lose)
    a Black move G -> G' wins  <=>  G' <= 0

This module only reads cylcgt (read-only) and builds FENs / move labels.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from cylcgt import cgt, pawns  # noqa: E402

B4 = pawns.Board(4, 8, False, True)  # files a-d, flat (a-file edge, e-file empty), e.p. on
FILES = "abcdefgh"
RULES = ("count", "mover", "opponent")


def sqn(s):
    return f"{FILES[s[0]]}{s[1]}"


def labeled_moves(board, pos, side):
    """Pawn moves of `side` as (uci, san, kind, child Pos).

    Mirrors pawns.moves() exactly (asserted), but keeps the move label."""
    mine, theirs = (pos.white, pos.black) if side == "W" else (pos.black, pos.white)
    occ = pos.white | pos.black
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else board.ranks - 1
    last = board.ranks if side == "W" else 1
    ep_target = pos.ep if (pos.ep and pos.ep[2] == side) else None
    out = []

    def mk(new_mine, new_theirs, ep=None):
        if side == "W":
            return pawns.Pos(frozenset(new_mine), frozenset(new_theirs), ep)
        return pawns.Pos(frozenset(new_theirs), frozenset(new_mine), ep)

    for (f, r) in sorted(mine):
        rest = mine - {(f, r)}
        r1 = r + d
        if not (1 <= r1 <= board.ranks):
            continue
        promo = "q" if r1 == last else ""
        if (f, r1) not in occ:
            out.append((sqn((f, r)) + sqn((f, r1)) + promo, sqn((f, r1)) + ("=Q" if promo else ""),
                        "push", mk(rest | {(f, r1)}, theirs)))
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= board.ranks and (f, r2) not in occ:
                ep = None
                if board.ep:
                    other = "B" if side == "W" else "W"
                    ep = ((f, r1), (f, r2), other)
                out.append((sqn((f, r)) + sqn((f, r2)), sqn((f, r2)), "double",
                            mk(rest | {(f, r2)}, theirs, ep)))
        for df in (-1, 1):
            g = board.nb(f, df)
            if g is None:
                continue
            t = (g, r1)
            san = f"{FILES[f]}x{sqn(t)}" + ("=Q" if promo else "")
            if t in theirs:
                out.append((sqn((f, r)) + sqn(t) + promo, san, "capture", mk(rest | {t}, theirs - {t})))
            elif ep_target and ep_target[0] == t:
                out.append((sqn((f, r)) + sqn(t), san, "ep", mk(rest | {t}, theirs - {ep_target[1]})))
    ref = pawns.moves(board, pos, side)
    assert set(m[3] for m in out) == set(ref) and len(out) == len(ref), (pos, side)
    return out


def set_rule(rule):
    if pawns.RACE_RULE != rule:
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()


def race_sensitive_tree(pos, board=B4):
    """Number of race nodes in the full (uncached) game tree of pos."""
    old = pawns.RACE_RULE
    pawns._value.cache_clear()
    n0 = len(pawns.race_hits)
    pawns.value(board, pos)
    n = len(pawns.race_hits) - n0
    pawns._value.cache_clear()
    pawns.RACE_RULE = old
    return n


def root_value(pos, board=B4):
    return pawns.value(board, pos)


def child_value(pos, mover, board=B4):
    return pawns._child(board, pos, mover)


def wins_for(mover, v):
    """Does a move by `mover` to a position of value v (opponent to move) win?"""
    return cgt.le(cgt.ZERO, v) if mover == "W" else cgt.le(v, cgt.ZERO)


def analyse(pos, stm, rule, board=B4):
    """CGT prediction for one queenside component with `stm` to move."""
    set_rule(rule)
    n0 = len(pawns.race_hits)
    v = root_value(pos, board)
    kids = []
    for uci, san, kind, child in labeled_moves(board, pos, stm):
        cv = child_value(child, stm, board)
        kids.append({"uci": uci, "san": san, "kind": kind, "child": str(child),
                     "value": cgt.show(cv), "wins": wins_for(stm, cv)})
    if stm == "W":
        root_wins = not cgt.le(v, cgt.ZERO)
    else:
        root_wins = not cgt.le(cgt.ZERO, v)
    assert root_wins == any(k["wins"] for k in kids), (str(pos), stm, rule)
    return {"value": cgt.show(v), "outcome": cgt.outcome(v), "stm_wins": root_wins,
            "moves": kids, "new_race_nodes": len(pawns.race_hits) - n0}


# --- trebuchets -------------------------------------------------------------
# A_r: W Pg_r, B Pg_(r+1), WK f_(r+1), BK h_r   (WK nearer the queenside)
# B_r: W Pg_r, B Pg_(r+1), WK h_(r+1), BK f_r   (BK nearer the queenside)

def trebuchet(kind, r):
    assert kind in "AB" and 2 <= r <= 6
    t = {(6, r): "P", (6, r + 1): "p"}
    if kind == "A":
        t[(5, r + 1)] = "K"
        t[(7, r)] = "k"
    else:
        t[(7, r + 1)] = "K"
        t[(5, r)] = "k"
    return t


def fen(pos, treb, stm):
    board = dict(treb)
    for s in pos.white:
        board[s] = "P"
    for s in pos.black:
        board[s] = "p"
    assert len(board) == len(treb) + len(pos.white) + len(pos.black)
    rows = []
    for r in range(8, 0, -1):
        row, empty = "", 0
        for f in range(8):
            p = board.get((f, r))
            if p is None:
                empty += 1
            else:
                if empty:
                    row += str(empty)
                    empty = 0
                row += p
        if empty:
            row += str(empty)
        rows.append(row)
    ep = "-"
    if pos.ep and pos.ep[2] == stm:
        ep = sqn(pos.ep[0])
    return f"{'/'.join(rows)} {'w' if stm == 'W' else 'b'} - {ep} 0 1"
