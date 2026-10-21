"""C1-refute run2: Dawson's chess at the pawn level (3 x n flat board, compulsory captures,
misere: the player who makes the last move loses), compared with the candidate quotient.

Start positions: White pawns on rank 1, Black on rank 3, of every file except a chosen set of
empty files.  The quotient predicts: first player loses iff P[Psi(run lengths)].
Usage: python3 -I pawns_misere.py cert.txt NMAX
"""
import itertools
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
cert, NMAX = sys.argv[1], int(sys.argv[2])
it = iter(map(int, open(cert).read().split()))
N = next(it)
mult = [[next(it) for _ in range(N)] for _ in range(N)]
P = [next(it) for _ in range(N)]
phi = [next(it) for _ in range(33)]

promotions = [0]


def moves(board, n, side):
    """board: tuple of 3n cells (rank r in 0..2, file f) at index r*n+f; 0 empty, 1 W, 2 B.
    White moves r -> r+1, Black r -> r-1.  Returns successor boards (captures compulsory)."""
    me, op, d = (1, 2, 1) if side == 0 else (2, 1, -1)
    caps, pushes = [], []
    for r in range(3):
        for f in range(n):
            if board[r * n + f] != me:
                continue
            r2 = r + d
            if not 0 <= r2 < 3:
                continue
            for f2 in (f - 1, f + 1):
                if 0 <= f2 < n and board[r2 * n + f2] == op:
                    b = list(board)
                    b[r * n + f] = 0
                    b[r2 * n + f2] = me
                    if r2 == (2 if side == 0 else 0):
                        promotions[0] += 1
                    caps.append(tuple(b))
            if board[r2 * n + f] == 0:
                b = list(board)
                b[r * n + f] = 0
                b[r2 * n + f] = me
                if r2 == (2 if side == 0 else 0):
                    promotions[0] += 1
                pushes.append(tuple(b))
    return caps if caps else pushes


@lru_cache(None)
def mover_loses(board, n, side):
    """Misere: True iff the side to move loses with best play."""
    succ = moves(board, n, side)
    if not succ:
        return False  # cannot move: the opponent made the last move and loses
    return all(not mover_loses(b, n, 1 - side) for b in succ)


def psi(runs):
    x = phi[0]
    for k in runs:
        if k:
            x = mult[x][phi[k]]
    return x


checked = mism = 0
bad = []
for n in range(1, NMAX + 1):
    for nempty in range(0, 3):
        for empties in itertools.combinations(range(n), nempty):
            files = [f not in empties for f in range(n)]
            board = [0] * (3 * n)
            for f in range(n):
                if files[f]:
                    board[f] = 1
                    board[2 * n + f] = 2
            runs = [len(list(g)) for k, g in itertools.groupby(files) if k]
            if any(r > 32 for r in runs):
                continue
            pred = bool(P[psi(runs)])
            for side in (0, 1):
                got = mover_loses(tuple(board), n, side)
                checked += 1
                if got != pred:
                    mism += 1
                    bad.append((n, empties, side))
    print("n=%d: checked %d start positions so far, mismatches %d, promotions seen %d, cache %d"
          % (n, checked, mism, promotions[0], mover_loses.cache_info().currsize), flush=True)
print("RESULT: %d (board, empty-file set, side) cases on flat 3xn, n <= %d, <= 2 empty files; mismatches %d %s"
      % (checked, NMAX, mism, bad[:5]))
