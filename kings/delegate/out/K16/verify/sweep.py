#!/usr/bin/env python3
# Referee's exhaustive enumeration (beta = White). usage: enum.py kind:WxH nwmax nbmax out [bkfile0:1/0] [shard i n]
import sys, itertools, json
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/verify')
from cert import *
spec, nwmax, nbmax, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
bkfile0 = int(sys.argv[5]) if len(sys.argv) > 5 else 0
shard, nshard = (int(sys.argv[6]), int(sys.argv[7])) if len(sys.argv) > 7 else (0, 1)
kind, wh = spec.split(':'); W, H = map(int, wh.split('x'))
b = B(kind, W, H)
allsq = [(f, r) for f in range(W) for r in range(H)]
pawnsq = [(f, r) for f in range(W) for r in range(1, H - 1)]
bks = [(0, r) for r in range(H)] if bkfile0 else allsq
cnt = dict(cert=0, win=0, nsfail=0, ep=0, enumerated_cfg=0)
fcand = open(out + '.cand', 'w')   # certified but no p with NS ok -> to be solved
fsamp = open(out + '.samp', 'w')
import os
fall = open(out + '.all', 'w') if os.environ.get('DUMPALL') else None   # reservoir-ish: every 5000th NS-ok certified position
ci = 0
def eps_for(b, wp, bp, stm, kings=()):
    res = [None]
    if stm == 1:
        for (f, r) in wp:
            if r == 3 and (f, 2) not in bp|wp and (f, 1) not in bp|wp and (f, 2) not in kings and (f, 1) not in kings and any((g, 3) in bp for g in b.adjfiles(f)): res.append((f, 2))
    else:
        for (f, r) in bp:
            if r == H - 4 and (f, H - 3) not in bp|wp and (f, H - 2) not in bp|wp and (f, H - 3) not in kings and (f, H - 2) not in kings and any((g, H - 4) in wp for g in b.adjfiles(f)): res.append((f, H - 3))
    return res
cfgi = 0
for nw in range(1, nwmax + 1):
  for nbk in range(0, nbmax + 1):
    for wps in itertools.combinations(pawnsq, nw):
      wp = frozenset(wps)
      rest = [s for s in pawnsq if s not in wp]
      for bps in itertools.combinations(rest, nbk):
        cfgi += 1
        if cfgi % nshard != shard: continue
        bp = frozenset(bps)
        allp = wp | bp
        cnt['enumerated_cfg'] += 1
        for bk_ in bks:
            # H2 quick prefilter
            adj = b.adjfiles(bk_[0])
            if any(q[0] in adj for q in allp): continue
            if bk_ in allp: continue
            for ok_ in allsq:
                if ok_ == bk_ or ok_ in allp or b.dist(ok_, bk_) < 2: continue
                for stm in (0, 1):
                    # white = beta
                    for ep in eps_for(b, wp, bp, stm, (bk_, ok_)):
                        pos = (bk_, ok_, wp, bp, stm, ep)
                        if not legal_pos(b, pos): continue
                        certs = []
                        for p in wp:
                            c = cert_static(b, pos, 0, p)
                            if c is not None: certs.append((p, c))
                        if not certs: continue
                        cnt['cert'] += 1
                        if ep is not None: cnt['ep'] += 1
                        anyok = False
                        for p, c in certs:
                            ok, kd = ns_sim(b, pos, 0, p)
                            if ok: anyok = True; break
                        if anyok:
                            cnt['win'] += 1
                            ci += 1
                            if fall: fall.write(fmt(pos) + '\n')
                            if ci % 5000 == 0: fsamp.write(fmt(pos) + '\n')
                        else:
                            cnt['nsfail'] += 1
                            fcand.write(fmt(pos) + '\n')
json.dump(cnt, open(out + '.json', 'w'))
print(cnt)
