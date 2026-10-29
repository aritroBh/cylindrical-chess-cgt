#!/usr/bin/env python3
# ctxcheck.py KB RB PW PB "Z" CTXFILE : for each context line (pawn tokens, may be empty) compare Phi (kpp, ref3) with Psi (kp --frozen, ref3 --frozen), both sides to move.
import sys, subprocess
kb, rb, pw, pb, z, cf = sys.argv[1:7]
B = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify/bin/'
ctxs = [l.strip() for l in open(cf) if l.strip() != '#']
def run(cmd, lines):
    r = subprocess.run(cmd, input='\n'.join(lines) + '\n', capture_output=True, text=True)
    return [l.rsplit(' | ', 1)[1].split()[0] for l in r.stdout.splitlines() if ' | ' in l]
phi = [' '.join(z.split() + c.split() + [s, '-']) for c in ctxs for s in 'wb']
psi = [' '.join(['K' + pw, 'k' + pb] + c.split() + [s, '-']) for c in ctxs for s in 'wb']
pk = run([B + 'kpp', '--board', kb, '--pmodel', '--ep', 'on', '--promote', 'Q'], phi)
pr = run([B + 'ref3', '--board', rb], phi)
fk = run([B + 'kp', '--board', kb, '--frozen', '--ep', 'on', '--promote', 'Q'], psi)
fr = run([B + 'ref3', '--board', rb, '--frozen'], psi)
assert len(pk) == len(pr) == len(fk) == len(fr) == len(phi), (len(pk), len(pr), len(fk), len(fr), len(phi))
nd = 0; dis = 0
for i, c in enumerate(ctxs):
    a = pk[2*i] + pk[2*i+1]; b = pr[2*i] + pr[2*i+1]; f = fk[2*i] + fk[2*i+1]; g = fr[2*i] + fr[2*i+1]
    if a != b or f != g: dis += 1
    if a != f or b != g:
        nd += 1
        if nd <= 6: print('  FAIL ctx [%s]: Phi kpp %s ref3 %s | Psi kp %s ref3 %s' % (c, a, b, f, g))
print('Z=%s: %d contexts, solver disagreements %d, contexts with Phi != Psi (either pair) %d, X: %d' % (z, len(ctxs), dis, nd, (pk + pr + fk + fr).count('X')))
