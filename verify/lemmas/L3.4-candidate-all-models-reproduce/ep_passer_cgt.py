"""Canonical values of the e.p.-aware variants (uses cylcgt.cgt read-only for
canonical forms; move generation and scoring from the verifier's indep.py).
  V1: every child that is decided (single passer or race) but whose double-stepped
      pawn can be taken e.p. at once is NOT scored; it becomes the node
      {entitled side's moves | passer stands} (orientation by colour).
  V2: the same, but only for single-passer children; races keep the convention score.
Run: PYTHONPATH=. .venv/bin/python verify/lemmas/L3.4-candidate-all-models-reproduce/ep_passer_cgt.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cylcgt import cgt
import indep as I
from ep_passer import contested

PB, NB = cgt.integer(I.BIG), cgt.integer(-I.BIG)

def make_model(board, rule, races_too):
    memo = {}
    def is_cont(c):
        return contested(board, c) and (races_too or I.term(board, c) != 0)
    def child(c, mover):
        if is_cont(c):
            return node(c)
        r = I.child_result(board, c, mover, rule)
        if r is None:
            return node(c)
        return PB if r == "W" else NB
    def node(x):
        g = memo.get(x)
        if g is not None:
            return g
        t = I.term(board, x)
        if t is not None:
            assert is_cont(x)
            s = x[2][2]
            stands = (PB if t == 1 else NB) if t != 0 else \
                (PB if I.race_win(board, x, "B" if s == "W" else "W", rule) == "W" else NB)
            kids = [child(c, s) for c in I.gen(board, x, s)]
            g = cgt.make(kids, [stands]) if s == "W" else cgt.make([stands], kids)
        else:
            lsrc = x if (x[2] is None or x[2][2] == "W") else (x[0], x[1], None)
            rsrc = x if (x[2] is None or x[2][2] == "B") else (x[0], x[1], None)
            g = cgt.make([child(c, "W") for c in I.gen(board, lsrc, "W")],
                         [child(c, "B") for c in I.gen(board, rsrc, "B")])
        memo[x] = g
        return g
    return node

if __name__ == "__main__":
    root = I.mkpos("a2 c2", "b7 d7")
    board = (4, 8, True)
    for races_too in (False, True):
        for rule in ("count", "mover", "opponent"):
            g = make_model(board, rule, races_too)(root)
            print(f"{'V1 (singles+races)' if races_too else 'V2 (singles only)  '} rule={rule:8s}: "
                  f"value {cgt.show(g)}  outcome {cgt.outcome(g)}")
    # sanity: with the contested test switched off the same code must give the convention W
    import ep_passer
    ep_passer_contested = contested
    def never(board, c): return False
    sys.modules[__name__].contested = never
    for rule in ("count", "mover", "opponent"):
        g = make_model(board, rule, True)(root)
        print(f"control (no contested nodes) rule={rule:8s}: value {cgt.show(g)}")
