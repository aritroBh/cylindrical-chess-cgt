"""Independent exhaustive misere outcomes for sums of 0.137 strips, and comparison with a
quotient certificate's predictions.  Written for C1-refute; imports nothing from the project.

Move rule (from the pawn picture): in a strip of n untouched files, a move picks f in 1..n
and leaves strips max(0, f-2) and max(0, n-f-1).  Misere: a player with no move WINS, so the
empty position is N; a nonempty position is P iff every option is N.

Usage: python3 brute_misere.py cert.txt T
  compares, for every multiset of strips of length 1..nmax (strip 2 kept as its own length)
  with total <= T, the brute outcome with "Phi(G) in P" from the certificate.
"""
import sys
import time


def load_cert(path):
    tok = open(path).read().split()
    it = iter(tok)
    N = int(next(it))
    mult = [[int(next(it)) for _ in range(N)] for _ in range(N)]
    P = [next(it) == "1" for _ in range(N)]
    nmax = int(next(it))
    phi = [int(next(it)) for _ in range(nmax + 1)]
    return N, mult, P, nmax, phi


def strip_options(n):
    return sorted({(max(0, f - 2), max(0, n - f - 1)) for f in range(1, n + 1)})


def partitions(t, maxpart):
    """partitions of t into parts <= maxpart, as non-increasing tuples"""
    if t == 0:
        yield ()
        return
    for first in range(min(t, maxpart), 0, -1):
        for rest in partitions(t - first, first):
            yield (first,) + rest


def main(certpath, T):
    N, mult, P, nmax, phi = load_cert(certpath)
    OPT = {n: strip_options(n) for n in range(1, T + 1)}
    outcome = {(): False}  # False = N (mover wins), True = P
    t0 = time.time()
    single_P = []
    checked = bad = 0
    first_bad = []
    for t in range(1, T + 1):
        for lam in partitions(t, t):
            lst = list(lam)
            isP = True
            seen = set()
            for i, n in enumerate(lst):
                if n in seen:
                    continue
                seen.add(n)
                rest = lst[:i] + lst[i + 1:]
                for (a, b) in OPT[n]:
                    new = rest + [x for x in (a, b) if x > 0]
                    key = tuple(sorted(new, reverse=True))
                    if outcome[key]:  # option is P -> current is N
                        isP = False
                        break
                if not isP:
                    break
            outcome[lam] = isP
            if len(lam) == 1 and isP:
                single_P.append(lam[0])
            if max(lam) <= nmax:
                x = phi[0]
                for n in lam:
                    x = mult[x][phi[n]]
                checked += 1
                if P[x] != isP:
                    bad += 1
                    if len(first_bad) < 5:
                        first_bad.append(lam)
        print(f"total {t:3d}: {len(outcome)} positions so far, {time.time() - t0:.1f}s", flush=True)
    print(f"single strips n <= {T} that are misere P-positions: {single_P}")
    print(f"certificate {certpath}: checked {checked} positions (strips <= {nmax}, total <= {T}); "
          f"disagreements: {bad} {first_bad}")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
