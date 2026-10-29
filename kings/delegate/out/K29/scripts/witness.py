#!/usr/bin/env python3
"""witness.py gen NAME ZS H   : read data/screen_NAME.txt ('R' lines of grp --mode test), write the witness positions
                                 data/wit_NAME.pos   (Z + first failing context, w and b, e.p. '-')   -> kpp, ref3  (P)
                                 data/wit_NAME.ppos  (parked kings + the same context, w and b)       -> kp, ref3 --frozen
   witness.py cmp NAME         : compare data/wit_NAME.{Pkp,Pref,Fkp,Fref}; one line per group.
Parking: White king on file ZS rank 1, Black king on file ZS rank H (a file of F_Z, rank 1 / rank H)."""
import sys, re
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/data/'
mode, name = sys.argv[1], sys.argv[2]
def rd(fn):
    out = []
    for l in open(fn):
        l = l.rstrip('\n')
        if not l or l.startswith('#'): continue
        pos, r = l.rsplit(' | ', 1)
        out.append((pos, r.replace(' ', '')[:2]))
    return out
if mode == 'gen':
    zs, H = int(sys.argv[3]), int(sys.argv[4])
    pk = 'K%s1 k%s%d' % (chr(97 + zs), chr(97 + zs), H)
    pos, ppos, idx = [], [], []
    for l in open(D + 'screen_%s.txt' % name):
        if not l.startswith('R '): continue
        m = re.match(r'R (.*?) \| contexts_checked (\d+) differ (\d+) parking_mismatch (\d+) \| first fail:(.*?) \| P=(\w\w) F=(\w\w)', l)
        if not m or int(m.group(3)) == 0: continue
        z, ctx = m.group(1), m.group(5).strip()
        for stm in 'wb':
            pos.append('%s %s %s -' % (z, ctx, stm)); ppos.append('%s %s %s -' % (pk, ctx, stm))
        idx.append((z, ctx, m.group(6), m.group(7)))
    open(D + 'wit_%s.pos' % name, 'w').write('\n'.join(pos) + '\n')
    open(D + 'wit_%s.ppos' % name, 'w').write('\n'.join(ppos) + '\n')
    print(len(idx), 'witnesses')
else:
    Pkp, Pref, Fkp, Fref = [rd(D + 'wit_%s.%s' % (name, s)) for s in ('Pkp', 'Pref', 'Fkp', 'Fref')]
    assert len(Pkp) == len(Pref) == len(Fkp) == len(Fref)
    nconf = ndis = 0
    for i in range(0, len(Pkp), 2):
        z = Pkp[i][0]
        a, b, c, d = [x[i][1] + x[i + 1][1] for x in (Pkp, Pref, Fkp, Fref)]
        solverdis = (a != b) or (c != d)
        conf = (a == b) and (c == d) and (a != c)
        nconf += conf; ndis += solverdis
        print('%s | Phi kp_p=%s ref3=%s | Psi kp=%s ref3=%s | %s' % (z[:-4], a, b, c, d, 'CONFIRMED (two solvers, Phi != Psi)' if conf else ('SOLVERS DISAGREE' if solverdis else 'NOT A FAILURE')))
    print('SUMMARY %s witnesses %d confirmed %d solver-disagreements %d' % (name, len(Pkp) // 2, nconf, ndis))
