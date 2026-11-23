"""Stage 1: pump blocks into the known *3 rings. Blocks: 4 wall pairs + all single files + all 2-file single-pawn blocks.
m = 1, 2 at every cut; survivors (NNNP at m=1 and 2) extended to m <= MMAX with mob2."""
import sys, itertools, json, time
from lib import *
BASES = ['B67 W4 W2B6 W2B5 W5B7', 'B7 W4 W23 B5 W3B7 W4B7', 'B5 W3 W4 B7 B7 W3 W2 W2B7 B7']
SINGLES = [f'W{r}' for r in range(2, 7)] + [f'B{r}' for r in range(3, 8)]
WALL = [['B4', 'W2'], ['W2', 'B4'], ['B7', 'W5'], ['W5', 'B7']]
BLOCKS = [[s] for s in SINGLES] + [list(b) for b in itertools.product(SINGLES, repeat=2)]
MMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
def ins(t, k, b, m): return t[:k] + b * m + t[k:]
t0 = time.time(); out = []
for base in BASES:
    t = base.split()
    cand = {(k, ' '.join(b), m): ' '.join(ins(t, k, b, m)) for m in (1, 2) for k in range(len(t) + 1) for b in BLOCKS}
    sig = solve(list(cand.values()))
    hist = collections.Counter(sig[r] for r in cand.values())
    print(f'BASE {base} n={len(t)}: {len(cand)} candidates (m=1,2), sig histogram {dict(hist)}', flush=True)
    wl = {' '.join(b) for b in WALL}
    for (k, b, m), r in cand.items():
        if b in wl: print(f'  wall k={k} block={b} m={m} {sig[r]}  {r}')
    surv = sorted({(k, b) for (k, b, m) in cand if all(sig[cand[(k, b, mm)]] == 'NNNP' for mm in (1, 2))})
    print(f'  survivors m=1,2: {len(surv)}', flush=True)
    m1 = sorted({(k, b) for (k, b, m) in cand if m == 1 and sig[cand[(k, b, 1)]] == 'NNNP'})
    print(f'  NNNP at m=1: {len(m1)}: {m1}', flush=True)
    for k, b in surv:
        rs = [' '.join(ins(t, k, b.split(), m)) for m in range(1, MMAX + 1)]
        s = solve(rs)
        print(f'  SURV k={k} block={b}: ' + ' '.join(s[r] for r in rs), flush=True)
        out.append([base, k, b, [s[r] for r in rs]])
json.dump(out, open('logs/stage1.json', 'w'))
print('time', round(time.time() - t0, 1))
