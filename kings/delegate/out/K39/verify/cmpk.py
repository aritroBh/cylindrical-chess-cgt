#!/usr/bin/env python3
"""compare rf39 output (one bound) with kpsolve-format output (kp/kp39 --moves). usage: cmpk.py KP.out RF.out A|B"""
import sys
def norm(ms): return sorted(m.replace('=', '') for m in ms.split())
K = {}
for l in open(sys.argv[1]):
    l = l.rstrip('\n')
    if not l or l.startswith('#'): continue
    p = l.split(' | '); ab = p[1].split()
    if len(p) == 3: ma = mb = p[2]
    elif len(p) == 4: ma, mb = p[2][3:], p[3][3:]
    else: ma = mb = ''
    K[p[0]] = (ab, norm(ma), norm(mb))
i = 0 if sys.argv[3] == 'A' else 1
n = nd = nm = nx = 0
for l in open(sys.argv[2]):
    l = l.rstrip('\n')
    if not l or l.startswith('#'): continue
    p = l.split(' | '); n += 1
    if p[0] not in K: n -= 1; continue
    ab, ma, mb = K[p[0]]
    if p[1] == 'X' or ab[i] == 'X':
        nx += 1
        if p[1] != ab[i]: nd += 1; print('X-diff', p[0])
        continue
    if p[1] != ab[i]: nd += 1; print('root-diff', p[0], ab[i], p[1])
    mv = norm(p[2]) if len(p) > 2 else []
    if mv != (ma if i == 0 else mb): nm += 1; print('move-diff', p[0], set(mv) ^ set(ma if i == 0 else mb))
print(f"{sys.argv[2]}: positions {n} (illegal {nx}); root diffs {nd}; move-list diffs {nm}")
