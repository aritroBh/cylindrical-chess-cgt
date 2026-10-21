"""Board geometry, move names and text rendering for ChessSums instances.

This module has its own move generator (it does not call `cylcgt.pawns.moves`)
so that move names are explicit; `bench/tests` checks that both generators give
the same set of successor positions.

Coordinates: files 0..W-1 are named a, b, c, ...; ranks are 1..8.
Move names: "e2-e4" (push), "d4xe5" (capture), "a4xh5" (capture across the
seam of a cylinder). En passant never occurs in ChessSums positions: every
component is filtered so that no en-passant capture is ever available in its
game tree (see components.py), and different components cannot interact.
"""
from __future__ import annotations

from dataclasses import dataclass

FILES = "abcdefghijklmnopqrstuvwxyz"
RANKS = 8


@dataclass(frozen=True)
class Geometry:
    files: int
    wrap: bool
    ranks: int = RANKS

    def nb(self, f: int, df: int):
        g = f + df
        if self.wrap:
            return g % self.files
        return g if 0 <= g < self.files else None


def sqname(s) -> str:
    return f"{FILES[s[0]]}{s[1]}"


def parse_sq(t: str):
    t = t.strip()
    if len(t) < 2 or t[0] not in FILES or not t[1:].isdigit():
        raise ValueError(f"bad square {t!r}")
    return (FILES.index(t[0]), int(t[1:]))


def gen_moves(geo: Geometry, white: frozenset, black: frozenset, side: str):
    """Yield (name, from_sq, to_sq, new_white, new_black) for every legal pawn
    move of `side`, assuming no en-passant right is pending."""
    mine, theirs = (white, black) if side == "W" else (black, white)
    occ = white | black
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else geo.ranks - 1
    out = []
    for (f, r) in sorted(mine):
        r1 = r + d
        if not (1 <= r1 <= geo.ranks):
            continue
        rest = mine - {(f, r)}
        if (f, r1) not in occ:
            out.append((f"{sqname((f, r))}-{sqname((f, r1))}", (f, r), (f, r1), rest | {(f, r1)}, theirs))
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= geo.ranks and (f, r2) not in occ:
                out.append((f"{sqname((f, r))}-{sqname((f, r2))}", (f, r), (f, r2), rest | {(f, r2)}, theirs))
        for df in (-1, 1):
            g = geo.nb(f, df)
            if g is None:
                continue
            t = (g, r1)
            if t in theirs:
                out.append((f"{sqname((f, r))}x{sqname(t)}", (f, r), t, rest | {t}, theirs - {t}))
    res = []
    seen = set()
    for name, fr, to, m2, t2 in out:
        if name in seen:  # a capture to the same square from both sides on a 2-file ring
            continue
        seen.add(name)
        if side == "W":
            res.append((name, fr, to, frozenset(m2), frozenset(t2)))
        else:
            res.append((name, fr, to, frozenset(t2), frozenset(m2)))
    return res


def parse_move(text: str):
    """Parse 'e2-e4', 'e2e4', 'd4xe5', 'd4:e5' into (from_sq, to_sq); also
    returns None for a SAN-like answer such as 'e4' or 'dxe5' (resolved by
    `resolve_move`)."""
    t = text.strip().rstrip("+#!?.").replace(" ", "")
    for sep in ("-", "x", ":", "×"):
        if sep in t:
            a, b = t.split(sep, 1)
            try:
                return parse_sq(a), parse_sq(b)
            except ValueError:
                return None
    if len(t) >= 4:
        # e2e4 / a10a11
        for i in range(2, len(t) - 1):
            try:
                return parse_sq(t[:i]), parse_sq(t[i:])
            except ValueError:
                continue
    return None


def resolve_move(text: str, legal: list[tuple]):
    """Map a move answer to the name of a legal move, or None if it is not
    legal / not recognisable. `legal` is the output of gen_moves."""
    if not isinstance(text, str):
        return None
    t = text.strip().rstrip("+#!?.").replace(" ", "")
    if not t:
        return None
    fr_to = parse_move(t)
    if fr_to is not None:
        for name, fr, to, *_ in legal:
            if (fr, to) == fr_to:
                return name
        return None
    # SAN-like: "e4" (push to e4) or "dxe5" (capture from the d-file)
    t2 = t.replace("×", "x").replace(":", "x")
    try:
        if "x" in t2:
            ffile, dest = t2.split("x", 1)
            if len(ffile) != 1 or ffile not in FILES:
                return None
            to = parse_sq(dest)
            cands = [name for name, fr, tt, *_ in legal if tt == to and fr[0] == FILES.index(ffile) and fr[0] != tt[0]]
        else:
            to = parse_sq(t2)
            cands = [name for name, fr, tt, *_ in legal if tt == to and fr[0] == tt[0]]
    except ValueError:
        return None
    return cands[0] if len(cands) == 1 else None


def diagram(geo: Geometry, white, black) -> str:
    """ASCII board, rank 8 at the top. P = White pawn, p = Black pawn."""
    lines = []
    for r in range(geo.ranks, 0, -1):
        row = []
        for f in range(geo.files):
            row.append("P" if (f, r) in white else "p" if (f, r) in black else ".")
        lines.append(f"{r} " + " ".join(row))
    lines.append("  " + " ".join(FILES[f] for f in range(geo.files)))
    return "\n".join(lines)


def placement(geo: Geometry, white, black) -> str:
    """FEN-style piece placement (rank 8 first, '/' between ranks, digits for
    runs of empty squares; runs may exceed 8 on wide boards). No kings: this
    is a pawn-only game, not a legal chess FEN."""
    ranks = []
    for r in range(geo.ranks, 0, -1):
        s, run = "", 0
        for f in range(geo.files):
            c = "P" if (f, r) in white else "p" if (f, r) in black else None
            if c is None:
                run += 1
            else:
                if run:
                    s += str(run)
                    run = 0
                s += c
        if run:
            s += str(run)
        ranks.append(s)
    return "/".join(ranks)


def pos_text(white, black) -> str:
    """Same text format as cylcgt.pawns.Pos.__str__ (without e.p.)."""
    w = " ".join(sorted(map(sqname, white)))
    b = " ".join(sorted(map(sqname, black)))
    return f"W: {w} / B: {b}"


def parse_pos_text(text: str):
    w_part, b_part = text.split("/")
    w = frozenset(parse_sq(t) for t in w_part.split(":")[1].split())
    b = frozenset(parse_sq(t) for t in b_part.split(":")[1].split())
    return w, b
