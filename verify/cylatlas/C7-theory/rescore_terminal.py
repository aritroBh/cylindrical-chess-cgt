"""Does the *2 depend on the terminal nodes where the new passer stands en prise to the
enemy king?  Whole-board recursion (no component splitting) over the 4-file component,
using cylcgt.pawns.moves/passed and cylcgt.cgt (read-only), count race rule, e.p. on,
textbook passed test.  Placement on the 8-file cylinder: component on a-d, trebuchet
W g4 / B g5, WK h5, BK f4 (FEN 8/1p1p4/8/6pK/5kP1/8/P1P5/8).  Terminal nodes whose black
passer-holding side has a pawn on a square WK h5 attacks (a4,a5,a6,g/h squares) or that
checks h5 are rescored to S in {-BIG (model), 0, +BIG}.  Also the mirror placement for White.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/cylatlas/C7-theory/rescore_terminal.py"""
from functools import lru_cache
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
BIG = pawns.BIG
board = Board(4, 8, False, True)
WK = (7, 5)  # h5 ; component files a-d are 0..3 on the 8-file cylinder
def adj_cyl(p, k):
    return p != k and min((p[0] - k[0]) % 8, (k[0] - p[0]) % 8) <= 1 and abs(p[1] - k[1]) <= 1
def b_checks(p, k):
    return p[1] - 1 == k[1] and min((p[0] - k[0]) % 8, (k[0] - p[0]) % 8) == 1
def run(S):
    hits = [0]
    @lru_cache(maxsize=None)
    def val(pos):
        wp, bp = pawns.passed(board, pos, "W"), pawns.passed(board, pos, "B")
        if wp and bp:
            raise RuntimeError("race at entry")
        if wp:
            return cgt.integer(BIG)
        if bp:
            if any(adj_cyl(p, WK) or b_checks(p, WK) for p in pos.black):
                hits[0] += 1
                return cgt.integer(S)
            return cgt.integer(-BIG)
        plain = Pos(pos.white, pos.black, None)
        lpos = plain if (pos.ep and pos.ep[2] != "W") else pos
        rpos = plain if (pos.ep and pos.ep[2] != "B") else pos
        L = [child(p, "W") for p in pawns.moves(board, lpos, "W")]
        R = [child(p, "B") for p in pawns.moves(board, rpos, "B")]
        return cgt.make(L, R)
    def child(p, mover):
        if pawns.passed(board, p, "W") and pawns.passed(board, p, "B"):
            other = "B" if mover == "W" else "W"
            win = other if pawns.promote_distance(board, p, other) <= pawns.promote_distance(board, p, mover) else mover
            return cgt.integer(BIG if win == "W" else -BIG)
        return val(p)
    g = val(Pos.parse("W: a2 c2 / B: b7 d7"))
    return cgt.show(g), hits[0]
pawns.RACE_RULE = "count"
for S in (-BIG, 0, BIG):
    print(f"terminal en-prise-passer nodes scored {S:+d}: value = {run(S)[0]}   (distinct such nodes hit: {run(S)[1]})")
