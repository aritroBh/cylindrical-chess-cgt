#!/usr/bin/env python3
"""cmp_gapped_nim.py < scanner_tsv   : for every GAPPED row (an empty interior file) compare
   scanner  (whole-board game, passed pawns end the game):  nimber class in {0,1,2,other}
   cylcgt SUM model (pawns.value default: sum of the cylcgt values of the parts, +BIG and -BIG may cancel across parts)
by the exact identity test  g1+...+gm = *n  <=>  g1+..+g(m-1) = *n - gm  (canonical forms, no big sums).
Prints the confusion matrix (scanner class, sum-model class) and, for every sum-model *2 row, the position.
A mismatch is 'explained' when two different parts can reach +BIG and -BIG respectively (pawns.sum_safe's criterion)."""
import sys, time, collections
from common import *
BIGH = pawns.BIG // 2
parts_cache, H_cache, sign_cache, pair_cache = {}, {}, {}, {}
STARS = [cgt.nimber(0), cgt.nimber(1), cgt.nimber(2)]
def part_value(width, w, b):
    k = part_key(width, w, b)
    g = parts_cache.get(k)
    if g is None: g = parts_cache[k] = value_of_part(width, w, b)
    return g
def H(g, n):
    k = (g.id, n); h = H_cache.get(k)
    if h is None: h = H_cache[k] = cgt.add(STARS[n], cgt.neg(g))
    return h
def signs(g):
    s = sign_cache.get(g.id)
    if s is None:
        seen, stack, s = set(), [g], set()
        while stack:
            x = stack.pop()
            if x.id in seen: continue
            seen.add(x.id)
            if x.num is not None and abs(x.num) >= BIGH: s.add(1 if x.num > 0 else -1)
            stack.extend(x.L + x.R)
        sign_cache[g.id] = s = frozenset(s)
    return s
def sum_class(gs):
    """n in {0,1,2} if sum(gs) == *n, else -1"""
    if len(gs) == 2: head, last = gs[0], gs[1]
    else:
        key = (gs[0].id, gs[1].id); head = pair_cache.get(key)
        if head is None: head = pair_cache[key] = cgt.add(gs[0], gs[1])
        last = gs[2]
    for n in (0, 1, 2):
        if head is H(last, n): return n
    return -1
minspan_rows = collections.Counter(); conf = collections.Counter(); unexplained = []; star2_rows = []; nrows = 0; t0 = time.time(); expl = collections.Counter()
for line in sys.stdin:
    if line.startswith("#"): continue
    pos, width, npaw, res = line.rstrip("\n").split("\t")
    W, B = parse_pos(pos)
    if len(occupied_groups(W, B)) < 2: continue
    nrows += 1
    parts = split_parts(W, B)
    assert len(parts) <= 3
    gs = [part_value(*p) for p in parts]
    minspan_rows[sum(p[0] for p in parts) + len(parts) - 1] += 1
    sc = int(res.split(",")[1]); sc = sc if sc in (0, 1, 2) else -1
    sm = sum_class(gs)
    conf[(sc, sm)] += 1
    if sm == 2: star2_rows.append((pos, res))
    if sc != sm:
        sg = [signs(g) for g in gs]
        unsafe = any((1 in a and -1 in b) for i, a in enumerate(sg) for j, b in enumerate(sg) if i != j)
        expl[unsafe] += 1
        if not unsafe and len(unexplained) < 20: unexplained.append((pos, res, sm))
    if nrows % 100000 == 0: print(f"  ..{nrows} rows {time.time()-t0:.0f}s parts={len(parts_cache)}", file=sys.stderr, flush=True); cgt._le_memo.clear()
print(f"gapped rows={nrows} elapsed={time.time()-t0:.0f}s")
print("confusion (scanner class, sum-model class)  [class = nimber 0/1/2, -1 = anything else]:")
for k, v in sorted(conf.items()): print(f"   scanner={k[0]:2d} sum_model={k[1]:2d}  rows={v}")
print("rows by minimal span (gaps collapsed to one empty file):", dict(sorted(minspan_rows.items())))
print(f"mismatching rows: {sum(expl.values())}; explained by +BIG/-BIG in different parts: {expl[True]}; NOT explained: {expl[False]}")
print(f"sum-model *2 rows: {len(star2_rows)}; scanner says (first 3): {star2_rows[:3]}")
for u in unexplained: print("UNEXPLAINED", *u)
import os
if os.environ.get("DUMP_SUM_STAR2"):
    with open(os.environ["DUMP_SUM_STAR2"], "a") as fh:
        for pos, res in star2_rows: fh.write(f"{pos}\tscanner(whole-board)={res}\tsum-model=*2\n")
