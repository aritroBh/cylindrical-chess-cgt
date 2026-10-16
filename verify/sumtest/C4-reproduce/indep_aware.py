"""C4 verifier: an independent e.p.-aware value computation.

Move generation: cylcgt.pawns.moves (read-only import; stores an e.p. flag after
every double step).  Passer test, e.p.-awareness, race resolution and the
recursion are written here from scratch, so this shares no code with
sumtest/sumsolver.py.  Canonical forms from cylcgt.cgt.

Convention (as claimed for the 'aware' test): a pawn that the opponent could
capture en passant on its very next move in this component is not yet passed.
An e.p. right dies with the next move made in the component (by either side).
"""
import sys
from functools import lru_cache
from cylcgt import pawns, cgt

BIG = 256
RULE = sys.argv[1] if len(sys.argv) > 1 else "count"
AWARE = (sys.argv[2] != "plain") if len(sys.argv) > 2 else True
B = pawns.Board(4, 8, False, True)


def adjacent_files(f):
    return [g for g in (f - 1, f + 1) if 0 <= g < B.files]


def ep_capturable(pos):
    """the square of a pawn that can be taken e.p. right now, else None"""
    if not pos.ep:
        return None
    target, victim, capturer = pos.ep
    theirs = pos.black if capturer == "B" else pos.white
    for g in adjacent_files(victim[0]):
        if (g, victim[1]) in theirs:
            return victim
    return None


def passers(pos, side):
    mine = pos.white if side == "W" else pos.black
    theirs = pos.black if side == "W" else pos.white
    if AWARE:
        v = ep_capturable(pos)
        if v is not None and v in mine:
            mine = mine - {v}
    out = []
    for f, r in mine:
        span = {f, *adjacent_files(f)}
        if side == "W":
            stop = any(g in span and s > r for g, s in theirs)
        else:
            stop = any(g in span and s < r for g, s in theirs)
        if not stop:
            out.append((f, r))
    return out


def dist(sqs, side):
    best = 99
    for f, r in sqs:
        if side == "W":
            d = 8 - r - (1 if r == 2 else 0)
        else:
            d = r - 1 - (1 if r == 7 else 0)
        best = min(best, d)
    return best


def after(pos, mover):
    wp, bp = passers(pos, "W"), passers(pos, "B")
    if wp and not bp:
        return cgt.integer(BIG)
    if bp and not wp:
        return cgt.integer(-BIG)
    if wp and bp:
        other = "B" if mover == "W" else "W"
        if RULE == "mover":
            win = mover
        elif RULE == "opponent":
            win = other
        else:
            dm = dist(wp if mover == "W" else bp, mover)
            do = dist(bp if mover == "W" else wp, other)
            win = other if do <= dm else mover
        return cgt.integer(BIG if win == "W" else -BIG)
    return val(pos)


@lru_cache(maxsize=None)
def val(pos):
    L = [after(c, "W") for c in pawns.moves(B, pos, "W")]
    R = [after(c, "B") for c in pawns.moves(B, pos, "B")]
    return cgt.make(L, R)


for txt in ("W: a2 c2 / B: b4 d7", "W: a2 c2 / B: b5 d7", "W: a2 c2 / B: b7 d7"):
    p = pawns.Pos.parse(txt)
    print(RULE, "aware" if AWARE else "plain", txt, "->", cgt.show(val(p)))

if len(sys.argv) > 3:
    X = pawns.Pos.parse("W: a2 c2 / B: b4 d7")
    for side in "WB":
        for c in pawns.moves(B, X, side):
            print("   ", side, "->", c, ":", cgt.show(after(c, side)))
    a4 = [c for c in pawns.moves(B, X, "W") if (0, 4) in c.white][0]
    print("after a2-a4:", a4, "passersW", passers(a4, "W"), "passersB", passers(a4, "B"))
    for c in pawns.moves(B, a4, "B"):
        print("   B reply ->", c, ": wp", passers(c, "W"), "bp", passers(c, "B"), ":", cgt.show(after(c, "B")))
