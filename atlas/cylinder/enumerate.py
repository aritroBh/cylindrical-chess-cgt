"""Canonical enumeration of pawn-only positions for the cylinder/flat atlas.

A position is a set of white pawns W and black pawns B on an n-file x 8-rank
board, with every pawn on ranks 2..7 (a pawn on rank 1 or 8 is illegal in
chess).  Positions with an initial passed pawn (for either side) are skipped,
exactly as cylcgt.explore does.  En passant rights are absent at the root.

Symmetry (orbit representatives only are produced):
  * cylinder (wrap=True): the dihedral group of order 2n acting on files,
    f -> (s*f + k) mod n, s in {+1,-1}.
  * flat strip (wrap=False): identity and the mirror f -> n-1-f.
Colour reversal (swap colours, flip ranks) maps (w,b) to (b,w) and negates the
value; it is NOT used to cut the enumeration (both (w,b) and (b,w) are
computed), so it can serve as a consistency check.

Usage (counting only):
  PYTHONPATH=. .venv/bin/python atlas/cylinder/enumerate.py --count
"""
from __future__ import annotations

import argparse
import itertools
import sys
import time

RANKS = 8
PAWN_RANKS = range(2, RANKS)  # 2..7


def group(n: int, wrap: bool):
    """List of file maps (as tuples f -> g[f])."""
    if wrap:
        out = []
        for s in (1, -1):
            for k in range(n):
                out.append(tuple((s * f + k) % n for f in range(n)))
        # remove duplicates (n small, e.g. n<=2 never used here)
        return list(dict.fromkeys(out))
    return [tuple(range(n)), tuple(n - 1 - f for f in range(n))]


def neighbours(n: int, wrap: bool, f: int):
    out = {f}
    for d in (-1, 1):
        g = f + d
        if wrap:
            out.add(g % n)
        elif 0 <= g < n:
            out.add(g)
    return out


def canon_positions(n: int, wrap: bool, w: int, b: int, shard: int = 0, nshards: int = 1):
    """Yield (W, B) orbit representatives (sorted tuples of (file, rank)) with
    no passed pawn for either side.  With nshards > 1, only canonical white
    sets whose index is congruent to `shard` mod `nshards` are used."""
    sqs = [(f, r) for f in range(n) for r in PAWN_RANKS]
    G = group(n, wrap)
    nbr = [neighbours(n, wrap, f) for f in range(n)]

    def img(g, S):
        return tuple(sorted((g[f], r) for f, r in S))

    widx = -1
    for W in itertools.combinations(sqs, w):
        imgs = [img(g, W) for g in G]
        if min(imgs) != W:
            continue
        widx += 1
        if widx % nshards != shard:
            continue
        stab = [g for g, im in zip(G, imgs) if im == W and g != G[0]]
        Wset = set(W)
        # black pawn (f,r) is not passed iff some white pawn (g,s), g in nbr(f), s < r
        zone = [(f, r) for (f, r) in sqs if (f, r) not in Wset and
                any(g in nbr[f] and s < r for (g, s) in W)]
        for B in itertools.combinations(zone, b):
            # every white pawn must be blocked: black pawn on nbr files, higher rank
            ok = True
            for (f, r) in W:
                if not any(g in nbr[f] and s > r for (g, s) in B):
                    ok = False
                    break
            if not ok:
                continue
            if stab and any(img(g, B) < B for g in stab):
                continue
            yield W, B


def count(n, wrap, w, b):
    c = 0
    for _ in canon_positions(n, wrap, w, b):
        c += 1
    return c


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", action="store_true")
    ap.add_argument("--maxpawns", type=int, default=4)
    ap.add_argument("--widths", default="3,4,5,6,7,8")
    a = ap.parse_args()
    if a.count:
        for n in map(int, a.widths.split(",")):
            for wrap in (True, False):
                for tot in range(2, a.maxpawns + 1):
                    for w in range(1, tot):
                        t = time.time()
                        c = count(n, wrap, w, tot - w)
                        print(f"n={n} {'cyl ' if wrap else 'flat'} w={w} b={tot-w} canonical_no_passer={c} "
                              f"({time.time()-t:.1f}s)", flush=True)
