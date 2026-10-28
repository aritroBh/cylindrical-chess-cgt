#!/usr/bin/env python3
# NOTE: the e.p. generator ignores kings on the double-step origin / skipped square (3 of 16,500 samples were impossible positions, rejected by kpp). sweep.py has the fix.
# random certified-position sampler (referee's own). usage: gen.py kind:WxH npaw_max seed N outprefix [beta]
import sys, random
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/verify')
from cert import *
spec, pmax, seed, N, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
kind, wh = spec.split(':'); W, H = map(int, wh.split('x'))
b = B(kind, W, H); rnd = random.Random(seed)
allsq = [(f, r) for f in range(W) for r in range(H)]
pawnsq = [(f, r) for f in range(W) for r in range(1, H - 1)]
rows = []
tries = 0
fin = open(out + '.in', 'w'); fmeta = open(out + '.meta', 'w')
while len(rows) < N:
    tries += 1
    nw = rnd.randint(1, pmax); nb = rnd.randint(0, pmax)
    beta = rnd.randint(0, 1)
    if beta == 1: nw, nb = nb, nw
    if nw + nb == 0: continue
    ps = rnd.sample(pawnsq, nw + nb)
    wp = frozenset(ps[:nw]); bp = frozenset(ps[nw:])
    kk = rnd.sample(allsq, 2)
    stm = rnd.randint(0, 1)
    ep = None
    # optional e.p.
    if rnd.random() < 0.3:
        if stm == 1:
            for (f, r) in wp:
                if r == 3 and (f, 2) not in bp|wp and (f, 1) not in bp|wp and any((g, 3) in bp for g in b.adjfiles(f)): ep = (f, 2)
        else:
            for (f, r) in bp:
                if r == H - 4 and (f, H - 3) not in bp|wp and (f, H - 2) not in bp|wp and any((g, H - 4) in wp for g in b.adjfiles(f)): ep = (f, H - 3)
    pos = (kk[0], kk[1], wp, bp, stm, ep)
    if not legal_pos(b, pos): continue
    pawns = wp if beta == 0 else bp
    best = None
    for p in pawns:
        c = cert_static(b, pos, beta, p)
        if c is not None:
            ok, kind_ = ns_sim(b, pos, beta, p)
            h = h3k(b, pos, beta, c['e'])
            cand = (p, c['e'], c['d'], ok, kind_, h)
            if best is None or (ok and not best[3]) or (ok == best[3] and h and not best[5]): best = cand
    if best is None: continue
    rows.append(1)
    fin.write(fmt(pos) + '\n')
    fmeta.write('%d %s %d %d %d %s %d\n' % (beta, 'p%d_%d' % best[0], best[1], best[2], int(best[3]), best[4], int(best[5])))
fin.close(); fmeta.close()
print('tries', tries, 'accepted', len(rows))
