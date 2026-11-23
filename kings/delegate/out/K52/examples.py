"""Reproduce the referee's examples; run from the repository root."""
from functools import cache
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas import common
from check import conditions

assert pawns.BIG == 256 and pawns.PASSED_RESPECTS_EP and pawns.RACE_RULE == "count"
cgt.integer = cache(cgt.integer)


def outcomes(board, x):
    return cgt.outcome(pawns.value(board, x)), common.alt_outcome(board, x)


def e_witness(pieces, expected):
    board = Board(5, 7, False)
    plain = Pos.parse(pieces)
    x = Pos(plain.white, plain.black, ((0,3), (0,4), "B"))
    parent = Pos((x.white - {(0,4)}) | {(0,2)}, x.black)
    assert common.terminal(board, parent) is None and x in pawns.moves(board,parent,"W")
    assert common.terminal(board,x) is None and conditions(board,x) == (True,False)
    assert outcomes(board,x) == expected
    print(board, x, expected)
    for z in pawns.components(board,x):
        g = pawns.value(board,z)
        print(" component", z, g.num if g.num is not None else cgt.show(g),
              "threats", sorted(common.threats(board,z)))
    for y in pawns.moves(board,x,"B"):
        print(" Black option in W", y, common.alt_winner(board,y,"W"))


e_witness("W: a4 b3 e2 / B: a5 b4 e4", ("R","N"))
e_witness("W: a4 b2 b3 e2 e4 / B: a5 b4 b6 e6", ("N","L"))


@cache
def tempo(board, x, side):
    if common.terminal(board,x) is not None:
        return 0
    return max(((mover == side) + tempo(board,y,side) for mover in "WB"
                for y in pawns.moves(board,x,mover)), default=0)


b = Board(5,6,False,False)
x = Pos.parse("W: a2 a3 c2 d2 d3 e3 / B: a4 b3 d4")
y = Pos.parse("W: a2 a3 b3 d2 d3 e3 / B: a4 d4")
assert y in pawns.moves(b,x,"W") and conditions(b,x) == (True,True)
ms = [tempo(b,z,"B") for z in pawns.components(b,y)]
assert tempo(b,x,"B") == 1 and ms == [1,1]
print("stopped M_Black before/after c2xb3", tempo(b,x,"B"), ms)

x = Pos.parse("W: a4 d4 / B: b5 e5")
assert conditions(b,x) == (False,True) and outcomes(b,x) == ("P","N")
print("without HSS", x, outcomes(b,x))


@cache
def scored_threats(board, x):
    signs = set()
    for side in "WB":
        for y in pawns.moves(board,x,side):
            t = common.terminal(board,y)
            if t is None:
                signs.update(scored_threats(board,y))
            elif t == 0:
                signs.add(common.race_winner(board,y,side,"count"))
            else:
                signs.add("W" if t == 1 else "B")
    return frozenset(signs)


b = pawns.FLAT8
x = Pos.parse("W: b2 d6 / B: c7")
y = Pos.parse("W: b2 / B: d6")
assert y in pawns.moves(b,x,"B") and common.terminal(b,y) == 0
dist = [pawns.promote_distance(b,y,s) for s in "WB"]
assert dist == [5,5] and common.race_winner(b,y,"B","count") == "W"
assert scored_threats(b,x) == {"W"} and common.threats(b,x) == {-1,1}
assert outcomes(b,x) == ("L","L") and pawns.value(b,y).num == 0
print("c7xd6 distances",dist,"child score",pawns._child(b,y,"B").num,
      "split as a new root",pawns.value(b,y).num,"root",outcomes(b,x))

x = Pos.parse("W: a2 / B: h7")
assert pawns.value(b,x).num == 0 and common.terminal(b,x) == 0
print("opposite passers at root",x,pawns.value(b,x).num)

for height, text in ((4,"W: a2 / B: b3"), (5,"W: a2 b2 / B: b4")):
    b = Board(3,height,False)
    x = Pos.parse(text)
    assert common.terminal(b,x) is None
    y = next(y for y in pawns.moves(b,x,"W") if (0,4) in y.white)
    if height == 4:
        assert common.terminal(b,y) == 0 and pawns._child(b,y,"W").num == 256
    else:
        assert common.terminal(b,y) is None
        z = next(z for z in pawns.moves(b,y,"W") if (0,5) in z.white)
        assert pawns._child(b,z,"W").num == 256
    print("height",height,"after double step",y,common.terminal(b,y))
