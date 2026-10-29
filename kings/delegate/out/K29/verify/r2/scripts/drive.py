#!/usr/bin/env python3
"""drive.py TAG BOARD FILES MW MB LO HI PARK0 PARK1 GROUPFILE [nokpp]
Referee-2 harness. BOARD like cyl:7x6 / flat:7x6 (ref3 gets flat7x6). GROUPFILE: one group per line ('Kb3 Pa2 ... pc3', optional ' | ...').
Phi(Z+H): kp_p --pmodel and ref3 (P).  Psi(H): kpsolve --frozen and ref3 --frozen, parked kings PARK0 (and PARK1 for neutrality), same contexts.
Prints one line per group: contexts, solver disagreements, #contexts with Phi!=Psi (kp_p side, ref3 side, either), first failing contexts."""
import sys, subprocess, os, re
R = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify/r2/'
tag, board, files, mw, mb, lo, hi, pk0, pk1, gf = sys.argv[1:11]
nokpp = len(sys.argv) > 11
if os.path.exists(R + 'data/cancel_' + tag): print('CANCELLED before start (referee: queued run dropped to save shared CPU)'); sys.exit(0)
mw, mb, lo, hi = int(mw), int(mb), int(lo), int(hi)
rb = 'flat' + board[5:] if board.startswith('flat') else board
def gen(z):
    return subprocess.run(['python3', R + 'scripts/ctx.py', z, files, str(mw), str(mb), str(lo), str(hi)], capture_output=True, text=True).stdout
def run(cmd, inp):
    return subprocess.run(['nice', '-n', '15'] + cmd, input=inp, capture_output=True, text=True).stdout
def rd(out):
    res = []
    for l in out.splitlines():
        if not l.strip() or l.startswith('#'): continue
        pos, r = l.rsplit(' | ', 1); res.append((pos, r.split()[0]))
    return res
def pairs(x): return [x[i][1] + x[i + 1][1] for i in range(0, len(x), 2)]
# Psi, two parkings
psi = {}
for nm, pk in (('p0', pk0), ('p1', pk1)):
    pos = gen(pk)
    k = rd(run([R + 'bin/kp', '--board', board, '--frozen', '--ep', 'on', '--promote', 'Q'], pos))
    r = rd(run([R + 'bin/ref3', '--board', rb, '--frozen'], pos))
    assert len(k) == len(r) == pos.count('\n'), (len(k), len(r))
    psi[nm] = (pairs(k), pairs(r))
ctxs = [l.rsplit(' ', 2)[0] for l in gen(pk0).splitlines()][::2]
pk_dis = sum(a != b for a, b in zip(*psi['p0'])) + sum(a != b for a, b in zip(*psi['p1']))
park_mis = sum(a != b for a, b in zip(psi['p0'][1], psi['p1'][1]))
print('PSI %s contexts %d | Psi solver disagreements (contexts, both parkings) %d | parking mismatch (ref3) %d | parking mismatch (kp) %d' % (tag, len(ctxs), pk_dis, park_mis, sum(a != b for a, b in zip(psi['p0'][0], psi['p1'][0]))), flush=True)
tot_fail_groups = 0
for l in open(gf):
    z = l.split('|')[0].strip()
    if not z: continue
    if os.path.exists(R + 'data/cancel_' + tag): print('CANCELLED'); break
    pos = gen(z)
    r = rd(run([R + 'bin/ref3', '--board', rb], pos)); rp = pairs(r)
    assert len(r) == pos.count('\n')
    if nokpp: kp_ = rp
    else:
        k = rd(run([R + 'bin/kpp', '--board', board, '--pmodel', '--ep', 'on', '--promote', 'Q'], pos)); assert len(k) == len(r); kp_ = pairs(k)
    dis = sum(a != b for a, b in zip(rp, kp_))
    fk = [i for i, (a, b) in enumerate(zip(kp_, psi['p0'][0])) if a != b]
    fr = [i for i, (a, b) in enumerate(zip(rp, psi['p0'][1])) if a != b]
    either = sorted(set(fk) | set(fr))
    tot_fail_groups += bool(either)
    print('GRP %s | %s | contexts %d | Phi solver disagreements %d | Phi!=Psi: kp %d ref3 %d either %d%s' % (tag, z, len(ctxs), dis, len(fk), len(fr), len(either), (' | first: ' + '; '.join('%s => Phi %s Psi %s' % (ctxs[i] or '-', rp[i], psi['p0'][1][i]) for i in either[:3])) if either else ''), flush=True)
