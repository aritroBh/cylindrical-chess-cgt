#!/usr/bin/env python3
"""parts.py: enumerate every connected no-passer root with k = 2..K pawns (a 'part': all files occupied, W on ranks 2..6,
B on ranks 3..7, >= 1 pawn per side, no passed pawn), left-right-mirror-reduced, evaluate it with cylcgt (default setting)
and write parts_k{k}.tsv  (key, width, nW, nB, outcome, nimber-or-minus1, value-string).
Also prints the enumeration counts, which must equal count_connected (C) summed over widths."""
import sys, itertools, time, json
from common import *

K = int(sys.argv[1]) if len(sys.argv) > 1 else 5
t0 = time.time()
def enum_parts(k):
    res = {}
    for width in range(1, k + 1):
        wsq = [(f, r) for f in range(width) for r in range(2, 7)]
        bsq = [(f, r) for f in range(width) for r in range(3, 8)]
        board = pawns.Board(width, 8, False, True)
        for nw in range(1, k):
            nb = k - nw
            for wc in itertools.combinations(wsq, nw):
                wset = set(wc); wfiles = {f for f, _ in wc}
                for bc in itertools.combinations(bsq, nb):
                    if wset.intersection(bc): continue
                    if len(wfiles | {f for f, _ in bc}) != width: continue
                    pos = pawns.Pos(frozenset(wc), frozenset(bc))
                    if pawns.passed(board, pos, "W") or pawns.passed(board, pos, "B"): continue
                    key = part_key(width, wc, bc)
                    res.setdefault(key, (width, wc, bc))
    return res
summary = {}
for k in range(2, K + 1):
    parts = enum_parts(k)
    rows = []
    for key, (width, wc, bc) in sorted(parts.items()):
        g = value_of_part(width, wc, bc)
        o, n = outcome_nim(g)
        rows.append((pos_text(wc, bc), width, len(wc), len(bc), o, n, cgt.show(g)))
    with open(f"parts_k{k}.tsv", "w") as fh:
        fh.write("#position\twidth\tnW\tnB\toutcome\tnimber\tvalue\n")
        for r in rows: fh.write("\t".join(map(str, r)) + "\n")
    distinct = len({r[6] for r in rows})
    summary[k] = (len(rows), distinct)
    print(f"k={k}: connected mirror-reduced roots={len(rows)} distinct display strings={distinct} "
          f"star2={sum(1 for r in rows if r[5]==2)} elapsed={time.time()-t0:.0f}s", flush=True)
