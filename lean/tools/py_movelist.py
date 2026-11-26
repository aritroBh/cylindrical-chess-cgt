#!/usr/bin/env python3
"""Python printer with the same input and output as `lake exe movelist` (lean/MoveList.lean).

Format: lean/notes/L1.md section 1. Flat boards and cylinders use cylcgt/pawns.py, the Mobius strip
research/mobius/mob_pawns.py. The engines supply only moves() and passed(); the module settings
PASSED_RESPECTS_EP and RACE_RULE are set per input line. Normal form (e.p. rights), the race
distances, the classification and the ordering are written here, from the notes.

Usage (repository root): .venv/bin/python lean/tools/py_movelist.py < positions.txt
"""
import os
import re
import sys
from dataclasses import dataclass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "research", "mobius"))
from cylcgt import pawns as flat_engine  # noqa: E402
import mob_pawns as mob_engine  # noqa: E402

FILES = "abcdefghijklmnopqrstuvwxyz"
INF = 10 ** 6  # "no front passed pawn" in the count rule (Lean: none = infinity)


class Err(Exception):
    pass


@dataclass(frozen=True)
class Geo:
    topo: str  # flat | cyl | mob
    files: int
    ranks: int
    ep_on: bool


def cap_targets(geo, f, r, up):
    """Diagonal forward capture squares (file, rank, up) of a pawn (Lean Board.captureTargets)."""
    out = []
    r1 = r + 1 if up else r - 1
    if not 1 <= r1 <= geo.ranks:
        return out
    for df in (1, -1):
        g = f + df
        flip = False
        if g < 0 or g >= geo.files:
            if geo.topo == "flat":
                continue
            g %= geo.files
            flip = geo.topo == "mob"
        if flip:
            out.append((g, geo.ranks + 1 - r1, not up))
        else:
            out.append((g, r1, up))
    return out


def normalise(geo, W, B, ep_sq):
    """Normal form of the e.p. right (Lean Position.normalize). W, B: lists of (file, rank, up).
    Returns (file, rank, owner, up) of the named pawn if the right is real, else None."""
    if ep_sq is None or not geo.ep_on:
        return None
    named = None
    for owner, pawns in (("W", W), ("B", B)):
        for p in pawns:
            if (p[0], p[1]) == ep_sq:
                named = (p, owner)
    if named is None:
        return None
    (f, r, up), owner = named
    home = 2 if up else geo.ranks - 1
    step = 1 if up else -1
    if r != home + 2 * step:
        return None
    occupied = {(p[0], p[1]) for p in W + B}
    skipped = (f, home + step)
    if skipped in occupied or (f, home) in occupied:
        return None
    enemy = B if owner == "W" else W
    if not any(t[:2] == skipped for q in enemy for t in cap_targets(geo, q[0], q[1], q[2])):
        return None
    return (f, r, owner, up)


def canon(geo, W, B, ep_sq):
    """Normal form of a position: sorted pawns and the real e.p. right (or None)."""
    W = sorted(W)
    B = sorted(B)
    return W, B, normalise(geo, W, B, ep_sq)


def show_pos(W, B, ep):
    def side(colour, pawns):
        normal = colour == "W"
        return "".join(" " + FILES[f] + str(r) + ("" if up == normal else "*") for f, r, up in pawns)

    s = "W:" + side("W", W) + " / B:" + side("B", B)
    if ep is not None:
        s += " / ep " + FILES[ep[0]] + str(ep[1])
    return s


def engine_board(geo, mod):
    if geo.topo == "mob":
        return mod.Board(geo.files, "mob", geo.ep_on)
    return mod.Board(geo.files, geo.ranks, geo.topo == "cyl", geo.ep_on)


def engine_pos(geo, mod, W, B, ep):
    """Engine position for canonical (W, B, ep); ep is the output of normalise()."""
    if geo.topo == "mob":
        w = frozenset((f, r, 1 if up else -1) for f, r, up in W)
        b = frozenset((f, r, 1 if up else -1) for f, r, up in B)
    else:
        w = frozenset((f, r) for f, r, _ in W)
        b = frozenset((f, r) for f, r, _ in B)
    e = None
    if ep is not None:
        f, r, owner, up = ep
        step = 1 if up else -1
        e = ((f, r - step), (f, r), "B" if owner == "W" else "W")
    return mod.Pos(w, b, e)


