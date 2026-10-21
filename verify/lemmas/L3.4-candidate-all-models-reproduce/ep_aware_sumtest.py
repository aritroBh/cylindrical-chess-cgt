"""CGT-engine-free certificate of the e.p.-aware variant's value (verifier's own;
imports only indep.py / ep_passer.py from this directory, nothing from cylcgt/).

Claim checked: in the e.p.-aware variant V1 of ep_passer.py (a decided child whose
double-stepped pawn can be taken e.p. at once is not scored until the entitled side
has had its move), the candidate has value H = {2±1 | -2±1} = {{3|1} | {-1|-3}}
under the count and mover rules. Since -H = H, G = H iff G + H is a second-player
win. Contrast: the convention W (= *2) plus H is not P.
Also: G + *2 not P (so G != *2) is already shown by ep_passer.py.
Run: .venv/bin/python -I verify/lemmas/L3.4-candidate-all-models-reproduce/ep_aware_sumtest.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from functools import lru_cache
import indep as I
from ep_passer import contested

def intg(n):
    return ("i", n)
# H = {{3|1} | {-1|-3}}  (game nodes: ("g", Ls, Rs))
H = ("g", (("g", (intg(3),), (intg(1),)),), (("g", (intg(-1),), (intg(-3),)),))

def opts(h, side):
    if h[0] == "i":
        n = h[1]
        if side == "W":
            return (intg(n - 1),) if n > 0 else ()
        return (intg(n + 1),) if n < 0 else ()
    return h[1] if side == "W" else h[2]

def make(variant):
    def score_child(board, c, mover, rule):
        if variant and contested(board, c):
            return None
        return I.child_result(board, c, mover, rule)

    @lru_cache(maxsize=None)
    def wins(board, pos, h, stm, rule):
        other = "B" if stm == "W" else "W"
        t = I.term(board, pos)
        if t is not None:
            assert variant and contested(board, pos)
            s = pos[2][2]
            if stm != s:
                # the right lapses if the entitled side does not use it now:
                # stm may claim the standing result (BIG dominates any h here)
                res = I.race_win(board, pos, "B" if s == "W" else "W", rule) if t == 0 else ("W" if t == 1 else "B")
                if res == stm:
                    return True
                # otherwise stm may still move in h (keeping the right live for s)
                return any(not wins(board, pos, hh, other, rule) for hh in opts(h, stm))
        for c in I.gen(board, pos, stm):
            res = score_child(board, c, stm, rule)
            if res is None:
                res = stm if not wins(board, c, h, other, rule) else other
            if res == stm:
                return True
        for hh in opts(h, stm):
            if not wins(board, pos, hh, other, rule):
                return True
        return False
    return wins

def outcome(wins, board, pos, h, rule):
    a = wins(board, pos, h, "W", rule)
    b = not wins(board, pos, h, "B", rule)
    return {(True, True): "L", (False, False): "R", (True, False): "N", (False, True): "P"}[(a, b)]

if __name__ == "__main__":
    for files, root in ((4, I.mkpos("a2 c2", "b7 d7")), (8, I.mkpos("a2 c2 g4", "b7 d7 g5"))):
        board = (files, 8, True)
        for variant in (False, True):
            w = make(variant)
            for rule in ("count", "mover", "opponent"):
                print(f"files={files} ep=on {'e.p.-aware V1' if variant else 'convention W  '} rule={rule:8s}: "
                      f"o(G + H) = {outcome(w, board, root, H, rule)}   o(G + 0) = {outcome(w, board, root, intg(0), rule)}")
