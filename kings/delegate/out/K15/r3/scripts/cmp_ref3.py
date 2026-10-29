#!/usr/bin/env python3
"""K15 r3: compare ref3 (independent P solver) on the sampled positions with the kp_p output stored in fin2/cf/TAG.out.
usage: cmp_ref3.py TAG [TAG...]  -> prints per tag: sampled lines, ref3 lines, agree, differ (a kp_p inexact A != B counts as 'inexact')."""
import sys, os, glob
R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); FIN2 = os.path.join(os.path.dirname(R3), 'fin2')
tot = [0, 0, 0, 0, 0]
for tag in sys.argv[1:]:
    kp = {}
    for l in open(os.path.join(FIN2, 'cf', tag + '.out')):
        p = l.rstrip('\n').split(' | ')
        if len(p) >= 2: kp[p[0].strip()] = p[1].split()
    n = a = d = ix = miss = 0
    for f in sorted(glob.glob(os.path.join(R3, 'xs', tag + '.chunk*.in'))):
        o = f[:-3] + '.out'
        ref = {}
        for l in open(o) if os.path.exists(o) else []:
            p = l.rstrip('\n').split(' | ')
            if len(p) >= 2: ref[p[0].strip()] = p[1].strip()
        for l in open(f):
            pos = l.strip(); n += 1
            if pos not in ref: miss += 1; continue
            k = kp.get(pos)
            if k is None or k[0] != k[-1]: ix += 1; continue
            if k[0] == ref[pos]: a += 1
            else: d += 1; print('DIFF', tag, pos, 'kpp', k, 'ref3', ref[pos])
    print(tag, 'sampled', n, 'ref3 done', n - miss, 'agree', a, 'differ', d, 'kpp inexact', ix)
