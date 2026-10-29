#!/usr/bin/env python3
"""K15 fin2: confusion matrix between the exact classifier (grp, plain P, flat 7x6, 3 files, <=2+2 pawns, root passers allowed:
labels from `grp --dumproots`) and the one-ply classifier of the brief (oneply.py).  All roots of the exact classes frozen, on,
off, dud and a seeded random sample of the others.   usage: oneply_confusion.py roots.tsv SAMPLE_PER_OTHER_CLASS"""
import sys, random, collections
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2/scripts')
import oneply as O
g = O.G(7, 6, True); gf = {0, 1, 2}
rows = [l.rstrip('\n').split('\t') for l in open(sys.argv[1])]
nsamp = int(sys.argv[2]); rnd = random.Random(3)
by = collections.defaultdict(list)
for p, c in rows: by[c].append(p)
conf = collections.defaultdict(collections.Counter)
for c, ps in sorted(by.items()):
    if c not in ('frozen', 'on', 'off', 'dud', 'over', 'under'):
        ps = rnd.sample(ps, min(nsamp, len(ps)))
    for p in ps:
        lab = O.label(g, O.parse(p), gf)[0]
        conf[c][lab] += 1
print('rows: exact class (grp, plain P); columns: one-ply label (brief)')
labs = ['frozen', 'on', 'off', 'dud', 'over', 'other']
print('%-8s %8s ' % ('exact', 'n') + ' '.join('%7s' % l for l in labs))
for c in sorted(conf):
    n = sum(conf[c].values())
    print('%-8s %8d ' % (c, n) + ' '.join('%7d' % conf[c][l] for l in labs))
