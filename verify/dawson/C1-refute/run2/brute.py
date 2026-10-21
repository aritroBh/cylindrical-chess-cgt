"""C1-refute run2: brute-force misere outcomes straight from the octal-code definition,
compared with the candidate quotient's prediction P[Psi(G)].

Also checks that a 0.137 strip of n has the same game tree as a 0.07 heap of n+1 (heap 1 of 0.07
has no move, so it is a zero summand), which is what makes "strips <= 32" = "0.07 heaps <= 33".
No worker code is imported.  Usage: python3 -I brute.py cert.txt T
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)


def octal_options(code, n):
    """All options of a single heap n in octal game `code` (e.g. '0.137'), as sorted tuples of
    the nonempty heaps left behind.  Digit d_i (i = 1, 2, ...) governs removing i tokens:
    bit 1: allowed if that empties the heap; bit 2: allowed leaving one nonempty heap;
    bit 4: allowed leaving two nonempty heaps."""
    digits = [int(ch) for ch in code.split(".")[1]]
    out = set()
    for i, d in enumerate(digits, start=1):
        if n < i:
            continue
        r = n - i
        if d & 1 and r == 0:
            out.add(())
        if d & 2 and r >= 1:
            out.add((r,))
        if d & 4 and r >= 2:
            for a in range(1, r // 2 + 1):
                out.add(tuple(sorted((a, r - a))))
    return out


def main():
    cert, T = sys.argv[1], int(sys.argv[2])
    tok = open(cert).read().split()
    it = iter(map(int, tok))
    N = next(it)
    mult = [[next(it) for _ in range(N)] for _ in range(N)]
    P = [next(it) for _ in range(N)]
    phi = [next(it) for _ in range(33)]
    e = phi[0]

    # 1. game-tree identity 0.137 strip n  <->  0.07 heap n+1 (heaps of size 1 have no move)
    same = all({tuple(sorted(h + 1 for h in o)) for o in octal_options("0.137", n)}
               == {tuple(sorted(h for h in o if h >= 2)) for o in octal_options("0.07", n + 1)}
               for n in range(1, 33))
    print("0.137 strip n maps onto 0.07 heap n+1 option-for-option, n = 1..32:", same)
    print("0.07 heap 1 options:", octal_options("0.07", 1))
    print("0.137 options of strip 1..6:", [sorted(octal_options("0.137", n)) for n in range(1, 7)])

    # 2. brute-force misere outcomes of all sums of strips (lengths 1..32) with total <= T
    opts = {n: sorted(octal_options("0.137", n)) for n in range(1, 33)}

    @lru_cache(None)
    def isP(pos):  # misere: last player to move loses; pos = sorted tuple of strip lengths
        if not pos:
            return False  # no move: mover wins
        seen = set()
        for i, n in enumerate(pos):
            if n in seen:
                continue
            seen.add(n)
            rest = pos[:i] + pos[i + 1:]
            for o in opts[n]:
                if isP(tuple(sorted(rest + o))):
                    return False
        return True

    def psi(pos):
        x = e
        for n in pos:
            x = mult[x][phi[n]]
        return x

    def parts(total, maxpart):
        if total == 0:
            yield ()
            return
        for p in range(min(total, maxpart), 0, -1):
            for rest in parts(total - p, p):
                yield (p,) + rest

    count = mism = 0
    examples = []
    for t in range(T + 1):
        for pos in parts(t, 32):
            pos = tuple(sorted(pos))
            count += 1
            if isP(pos) != bool(P[psi(pos)]):
                mism += 1
                if len(examples) < 5:
                    examples.append(pos)
        print("total <= %d: %d positions, mismatches %d" % (t, count, mism), flush=True)
    print("RESULT: %d positions (all multisets of strips 1..32, total <= %d), mismatches %d %s"
          % (count, T, mism, examples))


main()
