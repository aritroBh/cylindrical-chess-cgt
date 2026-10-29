import subprocess, collections, re
K = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
cfgs = {'cyl7x6_f3':('cyl:7x6','cyl',7,0,3),'cyl7x6_f4':('cyl:7x6','cyl',7,0,4),'cyl8x6_f3':('cyl:8x6','cyl',8,0,3),'cyl8x6_f4':('cyl:8x6','cyl',8,0,4),'flat7x6_f3_z0':('flat7x6','flat',7,0,3),'flat7x6_f3_z2':('flat7x6','flat',7,2,3),'flat7x6_f4_z0':('flat7x6','flat',7,0,4),'flat8x6_f3_z0':('flat8x6','flat',8,0,3),'flat8x6_f3_z2':('flat8x6','flat',8,2,3),'flat8x6_f4_z0':('flat8x6','flat',8,0,4)}
tot = collections.Counter(); mism = []
for name, (rb, kind, W, zs, fz) in cfgs.items():
    lines = [l.rstrip('\n') for l in open(K + 'data/M_%s.txt' % name)]
    pos = []; meta = []
    for l in lines:
        p = [x.strip() for x in l.split(' | ')]
        z, ctx, stm, pp, cl, det = p[:6]
        pos.append('%s %s %s -' % (z, ctx, stm)); meta.append((z, ctx, stm, cl, det))
    r = subprocess.run(['bin/ref3m', '--board', rb, '--moves'], input='\n'.join(pos) + '\n', capture_output=True, text=True)
    out = [l for l in r.stdout.splitlines() if ' | ' in l]
    assert len(out) == len(pos)
    def fdist(f):
        zf = range(zs, zs + fz)
        if kind == 'cyl': return min(min((f - z) % W, (z - f) % W) for z in zf)
        return min(abs(f - z) for z in zf)
    for o, (z, ctx, stm, cl, det) in zip(out, meta):
        toks = o.rsplit(' | ', 1)[1].split()
        res = toks[0]; mv = toks[1:]
        mover_loses_frozen = None
        if cl.startswith('A'):
            # side to move s; non-losing moves for s: value not 'L' (s=white) or not 'W' (s=black), White's view
            bad = 'L' if stm == 'w' else 'W'
            non = [m.split(':')[0] for m in mv if m.split(':')[1] != bad]
            cats = set()
            for m in non:
                if m[0] == 'K':
                    to = m[3:5]; f = 'abcdefgh'.index(to[0])
                    d = fdist(f)
                    cats.add('K>B' if d == 1 else ('K>Z' if d == 0 else 'K>other'))
                else: cats.add('Pz')   # pawn move (Z or context): grouped as in K29's tag Pz
            if not mv: cats = {'STALE'}
            mine = ','.join(sorted(cats, key=lambda x: ['K>B','K>Z','Pz','STALE','K>other'].index(x)))
            theirs = det
            tot['A'] += 1
            if mine != theirs: mism.append((name, z, ctx, stm, 'mine', mine, 'K29', theirs))
            else: tot['A same'] += 1
print(dict(tot)); print('mismatches', len(mism))
for m in mism[:12]: print(m)
