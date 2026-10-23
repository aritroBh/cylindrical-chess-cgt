#!/usr/bin/env python3
"""cylcgt check of the C8 ten-pawn ring hits of the fixed2 scanner (default setting: count rule, e.p. on, e.p.-aware
passed test). Prints the value as a sum of components and as a whole-board game.
Run from the project root: nice -n 15 python3 research/star26_rings/c8/cylcgt_p10.py HITS.tsv"""
import sys, time
sys.path.insert(0, ".")
sys.setrecursionlimit(1000000)
from cylcgt import pawns
pawns.RACE_RULE = "count"
pawns.PASSED_RESPECTS_EP = True
bd = pawns.Board(8, 8, True, True)
seen = []
for line in open(sys.argv[1]):
    if line.startswith("#") or not line.strip():
        continue
    t, _, _, res = line.rstrip("\n").split("\t")
    if t in seen:
        continue
    seen.append(t)
    p = pawns.Pos.parse(t)
    assert pawns.is_ring(bd, p)
    t0 = time.time(); s = pawns.value(bd, p); ts = time.time() - t0
    orig = pawns.components
    pawns.components = lambda b, q: [q]
    pawns._value.cache_clear()
    t0 = time.time(); w = pawns._value(bd, p); tw = time.time() - t0
    pawns.components = orig
    pawns._value.cache_clear()
    print(f"{t}\tscanner={res}\tsum={s}\twhole={w}\t{ts:.0f}s/{tw:.0f}s", flush=True)
