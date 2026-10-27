#!/usr/bin/env python3
"""digest.py LOGFILE: for each run block of key_results.txt, print position, pk2 P, kp_p P, pk2 frozen, kp frozen (result pairs) and flag disagreements."""
import sys, re
blocks = {}; cur = None; sec = None
for l in open(sys.argv[1]):
    l = l.rstrip('\n')
    if l.startswith('==='): cur = l.split()[1]; blocks[cur] = {}; continue
    if l.startswith('---'):
        sec = l[4:]; 
        if cur is not None and sec.startswith(('pk2 P', 'pk2 F', 'kp_p --pmodel', 'kp --frozen')): blocks[cur][sec.split(' (')[0]] = []
        else: sec = None
        continue
    if sec and ' | ' in l and cur:
        pos, r = l.rsplit(' | ', 1); r = r.split()
        blocks[cur][sec.split(' (')[0]].append((pos, r[0] + r[1]))
bad = 0
for b, d in blocks.items():
    print('##', b)
    keys = list(d)
    n = len(d[keys[0]])
    for i in range(n):
        pos = d['pk2 P'][i][0]
        vals = [d[k][i][1] for k in ['pk2 P', 'kp_p --pmodel', 'pk2 F', 'kp --frozen']]
        flag = '' if vals[0] == vals[1] and vals[2] == vals[3] else '  *** DISAGREE'
        if flag: bad += 1
        print(f'{pos:40s} P={vals[0]}/{vals[1]}  frozen={vals[2]}/{vals[3]}{flag}')
print('disagreements between implementations:', bad)