def from_engine(geo, pos):
    """Canonical (W, B, ep-named-square) from an engine child; the e.p. right is normalised here."""
    def conv(pawns, up_of):
        out = []
        for p in pawns:
            if geo.topo == "mob":
                out.append((p[0], p[1], p[2] == 1))
            else:
                out.append((p[0], p[1], up_of))
        return out

    W = conv(pos.white, True)
    B = conv(pos.black, False)
    named = None if pos.ep is None else pos.ep[1]
    return canon(geo, W, B, named)


def passed(geo, mod, W, B, ep, colour):
    return mod.passed(engine_board(geo, mod), engine_pos(geo, mod, W, B, ep), colour)


def pawn_passed(geo, mod, W, B, ep, pawn, colour):
    """True if this one pawn of `colour` is passed in the position (the other pawns of that colour removed)."""
    if colour == "W":
        one_w, one_b = [pawn], B
    else:
        one_w, one_b = W, [pawn]
    return mod.passed(engine_board(geo, mod), engine_pos(geo, mod, one_w, one_b, ep), colour)


def race_distance(geo, mod, W, B, ep, colour):
    """Least distance to promotion over the front passed pawns of `colour` (Lean raceDistance); None = infinity."""
    mine = W if colour == "W" else B
    alls = W + B
    best = None
    for p in mine:
        f, r, up = p
        if not pawn_passed(geo, mod, W, B, ep, p, colour):
            continue
        ahead = [q for q in alls if q[0] == f and ((q[1] > r) if up else (q[1] < r))]
        if ahead:
            continue  # not the front pawn of its file
        d = geo.ranks - r if up else r - 1
        if r == (2 if up else geo.ranks - 1) and d >= 2:
            d -= 1
        best = d if best is None else min(best, d)
    return best


def classify_child(geo, mod, W, B, ep, mover):
    """Outcome of a position reached by a move of `mover`: '-', 'W', 'B', 'RW' or 'RB'."""
    wp = passed(geo, mod, W, B, ep, "W")
    bp = passed(geo, mod, W, B, ep, "B")
    if not wp and not bp:
        return "-"
    if wp and not bp:
        return "W"
    if bp and not wp:
        return "B"
    other = "B" if mover == "W" else "W"
    rule = mod.RACE_RULE
    if rule == "mover":
        winner = mover
    elif rule == "opponent":
        winner = other
    else:
        dm = race_distance(geo, mod, W, B, ep, mover)
        do = race_distance(geo, mod, W, B, ep, other)
        dm = INF if dm is None else dm
        do = INF if do is None else do
        winner = other if do <= dm else mover
    return "R" + winner


def side_line(geo, mod, W, B, ep, mover):
    kids = {}
    for child in mod.moves(engine_board(geo, mod), engine_pos(geo, mod, W, B, ep), mover):
        cw, cb, cep = from_engine(geo, child)
        text = show_pos(cw, cb, None if cep is None else (cep[0], cep[1]))
        kids[text] = (cw, cb, cep)
    items = []
    for text, (cw, cb, cep) in kids.items():
        cls = classify_child(geo, mod, cw, cb, cep, mover)
        items.append(text + " = " + cls)
    items.sort()
    tag = mover
    return f"{tag}[{len(items)}]:" + ("" if not items else " " + " ; ".join(items))


def tokens(text):
    return [t for t in text.split(" ") if t != ""]


def parse_square(t):
    cs = list(t)
    rev = bool(cs) and cs[-1] == "*"
    if rev:
        cs = cs[:-1]
    if not cs:
        raise Err("empty square")
    c, rest = cs[0], "".join(cs[1:])
    if not ("a" <= c <= "z") or not re.fullmatch(r"[0-9]+", rest):
        raise Err(f"bad square {t}")
    return FILES.index(c), int(rest), rev


