import sys, random
sys.path.insert(0,'.')
import cert
from cert import *
spec, pmax, seed, N, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
kind, wh = spec.split(':'); W, H = map(int, wh.split('x'))
b = B(kind, W, H); rnd = random.Random(seed)
allsq = [(f, r) for f in range(W) for r in range(H)]
pawnsq = [(f, r) for f in range(W) for r in range(1, H - 1)]
n=0; tries=0
fin=open(out,'w')
while n < N:
    tries+=1
    nw = rnd.randint(1, pmax); nb = rnd.randint(1, pmax)
    ps = rnd.sample(pawnsq, nw + nb)
    wp = frozenset(ps[:nw]); bp = frozenset(ps[nw:])
    kk = rnd.sample(allsq, 2); stm = rnd.randint(0, 1)
    pos = (kk[0], kk[1], wp, bp, stm, None)
    if not legal_pos(b, pos): continue
    res = {}
    for kv in (False, True):
        cert.KV2 = kv
        res[kv] = [p for p in wp if cert_static(b, pos, 0, p) is not None]
    # certified under KV2 only, and strategy passes NS for the p (real play)
    for p in res[True]:
        if p not in res[False]:
            cert.KV2 = True
            if ns_sim(b, pos, 0, p)[0]:
                fin.write(fmt(pos) + '\n'); n += 1; break
print('tries', tries, 'n', n)
