"""like enum1 but with the queen clause (qs=True) in L1/L3 ; reports margin = mu - T for the least T with LC; saves rows"""
import sys, json, time
from kb import B
from cert import Cert
kind, dims = sys.argv[1].split(':'); W, H = map(int, dims.split('x')); wrap = kind == 'cyl'
FZ = [int(x) for x in sys.argv[2].split(',')]; Tmax = int(sys.argv[3]); tag = sys.argv[4]
Bd = B(W, H, wrap); C = Cert(Bd, FZ)
zsq = [r * W + f for r in range(1, H - 1) for f in sorted(FZ)]
csq = [r * W + f for r in range(1, H - 1) for f in sorted(C.ctx)]
fzk = [r * W + f for r in range(H) for f in sorted(FZ)]
rows = []; n = 0; t0 = time.time()
for bp in zsq:
    for wp in csq:
        for bk in fzk:
            if bk == bp: continue
            for wk in range(Bd.N):
                if wk in (bp, wp, bk): continue
                pos = (wk, bk, frozenset([wp]), frozenset([bp]), 0, -1)
                if not Bd.legal_pos(pos): continue
                n += 1
                TP = C.minT(pos, Tmax, qs=True)
                if TP is None: continue
                m1 = C.mu(pos, True)
                for T in range(TP, Tmax + 1):
                    if m1 >= T + 1:
                        h, fl = C.L3(pos, T, qs=True)
                        if h:
                            rows.append(dict(Q=Bd.text(pos), T=T, TP=TP, mu=m1)); break
                if len(C.lmemo) > 2_000_000: C.lmemo.clear()
json.dump(rows, open(f"enum2_{tag}.json", "w"))
print(tag, n, len(rows), time.time() - t0)
