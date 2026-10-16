from cylcgt import cgt
from cylcgt.pawns import Pos

from realchess import component as C
from realchess import movegen as mg


def test_embedding_is_the_proposed_fen():
    p = Pos.parse("W: a2 c2 / B: b7 d7")
    assert mg.to_fen(C.embed(p, "W")) == "8/1p1p4/8/5Kp1/6Pk/8/P1P5/8 w - - 0 1"
    assert mg.to_fen(C.embed(p, "B")) == "8/1p1p4/8/5Kp1/6Pk/8/P1P5/8 b - - 0 1"


def test_terminal_substitution_reproduces_cylcgt():
    root = Pos.parse("W: a2 c2 / B: b7 d7")
    big, nbig = cgt.integer(C.BIG), cgt.integer(-C.BIG)
    for rule, want in (("count", cgt.nimber(2)), ("mover", cgt.nimber(2)), ("opponent", cgt.ZERO)):
        g = C.value_with(C.BOARD4, root,
                         lambda q, m: big if C.model_terminal_value(C.BOARD4, q, m, rule) > 0 else nbig)
        assert g is want
