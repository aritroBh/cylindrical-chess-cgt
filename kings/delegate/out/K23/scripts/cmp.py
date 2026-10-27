#!/usr/bin/env python3
"""cmp.py FILE_P FILE_F : pair up (w,b) results per context; list contexts where P differs from frozen."""
import sys, collections
def load(fn):
    d = {}
    for l in open(fn):
        if '|' not in l: continue
        pos, r = l.rsplit(' | ', 1); r = r.split()[0]
        toks = pos.split(); stm = toks[-2]; key = ' '.join(toks[:-2])
        d.setdefault(key, {})[stm] = r
    return d
P = load(sys.argv[1]); F = load(sys.argv[2])
same = diff = 0; rows = []
for k in P:
    p = (P[k]['w'], P[k]['b']); f = (F[k]['w'], F[k]['b'])
    if p == f: same += 1
    else: diff += 1; rows.append((k, p, f))
print('contexts', len(P), 'P==frozen', same, 'P!=frozen', diff)
for k, p, f in rows: print(k, 'P', p, 'frozen', f)
