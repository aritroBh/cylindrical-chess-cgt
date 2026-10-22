#!/usr/bin/env python3
"""cmp_cylcgt.py MODE [SAMPLE_MOD] < scanner_tsv   (scanner = frontier_split1_fixed2, flat, --only-setting 2)
Row-by-row comparison of the C whole-board scan (outcome, nimber) with cylcgt (default setting: count, e.p. on,
e.p.-aware passed test; Board(width,8,False,True)).
  MODE=gapped    : rows with an empty interior file.  cylcgt value = SUM of the cylcgt values of the parts (pawns.value
                   splits into components exactly like this); the parts are small connected roots, evaluated once and cached.
  MODE=connected : rows with every file occupied.  cylcgt value of the whole position, for rows with crc32(position) % SAMPLE_MOD == 0
                   (SAMPLE_MOD=1: all rows).
Prints counts and every mismatch (first 40)."""
import sys, zlib, time, collections, resource, subprocess, os
from common import *

WHOLE = os.environ.get("WHOLE") == "1"
if WHOLE: pawns.components = lambda b, p: [p]    # whole-board model
mode = sys.argv[1]; MOD = int(sys.argv[2]) if len(sys.argv) > 2 else 1
LO, HI = (int(sys.argv[2]), int(sys.argv[3])) if mode == "connected_range" else (0, 1 << 60)
if mode == "connected_range": mode = "connected"; MOD = 1; RANGE = True
else: RANGE = False
cidx = -1   # index among connected rows seen
parts_cache = {}
def clear_caches():
    pawns._value.cache_clear(); cgt._le_memo.clear(); cgt._add_memo.clear(); cgt._neg_memo.clear()
def rss_mb():
    return int(subprocess.run(["ps", "-o", "rss=", "-p", str(os.getpid())], capture_output=True, text=True).stdout.strip()) / 1024
def part_value(width, w, b):
    k = part_key(width, w, b)
    g = parts_cache.get(k)
    if g is None:
        g = parts_cache[k] = value_of_part(width, w, b)
    return g

n = checked = bad = skipped = 0; t0 = time.time()
cat = collections.Counter(); mism = []
for line in sys.stdin:
    if line.startswith("#"): continue
    pos, width, npaw, res = line.rstrip("\n").split("\t")
    n += 1
    W, B = parse_pos(pos)
    groups = occupied_groups(W, B)
    gapped = len(groups) > 1
    if gapped != (mode == "gapped"):
        continue
    if mode == "connected":
        cidx += 1
        if RANGE and not (LO <= cidx < HI): skipped += 1; continue
        if not RANGE and zlib.crc32(pos.encode()) % MOD != 0: skipped += 1; continue
    if gapped:
        g = cgt.total(part_value(*p) for p in split_parts(W, B))
    else:
        g = pawns.value(pawns.Board(int(width), 8, False, True), pawns.Pos(frozenset(W), frozenset(B)))
    o, nm = outcome_nim(g)
    so, sn = res.split(","); sn = int(sn)
    checked += 1; cat[(o, nm if nm >= 0 and nm < 3 else ("other" if nm < 0 else ">=3"))] += 1
    if (o, nm) != (so, sn):
        bad += 1
        if len(mism) < 40: mism.append((pos, f"scanner={so},{sn}", f"cylcgt={o},{nm}", cgt.show(g)[:80]))
    if mode == "connected" and checked % 500 == 0 and rss_mb() > 2500: clear_caches()
    if checked % 50000 == 0:
        print(f"  ..{checked} checked, {bad} mismatches, {time.time()-t0:.0f}s, {len(parts_cache)} parts cached", file=sys.stderr, flush=True)
        if mode == "gapped": clear_caches()
print(f"WHOLE_BOARD={WHOLE} mode={mode} sample_mod={MOD} range={(LO,HI) if RANGE else None} rows_read={n} checked={checked} (not selected: {skipped}) MISMATCHES={bad} elapsed={time.time()-t0:.0f}s")
print("cylcgt outcome/nimber classes among checked rows:", dict(sorted(cat.items(), key=str)))
for m in mism: print("MISMATCH", *m)
