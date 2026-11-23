"""stage4.py N: targeted search for a *3 ring on M_N with N+1 (and N+2) pawns, N small.
Seeds: rings of width N obtained from the *3 rings found here (H2(m), E2(m), the n=9 ring) by deleting files
(single-pawn files only, so the pawn excess stays 1) or inserting one single-pawn file; then the radius-1 and
radius-2 neighbourhoods of the seeds under 'move one pawn' (to any free square ranks 2..7, either colour, any file)
and radius 1 under 'add one pawn'. Not exhaustive. Seeds: deletions of at most 2 files; radius 1 around SEEDCAP random seeds; radius 2 a capped sample."""
import sys, itertools, time, random
from lib import *
N = int(sys.argv[1]); R2CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
SEEDCAP = int(sys.argv[3]) if len(sys.argv) > 3 else 40
H2 = lambda m: ('B5 W3' + ' W2 B4' * m + ' W4 B7 B7 W3 W2 W2B7 B7').split()
E2 = lambda m: ('B5 W3' + ' W2 B4' * m + ' W2 W4 B7 B7 W3 W2 W2B7 B7').split()
SINGLES = [f'W{r}' for r in range(2, 7)] + [f'B{r}' for r in range(3, 8)]
def parse(tok):
    w = [int(x) for x in tok.split('B')[0][1:]] if tok.startswith('W') else []
    b = [int(x) for x in tok.split('B')[1]] if 'B' in tok else []
    return set(w), set(b)
def unparse(w, b):
    return ('W' + ''.join(map(str, sorted(w))) if w else '') + ('B' + ''.join(map(str, sorted(b))) if b else '')
def key(t): return ' '.join(t)
seeds = set()
srcs = [H2(m) for m in range(0, 4)] + [E2(m) for m in range(1, 4)]
for t in srcs:
    d = len(t) - N
    if d == 0: seeds.add(key(t))
    if d < 0 and d == -1:
        for k in range(len(t) + 1):
            for s in SINGLES: seeds.add(key(t[:k] + [s] + t[k:]))
    if 0 < d <= 2:
        single = [i for i, x in enumerate(t) if len(x) == 2]
        for comb in itertools.combinations(single, d):
            seeds.add(key([x for i, x in enumerate(t) if i not in comb]))
seeds = sorted(s for s in seeds if npawns(s) == N + 1 and all(s.split()))
def nb_move(r):
    t = r.split(); out = set()
    for f, tok in enumerate(t):
        w, b = parse(tok)
        for c, ranks in (('W', w), ('B', b)):
            for r0 in ranks:
                w2, b2 = set(w), set(b)
                (w2 if c == 'W' else b2).discard(r0)
                base = list(t); base[f] = unparse(w2, b2)
                for g in range(len(t)):
                    ww, bb = parse(base[g]) if base[g] else (set(), set())
                    for c2 in 'WB':
                        for r1 in range(2, 8):
                            if (c2 == 'W' and r1 in ww) or (c2 == 'B' and r1 in bb): continue
                            w3, b3 = set(ww), set(bb); (w3 if c2 == 'W' else b3).add(r1)
                            nt = list(base); nt[g] = unparse(w3, b3)
                            if all(nt): out.add(key(nt))
    out.discard(r); return out
def nb_add(r):
    t = r.split(); out = set()
    for g in range(len(t)):
        ww, bb = parse(t[g])
        for c2 in 'WB':
            for r1 in range(2, 8):
                if (c2 == 'W' and r1 in ww) or (c2 == 'B' and r1 in bb): continue
                w3, b3 = set(ww), set(bb); (w3 if c2 == 'W' else b3).add(r1)
                nt = list(t); nt[g] = unparse(w3, b3); out.add(key(nt))
    return out
t0 = time.time()
print(f'N={N}: {len(seeds)} seeds with N+1 pawns', flush=True)
s0 = solve(seeds); hits1 = [r for r in seeds if s0[r] == 'NNNP']
rs1 = random.Random(0).sample(seeds, min(len(seeds), SEEDCAP))
r1 = set().union(*(nb_move(r) for r in rs1)) - set(seeds)
s1 = solve(sorted(r1)); hits1 += [r for r in r1 if s1[r] == 'NNNP']
print(f'  radius 1 (move one pawn) around {len(rs1)} random seeds: {len(r1)} rings; N+1-pawn *3 so far: {len(hits1)}', flush=True)
for h in hits1: print('   HIT n+1', h, flush=True)
# radius 2 from the radius-1 rings that are 'close' (signature with a P or N first) -- capped random sample
pool = sorted(r for r in r1 if s1[r][:1] in 'NP')
rnd = random.Random(1); r2 = set()
for r in rnd.sample(pool, min(len(pool), 30)): r2 |= nb_move(r)
r2 = sorted(r2 - r1 - set(seeds)); rnd.shuffle(r2); r2 = r2[:R2CAP]
s2 = solve(r2); h2 = [r for r in r2 if s2[r] == 'NNNP']
print(f'  radius 2 sample: {len(r2)} rings (from {min(len(pool),30)} radius-1 rings with sig N.../P...); *3: {len(h2)}', flush=True)
for h in h2: print('   HIT n+1', h, flush=True)
ad = sorted(set().union(*(nb_add(r) for r in seeds)))
sa = solve(ad); ha = [r for r in ad if sa[r] == 'NNNP']
print(f'  N+2 pawns (seed + one pawn): {len(ad)} rings; *3: {len(ha)}', flush=True)
for h in ha[:20]: print('   HIT n+2', h, flush=True)
print('time', round(time.time() - t0, 1))
