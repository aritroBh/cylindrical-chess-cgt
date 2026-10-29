#!/usr/bin/env python3
"""K39: compare a one-bound kp39 output (--bound X: "pos | V V | moves") with an own39/own2 output ("pos | V | moves").
usage: cmp1.py KP.out OWN.out"""
import sys
def rd(path, kp):
    d = {}
    for l in open(path):
        l = l.rstrip('\n')
        if not l or l.startswith('#'): continue
        p = l.split(' | ')
        v = p[1].split()[0]
        d[p[0]] = (v, sorted(p[2].split()) if len(p) > 2 else [])
    return d
K, O = rd(sys.argv[1], 1), rd(sys.argv[2], 0)
nr = nd = nm = nx = 0
for pos, (v, m) in K.items():
    nr += 1
    if pos not in O: print("missing", pos); nd += 1; continue
    ov, om = O[pos]
    if v == 'X' or ov == 'X':
        nx += 1
        if v != ov: print("X-diff", pos, v, ov); nd += 1
        continue
    if v != ov: print("root-diff", pos, v, ov); nd += 1
    if m != om: nm += 1; print("move-diff", pos, set(m) ^ set(om))
print(f"positions {nr} (illegal {nx}); root differences {nd}; positions with move-list differences {nm}")
