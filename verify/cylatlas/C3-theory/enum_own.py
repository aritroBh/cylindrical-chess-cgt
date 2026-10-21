"""Own enumerator (does not use atlas/cylinder/enumerate.py).
Flat single components: span exactly k (every file of a-..k occupied), w,b>=1, w+b<=P, pawns on ranks 2..7,
no initial passed pawn; mirror-reduced.  Rings: cylinder of n files, every file occupied; dihedral-reduced."""
import itertools
from cylcgt import pawns
from cylcgt.pawns import Board, Pos

def positions(n, wrap, P):
    sqs = [(f, r) for f in range(n) for r in range(2, 8)]
    if wrap:
        G = [tuple((s * f + k) % n for f in range(n)) for s in (1, -1) for k in range(n)]
    else:
        G = [tuple(range(n)), tuple(n - 1 - f for f in range(n))]
    board = Board(n, 8, wrap, True)
    for tot in range(2, P + 1):
        for w in range(1, tot):
            b = tot - w
            for W in itertools.combinations(sqs, w):
                rest = [s for s in sqs if s not in W]
                for B in itertools.combinations(rest, b):
                    if len({f for f, _ in W + B}) != n:
                        continue
                    key = (tuple(sorted(W)), tuple(sorted(B)))
                    imgs = [(tuple(sorted((g[f], r) for f, r in W)), tuple(sorted((g[f], r) for f, r in B))) for g in G]
                    if min(imgs) != key:
                        continue
                    pos = Pos(frozenset(W), frozenset(B))
                    if pawns.passed(board, pos, "W") or pawns.passed(board, pos, "B"):
                        continue
                    yield w, b, pos

if __name__ == "__main__":
    import sys
    P = 5
    for n in range(1, 6):
        print("flat span", n, sum(1 for _ in positions(n, False, P)), flush=True)
    for n in (3, 4, 5):
        print("ring", n, sum(1 for _ in positions(n, True, P)), flush=True)
