#!/usr/bin/env python3
"""Referee's own T2 (two-shuttle) search.  Own enumerator, own leak classification, solver = ref3m only.
Nothing from K26/scripts is imported.  Definitions from the task text:
 F_Z = files a,b,c (index 0,1,2), <= nW white and <= nB black pawns on ranks 2..H-1 of F_Z,
 K1 king squares empty and not attacked by an enemy group pawn, K2 white-pair squares and black-pair squares at
 Chebyshev distance >= 2, both pairs adjacent squares.
 leak = legal non-shuttle move of the mover whose value is not L (white mover) / not W (black mover).
 Promotions in ref3m output are one entry per push/capture (collapsed convention).
usage: my_t2.py BOARD(flat7x6|cyl:8x6) NW NB OUT.json [shard i/n] [--maxleak 2]
"""
import sys, itertools, subprocess, json, collections, time, os

board = sys.argv[1]
NW = int(sys.argv[2]); NB = int(sys.argv[3]); OUTF = sys.argv[4]
shard = (0, 1)
for a in sys.argv[5:]:
    if '/' in a:
        shard = tuple(map(int, a.split('/')))
dims = board.split(':')[-1] if ':' in board else board[4:]
W_, H = map(int, dims.split('x'))
BIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bin', 'ref3m')   # attempt 5 copy: fresh build in K26/bin
t0 = time.time()
sq = [(f, r) for f in range(3) for r in range(1, H + 1)]
nm = {s: 'abc'[s[0]] + str(s[1]) for s in sq}
def d(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
pawn_sq = [s for s in sq if 2 <= s[1] <= H - 1]
def watt(s):   # squares of F_Z attacked by a white pawn on s
    return {(s[0] + df, s[1] + 1) for df in (-1, 1) if 0 <= s[0] + df <= 2 and s[1] + 1 <= H}
def batt(s):
    return {(s[0] + df, s[1] - 1) for df in (-1, 1) if 0 <= s[0] + df <= 2 and s[1] - 1 >= 1}
adj_pairs = [(a, b) for i, a in enumerate(sq) for b in sq[i + 1:] if d(a, b) == 1]

def configs():
    for kw in range(NW + 1):
        for wp in itertools.combinations(pawn_sq, kw):
            for kb in range(NB + 1):
                for bp in itertools.combinations(pawn_sq, kb):
                    if set(wp) & set(bp):
                        continue
                    yield wp, bp

cands = []
ncfg = 0
for wp, bp in configs():
    ncfg += 1
    occ = set(wp) | set(bp)
    wa = set().union(*[watt(s) for s in wp]) if wp else set()
    ba = set().union(*[batt(s) for s in bp]) if bp else set()
    wsafe = {s for s in sq if s not in occ and s not in ba}
    bsafe = {s for s in sq if s not in occ and s not in wa}
    wps = [p for p in adj_pairs if p[0] in wsafe and p[1] in wsafe]
    bps = [p for p in adj_pairs if p[0] in bsafe and p[1] in bsafe]
    for zp in wps:
        for bq in bps:
            if all(d(x, y) >= 2 for x in zp for y in bq):
                cands.append((wp, bp, zp, bq))
if shard[1] > 1:
    cands = [c for i, c in enumerate(cands) if i % shard[1] == shard[0]]
print('configs', ncfg, 'candidates', len(cands), 'time %.1f' % (time.time() - t0), file=sys.stderr, flush=True)

def pos(c, wk, bk, stm):
    wp, bp, zp, bq = c
    ps = ' '.join(['P' + nm[s] for s in wp] + ['p' + nm[s] for s in bp])
    return 'K%s k%s %s%s -' % (nm[wk], nm[bk], (ps + ' ') if ps else '', stm) if False else (
        'K%s k%s %s %s -' % (nm[wk], nm[bk], ps, stm) if ps else 'K%s k%s %s -' % (nm[wk], nm[bk], stm))

def run(lines):
    p = subprocess.Popen([BIN, '--board', board, '--moves'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True)
    out, err = p.communicate('\n'.join(lines) + '\n')
    res = out.split('\n')
    res = [x for x in res if x and not x.startswith('layers')]
    assert len(res) == len(lines), (len(res), len(lines), err[-300:])
    return res

def leaks_of(line, stm, shuttle):
    parts = line.split(' | ')
    rest = parts[1].split()
    root = rest[0]
    if root == 'X':
        return None
    lose = 'L' if stm == 'w' else 'W'
    nsh = 0; lk = []
    for tok in rest[1:]:
        n, v = tok.rsplit(':', 1)
        if n == shuttle:
            nsh += 1
            continue
        if v != lose:
            lk.append(tok)
    return root, nsh, lk

def roots(c, which):
    wp, bp, zp, bq = c
    L = []
    meta = []
    for a in (0, 1):
        for b in (0, 1):
            for s in 'wb':
                if which == 1 and not (a == 0 and b == 0):
                    continue
                L.append(pos(c, zp[a], bq[b], s))
                sh = ('K' + nm[zp[a]] + nm[zp[1 - a]]) if s == 'w' else ('K' + nm[bq[b]] + nm[bq[1 - b]])
                meta.append((s, sh))
    return L, meta

BATCH = 60000
hist1 = collections.Counter()
keep = []
bad = 0
for i in range(0, len(cands), BATCH):
    chunk = cands[i:i + BATCH]
    L = []; M = []
    for c in chunk:
        l, m = roots(c, 1)
        L += l; M += m
    res = run(L)
    for j, c in enumerate(chunk):
        tot = 0; ok = True
        for k in range(2):
            r = leaks_of(res[2 * j + k], M[2 * j + k][0], M[2 * j + k][1])
            if r is None or r[1] != 1:
                ok = False; break
            tot += len(r[2])
        if not ok:
            bad += 1; continue
        hist1[tot] += 1
        if tot <= 2:
            keep.append(c)
    print('stage1', i + len(chunk), 'of', len(cands), 'time %.1f' % (time.time() - t0), file=sys.stderr, flush=True)

hist2 = collections.Counter()
duds = []; ones = []
for i in range(0, len(keep), 15000):
    chunk = keep[i:i + 15000]
    L = []; M = []
    for c in chunk:
        l, m = roots(c, 8)
        L += l; M += m
    res = run(L)
    for j, c in enumerate(chunk):
        tot = 0; ok = True; vals = []
        for k in range(8):
            r = leaks_of(res[8 * j + k], M[8 * j + k][0], M[8 * j + k][1])
            if r is None or r[1] != 1:
                ok = False; break
            tot += len(r[2]); vals.append(r[0])
        if not ok:
            bad += 1; continue
        hist2[tot] += 1
        if tot == 0:
            duds.append((c, vals))
        elif tot <= 2:
            ones.append((c, tot))
    print('stage2', i + len(chunk), 'of', len(keep), 'time %.1f' % (time.time() - t0), file=sys.stderr, flush=True)

def cs(c):
    wp, bp, zp, bq = c
    return {'W': [nm[x] for x in zp], 'B': [nm[x] for x in bq], 'wp': [nm[x] for x in wp], 'bp': [nm[x] for x in bp]}
out = {'board': board, 'nw': NW, 'nb': NB, 'shard': shard, 'configs': ncfg, 'candidates': len(cands), 'bad': bad,
       'stage1_hist_two_roots': dict(sorted(hist1.items())), 'stage2_hist_8roots_upto2': dict(sorted(hist2.items())),
       'duds': [dict(cs(c), vals=v) for c, v in duds],
       'low_leak': [dict(cs(c), total=t) for c, t in ones], 'seconds': round(time.time() - t0, 1)}
json.dump(out, open(OUTF, 'w'), indent=1)
print(json.dumps({k: out[k] for k in ('candidates', 'bad', 'stage1_hist_two_roots', 'stage2_hist_8roots_upto2')}), file=sys.stderr)
print('DUDS', json.dumps(out['duds']), file=sys.stderr)
