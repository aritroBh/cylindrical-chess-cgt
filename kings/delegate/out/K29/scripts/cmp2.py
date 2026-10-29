#!/usr/bin/env python3
"""cmp2.py TAG KEY Z: compare data/ver_KEY.{kpp,ref3} (Phi, both solvers) with data/psi_TAG.{kp,ref3} (Psi, both solvers).
One summary line plus the first failing contexts (at most 8)."""
import sys
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/data/'
tag, key, z = sys.argv[1:4]
def rd(fn):
    out = []
    for l in open(fn):
        l = l.rstrip('\n')
        if not l or l.startswith('#'): continue
        pos, r = l.rsplit(' | ', 1)
        out.append((pos, r.split()[0]))
    return out
Pk, Pr = rd(D + 'ver_%s.kpp' % key), rd(D + 'ver_%s.ref3' % key)
Fk, Fr = rd(D + 'psi_%s.kp' % tag), rd(D + 'psi_%s.ref3' % tag)
n = len(Pk)
assert n == len(Pr) == len(Fk) == len(Fr), (n, len(Pr), len(Fk), len(Fr))
zn = len(z.split())
dP = sum(a[1] != b[1] for a, b in zip(Pk, Pr)); dF = sum(a[1] != b[1] for a, b in zip(Fk, Fr))
bad_k = bad_r = bad_any = ill = 0; fails = []
for i in range(0, n, 2):
    ctx = ' '.join(Pk[i][0].split()[zn:-2]); cf = ' '.join(Fk[i][0].split()[2:-2])
    assert ctx == cf, (ctx, cf)
    pk = Pk[i][1] + Pk[i + 1][1]; pr = Pr[i][1] + Pr[i + 1][1]; fk = Fk[i][1] + Fk[i + 1][1]; fr = Fr[i][1] + Fr[i + 1][1]
    bk, br = pk != fk, pr != fr
    bad_k += bk; bad_r += br
    if bk or br:
        bad_any += 1
        if len(fails) < 8: fails.append('   fail: %s | Phi kp_p=%s ref3=%s | Psi kp=%s ref3=%s' % (ctx or '(empty)', pk, pr, fk, fr))
print('VER %s | Z = %s | contexts %d | solver disagreements: Phi %d, Psi %d (positions) | contexts with Phi != Psi: kp-family %d, ref3 %d, either %d' % (key, z, n // 2, dP, dF, bad_k, bad_r, bad_any))
for f in fails: print(f)
