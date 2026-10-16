"""A deliberately small legal-move chess checker for the lemma notes (L3, L4).

Scope: kings, queens, rooks, bishops, knights and pawns on an F x R board,
flat or cylindrical (files wrap: a and the last file are adjacent). Double
steps, en passant (also across the seam), promotion to Q/R/B/N, check,
checkmate and stalemate. No castling (the lemma positions never need it), no
50-move rule, no repetition rule.

It is NOT an engine. It is used to
  * enumerate legal moves exactly (e.g. "every king move drops the g-pawn",
    "no king is ever in check"), and
  * prove short forced wins by AND-OR search, where a line ends either in
    checkmate or in a "KQK leaf": exactly K+Q against a lone K on a FLAT board,
    with the lone king unable to capture the queen at once and not stalemated.
    That such a leaf is a forced win for the queen side is the standard
    tablebase fact for KQK (every such position is won); it is imported, not
    proved here. On a cylinder no KQK leaf is used.

Squares are (file, rank): file 0..F-1 (a=0), rank 1..R.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from functools import lru_cache

sys.setrecursionlimit(100000)

FILES = "abcdefghijklmnopqrstuvwxyz"
KNIGHT = ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1))
KING = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
ROOK_D = ((1, 0), (-1, 0), (0, 1), (0, -1))
BISHOP_D = ((1, 1), (1, -1), (-1, 1), (-1, -1))


@dataclass(frozen=True)
class Geo:
    files: int = 8
    ranks: int = 8
    wrap: bool = False

    def step(self, sq, df, dr):
        f, r = sq[0] + df, sq[1] + dr
        if not 1 <= r <= self.ranks:
            return None
        if self.wrap:
            f %= self.files
        elif not 0 <= f < self.files:
            return None
        return (f, r)


FLAT = Geo(8, 8, False)
CYL = Geo(8, 8, True)


@dataclass(frozen=True)
class Pos:
    geo: Geo
    pieces: frozenset  # of (square, colour, kind); colour in "WB", kind in "KQRBNP"
    stm: str           # side to move
    ep: tuple | None = None  # en-passant target square, usable by stm only

    def board(self):
        return {sq: (c, k) for sq, c, k in self.pieces}

    def __str__(self):
        def names(col):
            order = "KQRBNP"
            ps = sorted(((order.index(k), sq) for sq, c, k in self.pieces if c == col))
            return " ".join(f"{order[i]}{sqname(sq)}" for i, sq in ps)
        s = f"W: {names('W')} / B: {names('B')}, {self.stm} to move"
        if self.ep:
            s += f", ep {sqname(self.ep)}"
        return s


def sqname(sq):
    return f"{FILES[sq[0]]}{sq[1]}"


def sq_of(name):
    return (FILES.index(name[0]), int(name[1:]))


def make_pos(text: str, stm: str, geo: Geo = FLAT, ep=None) -> Pos:
    """'W: Kh8 Pa6 / B: Kb6 Pd3' ; a bare square means a pawn."""
    w, b = text.split("/")
    pieces = []
    for col, part in (("W", w), ("B", b)):
        for tok in part.split(":", 1)[1].split():
            if tok[0] in "KQRBN":
                pieces.append((sq_of(tok[1:]), col, tok[0]))
            else:
                pieces.append((sq_of(tok.lstrip("P")), col, "P"))
    return Pos(geo, frozenset(pieces), stm, sq_of(ep) if isinstance(ep, str) else ep)


def from_fen(fen: str, geo: Geo = FLAT) -> Pos:
    parts = fen.split()
    rows = parts[0].split("/")
    pieces = []
    for i, row in enumerate(rows):
        r = geo.ranks - i
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                pieces.append(((f, r), "W" if ch.isupper() else "B", ch.upper()))
                f += 1
    stm = "W" if parts[1] == "w" else "B"
    ep = None if len(parts) < 4 or parts[3] == "-" else sq_of(parts[3])
    return Pos(geo, frozenset(pieces), stm, ep)


# ---------------------------------------------------------------------------
# attacks and moves
# ---------------------------------------------------------------------------

def attacks_from(geo: Geo, bd: dict, sq, col, kind):
    """Squares attacked by the piece (col, kind) on sq."""
    out = []
    if kind == "P":
        dr = 1 if col == "W" else -1
        for df in (-1, 1):
            t = geo.step(sq, df, dr)
            if t is not None:
                out.append(t)
    elif kind == "N":
        out = [t for t in (geo.step(sq, df, dr) for df, dr in KNIGHT) if t is not None]
    elif kind == "K":
        out = [t for t in (geo.step(sq, df, dr) for df, dr in KING) if t is not None]
    else:
        dirs = (ROOK_D if kind == "R" else BISHOP_D if kind == "B" else ROOK_D + BISHOP_D)
        for df, dr in dirs:
            t = sq
            for _ in range(max(geo.files, geo.ranks)):
                t = geo.step(t, df, dr)
                if t is None or t == sq:
                    break
                out.append(t)
                if t in bd:
                    break
    return set(out)


def attacked(geo: Geo, bd: dict, sq, by: str) -> bool:
    for s, (c, k) in bd.items():
        if c == by and sq in attacks_from(geo, bd, s, c, k):
            return True
    return False


def king_sq(bd, col):
    for s, (c, k) in bd.items():
        if c == col and k == "K":
            return s
    return None


def in_check(pos: Pos, col: str | None = None) -> bool:
    col = pos.stm if col is None else col
    bd = pos.board()
    ks = king_sq(bd, col)
    return ks is not None and attacked(pos.geo, bd, ks, "B" if col == "W" else "W")


def _pseudo(pos: Pos):
    """Yields (description, new_board_dict, new_ep)."""
    geo, bd, col = pos.geo, pos.board(), pos.stm
    opp = "B" if col == "W" else "W"
    for sq, (c, k) in list(bd.items()):
        if c != col:
            continue
        if k == "P":
            dr = 1 if col == "W" else -1
            last = geo.ranks if col == "W" else 1
            start = 2 if col == "W" else geo.ranks - 1
            targets = []
            one = geo.step(sq, 0, dr)
            if one is not None and one not in bd:
                targets.append((one, None, None))
                two = geo.step(sq, 0, 2 * dr)
                if sq[1] == start and two is not None and two not in bd:
                    targets.append((two, None, one))
            for df in (-1, 1):
                t = geo.step(sq, df, dr)
                if t is None:
                    continue
                if t in bd and bd[t][0] == opp and bd[t][1] != "K":
                    targets.append((t, t, None))
                elif pos.ep is not None and t == pos.ep and t not in bd:
                    victim = (t[0], sq[1])
                    if bd.get(victim) == (opp, "P"):
                        targets.append((t, victim, None))
            for t, victim, new_ep in targets:
                nb = dict(bd)
                del nb[sq]
                if victim is not None:
                    del nb[victim]
                promos = "QRBN" if t[1] == last else "P"
                for pk in promos:
                    nb2 = dict(nb)
                    nb2[t] = (col, pk)
                    tag = "x" if victim else "-"
                    desc = f"{sqname(sq)}{tag}{sqname(t)}" + ("" if pk == "P" else f"={pk}")
                    yield desc, nb2, new_ep
        else:
            for t in attacks_from(geo, bd, sq, c, k):
                if t in bd and (bd[t][0] == col or bd[t][1] == "K"):
                    continue
                nb = dict(bd)
                del nb[sq]
                tag = "x" if t in bd else "-"
                nb[t] = (col, k)
                yield f"{k}{sqname(sq)}{tag}{sqname(t)}", nb, None


def legal_moves(pos: Pos):
    """List of (description, child Pos)."""
    out = []
    opp = "B" if pos.stm == "W" else "W"
    for desc, nb, new_ep in _pseudo(pos):
        ks = king_sq(nb, pos.stm)
        if ks is not None and attacked(pos.geo, nb, ks, opp):
            continue
        child = Pos(pos.geo, frozenset((s, c, k) for s, (c, k) in nb.items()), opp, new_ep)
        out.append((desc, child))
    return out


# ---------------------------------------------------------------------------
# forced-win search
# ---------------------------------------------------------------------------

def kqk_leaf(pos: Pos):
    """Winner if pos is a KQK leaf (see module doc), else None."""
    if pos.geo.wrap:
        return None
    kinds = sorted((c, k) for _, c, k in pos.pieces)
    if len(kinds) != 3 or sum(1 for _, k in kinds if k == "K") != 2:
        return None
    q = [(s, c) for s, c, k in pos.pieces if k == "Q"]
    if len(q) != 1:
        return None
    qsq, qcol = q[0]
    if pos.stm != qcol:
        moves = legal_moves(pos)
        if not moves:
            return None  # stalemate (or mate, handled by the caller)
        if any(child_has_no_queen(ch) for _, ch in moves):
            return None  # the lone king captures the queen
    return qcol


def child_has_no_queen(pos: Pos) -> bool:
    return not any(k == "Q" for _, _, k in pos.pieces)


@lru_cache(maxsize=None)
def forces_win(pos: Pos, who: str, depth: int) -> bool:
    """True if `who` can force checkmate or a KQK leaf within `depth` plies."""
    leaf = kqk_leaf(pos)
    if leaf is not None:
        return leaf == who
    moves = legal_moves(pos)
    if not moves:
        return in_check(pos) and pos.stm != who
    if depth == 0:
        return False
    if pos.stm == who:
        return any(forces_win(ch, who, depth - 1) for _, ch in moves)
    return all(forces_win(ch, who, depth - 1) for _, ch in moves)


def min_forced_win(pos: Pos, who: str, max_depth: int):
    """Smallest depth (plies) at which forces_win holds, or None."""
    for d in range(0, max_depth + 1):
        if forces_win(pos, who, d):
            return d
    return None


def principal_line(pos: Pos, who: str, depth: int, max_len: int = 40):
    """One line consistent with the forced win: `who` plays a fastest winning
    move; the defender plays a move that delays longest."""
    line = []
    while len(line) < max_len:
        if kqk_leaf(pos) is not None:
            line.append("(KQK leaf)")
            break
        moves = legal_moves(pos)
        if not moves:
            line.append("#" if in_check(pos) else "(stalemate)")
            break
        if pos.stm == who:
            best = None
            for desc, ch in moves:
                d = min_forced_win(ch, who, depth - 1)
                if d is not None and (best is None or d < best[0]):
                    best = (d, desc, ch)
            if best is None:
                line.append("(no win found)")
                break
            _, desc, pos = best
        else:
            worst = None
            for desc, ch in moves:
                d = min_forced_win(ch, who, depth - 1)
                if worst is None or (d if d is not None else 10**9) > worst[0]:
                    worst = (d if d is not None else 10**9, desc, ch)
            _, desc, pos = worst
        line.append(desc)
        depth -= 1
    return line
