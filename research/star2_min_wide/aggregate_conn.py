#!/usr/bin/env python3
"""Aggregate conn/*.out (cmp_cylcgt.py connected outputs): rows checked and mismatches per file and in total."""
import glob, re
tot = chk = bad = 0
print("file                                        checked   mismatches")
for f in sorted(glob.glob("conn/*.out")):
    t = open(f).readline()
    m = re.search(r"checked=(\d+) .*MISMATCHES=(\d+)", t)
    if not m: print(f"{f}: INCOMPLETE"); continue
    c, b = int(m.group(1)), int(m.group(2)); chk += c; bad += b
    print(f"{f:44s} {c:8d} {b:6d}")
print(f"TOTAL checked={chk} mismatches={bad}")
