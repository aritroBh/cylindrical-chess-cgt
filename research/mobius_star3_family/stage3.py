"""stage3.py: even widths. Insert one extra file X at every position of H2(m) = B5 W3 (W2 B4)^m W4 B7 B7 W3 W2 W2B7 B7
(positions counted on the base ring; at position 2 both before and after the block), X = any single pawn (n+1 pawns)
or any two-pawn file (n+2 pawns). Keep X/position if NNNP for m = 0, 1, 2; extend survivors to m <= MMAX (mob2)."""
import sys, itertools, json, time
from lib import *
HEAD, TAIL = ['B5', 'W3'], 'W4 B7 B7 W3 W2 W2B7 B7'.split()
BASE = HEAD + TAIL
SINGLES = [f'W{r}' for r in range(2, 7)] + [f'B{r}' for r in range(3, 8)]
DOUBLES = [f'W{a}{b}' for a, b in itertools.combinations(range(2, 8), 2)] + [f'B{a}{b}' for a, b in itertools.combinations(range(2, 8), 2)] \
        + [f'W{a}B{b}' for a in range(2, 8) for b in range(2, 8) if a != b]
MMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 6
XS = SINGLES if sys.argv[1] == 'single' else DOUBLES
POS = [(k, 'pre') for k in range(len(BASE) + 1)] + [(2, 'post')]
def ring(k, where, x, m):
    t = list(BASE); t.insert(k, x)          # x inserted before base index k
    blk = ['W2', 'B4'] * m
    i = 2 + (1 if (k < 2 or (k == 2 and where == 'post')) else 0)   # index where the block goes
    return ' '.join(t[:i] + blk + t[i:])
t0 = time.time()
cand = {(k, w, x, m): ring(k, w, x, m) for (k, w) in POS for x in XS for m in (0, 1, 2)}
sig = solve(list(cand.values()))
print(f'{sys.argv[1]}: {len(cand)} rings, hist {dict(collections.Counter(sig[r] for r in cand.values()))}', flush=True)
for m in (0, 1, 2):
    print(f'  NNNP at m={m}:', sorted((k, w, x) for (k, w, x, mm) in cand if mm == m and sig[cand[(k, w, x, m)]] == 'NNNP'), flush=True)
surv = sorted({(k, w, x) for (k, w, x, m) in cand if all(sig[cand[(k, w, x, mm)]] == 'NNNP' for mm in (0, 1, 2))})
print('  survivors m=0,1,2:', surv, flush=True)
for k, w, x in surv:
    rs = [ring(k, w, x, m) for m in range(0, MMAX + 1)]; s = solve(rs)
    print(f'  SURV pos={k}{w} X={x}: ' + ' '.join(s[r] for r in rs) + f'   e.g. m=1: {rs[1]}', flush=True)
print('time', round(time.time() - t0, 1))
