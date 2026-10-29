"""Compare the multiset of (lam, rho, LS, RS) over the 2,169,427 four-node classes: my root-only report (stopsA K32_ROOT=1)
against data/B_4.txt left in the output directory by an earlier attempt of this task (lines: key LS RS lam rho).
Usage: cmp_earlier.py my_root_report.txt data/B_4.txt"""
import sys, re, math
from fractions import Fraction
from collections import Counter
def v(s):
    if s in ("inf", "+inf"): return "+inf"
    if s == "-inf": return "-inf"
    return str(Fraction(s)) if "/" in s or s.lstrip("-").isdigit() else s
def norm_stop(s):
    if s in ("inf", "+inf"): return "+inf"
    if s == "-inf": return "-inf"
    return Fraction(s)
mine = Counter()
for l in open(sys.argv[1]):
    m = re.match(r"lam=(\S+) rho=(\S+) LS=(\S+) RS=(\S+) count=(\d+)", l)
    if m:
        ls = norm_stop(m[3].replace("/16", "") + "/16") if m[3] not in ("+inf", "-inf") else m[3]
        rs = norm_stop(m[4].replace("/16", "") + "/16") if m[4] not in ("+inf", "-inf") else m[4]
        mine[(m[1], m[2], ls, rs)] += int(m[5])
theirs = Counter()
import gzip
for l in (gzip.open(sys.argv[2], "rt") if sys.argv[2].endswith(".gz") else open(sys.argv[2])):
    k, ls, rs, lam, rho = l.split()
    theirs[(lam, rho, norm_stop(ls), norm_stop(rs))] += 1
print("signatures: mine %d, earlier %d; classes: mine %d, earlier %d; identical multisets: %s" % (len(mine), len(theirs), sum(mine.values()), sum(theirs.values()), mine == theirs))
if mine != theirs:
    for k in sorted(set(mine) | set(theirs), key=str):
        if mine[k] != theirs[k]: print("DIFF", k, mine[k], theirs[k])
