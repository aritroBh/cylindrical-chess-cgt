#!/usr/bin/env python3
"""sums_le8.py -- complement of the <=8-pawn whole-board scan for positions the C scanner cannot hold (span > 8 files).

The C scanner (s3) holds boards of width <= 8.  A multi-component position with at most 8 pawns whose components
are placed with single-file gaps has span  sum(w_i) + k - 1  (w_i = files of component i).  It needs this script only if
that span is >= 9; with sum(p_i) <= 8 (p_i = pawns of component i, p_i >= 2, w_i <= p_i) that forces
   k=2: p = (4,4), (3,5), (2,6) with w_i = p_i;   k=3 and k=4: small components (p_i <= 4).
So enumerate (a) every single-component flat position with 2..4 pawns, (b) every one-pawn-per-file component with 5 or 6
pawns; value each with cylcgt (default setting); then add up every multiset of components with <= 8 pawns in total
(k >= 2) and test the sum for *3 (sum-model value; the C scanner's whole-board model agrees on span <= 8).
Output: number of distinct component values per pawn count, the number of sums tested, and any sum equal to *3.
"""
import itertools, os, sys, time, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
sys.setrecursionlimit(1000000)
from cylcgt import pawns, cgt

pawns.RACE_RULE = "count"
pawns.PASSED_RESPECTS_EP = True
STAR3 = cgt.nimber(3)


def components(p, one_per_file):
    """yield (width, Pos) for single-component flat positions with p pawns and no passed pawn"""
    for w in range(1, p + 1):
        if one_per_file and w != p:
            continue
        bd = pawns.Board(w, 8, False, True)
        wsq = [(f, r) for f in range(w) for r in range(2, 7)]
        bsq = [(f, r) for f in range(w) for r in range(3, 8)]
        for nw in range(1, p):
            nb = p - nw
            for ws in itertools.combinations(wsq, nw):
                wset = frozenset(ws)
                wfiles = {f for f, _ in ws}
                if one_per_file and len(wfiles) != nw:
                    continue
                for bs in itertools.combinations(bsq, nb):
                    bset = frozenset(bs)
                    if wset & bset:
                        continue
                    if len({f for f, _ in ws} | {f for f, _ in bs}) != w:
                        continue
                    if one_per_file and (len({f for f, _ in bs}) != nb or (wfiles & {f for f, _ in bs})):
                        continue
                    pos = pawns.Pos(wset, bset)
                    if pawns.passed(bd, pos, "W") or pawns.passed(bd, pos, "B"):
                        continue
                    yield w, bd, pos


def main():
    t0 = time.time()
    vals = {p: {} for p in range(2, 7)}     # p -> {Game: example position}
    ncomp = collections.Counter()
    for p, opf in [(2, False), (3, False), (4, False), (5, True), (6, True)]:
        for w, bd, pos in components(p, opf):
            g = pawns._value(bd, pos)
            ncomp[p] += 1
            vals[p].setdefault(g, f"{pos} [{w} files]")
        print(f"p={p}{' (one pawn per file)' if opf else ''}: {ncomp[p]} components, {len(vals[p])} distinct values  ({time.time()-t0:.0f}s)", flush=True)
    # multisets of component sizes with total <= 8, k >= 2
    found = []
    tested = 0
    sizes = [2, 3, 4, 5, 6]
    parts = []
    def rec(rem, minp, cur):
        if len(cur) >= 2:
            parts.append(tuple(cur))
        for p in sizes:
            if p >= minp and p <= rem:
                rec(rem - p, p, cur + [p])
    rec(8, 2, [])
    for part in sorted(set(parts)):
        # sums over value choices; unordered inside equal sizes is not needed (just brute force with itertools.product)
        lists = [list(vals[p].items()) for p in part]
        # incremental sum with dedupe on partial sums to keep it small
        partial = {None: ()}
        acc = [(cgt.integer(0), ())]
        for lst in lists:
            seen = {}
            for g0, ex0 in acc:
                for g, ex in lst:
                    s = cgt.add(g0, g)
                    seen.setdefault(s, ex0 + (ex,))
            acc = list(seen.items())
        tested += len(acc)
        for g, ex in acc:
            if g is STAR3:
                found.append((part, ex))
        print(f"sizes {part}: {len(acc)} distinct sums, *3 among them: {sum(1 for g,_ in acc if g is STAR3)}", flush=True)
    print(f"TOTAL distinct sums examined: {tested}; sums equal to *3: {len(found)}; {time.time()-t0:.0f}s")
    for part, ex in found[:20]:
        print("FOUND", part, ex)


if __name__ == "__main__":
    main()