def parse_pawns(colour, body):
    out = []
    for t in tokens(body):
        f, r, rev = parse_square(t)
        up = (colour == "W") != rev
        out.append((f, r, up))
    return out


def parse_line(line):
    parts = line.split("|")
    if len(parts) != 2:
        raise Err("expected `<settings> | <position>`")
    head, body = parts
    h = tokens(head)
    if len(h) != 5:
        raise Err("expected `<topology> <files> <ranks> <ep> <race>`")
    topo, files, ranks, ep, race = h
    if topo not in ("flat", "cyl", "mob"):
        raise Err(f"bad topology {topo}")
    if not re.fullmatch(r"[0-9]+", files):
        raise Err(f"bad files {files}")
    if not re.fullmatch(r"[0-9]+", ranks):
        raise Err(f"bad ranks {ranks}")
    if ep not in ("off", "textbook", "aware"):
        raise Err(f"bad ep option {ep}")
    if race not in ("count", "mover", "opponent"):
        raise Err(f"bad race rule {race}")
    geo = Geo(topo, int(files), int(ranks), ep != "off")
    settings = (ep, race)

    pp = [x.strip() for x in body.split("/")]
    if len(pp) == 2:
        w_part, b_part, e_part = pp[0], pp[1], None
    elif len(pp) == 3:
        w_part, b_part, e_part = pp
    else:
        raise Err("expected `W: ... / B: ...[ / ep <square>]`")
    if not (w_part.startswith("W:") and b_part.startswith("B:")):
        raise Err("expected `W: ... / B: ...`")
    W = parse_pawns("W", w_part[2:])
    B = parse_pawns("B", b_part[2:])
    ep_sq = None
    if e_part is not None:
        if not e_part.startswith("ep "):
            raise Err("expected `ep <square>`")
        f, r, _ = parse_square(e_part[3:].strip())
        ep_sq = (f, r)
    allp = W + B
    squares = [(f, r) for f, r, _ in allp]
    # Lean Board.valid
    if topo != "flat" and geo.files < 3:
        raise Err("invalid board (a cylinder or strip needs at least 3 files)")
    ok = all(f < geo.files and 1 <= r <= geo.ranks for f, r, _ in allp) and len(set(squares)) == len(squares)
    if topo != "mob":
        # Lean Position.valid: normal directions, no white pawn on rank 1, no black pawn on the last rank
        ok = ok and all(up and r != 1 for _, r, up in W) and all(not up and r != geo.ranks for _, r, up in B)
    if not ok:
        raise Err("invalid position (off board, two pawns on a square, a pawn on its first rank, or a * off the strip)")
    return geo, settings, W, B, ep_sq


def configure(geo, settings):
    ep, race = settings
    for mod in (flat_engine, mob_engine):
        mod.PASSED_RESPECTS_EP = ep == "aware"
        mod.RACE_RULE = race
    if geo.topo == "mob":
        mob_engine.H = geo.ranks  # the strip's mirror is ranks + 1 - r (Lean Board.mirror)
    return mob_engine if geo.topo == "mob" else flat_engine


def process(line):
    geo, settings, W, B, ep_sq = parse_line(line)
    mod = configure(geo, settings)
    W, B, ep = canon(geo, W, B, ep_sq)
    root = show_pos(W, B, None if ep is None else (ep[0], ep[1]))
    wp = passed(geo, mod, W, B, ep, "W")
    bp = passed(geo, mod, W, B, ep, "B")
    status = {(False, False): "-", (True, False): "W", (False, True): "B", (True, True): "WB"}[(wp, bp)]
    left = side_line(geo, mod, W, B, ep, "W")
    right = side_line(geo, mod, W, B, ep, "B")
    return f"{root} | {status} | {left} | {right}"


def main():
    for raw in sys.stdin:
        line = raw.strip()
        if line == "" or line.startswith("#"):
            continue
        try:
            out = process(line)
        except Err as e:
            out = "error: " + str(e)
        sys.stdout.write(out + "\n")


if __name__ == "__main__":
    main()
