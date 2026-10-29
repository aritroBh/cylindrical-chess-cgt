#!/usr/bin/env python3
# witsym_own.py CONFIG KB RB W ZS FZ MIRROR(0/1) SEED : own symmetric-member check: every failing class representative of CONFIG is mapped by a random symmetry
# (colour swap + rank flip, and/or file reflection of F_Z when MIRROR=1), witness context mapped the same way, and re-solved (two solver pairs).
import sys, random, subprocess
cfg, kb, rb, Wd, zs, fz, mir, seed = sys.argv[1:9]; Wd = int(Wd); zs = int(zs); fz = int(fz); mir = int(mir)
K = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'; B = K + 'verify/bin/'
rows = [l.rstrip('\n').split('\t') for l in open(K + 'data/table_all.tsv')]
fails = [r for r in rows if r[0] == cfg and r[5] == 'FAIL']
random.seed(int(seed))
def tok(t, swap, mirror):
    c, f, r = t[0], 'abcdefgh'.index(t[1]), int(t[2:])
    if swap: c = c.swapcase(); r = 7 - r
    if mirror: f = (2 * zs + fz - 1 - f) % Wd
    return c + 'abcdefgh'[f] + str(r)
def run(cmd, lines):
    r = subprocess.run(cmd, input='\n'.join(lines) + '\n', capture_output=True, text=True)
    return [l.rsplit(' | ', 1)[1].split()[0] for l in r.stdout.splitlines() if ' | ' in l]
phi, psi, meta = [], [], []
for r in fails:
    swap = random.random() < 0.5 or not mir
    mirror = bool(mir) and (random.random() < 0.5 or not swap)
    if not swap and not mirror: swap = True
    z = [tok(t, swap, mirror) for t in r[1].split()]; c = [tok(t, swap, mirror) for t in r[6].split()]
    for s in 'wb':
        phi.append(' '.join(z + c + [s, '-'])); psi.append(' '.join(['Ka1', 'ka6'] + c + [s, '-']))
    meta.append((r[1], r[6], swap, mirror))
pk = run([B + 'kpp', '--board', kb, '--pmodel', '--ep', 'on', '--promote', 'Q'], phi); pr = run([B + 'ref3', '--board', rb], phi)
fk = run([B + 'kp', '--board', kb, '--frozen', '--ep', 'on', '--promote', 'Q'], psi); fr = run([B + 'ref3', '--board', rb, '--frozen'], psi)
ok = 0
for i, m in enumerate(meta):
    a = pk[2*i] + pk[2*i+1]; b = pr[2*i] + pr[2*i+1]; c = fk[2*i] + fk[2*i+1]; d = fr[2*i] + fr[2*i+1]
    good = a == b and c == d and a != c and 'X' not in a + c
    ok += good
    if not good: print('NOT CONFIRMED', m, a, b, c, d)
print('SYM %s: %d of %d symmetric images of witnesses confirmed' % (cfg, ok, len(meta)))
