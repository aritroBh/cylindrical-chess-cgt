#!/usr/bin/env python3
"""Compare D-model 'alone' prediction (alone_<board>.pred) with kp_p --pmodel (or kpsolve chess) output."""
import sys, collections
pred, res = sys.argv[1], sys.argv[2]
R = {}
for l in open(res):
    if l.startswith('[') or ' | ' not in l: continue
    p, r = l.rstrip('\n').split(' | ')
    R[p.strip()] = r.split()
C = collections.Counter(); bad = collections.defaultdict(list)
for l in open(pred):
    pos, nm, cn, d = l.rstrip('\n').split(' | ')
    r = R.get(pos.strip())
    if r is None: C[(nm, 'missing')] += 1; continue
    exact = r[0] == r[1]
    k = (nm, 'agree' if (exact and r[0] == d) else ('bounds-differ' if not exact else 'differ'))
    C[k] += 1
    if k[1] != 'agree' and len(bad[k]) < 4: bad[k].append('%s D=%s got=%s' % (pos.strip(), d, ''.join(r)))
for k in sorted(C): print(k, C[k])
for k, v in bad.items():
    print(k)
    for x in v: print('    ', x)
