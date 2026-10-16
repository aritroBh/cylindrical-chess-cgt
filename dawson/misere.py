"""Misere play of Dawson's chess as the heap game 0.137 (sums of strips), by exhaustive
memoised search over multisets of heap sizes.

Exact simplifications used (game trees are identical, so they are exact in misere play):
  * heaps of size 0 are dropped;
  * a heap of size 2 has the single option "empty", exactly like a heap of size 1,
    so 2 is replaced by 1.
No other simplification is used.

Run from the project root:
    PYTHONPATH=. .venv/bin/python -m dawson.misere 40
"""
import sys
from functools import lru_cache

from dawson.octal import grundy, heap_moves, octal_options

sys.setrecursionlimit(1_000_000)
MV = octal_options("0.137")
HEAP_MOVES = {}


def hm(h):
    r = HEAP_MOVES.get(h)
    if r is None:
        r = HEAP_MOVES[h] = heap_moves(MV, h)
    return r


def canon(heaps):
    return tuple(sorted(1 if h == 2 else h for h in heaps if h > 0))


def options(pos):
    out = set()
    seen = set()
    for i, h in enumerate(pos):
        if h in seen:
            continue
        seen.add(h)
        rest = pos[:i] + pos[i + 1:]
        for parts in hm(h):
            out.add(canon(rest + parts))
    return out


@lru_cache(maxsize=None)
def _P(pos):
    if not pos:
        return False          # misere: the player to move with no move wins, so () is an N-position
    for q in options(pos):
        if _P(q):
            return False
    return True


def misere_P(heaps):
    """True iff the multiset of strips is a misere P-position (previous player wins)."""
    return _P(canon(heaps))


def partitions(total, maxpart=None):
    """All canonical multisets (parts != 2) with sum exactly `total`, as sorted tuples."""
    if maxpart is None:
        maxpart = total
    if total == 0:
        yield ()
        return
    for k in range(min(total, maxpart), 0, -1):
        if k == 2:
            continue
        for rest in partitions(total - k, k):
            yield rest + (k,)


def misere_nim_P(values):
    """Misere Nim P-positions: all heaps <= 1 and odd count of 1s, or some heap >= 2 and xor 0."""
    if all(v <= 1 for v in values):
        return sum(values) % 2 == 1
    x = 0
    for v in values:
        x ^= v
    return x == 0


def main(T=40):
    g = grundy("0.137", max(T, 60) + 5)
    print(f"Misere Dawson's chess (octal 0.137), exhaustive over all canonical positions of total <= {T}")
    counts, Pcounts = [], []
    tame_fail = []
    for t in range(T + 1):
        c = pc = 0
        for pos in partitions(t):
            c += 1
            isP = _P(pos)
            pc += isP
            if isP != misere_nim_P([g[h] for h in pos]):
                tame_fail.append(pos)
        counts.append(c)
        Pcounts.append(pc)
        print(f"  total {t:3d}: {c:7d} positions, {pc:6d} misere P-positions; cache {_P.cache_info().currsize}")
        sys.stdout.flush()
    print(f"positions with total <= {T}: {sum(counts)}; misere P-positions: {sum(Pcounts)}")
    single = "".join("P" if _P(canon((n,))) else "N" for n in range(0, T + 1))
    print(f"single strip n = 0..{T} misere outcome: {single}")
    print("single strips that are misere P:", [n for n in range(T + 1) if _P(canon((n,)))])
    print("single strips with normal g(n) = 0 (normal P):", [n for n in range(T + 1) if g[n] == 0])
    ring = {n: ("N" if _P(canon((n - 3,))) else "P") for n in range(3, T + 4)}
    print(f"single ring n = 3..{T+3} misere outcome (N = first player wins): " + "".join(ring[n] for n in range(3, T + 4)))
    print("rings that are misere N (first player wins):", [n for n in range(3, T + 4) if ring[n] == "N"])
    print("rings that are normal N (R_n = 1):", [n for n in range(3, T + 4) if g[n - 3] == 0])
    tame_fail.sort(key=lambda p: (sum(p), len(p), p))
    print(f"positions where the misere-Nim rule on normal Grundy values fails: {len(tame_fail)}")
    print("  smallest:", tame_fail[:15])
    return single, ring


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 40)
