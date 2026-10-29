"""K32 table: pivot of lam against ceil(-RS) and rho against ceil(LS) from the signature lines of a stopsA report.
Usage: table.py report1.txt [report2.txt ...]   (counts are node instances; reports are added)."""
import sys, re, math
from fractions import Fraction
INFD = {"+inf": math.inf, "-inf": -math.inf}
def val(s): return INFD[s] if s in INFD else Fraction(int(s.split("/")[0]), 16)
rows = []
for fn in sys.argv[1:]:
    for l in open(fn):
        m = re.match(r"lam=(\S+) rho=(\S+) LS=(\S+) RS=(\S+) count=(\d+)", l)
        if m:
            lam = math.inf if m[1] == "inf" else int(m[1]); rho = math.inf if m[2] == "inf" else int(m[2])
            rows.append((lam, rho, val(m[3]), val(m[4]), int(m[5])))
def cls(u):   # u = -RS (for lam) or LS (for rho)
    if u == math.inf: return "stop = the bad infinity (reserve must be infinite)"
    if u == -math.inf: return "stop = the good infinity (reserve must be 0)"
    if u > 0 and u.denominator == 1: return "u = %d (positive integer)" % u if u <= 3 else "u >= 4 (integer)"
    if u > 0: return "u positive non-integer"
    if u == 0: return "u = 0"
    return "u < 0 (reserve must be 0)"
order = ["stop = the bad infinity (reserve must be infinite)", "u = 1 (positive integer)", "u = 2 (positive integer)", "u = 3 (positive integer)", "u >= 4 (integer)", "u positive non-integer", "u = 0", "u < 0 (reserve must be 0)", "stop = the good infinity (reserve must be 0)"]
for w, name in ((0, "lambda against RS  (u = -RS)"), (1, "rho against LS  (u = LS)")):
    T = {}
    for lam, rho, LS, RS, c in rows:
        res = rho if w else lam; u = LS if w else -RS
        k = cls(u)
        if u in (math.inf, -math.inf): d = "res=inf" if res == math.inf else "res=%d" % res
        else:
            if res == math.inf: d = "res=inf"
            else:
                base = max(0, math.ceil(u)); d = "res-base=%d" % (res - base)
        T.setdefault(k, {}); T[k][d] = T[k].get(d, 0) + c
    print("\n== %s: counts of node instances; base = max(0, ceil(u)) ==" % name)
    for k in order:
        if k in T: print("%-52s %s" % (k, "  ".join("%s:%d" % (a, b) for a, b in sorted(T[k].items()))))
