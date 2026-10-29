# compare.py (K38): own P values (p5gen.solve) vs kp_p --pmodel and ref3 on every position reachable from P5.
import sys
b = sys.argv[1]
own = [l.rsplit('|', 1) for l in open('../logs/own_positions_%s.txt' % b)]
kpp = [l.rsplit('|', 1) for l in open('../logs/cmp_kpp_%s.txt' % b)]
ref = [l.rsplit('|', 1) for l in open('../logs/cmp_ref3_%s.txt' % b)]
d_k = d_r = 0; tally = {}
for (p, v), (p2, v2), (p3, v3) in zip(own, kpp, ref):
    assert p.strip() == p2.strip() == p3.strip()
    P = v.split()[0]; A, Bv = v2.split(); R = v3.split()[0]
    tally[P] = tally.get(P, 0) + 1
    if not (A == Bv == P): d_k += 1; print('kp_p differs', p, P, A, Bv)
    if R != P: d_r += 1; print('ref3 differs', p, P, R)
print(b, 'positions', len(own), 'own P tally', tally, 'differences: kp_p', d_k, 'ref3', d_r)
