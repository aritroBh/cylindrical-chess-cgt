"""Independent pawn-level solver for 3 x n Dawson's chess (flat or cylinder). Stdlib only.
Rules: W pawns on rank index 0, B on rank index 2, rank 1 empty.  Pawns push one square
forward onto an empty square or capture one square diagonally forward.  Captures are compulsory.
Normal play: side with no legal move loses.  No double step.  Any move that lands on the last
rank (promotion) is recorded in FLAGS and still allowed (promoted man treated as immobile)."""
import sys
from functools import lru_cache
sys.setrecursionlimit(100000)
FLAGS = {"promotion": 0, "dbl_step_geom": 0}

def make(n, wrap):
    def nb(f):
        out = []
        for g in (f - 1, f + 1):
            if wrap: g %= n
            if 0 <= g < n and g != f and g not in out: out.append(g)
        return out
    NB = [nb(f) for f in range(n)]

    def moves(b, side):  # b: tuple length 3n, index f*3+r ; side 1=W, 2=B
        caps, pushes = [], []
        d = 1 if side == 1 else -1
        opp = 3 - side
        for f in range(n):
            for r in range(3):
                if b[f*3+r] != side: continue
                r2 = r + d
                if not 0 <= r2 <= 2: continue          # promoted / last-rank man: immobile
                for g in NB[f]:
                    if b[g*3+r2] == opp: caps.append((f*3+r, g*3+r2, r2))
                if b[f*3+r2] == 0: pushes.append((f*3+r, f*3+r2, r2))
                if side == 1 and r == 0 and b[f*3+1] == 0 and b[f*3+2] == 0: FLAGS["dbl_step_geom"] += 1
                if side == 2 and r == 2 and b[f*3+1] == 0 and b[f*3+0] == 0: FLAGS["dbl_step_geom"] += 1
        res = []
        for (a, c, r2) in (caps if caps else pushes):
            if (side == 1 and r2 == 2) or (side == 2 and r2 == 0): FLAGS["promotion"] += 1
            l = list(b); l[a] = 0; l[c] = side; res.append(tuple(l))
        return res

    @lru_cache(maxsize=None)
    def win(b, side):  # True iff side to move wins (normal play)
        return any(not win(c, 3 - side) for c in moves(b, side))
    return win

def board(n, untouched):
    l = []
    for f in range(n):
        l += [1, 0, 2] if f in untouched else [0, 0, 0]
    return tuple(l)

def strips_board(lens):
    """strips of given lengths separated by single empty files on a flat board"""
    files, f = set(), 0
    for i, L in enumerate(lens):
        files |= set(range(f, f + L)); f += L + 1
    n = f - 1
    return n, board(n, files)
