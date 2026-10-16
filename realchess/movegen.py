"""Fully legal standard-chess move generation (pure stdlib).

Scope: positions with kings, pawns and Q/R/B/N on the ordinary 8x8 board.
Castling is NOT generated: a FEN whose castling field is not "-" is rejected
(none of the positions studied here can castle). Everything else is handled:
checks (single and double), pins, en passant (including the horizontal
"ep discovers a rook check" case), promotions and under-promotions,
checkmate and stalemate.

Squares are integers 0..63, index = 8 * rank + file, with a1 = 0, h8 = 63.
A Position is immutable; make() returns a new Position.

Legality is decided the simple, robust way: play the pseudo-legal move and
reject it if the mover's own king is then attacked.
"""
from __future__ import annotations

from dataclasses import dataclass

FILES = "abcdefgh"
WHITE, BLACK = "w", "b"
EMPTY = "."
PROMOS = "qrbn"

KNIGHT_D = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
KING_D = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
ROOK_D = [(1, 0), (-1, 0), (0, 1), (0, -1)]
BISHOP_D = [(1, 1), (1, -1), (-1, 1), (-1, -1)]


def sq(name: str) -> int:
    return 8 * (int(name[1]) - 1) + FILES.index(name[0])


def sqname(s: int) -> str:
    return FILES[s % 8] + str(s // 8 + 1)


def _off(s: int, df: int, dr: int):
    f, r = s % 8 + df, s // 8 + dr
    if 0 <= f < 8 and 0 <= r < 8:
        return 8 * r + f
    return None


# precomputed leaper targets and slider rays
_KN = [[t for t in (_off(s, df, dr) for df, dr in KNIGHT_D) if t is not None] for s in range(64)]
_KG = [[t for t in (_off(s, df, dr) for df, dr in KING_D) if t is not None] for s in range(64)]


def _ray(s, df, dr):
    out, t = [], _off(s, df, dr)
    while t is not None:
        out.append(t)
        t = _off(t, df, dr)
    return out


_RAYS_R = [[_ray(s, df, dr) for df, dr in ROOK_D] for s in range(64)]
_RAYS_B = [[_ray(s, df, dr) for df, dr in BISHOP_D] for s in range(64)]


def color_of(p: str):
    if p == EMPTY:
        return None
    return WHITE if p.isupper() else BLACK


@dataclass(frozen=True)
class Move:
    frm: int
    to: int
    promo: str | None = None  # lower-case piece letter
    ep: bool = False
    double: bool = False

    def uci(self) -> str:
        return sqname(self.frm) + sqname(self.to) + (self.promo or "")

    def __str__(self):
        return self.uci()


@dataclass(frozen=True)
class Position:
    board: tuple  # 64 one-char strings
    stm: str = WHITE
    ep: int | None = None  # en-passant target square (the square passed over)
    halfmove: int = 0
    fullmove: int = 1

    # ------------------------------------------------------------- queries
    def men(self) -> int:
        return sum(1 for p in self.board if p != EMPTY)

    def king(self, color: str) -> int:
        k = "K" if color == WHITE else "k"
        return self.board.index(k)

    def pieces(self, color: str):
        return [(s, p) for s, p in enumerate(self.board) if p != EMPTY and color_of(p) == color]


def attacked(board, s: int, by: str) -> bool:
    """Is square s attacked by side `by`?"""
    if by == WHITE:
        P, N, B, R, Q, K = "PNBRQK"
        # a white pawn attacks s from one rank below
        for df in (-1, 1):
            t = _off(s, df, -1)
            if t is not None and board[t] == P:
                return True
    else:
        P, N, B, R, Q, K = "pnbrqk"
        for df in (-1, 1):
            t = _off(s, df, 1)
            if t is not None and board[t] == P:
                return True
    for t in _KN[s]:
        if board[t] == N:
            return True
    for t in _KG[s]:
        if board[t] == K:
            return True
    for ray in _RAYS_R[s]:
        for t in ray:
            p = board[t]
            if p != EMPTY:
                if p == R or p == Q:
                    return True
                break
    for ray in _RAYS_B[s]:
        for t in ray:
            p = board[t]
            if p != EMPTY:
                if p == B or p == Q:
                    return True
                break
    return False


def in_check(pos: Position, color: str | None = None) -> bool:
    color = color or pos.stm
    other = BLACK if color == WHITE else WHITE
    return attacked(pos.board, pos.king(color), other)


def checkers(pos: Position, color: str | None = None):
    """Squares of the pieces giving check to `color`'s king."""
    color = color or pos.stm
    other = BLACK if color == WHITE else WHITE
    k = pos.king(color)
    out = []
    for s, p in pos.pieces(other):
        if _piece_attacks(pos.board, s, p, k):
            out.append(s)
    return out


def _piece_attacks(board, s, p, target) -> bool:
    u = p.upper()
    if u == "P":
        dr = 1 if p == "P" else -1
        return target in [t for t in (_off(s, -1, dr), _off(s, 1, dr)) if t is not None]
    if u == "N":
        return target in _KN[s]
    if u == "K":
        return target in _KG[s]
    rays = []
    if u in "RQ":
        rays += _RAYS_R[s]
    if u in "BQ":
        rays += _RAYS_B[s]
    for ray in rays:
        for t in ray:
            if t == target:
                return True
            if board[t] != EMPTY:
                break
    return False


def pseudo_moves(pos: Position):
    board, me = pos.board, pos.stm
    out = []
    for s, p in enumerate(board):
        if p == EMPTY or color_of(p) != me:
            continue
        u = p.upper()
        if u == "P":
            dr = 1 if me == WHITE else -1
            start = 1 if me == WHITE else 6
            last = 7 if me == WHITE else 0
            t = _off(s, 0, dr)
            if t is not None and board[t] == EMPTY:
                if t // 8 == last:
                    out += [Move(s, t, pr) for pr in PROMOS]
                else:
                    out.append(Move(s, t))
                    t2 = _off(s, 0, 2 * dr)
                    if s // 8 == start and board[t2] == EMPTY:
                        out.append(Move(s, t2, double=True))
            for df in (-1, 1):
                t = _off(s, df, dr)
                if t is None:
                    continue
                q = board[t]
                if q != EMPTY and color_of(q) != me and q.upper() != "K":
                    if t // 8 == last:
                        out += [Move(s, t, pr) for pr in PROMOS]
                    else:
                        out.append(Move(s, t))
                elif q == EMPTY and pos.ep is not None and t == pos.ep:
                    out.append(Move(s, t, ep=True))
        elif u == "N" or u == "K":
            for t in (_KN[s] if u == "N" else _KG[s]):
                q = board[t]
                if q == EMPTY or (color_of(q) != me and q.upper() != "K"):
                    out.append(Move(s, t))
        else:
            rays = []
            if u in "RQ":
                rays += _RAYS_R[s]
            if u in "BQ":
                rays += _RAYS_B[s]
            for ray in rays:
                for t in ray:
                    q = board[t]
                    if q == EMPTY:
                        out.append(Move(s, t))
                    else:
                        if color_of(q) != me and q.upper() != "K":
                            out.append(Move(s, t))
                        break
    return out


def make(pos: Position, m: Move) -> Position:
    b = list(pos.board)
    p = b[m.frm]
    captured = b[m.to] != EMPTY
    b[m.frm] = EMPTY
    if m.ep:
        cap_sq = m.to - 8 if pos.stm == WHITE else m.to + 8
        b[cap_sq] = EMPTY
        captured = True
    if m.promo:
        p = m.promo.upper() if pos.stm == WHITE else m.promo
    b[m.to] = p
    ep = (m.frm + m.to) // 2 if m.double else None
    zeroing = captured or p.upper() == "P" or m.promo is not None
    nxt = BLACK if pos.stm == WHITE else WHITE
    return Position(tuple(b), nxt, ep,
                    0 if zeroing else pos.halfmove + 1,
                    pos.fullmove + (1 if pos.stm == BLACK else 0))


def is_capture(pos: Position, m: Move) -> bool:
    return m.ep or pos.board[m.to] != EMPTY


def legal_moves(pos: Position):
    me = pos.stm
    other = BLACK if me == WHITE else WHITE
    out = []
    for m in pseudo_moves(pos):
        nb = make(pos, m).board
        k = m.to if pos.board[m.frm].upper() == "K" else pos.king(me)
        if not attacked(nb, k, other):
            out.append(m)
    return out


def status(pos: Position) -> str:
    """'checkmate', 'stalemate' or 'ongoing'."""
    if legal_moves(pos):
        return "ongoing"
    return "checkmate" if in_check(pos) else "stalemate"


# ------------------------------------------------------------------ FEN I/O
def parse_fen(fen: str) -> Position:
    parts = fen.replace("_", " ").split()
    if len(parts) < 2:
        raise ValueError(f"bad FEN: {fen!r}")
    rows = parts[0].split("/")
    if len(rows) != 8:
        raise ValueError(f"bad FEN board: {fen!r}")
    b = [EMPTY] * 64
    for i, row in enumerate(rows):
        r = 7 - i
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                if ch not in "PNBRQKpnbrqk" or f > 7:
                    raise ValueError(f"bad FEN row {row!r}")
                b[8 * r + f] = ch
                f += 1
        if f != 8:
            raise ValueError(f"bad FEN row {row!r}")
    stm = parts[1]
    if stm not in (WHITE, BLACK):
        raise ValueError(f"bad side to move in {fen!r}")
    castling = parts[2] if len(parts) > 2 else "-"
    if castling != "-":
        raise ValueError("castling rights are not supported by this generator")
    ep = None
    if len(parts) > 3 and parts[3] != "-":
        ep = sq(parts[3])
    half = int(parts[4]) if len(parts) > 4 else 0
    full = int(parts[5]) if len(parts) > 5 else 1
    return Position(tuple(b), stm, ep, half, full)


def ep_legal(pos: Position) -> bool:
    """True iff the side to move has a LEGAL en-passant capture."""
    if pos.ep is None:
        return False
    return any(m.ep for m in legal_moves(pos))


def ep_pseudo(pos: Position) -> bool:
    """True iff an en-passant capture is pseudo-legal (a pawn of the side to
    move stands next to the pawn that just double-stepped)."""
    if pos.ep is None:
        return False
    return any(m.ep for m in pseudo_moves(pos))


def to_fen(pos: Position, ep_mode: str = "pseudo", clocks: bool = True) -> str:
    """ep_mode: 'legal' writes the ep square only if a legal ep capture exists;
    'pseudo' (default, used for cache keys) if a pseudo-legal one exists, so a
    server still gets to judge pinned e.p. captures; 'always' whenever set."""
    rows = []
    for r in range(7, -1, -1):
        row, n = "", 0
        for f in range(8):
            p = pos.board[8 * r + f]
            if p == EMPTY:
                n += 1
            else:
                if n:
                    row += str(n)
                    n = 0
                row += p
        if n:
            row += str(n)
        rows.append(row)
    ep = "-"
    if pos.ep is not None and (ep_mode == "always" or
                               (ep_mode == "pseudo" and ep_pseudo(pos)) or
                               (ep_mode == "legal" and ep_legal(pos))):
        ep = sqname(pos.ep)
    fen = f"{'/'.join(rows)} {pos.stm} - {ep}"
    if clocks:
        fen += f" {pos.halfmove} {pos.fullmove}"
    return fen


def normal_fen(fen_or_pos) -> str:
    """Canonical FEN for probing/caching: pseudo-legal ep only, clocks '0 1'."""
    pos = parse_fen(fen_or_pos) if isinstance(fen_or_pos, str) else fen_or_pos
    return to_fen(pos, "pseudo", clocks=False) + " 0 1"


def validity_errors(pos: Position):
    """Basic legality checks (the ones a tablebase server enforces)."""
    errs = []
    if pos.board.count("K") != 1 or pos.board.count("k") != 1:
        errs.append("need exactly one king per side")
        return errs
    for s, p in enumerate(pos.board):
        if p in "Pp" and s // 8 in (0, 7):
            errs.append(f"pawn on back rank {sqname(s)}")
    other = BLACK if pos.stm == WHITE else WHITE
    if in_check(pos, other):
        errs.append("side not to move is in check")
    n_chk = len(checkers(pos))
    if n_chk > 2:
        errs.append("more than two checkers")
    if pos.ep is not None:
        r = pos.ep // 8
        exp_r = 5 if pos.stm == WHITE else 2
        pawn_sq = pos.ep - 8 if pos.stm == WHITE else pos.ep + 8
        start_sq = pos.ep + 8 if pos.stm == WHITE else pos.ep - 8
        want = "p" if pos.stm == WHITE else "P"
        if r != exp_r or pos.board[pawn_sq] != want or pos.board[pos.ep] != EMPTY \
                or pos.board[start_sq] != EMPTY:
            errs.append("inconsistent en-passant square")
    return errs


def perft(pos: Position, depth: int) -> int:
    if depth == 0:
        return 1
    ms = legal_moves(pos)
    if depth == 1:
        return len(ms)
    return sum(perft(make(pos, m), depth - 1) for m in ms)


def legal_uci(fen: str) -> set:
    return {m.uci() for m in legal_moves(parse_fen(fen))}


if __name__ == "__main__":  # tiny CLI: python -m realchess.movegen "<FEN>"
    import sys
    p = parse_fen(" ".join(sys.argv[1:]))
    print(to_fen(p), status(p))
    print(" ".join(sorted(m.uci() for m in legal_moves(p))))
