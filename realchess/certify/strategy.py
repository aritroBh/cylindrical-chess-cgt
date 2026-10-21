"""White's strategy behind a certify_check lower-test certificate (heap 0):
in the pawn tree with the support terminals at +BIG (L) / -BIG (R) and every
other terminal at -2BIG, list White's winning strategy tree for the given
first player: every Black option, White's chosen reply, until a support
terminal or a Black zugzwang (no pawn move). Model-level object; see the
caveats (king moves are outside the tree).
    PYTHONPATH=. .venv/bin/python -m realchess.certify.strategy <cert.json> [W|B]"""
import json
import sys
from functools import lru_cache

from cylcgt.pawns import Pos

from realchess import component as C
from realchess.oracle_value import Terminals

d = json.load(open(sys.argv[1]))
first = sys.argv[2] if len(sys.argv) > 2 else "B"
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


nodes, terms, zug = set(), set(), set()


def walk(p, side, depth, lines, prefix):
    nodes.add((p, side))
    if side == "W":
        for q in C.options(T.board, p, "W"):
            if q in T.terms and val[q] > 0:
                terms.add(q)
                lines.append(prefix + f"W -> {q}  [support terminal, class L]")
                return
            if q not in T.terms and not win(q, "B"):
                lines.append(prefix + f"W -> {q}")
                walk(q, "B", depth + 1, lines, prefix + "  ")
                return
        raise AssertionError("no winning White move")
    opts = C.options(T.board, p, "B")
    if not opts:
        zug.add(p)
        lines.append(prefix + "B has no pawn move (zugzwang in the model)")
    for q in opts:
        assert q not in T.terms or val[q] > 0, q
        if q in T.terms:
            terms.add(q)
            lines.append(prefix + f"B -> {q}  [support terminal, class L]")
            continue
        lines.append(prefix + f"B -> {q}")
        walk(q, "W", depth + 1, lines, prefix + "  ")


lines = []
assert win(T.comp, first) == (first == "W") or first == "B" and not win(T.comp, "B")
walk(T.comp, first, 0, lines, "")
print("\n".join(lines))
print(json.dumps({"first": first, "strategy_nodes": len(nodes), "support_terminals_reached": sorted(map(str, terms)),
                  "black_zugzwang_nodes": sorted(map(str, zug))}))
