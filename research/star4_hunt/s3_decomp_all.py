#!/usr/bin/env python3
"""For every *3 position found in this study (flat boards), test whether removing some pair of pawns leaves a *2
(i.e. *3 = *2 core + *1 pair).  Reports the positions for which no pair removal leaves a *2 (candidate primitive *3)."""
import glob, itertools, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collect import parse, fmt, canon
H = './h4'
found = set()
for f in glob.glob('out/*.out') + glob.glob('out/w5p10/*.tsv'):
    if 'r1_' in f or 'r3_' in f or 'rsa' in f: continue      # ring runs handled separately
    for line in open(f):
        p = line.rstrip('\n').split('\t')
        if len(p) >= 5 and p[4] == 'nim=3': found.add(canon(p[1]))
        elif len(p) >= 5 and p[0].startswith('W:') and p[4] == '3' and not line.startswith('#'): found.add(canon(p[0]))
print(len(found), 'distinct flat *3 positions found (up to mirror and colour reversal)')
dec = 0; prim = []
for c in sorted(found):
    w, b = parse(c)
    allp = [('W', p) for p in w] + [('B', p) for p in b]
    rows = []
    for comb in itertools.combinations(range(len(allp)), 2):
        w2 = [p for i, (s, p) in enumerate(allp) if s == 'W' and i not in comb]
        b2 = [p for i, (s, p) in enumerate(allp) if s == 'B' and i not in comb]
        if w2 and b2: rows.append(fmt(w2, b2))
    open('/tmp/_s3d.txt', 'w').write("\n".join(rows) + "\n")
    out = subprocess.run([H, '--flat', '--width', '8', '--max-entries', '4194304', '--eval', '/tmp/_s3d.txt'], capture_output=True, text=True).stdout.splitlines()[1:]
    ok = any(len(l.split('\t')) > 4 and l.split('\t')[4] == '2' for l in out)
    dec += ok
    if not ok: prim.append(c)
print(dec, 'decomposable as (*2 after removing one pair); not directly decomposable:', len(prim))
# the others carry inert pawns: strip 1-2 inert pawns (value-preserving removals) and test again
still = []
if prim:
    open('/tmp/_prim.txt', 'w').write("\n".join(prim) + "\n")
    mins = [l.split('\t')[0] for l in subprocess.run([H, '--flat', '--width', '8', '--minimize', '/tmp/_prim.txt'], capture_output=True, text=True).stdout.splitlines() if l.startswith('W:')]
    for m_ in mins:
        w, b = parse(m_)
        allp = [('W', p) for p in w] + [('B', p) for p in b]
        rows = []
        for comb in itertools.combinations(range(len(allp)), 2):
            w2 = [p for i, (s_, p) in enumerate(allp) if s_ == 'W' and i not in comb]
            b2 = [p for i, (s_, p) in enumerate(allp) if s_ == 'B' and i not in comb]
            if w2 and b2: rows.append(fmt(w2, b2))
        open('/tmp/_s3d.txt', 'w').write("\n".join(rows) + "\n")
        out = subprocess.run([H, '--flat', '--width', '8', '--max-entries', '4194304', '--eval', '/tmp/_s3d.txt'], capture_output=True, text=True).stdout.splitlines()[1:]
        if not any(len(l.split('\t')) > 4 and l.split('\t')[4] == '2' for l in out): still.append(m_)
    print('after removing inert pawns:', len(mins) - len(still), 'of', len(mins), 'decompose;', len(still), 'remain (candidate primitive *3):', still)
