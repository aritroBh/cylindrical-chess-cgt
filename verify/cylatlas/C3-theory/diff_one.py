"""Find the first node where cylcgt.pawns (textbook) and sumtest's generator disagree, for one position.
  PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-theory/diff_one.py "W: a2 c2 / B: b3 d3 d7" 4"""
import sys
sys.setrecursionlimit(100000)
from functools import lru_cache
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from sumtest.sumsolver import Geometry, Rules
sys.path.insert(0, "verify/cylatlas/C3-theory")
from cgtkey import key
text, n = sys.argv[1], int(sys.argv[2])
geo = Geometry(n, False); rules = Rules(geo, ep=True, ep_aware=False, race_rule="count")
@lru_cache(maxsize=None)
def val(st):
    if st == "L": return cgt.integer(256)
    if st == "R": return cgt.integer(-256)
    W, B, e = st
    kids = {}
    for white in (True, False):
        kids[white] = [val(r if (r := rules.resolve(*c, white)) else c) for c in rules.moves(W, B, e, white)]
    return cgt.make(kids[True], kids[False])
board = Board(n, 8, False, True)
def walk(text, depth=0):
    p = Pos.parse(text); W, B = geo.parse(text)
    a = pawns.value(board, p); b = val((W, B, -1))
    print("  " * depth, text, "cylcgt", cgt.show(a)[:60], "| sumtest", cgt.show(b)[:60])
    if key(a) == key(b): return False
    # children without e.p. rights: compare child by child
    for side, white in (("W", True), ("B", False)):
        for q in pawns.moves(board, p, side):
            qa = pawns._child(board, q, side)
            Wq = sum(1 << geo.sq(f, r) for f, r in q.white); Bq = sum(1 << geo.sq(f, r) for f, r in q.black)
            e = -1
            if q.ep:
                e = geo.sq(*q.ep[0])
                # sumtest only records an e.p. square when an enemy pawn is adjacent
                if not any(m[2] == e for m in rules.moves(W, B, -1, white) if (m[0], m[1]) == (Wq, Bq)):
                    e = -1
            r = rules.resolve(Wq, Bq, e, white)
            qb = val(r if r else (Wq, Bq, e))
            if key(qa) != key(qb):
                print("  " * depth, " after", side, str(q), "cylcgt", cgt.show(qa)[:50], "| sumtest", cgt.show(qb)[:50],
                      "| cylcgt passed W/B:", pawns.passed(board, q, "W"), pawns.passed(board, q, "B"), "sumtest resolve:", r,
                      "dist cylcgt W/B", pawns.promote_distance(board, q, "W"), pawns.promote_distance(board, q, "B"))
                if r is None and not (pawns.passed(board, q, "W") or pawns.passed(board, q, "B")) and depth < 6:
                    walk(str(Pos(q.white, q.black)), depth + 1)
                return True
    return True
walk(text)
