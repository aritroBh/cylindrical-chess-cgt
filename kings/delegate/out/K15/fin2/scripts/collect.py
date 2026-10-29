#!/usr/bin/env python3
"""K15 fin2: distinct groups (up to file translation and file mirror on the cylinder, and colour flip = rank mirror + colour swap)
of a class (dud / over / under) over all census candidate files of a runs directory.
usage: collect.py RUNSDIR CLASS [BOARD-filter e.g. cyl:7x6 or -] [readings, default ABT]   -> TSV: canonical <TAB> n_roots <TAB> representative <TAB> found-in
reading: pA* = A (free passes for both sides), npB*/flat*np/flatB* = B (plain P), tp* = tempo signature census."""
import sys, os, glob, re, json
from collections import defaultdict
runsdir, cls = sys.argv[1], sys.argv[2]
bfilter = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != '-' else None
rfilter = sys.argv[4] if len(sys.argv) > 4 else 'ABT'
def parse(s):
    t = [x for x in s.split() if len(x) >= 3 and x[0] in 'KkPp']
    return [(x[0], ord(x[1]) - 97, int(x[2:])) for x in t]
def fmt(p):
    ks = sorted(p, key=lambda z: ('KkPp'.index(z[0]), z[1], z[2]))
    return ' '.join('%s%s%d' % (c, chr(97 + f), r) for c, f, r in ks)
def canon(p, W, H, flat):
    best = None
    for flip in (0, 1):
        for mir in ((0, 1) if not flat else (0,)):
            q = []
            for c, f, r in p:
                if mir: f = (-f) % W
                if flip: c = c.swapcase(); r = H + 1 - r
                q.append((c, f, r))
            for tr in (range(W) if not flat else [0]):
                v = fmt([(c, (f + tr) % W, r) for c, f, r in q])
                if best is None or v < best: best = v
    return best
d = defaultdict(lambda: [0, None, set()])
for fn in sorted(glob.glob(os.path.join(runsdir, '*_cands.txt'))):
    base = os.path.basename(fn)
    m = re.match(r'(.+?)_(strict|passer)_cands\.txt', base)
    if not m: continue
    run, var = m.group(1), m.group(2)
    mm = re.match(r'(?:pA|npB|tp|flat76_np|flatA|flatB)_?(\d+)x(\d+)', run)
    if run.startswith('flat76_np'): W, H, flat = 7, 6, True
    else:
        mm = re.search(r'(\d+)x(\d+)', run); W, H = int(mm.group(1)), int(mm.group(2)); flat = run.startswith('flat')
    board = ('flat:' if flat else 'cyl:') + '%dx%d' % (W, H)
    if bfilter and board != bfilter: continue
    reading = 'A' if run.startswith(('pA', 'flatA')) else ('T' if run.startswith('tp') else 'B')
    if reading not in rfilter: continue
    for l in open(fn):
        p = l.rstrip('\n').split('\t')
        if p[0] != cls: continue
        c = canon(parse(p[1]), W, H, flat)
        e = d[(board, c)]
        e[0] += 1
        if e[1] is None: e[1] = p[1]
        e[2].add('%s:%s:%s' % (reading, 'nopasser' if var == 'strict' else 'passer-ok', re.sub(r'^(pA|npB|tp|flatA|flatB)_', '', run)))
for (board, c), (n, rep, fi) in sorted(d.items()):
    print('%s\t%s\t%d\t%s\t%s' % (board, c, n, rep, ' '.join(sorted(fi))))
