#!/usr/bin/env python3
"""Compare local.cpp (C++) with local_py.py (independent Python) on roots of the hypothesis class.
usage: compare.py BOARD W H FZLO FZHI F WMAX BMAX SAMPLE_OTHERS SEED [safe] [ep]
All roots with >=2 attacked s-bar pawns are taken; of the other roots SAMPLE_OTHERS are drawn at random."""
import sys, random, subprocess, itertools, os
sys.path.insert(0, os.path.dirname(__file__))
import local_py
kind, W, H, lo, hi, F, wmax, bmax, nother, seed = sys.argv[1], *map(int, sys.argv[2:11])
safe = 'safe' in sys.argv[11:]
withep = 'ep' in sys.argv[11:]
random.seed(seed)
wrap = kind == 'cyl'
def name(f, r): return chr(97 + f) + str(r + 1)
def fl(a, d):   # neighbour file
    f = a + d
    return f % W if wrap else (f if 0 <= f < W else None)
wsq = [(F, r) for r in range(1, H - 1)]
bsq = [(f, r) for f in range(lo, hi + 1) for r in range(1, H - 1)]
wk_squares = [(f, r) for f in range(lo, hi + 1) for r in range(H)]
allsq = [(f, r) for f in range(W) for r in range(H)]
roots_att, roots_other = [], []
for nw in range(1, wmax + 1):
  for wp in itertools.combinations(wsq, nw):
    front = max(r for f, r in wp)
    for nb in range(0, bmax + 1):
      for bp in itertools.combinations(bsq, nb):
        if set(wp) & set(bp): continue
        att = sum(1 for (f, r) in wp if any((fl(f, d), r + 1) in bp for d in (-1, 1)))
        variants = [None]
        if withep and H >= 6 and (F, 3) in wp and (F, 1) not in wp and (F, 2) not in wp and not ((F,1) in bp or (F,2) in bp):
            if any((fl(F, d), 3) in bp for d in (-1, 1)): variants.append(name(F, 2))
        for ep in variants:
          for wk in wk_squares:
            for bk in allsq:
                if bk[0] != F or bk[1] <= front: continue
                if wk == bk or wk in wp or wk in bp or bk in bp: continue
                if any(fl(wk[0], d) is not None and (fl(wk[0], d), wk[1] + 1) in bp for d in (-1, 1)): continue   # White king attacked by a Black pawn: illegal with Black to move
                # kings not adjacent
                df = abs(wk[0] - bk[0]); df = min(df, W - df) if wrap else df
                if max(df, abs(wk[1] - bk[1])) <= 1: continue
                line = 'K%s k%s %s %s b %s' % (name(*wk), name(*bk), ' '.join('P' + name(*p) for p in wp), ' '.join('p' + name(*p) for p in bp), ep or '-')
                line = ' '.join(line.split())
                (roots_att if att >= 2 else roots_other).append(line)
sample = random.sample(roots_other, min(nother, len(roots_other)))
maxatt = int(os.environ.get('MAXATT', '100000'))
def cpp_eval(rs):
    a = ['./local', '--board', kind, str(W), str(H), '--fz', str(lo), str(hi)] + (['--safe'] if safe else []) + ['pos']
    o = subprocess.run(a, input='\n'.join(rs) + '\n', capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).stdout
    return [l for l in o.splitlines() if '|' in l and not l.startswith(' ')]
if len(roots_att) > maxatt:
    # keep every root that the C++ solver says White wins (up to 8), and fill up with random non-wins
    res = cpp_eval(roots_att)
    wins_k = set(l.split('|')[0].strip() for l in res if 'WHITE-WINS' in l)
    def nm(line):
        parts = line.split(); pcs = parts[:-2]
        wps = sorted([p for p in pcs if p[0] == 'P'], key=lambda p: (int(p[2:]), p[1]))
        bps = sorted([p for p in pcs if p[0] == 'p'], key=lambda p: (int(p[2:]), p[1]))
        return ' '.join([[p for p in pcs if p[0]=='K'][0], [p for p in pcs if p[0]=='k'][0]] + wps + bps + [parts[-2], parts[-1]])
    wl = [r for r in roots_att if nm(r) in wins_k]
    nl = [r for r in roots_att if nm(r) not in wins_k]
    wl = random.sample(wl, min(8, len(wl)))
    roots_att = wl + random.sample(nl, min(maxatt - len(wl), len(nl)))
roots = roots_att + sample
print('roots with >=2 attacked: %d, other roots total %d, sampled %d' % (len(roots_att), len(roots_other), len(sample)))
# C++
args = ['./local', '--board', kind, str(W), str(H), '--fz', str(lo), str(hi)] + (['--safe'] if safe else []) + ['pos']
out = subprocess.run(args, input='\n'.join(roots) + '\n', capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).stdout
cpp = {}
for l in out.splitlines():
    if '|' in l and not l.startswith(' '):
        a, b = l.split('|')
        a = a.strip(); b = b.strip()
        cpp[a] = None if b == 'no-win' else (-1 if b.startswith('ILLEGAL') else int(b.split('T=')[1]))
solve = local_py.make(kind, W, H, lo, hi, safe)
bad = 0; nwin = 0; nillegal = 0
for line in roots:
    s = local_py.parse(line, W, H)
    t = solve(s)
    key = ' '.join(line.split())
    # C++ normalises the position string (pieces order); find by re-normalisation
    cands = [k for k in cpp if k.replace('  ', ' ') == key]
    # normalise: C++ prints K k then P by square order then p by square order, side, ep
    parts = line.split(); pcs = parts[:-2]
    wps = sorted([p for p in pcs if p[0] == 'P'], key=lambda p: (int(p[2:]), p[1]))
    bps = sorted([p for p in pcs if p[0] == 'p'], key=lambda p: (int(p[2:]), p[1]))
    norm = ' '.join([[p for p in pcs if p[0]=='K'][0], [p for p in pcs if p[0]=='k'][0]] + wps + bps + [parts[-2], parts[-1]])
    c = cpp.get(norm, 'MISSING')
    if c == -1: nillegal += 1
    if c == 'MISSING' or c == -1 or c != t:
        bad += 1
        if bad <= 10: print('MISMATCH', line, 'cpp', c, 'py', t)
    if t is not None: nwin += 1
print('compared %d roots, %d White wins (python), mismatches %d, illegal %d' % (len(roots), nwin, bad, nillegal))
