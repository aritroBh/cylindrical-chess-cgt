"""exhaustive: s=White, one black Z-pawn, one white context pawn, all king squares; LC_T tight (mu==T+1 or mu>=T+2).  usage: enum1.py board FZ Tmax tag"""
import sys, json, time
from kb import B
from cert import Cert
kind, dims = sys.argv[1].split(':'); W, H = map(int, dims.split('x')); wrap = kind == 'cyl'
FZ = [int(x) for x in sys.argv[2].split(',')]; Tmax = int(sys.argv[3]); tag = sys.argv[4]
Bd = B(W, H, wrap); C = Cert(Bd, FZ)
zsq = [r * W + f for r in range(1, H - 1) for f in sorted(FZ)]
csq = [r * W + f for r in range(1, H - 1) for f in sorted(C.ctx)]
fzk = [r * W + f for r in range(H) for f in sorted(FZ)]
rows = []; t0 = time.time(); n = 0
for bp in zsq:
    for wp in csq:
        for bk in fzk:
            if bk == bp: continue
            for wk in range(Bd.N):
                if wk in (bp, wp, bk): continue
                pos = (wk, bk, frozenset([wp]), frozenset([bp]), 0, -1)
                if not Bd.legal_pos(pos): continue
                if wk in Bd.attacked_by_pawns([bp], 1): pass
                n += 1
                TP = C.minT(pos, Tmax)
                if TP is None: continue
                m1 = C.mu(pos, True)
                for T in range(TP, Tmax + 1):
                    if m1 >= T + 1:
                        h, fl = C.L3(pos, T)
                        if h:
                            rows.append(dict(Q=Bd.text(pos), T=T, TP=TP, mu=m1)); 
                if len(C.lmemo) > 2_000_000: C.lmemo.clear()
print(tag, "positions", n, "LC rows", len(rows), "tight", sum(1 for r in rows if r['mu'] == r['T'] + 1), "time", time.time() - t0)
json.dump(rows, open(f"enum1_{tag}.json", "w"))
