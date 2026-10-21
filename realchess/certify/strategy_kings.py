"""Real-chess side conditions of the candidate-2 strategy (strategy.py):
every Black-to-move node of White's strategy tree, embedded with the
trebuchet, and Black's KING moves there (outside the pawn tree). Writes the
list of (node FEN, king-move child FEN) for engine / tablebase checks.
    PYTHONPATH=. .venv/bin/python -m realchess.certify.strategy_kings <cert.json> <out.json>"""
import json
import sys
from functools import lru_cache

from cylcgt.pawns import Pos

from realchess import component as C
from realchess import movegen as mg
from realchess.oracle_value import Terminals

d = json.load(open(sys.argv[1]))
T = Terminals(Pos.parse(d["component"]))
by = {str(t): t for t in T.terms}
fixed = {by[s["terminal"]]: s["class"] for s in d["tests"]["lower"]["support"]}
val = {t: (1 if fixed.get(t) == "L" else (-1 if fixed.get(t) == "R" else -2)) for t in T.terms}
sys.setrecursionlimit(100000)


@lru_cache(maxsize=None)
def win(p, side):
    other = "B" if side == "W" else "W"
    for q in C.options(T.board, p, side):
        if q in T.terms:
            if (val[q] > 0) == (side == "W"):
                return True
            continue
        if not win(q, other):
            return True
    return False


bnodes = set()


def walk(p, side):
    if side == "W":
        for q in C.options(T.board, p, "W"):
            if q in T.terms and val[q] > 0:
                return
            if q not in T.terms and not win(q, "B"):
                walk(q, "B")
                return
        raise AssertionError
    bnodes.add(p)
    for q in C.options(T.board, p, "B"):
        if q not in T.terms:
            walk(q, "W")


for first in "WB":
    walk(T.comp, first)
rows = []
for p in sorted(bnodes, key=str):
    pos = C.embed(p, "B")
    kids = []
    for m in mg.legal_moves(pos):
        if pos.board[m.frm].upper() == "K":
            kids.append({"move": m.uci(), "fen": mg.normal_fen(mg.make(pos, m))})
    rows.append({"node": str(p), "fen": mg.normal_fen(pos), "men": pos.men(),
                 "black_pawn_moves": len(C.options(T.board, p, "B")), "king_moves": kids})
json.dump({"component": d["component"], "black_to_move_nodes": rows}, open(sys.argv[2], "w"), indent=1)
print(len(rows), "Black-to-move strategy nodes;", sum(len(r["king_moves"]) for r in rows), "king moves;",
      sum(1 for r in rows if r["black_pawn_moves"] == 0), "zugzwang nodes")
