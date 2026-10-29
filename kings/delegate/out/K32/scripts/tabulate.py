"""K32: tabulate lambda against ceil(-RS) and rho against ceil(LS) from result files (lines: graph LS RS lam rho).
usage: tabulate.py file [file...]   (graph counts; one line per isomorphism class of rooted graphs)"""
import sys, math
from fractions import Fraction
from collections import Counter

def val(s):
    if s == "inf": return math.inf
    if s == "-inf": return -math.inf
    return Fraction(s)

def ceil(v):
    return v if v in (math.inf, -math.inf) else math.ceil(v)

def rows(files):
    for f in files:
        for line in open(f):
            g, ls, rs, lam, rho = line.split()
            yield g, val(ls), val(rs), val(lam), val(rho)

def main():
    files = sys.argv[1:]
    tot = 0
    # classification of lambda
    cl = Counter(); cr = Counter()
    lit_l = Counter(); lit_r = Counter()
    fin_l = Counter(); fin_r = Counter()
    both = Counter()
    first_bad = {}
    maxabs = 0
    for g, ls, rs, lam, rho in rows(files):
        tot += 1
        assert ls >= rs, (g, ls, rs)   # LS >= RS for every stopper (check)
        # lambda: predicted max(0, ceil(-RS)) or one more
        if rs == math.inf: pl = 0
        elif rs == -math.inf: pl = math.inf
        else: pl = max(0, ceil(-rs))
        if lam == math.inf and pl == math.inf: k = "lam=inf, RS=-inf"
        elif lam == math.inf: k = "lam=inf with RS>-inf (VIOLATION)"
        elif pl == math.inf: k = "lam finite with RS=-inf (VIOLATION)"
        else:
            d = lam - pl
            k = {0: "lam = max(0,ceil(-RS))", 1: "lam = max(0,ceil(-RS)) + 1"}.get(d, "OTHER %s (VIOLATION)" % d)
        cl[k] += 1
        if "VIOLATION" in k: first_bad.setdefault(("L", k), g)
        # literal: lam - ceil(-RS) in {0,1}
        if rs in (math.inf, -math.inf): kl = "RS=%s" % ("+inf" if rs == math.inf else "-inf")
        else:
            d = lam - ceil(-rs) if lam != math.inf else "lam inf"
            kl = "lam-ceil(-RS) = %s" % d
            if d not in (0, 1): first_bad.setdefault(("literal-L", d if isinstance(d, str) else (0 if d < 0 else 2)), g)
        lit_l[kl] += 1
        # the +1 cases: -RS integer?
        if rs not in (math.inf, -math.inf) and lam != math.inf:
            isint = (Fraction(rs).denominator == 1)
            fin_l[(("RS integer" if isint else "RS not integer"), "RS>=1" if rs >= 1 else "RS<1", lam - pl)] += 1
        # rho: predicted max(0, ceil(LS)) or one more
        if ls == -math.inf: pr = 0
        elif ls == math.inf: pr = math.inf
        else: pr = max(0, ceil(ls))
        if rho == math.inf and pr == math.inf: k = "rho=inf, LS=+inf"
        elif rho == math.inf: k = "rho=inf with LS<+inf (VIOLATION)"
        elif pr == math.inf: k = "rho finite with LS=+inf (VIOLATION)"
        else:
            d = rho - pr
            k = {0: "rho = max(0,ceil(LS))", 1: "rho = max(0,ceil(LS)) + 1"}.get(d, "OTHER %s (VIOLATION)" % d)
        cr[k] += 1
        if "VIOLATION" in k: first_bad.setdefault(("R", k), g)
        if ls in (math.inf, -math.inf): kr = "LS=%s" % ("+inf" if ls == math.inf else "-inf")
        else:
            d = rho - ceil(ls) if rho != math.inf else "rho inf"
            kr = "rho-ceil(LS) = %s" % d
        lit_r[kr] += 1
        if ls not in (math.inf, -math.inf) and rho != math.inf:
            isint = (Fraction(ls).denominator == 1)
            fin_r[(("LS integer" if isint else "LS not integer"), "LS<=-1" if ls <= -1 else "LS>-1", rho - pr)] += 1
        if rs not in (math.inf, -math.inf):
            maxabs = max(maxabs, abs(rs))
        if ls not in (math.inf, -math.inf):
            maxabs = max(maxabs, abs(ls))
    print("graphs:", tot, " (LS >= RS held for all)")
    print("\nlambda against max(0, ceil(-RS)):")
    for k, v in sorted(cl.items()): print("  %-45s %9d" % (k, v))
    print("lambda, literal ceil(-RS) (no clipping):")
    for k, v in sorted(lit_l.items(), key=lambda t: str(t[0])): print("  %-45s %9d" % (k, v))
    print("finite lambda, RS finite: (integrality of RS, RS>=1?, lam - clipped prediction) :")
    for k, v in sorted(fin_l.items(), key=lambda t: str(t[0])): print("  %-45s %9d" % (str(k), v))
    print("\nrho against max(0, ceil(LS)):")
    for k, v in sorted(cr.items()): print("  %-45s %9d" % (k, v))
    print("rho, literal ceil(LS) (no clipping):")
    for k, v in sorted(lit_r.items(), key=lambda t: str(t[0])): print("  %-45s %9d" % (k, v))
    print("finite rho, LS finite: (integrality of LS, LS<=-1?, rho - clipped prediction) :")
    for k, v in sorted(fin_r.items(), key=lambda t: str(t[0])): print("  %-45s %9d" % (str(k), v))
    print("\nlargest finite |stop|:", maxabs)
    print("first examples of violations / literal failures:", first_bad)

main()
