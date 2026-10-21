"""Independent enumeration (verifier, not the worker's code) of the atoms that
determine the C3 value sets for w+b <= 5:

  flat atoms : flat k-file strip (k = 1..5), every file occupied, p pawns
               (max(k,2) <= p <= 5), no passed pawn for either side;
               reduced by the mirror f -> k-1-f.
  rings      : n-file cylinder (n = 3,4,5), every file occupied, p pawns
               (n <= p <= 5), no passed pawn; reduced by the dihedral group.

Pawns on ranks 2..7, at most one pawn per square, no e.p. right at the root.
Every flat position with <= 5 pawns on <= 8 files is a sum of at most two such
atoms (2+2 or 2+3 pawns when there are two), and every cylinder position with an
empty file equals the flat position cut there, so these atoms plus pairwise sums
give every value in the C3 comparison.

  .venv/bin/python verify/cylatlas/C3-reproduce/enum_atoms.py --count
"""
from __future__ import annotations

import itertools
import sys

RANKS = range(2, 8)


def nbrs(n, wrap, f):
    s = {f}
    for d in (-1, 1):
        g = f + d
        if wrap:
            s.add(g % n)
        elif 0 <= g < n:
            s.add(g)
    return s


def no_passer(n, wrap, W, B):
    for (f, r) in W:
        nb = nbrs(n, wrap, f)
        if not any(g in nb and s > r for (g, s) in B):
            return False
    for (f, r) in B:
        nb = nbrs(n, wrap, f)
        if not any(g in nb and s < r for (g, s) in W):
            return False
    return True


def images(n, wrap):
    if wrap:
        maps = []
        for s in (1, -1):
            for k in range(n):
                maps.append([(s * f + k) % n for f in range(n)])
        return maps
    return [list(range(n)), [n - 1 - f for f in range(n)]]


def canon(n, wrap, W, B, maps):
    best = None
    for m in maps:
        im = (tuple(sorted((m[f], r) for f, r in W)), tuple(sorted((m[f], r) for f, r in B)))
        if best is None or im < best:
            best = im
    return best


def atoms(n, wrap, p):
    """All canonical (W, B) with p pawns, every file occupied, no passer."""
    sqs = [(f, r) for f in range(n) for r in RANKS]
    maps = images(n, wrap)
    seen = set()
    for w in range(1, p):
        for W in itertools.combinations(sqs, w):
            Wset = set(W)
            rest = [s for s in sqs if s not in Wset]
            for B in itertools.combinations(rest, p - w):
                files = {f for f, _ in W} | {f for f, _ in B}
                if len(files) != n:
                    continue
                if not no_passer(n, wrap, W, B):
                    continue
                c = canon(n, wrap, W, B, maps)
                if c in seen:
                    continue
                seen.add(c)
    return sorted(seen)


TASKS = ([("flat", k, p) for k in range(1, 6) for p in range(max(k, 2), 6)] +
         [("ring", n, p) for n in (3, 4, 5) for p in range(n, 6)])


if __name__ == "__main__":
    if "--count" in sys.argv:
        tot = 0
        for kind, n, p in TASKS:
            c = len(atoms(n, kind == "ring", p))
            tot += c
            print(kind, n, p, c, flush=True)
        print("total", tot)
