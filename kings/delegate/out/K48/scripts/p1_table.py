#!/usr/bin/env python3
"""K48: per-position, per-move table for Z_O on cyl:8x6 in chess from kpsolve-format outputs (kp cap 1; kp39 --refine cap 1;
optional restricted cap-2 runs A' and B' of kp39) and own39 (bound A, bound B, refinement).
usage: p1_table.py KP.out KP39R.out OWNA.out OWNB.out [CAP2_Ap.out CAP2_Bp.out]
Values are from White's view. A move 'loses' if the value after it is a loss for the mover in both bounds; 'wins'/'draws' likewise;
'<=D' if the mover's favourable bound is D (it cannot win); 'open' otherwise."""
import sys
def kp(path):
    d = {}
    for l in open(path):
        if ' | ' not in l: continue
        parts = l.rstrip('\n').split(' | '); ab = parts[1].split()
        if len(parts) == 3: ma = mb = parts[2]
        else: ma, mb = parts[2][3:], parts[3][3:]
        A = dict(x.split(':') for x in ma.split()); B = dict(x.split(':') for x in mb.split())
        if len(ab) == 1: ab = ab * 2
        d[parts[0]] = (ab[0], ab[1], {m: (A[m], B[m]) for m in A})
    return d
def own(pa, pb):
    d = {}
    A = {l.split(' | ')[0]: l.rstrip('\n').split(' | ') for l in open(pa) if ' | ' in l}
    B = {l.split(' | ')[0]: l.rstrip('\n').split(' | ') for l in open(pb) if ' | ' in l}
    for p in A:
        ma = dict(x.split(':') for x in A[p][2].split()); mb = dict(x.split(':') for x in B[p][2].split())
        d[p] = (A[p][1], B[p][1], {m: (ma[m], mb[m]) for m in ma})
    return d
def onebound(path, which):   # restricted cap-2 run: one bound only
    d = {}
    for l in open(path):
        if ' | ' not in l: continue
        parts = l.rstrip('\n').split(' | '); v = parts[1].split()[0]
        mv = parts[2][3:] if parts[2][:2] in ('A:', 'B:') else parts[2]
        d[parts[0]] = (v, dict(x.split(':') for x in mv.split()))
    return d
def verdict(a, b, stm):
    good, bad = ('W', 'L') if stm == 'w' else ('L', 'W')
    if a == b: return 'wins' if a == good else 'loses' if a == bad else 'draws'
    fav = a if stm == 'w' else b
    if fav == bad: return 'loses'
    if fav == 'D': return '<=D'
    return 'open'
K, R, O = kp(sys.argv[1]), kp(sys.argv[2]), own(sys.argv[3], sys.argv[4])
C = None
if len(sys.argv) > 6: CA, CB = onebound(sys.argv[5], 'A'), onebound(sys.argv[6], 'B'); C = True
diff = 0
for p in K:
    stm = p.split()[-2]
    rv = (R[p][0], R[p][1]); ov = (O[p][0], O[p][1])
    line = f"POS {p}: kp {K[p][0]}{K[p][1]}  kp39r {rv[0]}{rv[1]}  own39r {ov[0]}{ov[1]}"
    if C: line += f"  cap2' {CA[p][0]}{CB[p][0]}"
    if rv != ov: diff += 1; line += '  DIFFER'
    print(line)
    assert set(K[p][2]) == set(R[p][2]) == set(O[p][2]), 'move sets differ'
    for m in sorted(K[p][2]):
        a, b = R[p][2][m]; oa, ob = O[p][2][m]
        s = f"   {m:8s} kp {''.join(K[p][2][m])}  kp39r {a}{b}  own39r {oa}{ob}"
        if (a, b) != (oa, ob): diff += 1; s += ' DIFFER'
        v = verdict(a, b, stm); s += f"  cap1r: {v}"
        if C:
            ca, cb = CA[p][1][m], CB[p][1][m]; s += f"  cap2' {ca}{cb}: {verdict(ca, cb, stm)}"
        print(s)
print('differences kp39r vs own39r (positions + moves):', diff)
