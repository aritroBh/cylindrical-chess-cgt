#!/usr/bin/env python3
"""wsample.py gen SEED PER : sample PER failing classes per configuration from K29 data/table_all.tsv; write data/ws_<board>.{pos,ppos,ppos1,meta}
   (position files for kp_p/ref3 (Phi) and kp/ref3 --frozen (Psi, parking 0 and parking 1)); half of the samples are mapped to a NON-representative class member
   by my own symmetry code (colour swap + rank flip, and/or reflection of the file axis about the centre of F_Z) and then solved directly.
   wsample.py cmp : read the solver outputs data/ws_<board>.{Pkp,Pref,Fkp,Fref,Fref1} and print one verdict line per sample."""
import sys, random, csv, os, glob
R = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
V = R + 'verify/r2/data/'
cfg = {}
for l in open(R + 'scripts/configs.txt'):
    if l.startswith('#') or not l.strip(): continue
    n, b, zs, fz, dmin, suf = l.split(); cfg[n] = (b, int(zs), int(fz))
def parse(s):
    return [(t[0], ord(t[1]) - 97, int(t[2:])) for t in s.split()]
def fmt(toks): return ' '.join('%s%s%d' % (c, chr(97 + f), r) for c, f, r in toks)
def swap(toks, H): return [(c.swapcase(), f, H + 1 - r) for c, f, r in toks]
def refl(toks, W, cyl, zs, fz):
    out = []
    for c, f, r in toks:
        g = (2 * zs + fz - 1 - f)
        g = g % W if cyl else g
        assert 0 <= g < W
        out.append((c, g, r))
    return out
flip = {'W': 'L', 'L': 'W', 'D': 'D'}
if sys.argv[1] == 'gen':
    seed, per = int(sys.argv[2]), int(sys.argv[3]); random.seed(seed)
    rows = [r for r in csv.reader(open(R + 'data/table_all.tsv'), delimiter='\t')][1:]
    byc = {}
    for r in rows:
        if r[5] == 'FAIL': byc.setdefault(r[0], []).append(r)
    files = {}
    for c, rs in sorted(byc.items()):
        b, zs, fz = cfg[c]; W, H = [int(x) for x in b.split(':')[1].split('x')]; cyl = b.startswith('cyl')
        for r in random.sample(rs, min(per, len(rs))):
            z, ctx = r[1], r[6]
            mode = random.choice(['rep', 'swap', 'refl', 'both'])
            toks = parse(z) + parse(ctx); stmmap = False
            if mode in ('swap', 'both'): toks = swap(toks, H); stmmap = True
            if mode in ('refl', 'both'):
                if cyl or (zs == 2 and W == 7): toks = refl(toks, W, cyl, zs, fz)
                else: mode = 'swap' if stmmap else 'rep'
            zlen = len(parse(z))
            zz, cc = fmt(toks[:zlen]), fmt(toks[zlen:])
            pk0 = 'K%s1 k%s%d' % (chr(97 + zs), chr(97 + zs), H); pk1 = 'K%s1 k%s%d' % (chr(97 + zs + 1), chr(97 + zs + fz - 1), H)
            fn = b.replace(':', '')
            f = files.setdefault(fn, ([], [], [], [], b))
            for stm in 'wb':
                f[0].append('%s %s %s -' % (zz, cc, stm)); f[1].append('%s %s %s -' % (pk0, cc, stm)); f[2].append('%s %s %s -' % (pk1, cc, stm))
            f[3].append('%s|%s|%s|%s|%s|%s' % (c, mode, z, ctx, r[7], zz + ' + ' + cc))
    for fn, (p, pp, pp1, meta, b) in files.items():
        open(V + 'ws_%s.pos' % fn, 'w').write('\n'.join(p) + '\n'); open(V + 'ws_%s.ppos' % fn, 'w').write('\n'.join(pp) + '\n')
        open(V + 'ws_%s.ppos1' % fn, 'w').write('\n'.join(pp1) + '\n'); open(V + 'ws_%s.meta' % fn, 'w').write('\n'.join(meta) + '\n'); open(V + 'ws_%s.board' % fn, 'w').write(b)
    print({fn: len(v[3]) for fn, v in files.items()})
else:
    def rd(fn):
        o = []
        for l in open(fn):
            l = l.rstrip('\n')
            if not l or l.startswith('#'): continue
            pos, r = l.rsplit(' | ', 1); o.append(r.split()[0])
        return o
    tot = conf = dis = 0
    for mf in sorted(glob.glob(V + 'ws_*.meta')):
        fn = mf[len(V) + 3:-5]
        a, b, c, d, e = [rd(V + 'ws_%s.%s' % (fn, s)) for s in ('Pkp', 'Pref', 'Fkp', 'Fref', 'Fref1')]
        meta = open(mf).read().splitlines()
        for i, m in enumerate(meta):
            cfgn, mode, z, ctx, claim, mapped = m.split('|')
            pk, pr, fk, fr, fr1 = [x[2 * i] + x[2 * i + 1] for x in (a, b, c, d, e)]
            ok = pk == pr and fk == fr and pk != fk and fr == fr1
            # for mapped members compare with the transform of K29's rep claim
            cl = claim.replace('P=', '').replace(' F=', ' ').split()
            repP, repF = cl[0], cl[1]
            if mode in ('swap', 'both'):
                repP = flip[repP[1]] + flip[repP[0]]; repF = flip[repF[1]] + flip[repF[0]]
            match = (pr == repP and fr == repF)
            tot += 1; conf += ok and match; dis += (pk != pr or fk != fr)
            print('%-14s %-5s %s | Phi kp_p=%s ref3=%s | Psi kp=%s ref3=%s park1=%s | %s%s' % (cfgn, mode, mapped, pk, pr, fk, fr, fr1, 'CONFIRMED' if ok else 'NOT CONFIRMED', '' if match else ' (differs from K29 rep pair %s/%s)' % (repP, repF)))
    print('SUMMARY samples %d confirmed(and equal to the K29 pair, mapped) %d solver disagreements %d' % (tot, conf, dis))
