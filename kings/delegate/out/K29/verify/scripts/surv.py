#!/usr/bin/env python3
# own survivor check (referee K29, pass 2): surv.py KPBOARD REFBOARD FILES PW PB "Z" ...
# Phi = P value (kp_p --pmodel, ref3) of Z+H, Psi = frozen value (kpsolve --frozen, ref3 --frozen) of H with kings parked on PW, PB.
import sys, subprocess, itertools, os
kb, rb, files, pw, pb = sys.argv[1:6]
Zs = sys.argv[6:]
B = os.path.dirname(os.path.abspath(__file__)) + '/../bin/'
sq = [f + str(r) for f in files for r in range(2, 6)]
def subs(k):
    for c in range(k + 1): yield from itertools.combinations(sq, c)
ctxs = []
for Wp in subs(2):
    for Bp in subs(2):
        if set(Wp) & set(Bp): continue
        ctxs.append((['P' + s for s in Wp] + ['p' + s for s in Bp]))
def run(cmd, lines):
    r = subprocess.run(cmd, input='\n'.join(lines) + '\n', capture_output=True, text=True)
    out = []
    for l in r.stdout.splitlines():
        if ' | ' in l: out.append(l.rsplit(' | ', 1)[1].split())
    return out
def pos(z, c, stm): return ' '.join(z.split() + c + [stm, '-'])
psi_in = [pos('K%s k%s' % (pw, pb), c, s) for c in ctxs for s in 'wb']
psi_kp = [x[0] + x[1] if len(x) > 1 else x[0] for x in run([B + 'kp', '--board', kb, '--frozen', '--ep', 'on', '--promote', 'Q'], psi_in)]
psi_r3 = [x[0] for x in run([B + 'ref3', '--board', rb, '--frozen'], psi_in)]
# kp prints "L L" for the two bounds; take the first token as one letter
psi_kp = [x[0] for x in run([B + 'kp', '--board', kb, '--frozen', '--ep', 'on', '--promote', 'Q'], psi_in)]
assert len(psi_kp) == len(psi_r3) == len(psi_in), (len(psi_kp), len(psi_r3), len(psi_in))
dpsi = sum(a != b for a, b in zip(psi_kp, psi_r3))
print('Psi: %d positions, kp vs ref3 disagreements %d, X count %d' % (len(psi_in), dpsi, psi_r3.count('X')))
for z in Zs:
    ins = [pos(z, c, s) for c in ctxs for s in 'wb']
    pk = [x[0] for x in run([B + 'kpp', '--board', kb, '--pmodel', '--ep', 'on', '--promote', 'Q'], ins)]
    pr = [x[0] for x in run([B + 'ref3', '--board', rb], ins)]
    assert len(pk) == len(pr) == len(ins), (z, len(pk), len(pr), len(ins))
    dP = sum(a != b for a, b in zip(pk, pr))
    bk = br = 0; fails = []
    for i in range(len(ctxs)):
        a = (pk[2*i], pk[2*i+1]); b = (pr[2*i], pr[2*i+1]); f = (psi_kp[2*i], psi_kp[2*i+1]); g = (psi_r3[2*i], psi_r3[2*i+1])
        if a != f: bk += 1
        if b != g: br += 1
        if (a != f or b != g) and len(fails) < 3: fails.append((' '.join(ctxs[i]), a, f, b, g))
    print('Z = %-32s contexts %d  P disagreements(kpp vs ref3) %d  Phi!=Psi: kp-family %d, ref3 %d  X in P: %d' % (z, len(ctxs), dP, bk, br, pr.count('X')))
    for f in fails: print('   fail', f)
