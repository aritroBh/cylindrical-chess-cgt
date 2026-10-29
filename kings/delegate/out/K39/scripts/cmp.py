#!/usr/bin/env python3
"""K39: compare kpsolve-format output (kp or kp39, with --moves) with two own39 runs (bound A and bound B, MOVES=1).
usage: cmp.py KP.out OWN_A.out OWN_B.out  -> counts of root and per-move differences (moves compared as sorted sets)."""
import sys
def kp(path):
    d = {}
    for l in open(path):
        l = l.rstrip('\n')
        if not l or l.startswith('#'): continue
        parts = l.split(' | ')
        pos, ab = parts[0], parts[1].split()
        ma = mb = None
        if len(parts) == 3: ma = mb = parts[2]
        elif len(parts) == 4: ma, mb = parts[2][3:], parts[3][3:]
        d[pos] = (ab[0], ab[1], sorted(ma.split()) if ma else [], sorted(mb.split()) if mb else [])
    return d
def own(path):
    d = {}
    for l in open(path):
        l = l.rstrip('\n')
        if not l or l.startswith('#'): continue
        parts = l.split(' | ')
        d[parts[0]] = (parts[1], sorted(parts[2].split()) if len(parts) > 2 else [])
    return d
K, A, B = kp(sys.argv[1]), own(sys.argv[2]), own(sys.argv[3])
nr = nd = nm = nx = 0
for pos, (a, b, ma, mb) in K.items():
    nr += 1
    oa, ob = A.get(pos), B.get(pos)
    if oa is None or ob is None: print("missing", pos); nd += 1; continue
    if a == 'X' or oa[0] == 'X':
        nx += 1
        if a != oa[0] or b != ob[0]: print("X-diff", pos, a, b, oa[0], ob[0]); nd += 1
        continue
    if (a, b) != (oa[0], ob[0]): print("root-diff", pos, (a, b), (oa[0], ob[0])); nd += 1
    if ma != oa[1] or mb != ob[1]:
        nm += 1; print("move-diff", pos, set(ma) ^ set(oa[1]), set(mb) ^ set(ob[1]))
print(f"positions {nr} (illegal {nx}); root differences {nd}; positions with move-list differences {nm}")
