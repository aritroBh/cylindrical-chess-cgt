"""Dawson's Chess on a 3 x n board, flat or cylindrical, solved as a partizan
game straight from the pawn rules (no octal-game shortcut).

Rules: White pawns start on rank 1, Black on rank 3, rank 2 empty. Pawns move
one square forward or capture diagonally forward; captures are compulsory.
Normal play: the player who cannot move loses.

The partizan values printed here are values of each board played alone; they
are not Grundy values (flat n=5 gives * where g(5) = 3) and must not be added.
Compulsory captures act across the whole board, so the additive invariant is
the impartial macro-move value g of octal 0.137 (notes/lemmas.md, L5.4).

Run: .venv/bin/python -m cylcgt.dawson 20
"""
import sys
from functools import lru_cache

from . import cgt


def octal_0137(N):
    """Grundy values of octal game 0.137 (Dawson's Kayles shifted), path of n pins."""
    g = [0] * (N + 1)
    for n in range(1, N + 1):
        opts = set()
        if n == 1:
            opts.add(0)
        if n >= 2:
            opts.add(g[n - 2])
        for a in range(0, n - 2):
            opts.add(g[a] ^ g[n - 3 - a])
        m = 0
        while m in opts:
            m += 1
        g[n] = m
    return g


def solve(n: int, wrap: bool):
    def nb(f, d):
        x = f + d
        if wrap:
            return x % n
        return x if 0 <= x < n else None

    @lru_cache(maxsize=None)
    def value(W, B):
        return cgt.make(options(W, B, "W"), options(W, B, "B"))

    def options(W, B, side):
        mine, theirs = (W, B) if side == "W" else (B, W)
        d = 1 if side == "W" else -1
        caps, pushes = [], []
        occ = W | B
        for (f, r) in mine:
            r1 = r + d
            if not 1 <= r1 <= 3:
                continue
            for df in (-1, 1):
                g = nb(f, df)
                if g is not None and (g, r1) in theirs:
                    caps.append((mine - {(f, r)} | {(g, r1)}, theirs - {(g, r1)}))
            if (f, r1) not in occ:
                pushes.append((mine - {(f, r)} | {(f, r1)}, theirs))
        moves = caps if caps else pushes
        out = []
        for m, t in dict.fromkeys(moves):
            W2, B2 = (m, t) if side == "W" else (t, m)
            out.append(value(frozenset(W2), frozenset(B2)))
        return out

    W = frozenset((f, 1) for f in range(n))
    B = frozenset((f, 3) for f in range(n))
    return value(W, B)


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    g = octal_0137(N + 3)
    print(" n | flat value | 0.137 g(n) | ring value | mex{g(n-3)} ")
    for n in range(1, N + 1):
        flat = solve(n, False)
        ring = solve(n, True) if n >= 3 else None
        pred_ring = None if n < 3 else (1 if g[n - 3] == 0 else 0)
        print(f"{n:2d} | {cgt.show(flat):10s} | {g[n]:10d} | {cgt.show(ring) if ring else '-':10s} | {pred_ring}")
