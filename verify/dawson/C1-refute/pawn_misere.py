"""Independent pawn-level misere solver for Dawson's chess on a flat 3 x n board (C1-refute).

Rules: White pawns on rank 1, Black on rank 3, rank 2 empty.  A pawn moves one square straight
forward onto an empty square or captures one square diagonally forward; captures are
compulsory.  A pawn reaching its last rank is flagged (promotion) -- it never happens.
Misere: the player with no legal move WINS (the last player to move loses).

Compares the outcome of the start position (White to move) with the misere outcome of a single
0.137 strip of length n, computed here by its own small recursion.

Usage: python3 -I pawn_misere.py NMAX
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
PROMO = []


def solve_board(n):
    start = tuple(["W"] * n + ["."] * n + ["B"] * n)  # index r*n + f, r = 0 (rank1) .. 2

    @lru_cache(maxsize=None)
    def wins(cells, side):  # True if side to move wins (misere)
        dr = 1 if side == "W" else -1
        enemy = "B" if side == "W" else "W"
        caps, pushes = [], []
        for r in range(3):
            for f in range(n):
                if cells[r * n + f] != side:
                    continue
                r2 = r + dr
                if not 0 <= r2 < 3:
                    continue
                for f2 in (f - 1, f + 1):
                    if 0 <= f2 < n and cells[r2 * n + f2] == enemy:
                        caps.append((r * n + f, r2 * n + f2, r2))
                if cells[r2 * n + f] == ".":
                    pushes.append((r * n + f, r2 * n + f, r2))
        moves = caps if caps else pushes
        if not moves:
            return True  # misere: no move -> win
        other = enemy
        for (a, b, r2) in moves:
            if (side == "W" and r2 == 2) or (side == "B" and r2 == 0):
                PROMO.append((n, cells, a, b))
            c = list(cells)
            c[b] = side
            c[a] = "."
            if not wins(tuple(c), other):
                return True
        return False

    return wins(start, "W")


@lru_cache(maxsize=None)
def strip_win(pos):  # pos: sorted tuple of strip lengths; True = mover wins (misere)
    if not pos:
        return True
    lst = list(pos)
    for i, m in enumerate(lst):
        rest = lst[:i] + lst[i + 1:]
        for f in range(1, m + 1):
            new = rest + [x for x in (max(0, f - 2), max(0, m - f - 1)) if x > 0]
            if not strip_win(tuple(sorted(new))):
                return True
    return False


def main(nmax):
    for n in range(1, nmax + 1):
        b = solve_board(n)
        s = strip_win((n,))
        print(f"3x{n}: pawn-level first player {'wins' if b else 'loses'}; strip {n}: "
              f"{'N' if s else 'P'}; {'agree' if b == s else 'DISAGREE'}", flush=True)
    print(f"promotions encountered: {len(PROMO)}")


if __name__ == "__main__":
    main(int(sys.argv[1]))
