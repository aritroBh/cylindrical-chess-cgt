#!/usr/bin/env python3
"""drive_ctx.py TAG BOARD CTXFILE PARK0 GROUPFILE CHUNK [kpp] : like drive.py for an explicit context list (one context per line, tokens), in chunks (one solver process per chunk).
Phi: ref3 (and kp_p if 'kpp'); Psi: ref3 --frozen with parked kings PARK0 (and kp --frozen if 'kpp').  Prints per group and chunk the contexts with Phi != Psi."""
import sys, subprocess
R = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify/r2/'
tag, board, cf, pk0, gf, chunk = sys.argv[1:7]; chunk = int(chunk); usekpp = len(sys.argv) > 7
rb = 'flat' + board[5:] if board.startswith('flat') else board
def run(cmd, inp): return subprocess.run(['nice', '-n', '15'] + cmd, input=inp, capture_output=True, text=True).stdout
def rd(out):
    res = []
    for l in out.splitlines():
        if not l.strip() or l.startswith('#'): continue
        pos, r = l.rsplit(' | ', 1); res.append(r.split()[0])
    return res
def pairs(x): return [x[i] + x[i + 1] for i in range(0, len(x), 2)]
ctxs = [l.strip() for l in open(cf)]
groups = [l.split('|')[0].strip() for l in open(gf) if l.strip()]
for z in groups:
    nfail = ndis = 0; n = 0
    for i in range(0, len(ctxs), chunk):
        cs = ctxs[i:i + chunk]
        posP = ''.join('%s %s %s -\n' % (z, c, s) for c in cs for s in 'wb')
        posF = ''.join('%s %s %s -\n' % (pk0, c, s) for c in cs for s in 'wb')
        P = pairs(rd(run([R + 'bin/ref3', '--board', rb], posP))); F = pairs(rd(run([R + 'bin/ref3', '--board', rb, '--frozen'], posF)))
        assert len(P) == len(F) == len(cs), (len(P), len(F), len(cs))
        if usekpp:
            Pk = pairs(rd(run([R + 'bin/kpp', '--board', board, '--pmodel', '--ep', 'on', '--promote', 'Q'], posP)))
            Fk = pairs(rd(run([R + 'bin/kp', '--board', board, '--frozen', '--ep', 'on', '--promote', 'Q'], posF)))
            ndis += sum(a != b for a, b in zip(P, Pk)) + sum(a != b for a, b in zip(F, Fk))
        for c, p, f in zip(cs, P, F):
            n += 1
            if p != f:
                nfail += 1; print('FAIL %s | %s | ctx %s | Phi %s Psi %s' % (tag, z, c, p, f), flush=True)
        print('CHUNK %s | %s | contexts %d..%d done | fails so far %d | solver disagreements so far %d' % (tag, z, i, i + len(cs), nfail, ndis), flush=True)
    print('GROUP %s | %s | contexts %d | Phi!=Psi %d | kp-vs-ref3 disagreements %d' % (tag, z, n, nfail, ndis), flush=True)
