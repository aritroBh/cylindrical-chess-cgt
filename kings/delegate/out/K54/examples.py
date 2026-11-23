"""Check both printed flags, their predecessors, and the short auxiliary examples."""
from functools import cache
from cylcgt import cgt, pawns
from lemmas import common

cgt.integer = cache(cgt.integer)
flat = pawns.Board(5, 7, False, True)
for aware in (True, False):
    pawns.PASSED_RESPECTS_EP = aware
    for rule in common.RULES:
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        common.alt_winner.cache_clear()
        common._T_memo.clear()
        for label, text, expected, values in (
            ("I", "W: a4 b3 e2 / B: a5 b4 e4", ("R", "N"), (cgt.integer(-257), cgt.STAR)),
            ("II", "W: a4 b2 b3 e2 e4 / B: a5 b4 b6 e6", ("N", "L"),
             (cgt.integer(-1), cgt.make([cgt.integer(2)], [cgt.integer(1)])))):
            root = pawns.Pos.parse(text)
            p = pawns.Pos(root.white, root.black, ((0, 3), (0, 4), "B"))
            pred = pawns.Pos(p.white-{(0,4)}|{(0,2)}, p.black)
            assert common.terminal(flat,p) is None and common.hereditarily_safe(flat,p)
            assert p in pawns.moves(flat,pred,"W") and common.terminal(flat,pred) is None
            assert tuple(pawns.value(flat,c) for c in pawns.components(flat,p)) == values
            pair = cgt.outcome(pawns.value(flat,p)),common.alt_outcome(flat,p,rule)
            prepair = cgt.outcome(pawns.value(flat,pred)),common.alt_outcome(flat,pred,rule)
            assert pair == expected
            print(label, "aware", aware, rule, "S,D", *pair, "predecessor", *prepair)

# A witness to (B) without the stronger bound B > N.
bd = pawns.Board(2,7,False,False)
p = pawns.Pos.parse("W: a2 / B: b3")
children = [q for side in "WB" for q in pawns.moves(bd,p,side)]
assert all(common.terminal(bd,q) is not None for q in children)
after = pawns.Pos.parse("W: b3 / B:")
assert after in children and pawns.moves(bd,after,"W")
print("strict bound witness: all first moves terminal, White b3-b4 still legal in the continuing game")

# Show exactly where an unqualified height-independent 6p bound fails.
bd = pawns.Board(1,11,False,False)
p = pawns.Pos.parse("W: a2 / B: a10")
for r in range(3,10):
    q = pawns.Pos(frozenset({(0,r)}),p.black)
    assert q in pawns.moves(bd,p,"W") and common.terminal(bd,q) is None
    p = q
print("H=11, one White pawn, seven quiet White moves")
