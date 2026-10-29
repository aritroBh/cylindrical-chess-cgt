#!/usr/bin/env python3
# wit.py CONFIG KPBOARD REFBOARD PARKW PARKB N SEED : own re-check of N random failing-class witnesses of CONFIG from data/table_all.tsv
# Phi: kp_p --pmodel and ref3 (Z+H, both sides to move); Psi: kpsolve --frozen and ref3 --frozen (parked kings + H).
import sys, random, subprocess
cfg, kb, rb, pw, pb, n, seed = sys.argv[1:8]; n = int(n)
K = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
B = K + 'verify/bin/'
rows = [l.rstrip('\n').split('\t') for l in open(K + 'data/table_all.tsv')]
fails = [r for r in rows if r[0] == cfg and r[5] == 'FAIL']
random.seed(int(seed)); samp = random.sample(fails, min(n, len(fails)))
def run(cmd, lines):
    r = subprocess.run(cmd, input='\n'.join(lines) + '\n', capture_output=True, text=True)
    return [l.rsplit(' | ', 1)[1].split()[0] for l in r.stdout.splitlines() if ' | ' in l]
phi_in, psi_in = [], []
for r in samp:
    z, ctx = r[1], r[6]
    for s in 'wb':
        phi_in.append('%s %s %s -' % (z, ctx, s)); psi_in.append('K%s k%s %s %s -' % (pw, pb, ctx, s))
pk = run([B + 'kpp', '--board', kb, '--pmodel', '--ep', 'on', '--promote', 'Q'], phi_in)
pr = run([B + 'ref3', '--board', rb], phi_in)
fk = run([B + 'kp', '--board', kb, '--frozen', '--ep', 'on', '--promote', 'Q'], psi_in)
fr = run([B + 'ref3', '--board', rb, '--frozen'], psi_in)
assert len(pk) == len(pr) == len(fk) == len(fr) == len(phi_in)
conf = 0
for i, r in enumerate(samp):
    a = (pk[2*i], pk[2*i+1]); b = (pr[2*i], pr[2*i+1]); c = (fk[2*i], fk[2*i+1]); d = (fr[2*i], fr[2*i+1])
    ok = a == b and c == d and a != c
    conf += ok
    print('%s | %s | ctx %s | Phi kpp %s ref3 %s | Psi kp %s ref3 %s | %s | K29 says %s' % (cfg, r[1], r[6], ''.join(a), ''.join(b), ''.join(c), ''.join(d), 'CONFIRMED' if ok else 'NOT CONFIRMED', r[7]))
print('SUMMARY %s: %d of %d sampled witnesses confirmed' % (cfg, conf, len(samp)))
