"""K32 tally P: recompute the tables of stopsA's report from per-graph result lines ('G [lam rho LS RS] ...'; stops in sixteenths),
independently of the C tally.  Usage: tally.py < lines   (prints the same text lines as stopsA, minus A-only diagnostics)."""
import sys, math
from fractions import Fraction
CINF = 99
ROOT = len(sys.argv) > 1 and sys.argv[1] == "--root"
def val(s):
    if s == "+inf": return math.inf
    if s == "-inf": return -math.inf
    a, b = s.split("/"); return Fraction(int(a), int(b))
ng = nn = 0
lit = [0, 0]; fix = [0, 0]; infv = [0, 0]
dh = [[0] * 6 for _ in range(2)]
sigs = {}
for line in sys.stdin:
    if not line.startswith("G"): continue
    ng += 1
    for tok in (line.split("[")[1:2] if ROOT else line.split("[")[1:]):
        f = tok.split("]")[0].split()
        lam, rho = int(f[0]), int(f[1]); LS, RS = val(f[2]), val(f[3])
        nn += 1
        key = (lam, rho, LS, RS); sigs[key] = sigs.get(key, 0) + 1
        for w in (0, 1):
            res = rho if w else lam; st = LS if w else RS
            x = st if w else -st               # w=0: -RS ;  w=1: LS
            stinf = st in (math.inf, -math.inf)
            extreme = (st == math.inf) if w else (st == -math.inf)
            if extreme != (res == CINF): infv[w] += 1
            if not stinf and res != CINF:
                lo = math.ceil(x); hi = math.floor(x) + 1
                if res not in (lo, lo + 1): lit[w] += 1
                if res < max(lo, 0) or res > max(hi, 0): fix[w] += 1
                isint = (x.denominator == 1)
                if x > 0 and isint: dh[w][0 if res == lo else (1 if res == lo + 1 else 5)] += 1
                elif x == 0: dh[w][0 if res == 0 else (1 if res == 1 else 5)] += 1
                elif x < 0: dh[w][4 if res == 0 else 5] += 1
                else: dh[w][2 if res == lo else 5] += 1
            elif not stinf and res == CINF:
                fix[w] += 1; lit[w] += 1
            if stinf and res != CINF and not extreme and res != 0: fix[w] += 1
print("graphs %d nodes %d" % (ng, nn))
for w in (0, 1): print("%s: literal-violations %d  corrected-violations %d  infinity-violations %d" % ("rho/LS" if w else "lam/RS", lit[w], fix[w], infv[w]))
for w in (0, 1): print("%s boundary(-RS or LS integer>=0, base) %d  boundary(+1) %d  nonint(base) %d  stop-on-wrong-side(0) %d  other %d" % ("rho/LS" if w else "lam/RS", dh[w][0], dh[w][1], dh[w][2], dh[w][4], dh[w][5]))
def sk(k):
    lam, rho, LS, RS = k
    return (lam, rho, LS, RS)
def f(s): return "+inf" if s == math.inf else "-inf" if s == -math.inf else "%d/16" % int(s * 16)
print("signatures %d" % len(sigs))
for k in sorted(sigs, key=sk):
    lam, rho, LS, RS = k
    print("lam=%s rho=%s LS=%s RS=%s count=%d" % ("inf" if lam == CINF else lam, "inf" if rho == CINF else rho, f(LS), f(RS), sigs[k]))
