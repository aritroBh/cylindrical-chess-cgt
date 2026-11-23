#!/usr/bin/env python3
"""tag FAIL lines of a test run: K18 NOESC plain-only (P / Q variant), pawn counts, king or pawn sortie.
usage: tagfails.py TESTOUT K18TAG.json CTXID"""
import sys, json, collections
T, J, cid = sys.argv[1:4]
tag = json.load(open(J)); P = {tuple(x) for x in tag["P"]}; Q = {tuple(x) for x in tag["Q"]}
def canon(y): t = y.split(); return " ".join(sorted(t[:-2])) + " " + " ".join(t[-2:])
rows = []
for l in open(T):
    p = l.rstrip("\n").split(" | ")
    if p[0] != "FAIL" or p[1] != cid: continue
    Y, m, fl, pos, v = p[2], p[3], p[4], p[5], p[6]
    k = (canon(Y), m.replace("x", "").replace("ep", ""))
    np_ = len([t for t in Y.split()[:-2] if t[0] in "Pp"])
    rows.append((k in P, k in Q, np_, Y, m, fl, v, pos))
c = collections.Counter((r[0], r[1], r[6], r[4][0]) for r in rows); print(cid, dict(c))
for r in sorted(rows, key=lambda r: (not r[1], not r[0], r[2]))[:15]: print(r)
