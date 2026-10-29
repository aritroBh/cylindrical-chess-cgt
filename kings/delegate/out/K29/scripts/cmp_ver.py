#!/usr/bin/env python3
"""cmp_ver.py TAG Z : compare the four result files of verify_one.sh.  Prints one summary line and the differing contexts."""
import sys, collections
tag, z = sys.argv[1], sys.argv[2]
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/data/ver_' + tag
def rd(fn, first=False):
    out = []
    for l in open(fn):
        l = l.rstrip('\n')
        if not l or l.startswith('#'): continue
        pos, r = l.rsplit(' | ', 1)
        out.append((pos, r.split()[0]))
    return out
Pkp, Pref, Fkp, Fref = rd(D + '.Pkp'), rd(D + '.Pref'), rd(D + '.Fkp'), rd(D + '.Fref')
n = len(Pkp)
assert len(Pref) == n and len(Fkp) == n and len(Fref) == n, (n, len(Pref), len(Fkp), len(Fref))
zn = len(z.split())
dis_P = sum(1 for a, b in zip(Pkp, Pref) if a[1] != b[1])
dis_F = sum(1 for a, b in zip(Fkp, Fref) if a[1] != b[1])
bad = []
for i in range(0, n, 2):  # w then b
    ctx = ' '.join(Pkp[i][0].split()[zn:-2])
    ph = Pkp[i][1] + Pkp[i + 1][1]; ps = Fkp[i][1] + Fkp[i + 1][1]
    phr = Pref[i][1] + Pref[i + 1][1]; psr = Fref[i][1] + Fref[i + 1][1]
    if ph != ps or phr != psr: bad.append((ctx, ph, ps, phr, psr))
print(f"VER {tag} | Z = {z} | positions {n} contexts {n // 2} | kp_p vs ref3 (P) differences {dis_P} | kp vs ref3 (frozen) differences {dis_F} | contexts with Phi != Psi: kp-family {sum(1 for b in bad if b[1] != b[2])}, ref3 {sum(1 for b in bad if b[3] != b[4])}")
for b in bad[:int(sys.argv[3]) if len(sys.argv) > 3 else 5]:
    print(f"   fail: {b[0]} | P kp={b[1]} ref3={b[3]} | frozen kp={b[2]} ref3={b[4]}")
