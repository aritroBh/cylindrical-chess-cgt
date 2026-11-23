import sys
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos, FLAT8, value, moves, passed, components, BIG
from lemmas import common as C

def show(b, p, tag):
    g = value(b, p)
    print(tag, str(p), "value", cgt.show(g), "outcome", cgt.outcome(g))

def split_first(b, p):
    # alternative model: split first, then replace each component with a passer by +-BIG
    comps = components(b, p)
    if len(comps) > 1:
        return cgt.total(split_first(b, c) for c in comps)
    wp, bp = passed(b, p, "W"), passed(b, p, "B")
    if wp and bp: raise pawns.RaceError(str(p))
    if wp: return cgt.integer(BIG)
    if bp: return cgt.integer(-BIG)
    plain = Pos(p.white, p.black, None)
    lpos = plain if (p.ep and p.ep[2] != "W") else p
    rpos = plain if (p.ep and p.ep[2] != "B") else p
    def child(c, mover):
        comps = components(b, c)
        if len(comps) == 1 and passed(b, c, "W") and passed(b, c, "B"):
            w = C.race_winner(b, c, mover, "count")
            return cgt.integer(BIG if w == "W" else -BIG)
        return split_first(b, c)
    return cgt.make([child(c, "W") for c in moves(b, lpos, "W")], [child(c, "B") for c in moves(b, rpos, "B")])

print("== Q1 flat 8x8, W b2 d6 / B c7")
b = FLAT8
p = Pos.parse("W: b2 d6 / B: c7")
print("passed W,B:", passed(b,p,"W"), passed(b,p,"B"), "components:", [str(c) for c in components(b,p)])
show(b, p, "engine S:")
print("whole-board W outcome:", cgt.outcome(C.W(b,p)), " alt_outcome:", C.alt_outcome(b,p))
g = split_first(b, p); print("split-first:", cgt.show(g), cgt.outcome(g))
for c in moves(b, Pos(p.white,p.black,None), "B"):
    print("  Black child", c, "| passed W,B", passed(b,c,"W"), passed(b,c,"B"), "| comps", len(components(b,c)),
          "| engine", cgt.show(pawns._child(b,c,"B")), "| split-first", cgt.show(split_first(b,c)) if len(components(b,c))>1 else "-",
          "| alt winner W-to-move", (C.alt_winner(b,c,"W") if C.terminal(b,c) is None else "terminal"))
for c in moves(b, Pos(p.white,p.black,None), "W"):
    print("  White child", c, "| passed W,B", passed(b,c,"W"), passed(b,c,"B"))
c = Pos.parse("W: b2 / B: d6")
print("  c7xd6 child: promote_distance W", pawns.promote_distance(b,c,"W"), "B", pawns.promote_distance(b,c,"B"),
      "race winner (mover B, count):", C.race_winner(b,c,"B","count"))

print("== Q2a flat 2x4 (also 8x4), W a2 / B b3")
for nf in (2, 8):
    b = Board(nf, 4, False, True)
    p = Pos.parse("W: a2 / B: b3")
    print(" files", nf, "passed W,B:", passed(b,p,"W"), passed(b,p,"B"))
    for c in moves(b, p, "W"):
        print("   W move ->", c, "passed W,B", passed(b,c,"W"), passed(b,c,"B"), "child", cgt.show(pawns._child(b,c,"W")),
              "| promote_distance W,B", pawns.promote_distance(b,c,"W"), pawns.promote_distance(b,c,"B"))
        print("     moves of the pawn on a4:", [str(x) for x in moves(b, Pos(c.white,c.black,None), "W")])
    try:
        show(b, p, "   engine S:")
    except Exception as e: print("   raises", type(e).__name__, e)
    print("   W outcome:", cgt.outcome(C.W(b,p)), "alt:", C.alt_outcome(b,p))

print("== Q2b flat 5 ranks, W a2 b2 / B b4")
for nf in (2, 3, 8):
  for epaware in (True, False):
    pawns.PASSED_RESPECTS_EP = epaware; pawns._value.cache_clear(); C._W_memo.clear(); C.alt_winner.cache_clear()
    b = Board(nf, 5, False, True)
    p = Pos.parse("W: a2 b2 / B: b4")
    print(" files", nf, "e.p.-aware", epaware, "root passed W,B:", passed(b,p,"W"), passed(b,p,"B"))
    a4 = [c for c in moves(b,p,"W") if (0,4) in c.white][0]
    print("   after a2-a4:", a4, "passed W,B:", passed(b,a4,"W"), passed(b,a4,"B"))
    try:
        g = pawns._child(b, a4, "W"); print("   engine value of a4 child:", cgt.show(g), cgt.outcome(g))
    except Exception as e: print("   raises", type(e).__name__, e)
    lpos = Pos(a4.white, a4.black, None) if a4.ep and a4.ep[2] != "W" else a4
    for c in moves(b, lpos, "W"):
        print("     White option", c, "passed W,B", passed(b,c,"W"), passed(b,c,"B"), "child value", cgt.show(pawns._child(b,c,"W")))
    for c in moves(b, a4, "B"):
        print("     Black option", c, "passed W,B", passed(b,c,"W"), passed(b,c,"B"))
    try:
        show(b, p, "   engine S root:")
        print("   W outcome:", cgt.outcome(C.W(b,p)), "alt:", C.alt_outcome(b,p))
    except Exception as e: print("   raises", type(e).__name__, e)
pawns.PASSED_RESPECTS_EP = True
