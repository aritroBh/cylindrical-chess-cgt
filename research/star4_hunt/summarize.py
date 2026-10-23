#!/usr/bin/env python3
"""Aggregate #summary lines of h4_scan outputs in a directory: python3 summarize.py out/w5p10"""
import sys, glob, re, collections
d = sys.argv[1]
tot = collections.Counter()
splits = collections.defaultdict(collections.Counter)
nfiles = collections.Counter()
hits = collections.defaultdict(list)
for f in sorted(glob.glob(d + '/*.tsv')):
    base = f.split('/')[-1]
    split = '_'.join(base.split('_')[:2])
    for line in open(f):
        if line.startswith('#summary'):
            nfiles[split] += 1
            for tok in line.split():
                if '=' in tok:
                    k, v = tok.split('=')
                    if re.fullmatch(r'-?\d+', v):
                        splits[split][k] += int(v)
        elif not line.startswith('#'):
            p = line.rstrip('\n').split('\t')
            if p[0].startswith('NEAR'):
                hits[split].append(('near', p))
            elif len(p) >= 5 and p[4].lstrip('-').isdigit() and int(p[4]) >= 2:
                hits[split].append(('nim', p))
print('split chunks roots states nim0 nim1 nim2 nim3 nim4+ near3 near4+')
for s in sorted(splits):
    c = splits[s]
    n4 = sum(v for k, v in c.items() if re.fullmatch(r'nim([4-9]|\d\d)', k))
    nr4 = sum(c.get('near%d' % i, 0) for i in range(4, 8))
    print(s, nfiles[s], c['roots'], c['states'], c['nim0'], c['nim1'], c['nim2'], c['nim3'], n4, c['near3'], nr4)
    tot.update(c)
print('TOTAL roots', tot['roots'], 'nim2', tot['nim2'], 'nim3', tot['nim3'], 'nim4+', sum(v for k, v in tot.items() if re.fullmatch(r'nim([4-9]|\d\d)', k)), 'near3', tot['near3'], 'near4+', sum(tot.get('near%d' % i, 0) for i in range(4, 8)))
