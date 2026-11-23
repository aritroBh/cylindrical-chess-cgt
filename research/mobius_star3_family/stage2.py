"""Stage 2: transplants.
(a) cylinder *3 cores T_n, S_n (PROOF_S3T3) and the bare tails, every rotation (seam in every gap), widths up to NMAX;
(b) Mobius *2 families F1, F2 (m=1..3), F3 (m=0..3) and the n=10,11 one-pawn-per-file *2 rings, plus one extra pawn
    on every free square (ranks 2..7, either colour) of every file. Signature NNNP = *3."""
import sys, json, time
from lib import *
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 18
TAIL_T = 'B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2'.split()
TAIL_S = 'W6B7 W3 B7 B6 W3 W2 B6 W2'.split()
def T(n): return ['B4', 'W2'] * ((n - 10) // 2) + TAIL_T
def S(n): return ['B4', 'B6', 'W3'] + ['W2', 'B4'] * ((n - 11) // 2) + TAIL_S
def rots(t): return [t[i:] + t[:i] for i in range(len(t))]
t0 = time.time()
print('(a) cylinder cores, all rotations', flush=True)
fams = {'T': [(n, T(n)) for n in range(10, NMAX + 1, 2)], 'S': [(n, S(n)) for n in range(11, NMAX + 1, 2)],
        'tailT': [(10, TAIL_T)], 'tailS': [(8, TAIL_S)]}
hits_a = []
for name, lst in fams.items():
    for n, t in lst:
        rs = [' '.join(x) for x in rots(t)]
        s = solve(rs)
        sig = [s[r] for r in rs]
        print(f'  {name} n={n} pawns={npawns(rs[0])}: ' + ' '.join(f'{i}:{x}' for i, x in enumerate(sig)), flush=True)
        hits_a += [(name, n, i, r) for i, r in enumerate(rs) if s[r] == 'NNNP']
print('  NNNP hits (a):', hits_a, flush=True)
print('(b) *2 cores + one pawn', flush=True)
F1 = lambda m: ['B4', 'W2'] * m + 'B6 W2 W3 B6 B7 W3 B7 W5'.split()
F2 = lambda m: ['B4', 'W2'] * m + 'B6 W2 W3 B6 B7 W3 B7 W5 B7'.split()
F3 = lambda m: 'B6 W2 W3 B6 B7 W3'.split() + ['B7', 'W5'] * m + ['W6B7']
cores = [('F1', m, F1(m)) for m in (1, 2, 3)] + [('F2', m, F2(m)) for m in (1, 2, 3)] + [('F3', m, F3(m)) for m in (0, 1, 2, 3)] \
      + [('n10b', 0, 'B6 W3 B7 W2 W3 B6 B7 W2 B6 W3'.split())]
def addpawn(tok, c, r):
    # tok like 'W2B7'; add colour c rank r, keep canonical order W first then B, ranks ascending
    w = [int(x) for x in tok.split('B')[0][1:]] if tok.startswith('W') else []
    b = [int(x) for x in tok.split('B')[1]] if 'B' in tok else []
    if c == 'W':
        if r in w: return None
        w = sorted(w + [r])
    else:
        if r in b: return None
        b = sorted(b + [r])
    return ('W' + ''.join(map(str, w)) if w else '') + ('B' + ''.join(map(str, b)) if b else '')
res_b = {}
for name, m, t in cores:
    cand = {}
    for f in range(len(t)):
        for c in 'WB':
            for r in range(2, 8):
                nt = addpawn(t[f], c, r)
                if nt: cand[(f, c + str(r))] = ' '.join(t[:f] + [nt] + t[f + 1:])
    s = solve(list(cand.values()))
    hist = collections.Counter(s[r] for r in cand.values())
    hits = [(f, p, cand[(f, p)]) for (f, p) in cand if s[cand[(f, p)]] == 'NNNP']
    res_b[f'{name}({m})'] = hits
    print(f'  {name}({m}) n={len(t)}: {len(cand)} cands {dict(hist)}; NNNP: {[(f, p) for f, p, _ in hits]}', flush=True)
json.dump({'a': hits_a, 'b': res_b}, open('logs/stage2.json', 'w'))
print('time', round(time.time() - t0, 1))
