"""Prop. 12 of the paper: pure pawn game (no passed-pawn rule), flat 6x6, e.p. on,
Y = W a4 f4 / B b4 e5 with Black's e.p. right b4xa3 (White has just played a2-a4).
Claim: whole board = {0 | -4, -3+-2} (first-player win); sum of the two components = {-1* | -5*} (black wins);
they differ with White to move.
Part 1: independent minimax outcomes.  Part 2 (repo engine, values): lemmas.common.pure / pure_sum.
Run:  PYTHONPATH=. .venv/bin/python notes/proof_audit2/checks/prop12_check.py
"""
import sys
from functools import lru_cache
sys.path.insert(0, "notes/proof_audit2/checks")
import indep_sum_model as M
M.configure(6, 6, False, True, "count", True)

def sq(s): return ("abcdef".index(s[0]), int(s[1:]))
W = frozenset(map(sq, ["a4", "f4"])); B = frozenset(map(sq, ["b4", "e5"]))
EP = (sq("a3"), sq("a4"), "B")          # target square, captured pawn, side entitled to capture

@lru_cache(maxsize=None)
def whole_win(Wp, Bp, ep, side):
    other = 'B' if side == 'W' else 'W'
    for (w2, b2, e2) in M.pawn_moves(Wp, Bp, ep, side):
        if not whole_win(w2, b2, e2, other):
            return True
    return False

@lru_cache(maxsize=None)
def sum_win(cs, side):
    other = 'B' if side == 'W' else 'W'
    for i, (Wp, Bp, ep) in enumerate(cs):
        rest = cs[:i] + cs[i+1:]
        for (w2, b2, e2) in M.pawn_moves(Wp, Bp, ep, side):
            nxt = M.canon(rest + tuple(M.comps(w2, b2, e2)))   # re-split; rights stay inside their component
            if not sum_win(nxt, other):
                return True
    return False

def cls(first_w, second_b_loses):  # White wins moving first?, White wins moving second?
    return {(True, True): 'L', (False, False): 'R', (True, False): 'N', (False, True): 'P'}[(first_w, second_b_loses)]

wf = whole_win(W, B, EP, 'W'); ws = not whole_win(W, B, EP, 'B')
print("whole board, as in chess (Black's right live):  White-first wins =", wf, " White-second wins =", ws, "-> class", cls(wf, ws))
# the chess position has Black to move: the right is live.  White to move: the right has expired (it is for Black only).
cs = M.canon(tuple(M.comps(W, B, EP)))
sf = sum_win(cs, 'W'); ss = not sum_win(cs, 'B')
print("sum of components (right survives elsewhere):  White-first wins =", sf, " White-second wins =", ss, "-> class", cls(sf, ss))
print("components:", [(sorted(c[0]), sorted(c[1]), c[2]) for c in cs])
try:
    from cylcgt import cgt
    from cylcgt.pawns import Board, Pos
    from lemmas import common as C
    b = Board(6, 6, False, True)
    pos = Pos(frozenset(W), frozenset(B), EP)
    print("repo pure whole  :", cgt.show(C.pure(b, pos)), cgt.outcome(C.pure(b, pos)))
    print("repo pure sum    :", cgt.show(C.pure_sum(b, pos)), cgt.outcome(C.pure_sum(b, pos)))
except Exception as e:
    print("repo engine part skipped:", e)
