#!/usr/bin/env python3
"""Compare KPK results of two boards on the same position list (T35).

usage: .venv/bin/python research/mobius/compare_kpk_boards.py A_RESULTS B_RESULTS
Keys are the position text before '|'. Reports how many positions differ in value (per side to move),
how many zugzwang boards (WTM=D, BTM=W) the two boards share, and a few example differences.
"""
import sys
from collections import Counter


def load(path):
    d = {}
    for line in open(path):
        if "|" not in line:
            continue
        pos, res = line.split("|", 1)
        d[pos.strip()] = res.split()
    return d


def boards(d):
    out = {}
    for pos, (a, b) in d.items():
        t = pos.split()
        out.setdefault(" ".join(t[:3]), {})[t[3]] = a
    return out


A, B = load(sys.argv[1]), load(sys.argv[2])
print("legal-set sizes A %d B %d; only in A %d; only in B %d; shared %d" % (
    len(A), len(B), len(set(A) - set(B)), len(set(B) - set(A)), len(set(A) & set(B))))
diff = Counter()
examples = []
for k in sorted(set(A) & set(B)):
    if A[k][0] != B[k][0]:
        diff[k.split()[3]] += 1
        if len(examples) < 6:
            examples.append((k, A[k][0], B[k][0]))
print("value differs (A vs B) by side to move:", dict(diff))
print("examples (position, A, B):", examples)
za = {k for k, v in boards(A).items() if v.get("w") == "D" and v.get("b") == "W"}
zb = {k for k, v in boards(B).items() if v.get("w") == "D" and v.get("b") == "W"}
print("zugzwang boards A: %d  B: %d  shared: %d" % (len(za), len(zb), len(za & zb)))
