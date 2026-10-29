"""Table of the named games: root results of stopsA (eval p) and stopsB on the graphs of named.py.
Usage: named_table.py named_tsv A_results B_results"""
import sys, math, re
from fractions import Fraction
names = [l.split("\t")[0] for l in open(sys.argv[1])]
A = [l for l in open(sys.argv[2]) if l.startswith("G")]; B = [l for l in open(sys.argv[3]) if l.startswith("G")]
assert A == B, "A and B differ"
def val(s): return math.inf if s == "+inf" else -math.inf if s == "-inf" else Fraction(int(s.split("/")[0]), 16)
def fs(x): return "+inf" if x == math.inf else "-inf" if x == -math.inf else (str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator))
print("%-24s %6s %6s %5s %5s  %-9s %-9s  %s" % ("game", "LS", "RS", "lam", "rho", "ceil(-RS)", "ceil(LS)", "corrected relation"))
for n, l in zip(names, A):
    f = l.split("[")[1].split("]")[0].split(); lam, rho = int(f[0]), int(f[1]); LS, RS = val(f[2]), val(f[3])
    ok = True
    def chk(res, u):
        if u in (math.inf, -math.inf): return None
        return max(0, math.ceil(u)) <= res <= max(0, math.floor(u) + 1)
    c1 = (lam == 99) == (RS == -math.inf); c2 = (rho == 99) == (LS == math.inf)
    if RS != -math.inf and RS != math.inf: c1 = c1 and chk(lam, -RS)
    if RS == math.inf: c1 = c1 and lam == 0
    if LS != math.inf and LS != -math.inf: c2 = c2 and chk(rho, LS)
    if LS == -math.inf: c2 = c2 and rho == 0
    ce1 = "-" if RS in (math.inf, -math.inf) else str(math.ceil(-RS)); ce2 = "-" if LS in (math.inf, -math.inf) else str(math.ceil(LS))
    print("%-24s %6s %6s %5s %5s  %-9s %-9s  %s" % (n, fs(LS), fs(RS), "inf" if lam == 99 else lam, "inf" if rho == 99 else rho, ce1, ce2, "holds" if (c1 and c2) else "FAILS"))
