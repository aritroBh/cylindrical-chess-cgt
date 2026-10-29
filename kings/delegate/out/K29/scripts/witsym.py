#!/usr/bin/env python3
"""witsym.py gen NAME BOARD ZS FZ RESULTS NSAMPLE SEED
   Take the first failing context of every class representative (RESULTS = merged R lines), and map it by the symmetries
   (colour swap with rank flip r -> H+1-r; file reflection f -> 2*zs+fz-1-f, cyl or symmetric flat) onto NSAMPLE randomly chosen
   non-representative members of the classes (data/classes_*.txt).  Writes
     data/wsym_NAME.pos   : member group + transformed context, both sides to move (P positions)
     data/wsym_NAME.ppos  : parked kings K<zs>1 k<zs><H> + transformed context, both sides to move (frozen positions)
   and data/wsym_NAME.idx (one line per member: member | context | which symmetry | expected Phi/Psi pair).
   witsym.py cmp NAME : compare data/wsym_NAME.{Pkp,Pref,Fkp,Fref}.  One line per member; a member is CONFIRMED if both
   P solvers give the same Phi, both frozen solvers the same Psi, and Phi != Psi."""
import sys, re, random
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/data/'
mode, name = sys.argv[1], sys.argv[2]
def rd(fn):
    out = []
    for l in open(fn):
        l = l.rstrip('\n')
        if not l or l.startswith('#'): continue
        pos, r = l.rsplit(' | ', 1)
        out.append((pos, r.split()[0]))
    return out
if mode == 'gen':
    board, zs, fz, res, ns, seed = sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6], int(sys.argv[7]), int(sys.argv[8])
    kind, dims = board.split(':'); W, H = map(int, dims.split('x')); cyl = kind == 'cyl'
    cf = sys.argv[9]
    def parse(z): return [(t[0], ord(t[1]) - 97, int(t[2:])) for t in z.split()]
    def fmt(p):
        key = {'K': 0, 'P': 1, 'k': 2, 'p': 3}
        return ' '.join('%s%s%d' % (c, chr(97 + f), r) for c, f, r in sorted(p, key=lambda x: (key[x[0]], x[1], x[2])))
    def colour(p): return [({'K': 'k', 'k': 'K', 'P': 'p', 'p': 'P'}[c], f, H + 1 - r) for c, f, r in p]
    def refl(p): return [(c, (2 * zs + fz - 1 - f) % W if cyl else 2 * zs + fz - 1 - f, r) for c, f, r in p]
    refl_ok = cyl or (2 * zs + fz - 1 == W - 1)
    tr = {'id': lambda p: p, 'colour': colour}
    if refl_ok: tr['refl'] = refl; tr['colour+refl'] = lambda p: refl(colour(p))
    fails = {}
    for l in open(res):
        m = re.match(r'R (.*?) \| contexts_checked (\d+) differ (\d+) parking_mismatch (\d+) \| first fail:(.*?) \| P=(\w\w) F=(\w\w)', l)
        if m and int(m.group(3)) > 0: fails[fmt(parse(m.group(1)))] = (m.group(5).strip(), m.group(6), m.group(7))
    members = []
    for l in open(cf):
        l = l.strip()
        if not l: continue
        rep, d, n, mem = l.split(' | ')
        for z in mem.split('; '):
            if fmt(parse(z)) != fmt(parse(rep)): members.append((fmt(parse(rep)), z))
    random.Random(seed).shuffle(members)
    pos, ppos, idx = [], [], []
    pk = 'K%s1 k%s%d' % (chr(97 + zs), chr(97 + zs), H)
    for rep, z in members:
        if rep not in fails or len(idx) >= ns: continue
        ctx, ph, ps = fails[rep]
        cp = parse(ctx.replace('  ', ' '))
        for tn, f in tr.items():
            if fmt(f(parse(rep))) == fmt(parse(z)):
                c2 = fmt(f(cp)) if cp else ''
                for stm in 'wb':
                    pos.append('%s %s %s -' % (z, c2, stm)); ppos.append('%s %s %s -' % (pk, c2, stm))
                idx.append('%s | %s | %s | rep %s | rep Phi=%s Psi=%s' % (z, c2, tn, rep, ph, ps)); break
    open(D + 'wsym_%s.pos' % name, 'w').write('\n'.join(pos) + '\n')
    open(D + 'wsym_%s.ppos' % name, 'w').write('\n'.join(ppos) + '\n')
    open(D + 'wsym_%s.idx' % name, 'w').write('\n'.join(idx) + '\n')
    print(name, len(idx), 'members of', len(members), 'non-rep members')
else:
    Pkp, Pref, Fkp, Fref = [rd(D + 'wsym_%s.%s' % (name, s)) for s in ('Pkp', 'Pref', 'Fkp', 'Fref')]
    idx = open(D + 'wsym_%s.idx' % name).read().split('\n')
    assert len(Pkp) == len(Pref) == len(Fkp) == len(Fref) == 2 * len([i for i in idx if i]), (len(Pkp), len(idx))
    nconf = 0; ndis = 0
    for i in range(0, len(Pkp), 2):
        a, b, c, d = [x[i][1] + x[i + 1][1] for x in (Pkp, Pref, Fkp, Fref)]
        dis = (a != b) or (c != d); conf = (not dis) and a != c
        nconf += conf; ndis += dis
        print('%s | Phi kp_p=%s ref3=%s | Psi kp=%s ref3=%s | %s' % (idx[i // 2], a, b, c, d, 'CONFIRMED' if conf else ('SOLVERS DISAGREE' if dis else 'NOT A FAILURE')))
    print('SUMMARY %s members %d confirmed %d solver-disagreements %d' % (name, len(Pkp) // 2, nconf, ndis))
