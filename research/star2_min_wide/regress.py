#!/usr/bin/env python3
"""regress.py STORED.tsv.zst < scanner_output : row-by-row compare of the stored 9-setting scan column 'count/epon/aware'
(field 5) with the fixed2 single-setting output (field 3).  Prints rows compared / mismatches."""
import sys, subprocess
stored = {}
for l in subprocess.run(["zstdcat", sys.argv[1]], capture_output=True, text=True, check=True).stdout.splitlines():
    if l.startswith("#"): continue
    p = l.split("\t"); stored[p[0]] = p[5]
n = bad = missing = 0
for l in sys.stdin:
    if l.startswith("#"): continue
    p = l.rstrip("\n").split("\t"); n += 1
    s = stored.pop(p[0], None)
    if s is None: missing += 1
    elif s != p[3]: bad += 1; print("MISMATCH", p[0], s, p[3])
print(f"{sys.argv[1]}: compared={n} mismatches={bad} not_in_stored={missing} stored_not_seen={len(stored)}")
