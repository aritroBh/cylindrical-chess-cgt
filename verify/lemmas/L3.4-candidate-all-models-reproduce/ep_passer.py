"""Side probe (verifier's own, imports only indep.py): in the candidate's tree with
e.p. on, count children created by a double step whose double-stepped pawn is a
passer (child terminal or race) while the opponent holds a LEGAL e.p. capture of it.
The convention scores such a child at once, although in chess the passer can be
captured e.p. on the next move.  Then evaluate an e.p.-aware variant in which such a
child is not scored: the entitled side may capture e.p.; any other move of it, or a
move by the other side, leaves the passer standing (scored as before).
Run: .venv/bin/python -I verify/lemmas/L3.4-candidate-all-models-reproduce/ep_passer.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from functools import lru_cache
import indep as I

def contested(board, c):
    """c has a live right whose side can capture e.p., and c is decided (terminal/race)."""
    if c[2] is None or I.term(board, c) is None:
        return False
    s = c[2][2]
    t, victim, _ = c[2]
    mine = c[0] if s == "W" else c[1]
    d = 1 if s == "W" else -1
    return any((t[0] - p[0]) in (-1, 1) and p[1] + d == t[1] for p in mine)

def scan(board, root):
    R = I.reachable(board, root)
    hits = set()
    for y in R:
        if I.term(board, y) is not None:
            continue
        for side in "WB":
            src = y if (y[2] is None or y[2][2] == side) else (y[0], y[1], None)
            for c in I.gen(board, src, side):
                if contested(board, c):
                    hits.add((c, side, I.term(board, c)))
    return hits

def show(c):
    n = lambda s: "abcdefgh"[s[0]] + str(s[1])
    return "W: %s / B: %s (ep %s for %s)" % (" ".join(sorted(map(n, c[0]))), " ".join(sorted(map(n, c[1]))), n(c[2][0]), c[2][2])

def score_child(board, c, mover, rule):
    """'W'/'B' if decided; None if play continues (non-terminal or contested)."""
    if contested(board, c):
        return None
    return I.child_result(board, c, mover, rule)

@lru_cache(maxsize=None)
def wins(board, pos, heap, stm, rule):
    other = "B" if stm == "W" else "W"
    t = I.term(board, pos)
    if t is not None:
        assert contested(board, pos)
        s = pos[2][2]
        if stm != s:          # the other side moves: the right lapses, the passer stands
            # (race at a contested node: score by the rule as if the double-stepper just moved)
            res = I.race_win(board, pos, s == "W" and "B" or "W", rule) if t == 0 else ("W" if t == 1 else "B")
            return res == stm
        # entitled side to move: e.p. capture, any other pawn move, or a heap move
        for c in I.gen(board, pos, stm):
            res = score_child(board, c, stm, rule)
            if res is None:
                res = stm if not wins(board, c, heap, other, rule) else other
            if res == stm:
                return True
        for j in range(heap):
            if not wins(board, pos, j, other, rule):
                return True
        return False
    for c in I.gen(board, pos, stm):
        res = score_child(board, c, stm, rule)
        if res is None:
            res = stm if not wins(board, c, heap, other, rule) else other
        if res == stm:
            return True
    for j in range(heap):
        if not wins(board, pos, j, other, rule):
            return True
    return False

def outcome(board, pos, heap, rule):
    a = wins(board, pos, heap, "W", rule)
    b = not wins(board, pos, heap, "B", rule)
    return {(True, True): "L", (False, False): "R", (True, False): "N", (False, True): "P"}[(a, b)]

if __name__ == "__main__":
    for files, root in ((4, I.mkpos("a2 c2", "b7 d7")), (8, I.mkpos("a2 c2 g4", "b7 d7 g5"))):
        board = (files, 8, True)
        hits = scan(board, root)
        print(f"files={files}: contested children (double-step passer capturable e.p.): {len(hits)}")
        if files == 4:
            for c, mover, t in sorted(hits, key=lambda h: show(h[0])):
                print("   after", mover, ":", show(c), " convention score:", {1: "+BIG", -1: "-BIG", 0: "race"}[t])
        for rule in ("count", "mover", "opponent"):
            outs = {k: outcome(board, root, k, rule) for k in range(4)}
            print(f"   e.p.-aware variant, rule={rule:8s}: o(G+*k) k=0..3 {outs}")
