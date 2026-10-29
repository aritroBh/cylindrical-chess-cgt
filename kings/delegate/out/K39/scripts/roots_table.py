#!/usr/bin/env python3
"""K39: per-root and per-move table for a group from kpsolve-format outputs (kp cap 1, kp39 --refine cap 1) and own39
(bound A, bound B, refine). usage: roots_table.py GROUP KP.out KP39.out OWNA.out OWNB.out
Prints for each root and each move: kp cap-1 bounds, kp39 refine bounds, own39 refine bounds, the shuttle flag, and
whether the refined value is exact. Deviation verdict: 'loses' (exact, the mover loses), 'draws', 'wins', or 'open'."""
import sys
SH = {'ZB': ({'b2', 'c3'}, {'a4', 'b5'}), 'ZC': ({'c2', 'c3'}, {'a4', 'a5'})}
g = sys.argv[1]; WS, BS = SH[g]
def kp(path):
    d = {}
    for l in open(path):
        parts = l.rstrip('\n').split(' | ')
        ab = parts[1].split()
        if len(parts) == 3: ma = mb = parts[2]
        else: ma, mb = parts[2][3:], parts[3][3:]
        A = dict(x.split(':') for x in ma.split()); B = dict(x.split(':') for x in mb.split())
        d[parts[0]] = (ab[0], ab[1], {m: (A[m], B[m]) for m in A})
    return d
def own(pa, pb):
    d = {}
    A = {l.split(' | ')[0]: l.rstrip('\n').split(' | ') for l in open(pa)}
    B = {l.split(' | ')[0]: l.rstrip('\n').split(' | ') for l in open(pb)}
    for p in A:
        ma = dict(x.split(':') for x in A[p][2].split()); mb = dict(x.split(':') for x in B[p][2].split())
        d[p] = (A[p][1], B[p][1], {m: (ma[m], mb[m]) for m in ma})
    return d
K, R, O = kp(sys.argv[2]), kp(sys.argv[3]), own(sys.argv[4], sys.argv[5])
summ = {}
for p in K:
    stm = p.split()[-2]
    print(f"ROOT {p}: kp {K[p][0]}{K[p][1]}  kp39r {R[p][0]}{R[p][1]}  own39r {O[p][0]}{O[p][1]}")
    assert set(K[p][2]) == set(R[p][2]) == set(O[p][2]), "move sets differ"
    for m in sorted(K[p][2]):
        frm, to = m[1:3], m[3:5]
        shuttle = m[0] == 'K' and ((stm == 'w' and {frm, to} <= WS) or (stm == 'b' and {frm, to} <= BS))
        a, b = R[p][2][m]; oa, ob = O[p][2][m]
        agree = (a, b) == (oa, ob)
        if a == b:
            v = a
            mover_loses = (v == 'L') if stm == 'w' else (v == 'W')
            mover_wins = (v == 'W') if stm == 'w' else (v == 'L')
            verdict = 'loses' if mover_loses else 'wins' if mover_wins else 'draws'
        else:
            # mover cannot do better than its favourable bound
            fav = a if stm == 'w' else b
            verdict = 'loses' if (stm == 'w' and fav == 'L') or (stm == 'b' and fav == 'W') else 'open'
        tag = 'shuttle' if shuttle else 'dev'
        print(f"   {m:10s} {tag:7s} kp {''.join(K[p][2][m])}  kp39r {a}{b}  own39r {oa}{ob} {'agree' if agree else 'DIFFER'}  -> {verdict}")
        summ.setdefault((tag, verdict), []).append((p, m))
print("SUMMARY")
for k, v in sorted(summ.items()): print(" ", k, len(v))
