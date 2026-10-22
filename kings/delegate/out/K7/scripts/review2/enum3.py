"""(Y,m,r) triples, s=White: Y has both kings on F_Z, one black Z-pawn, one white context pawn.  LC_T with queen clause; margin = mu - T.
saves post-m positions (black to move) for the C solver"""
import sys, json, time
from kb import B
from cert import Cert
kind, dims = sys.argv[1].split(':'); W, H = map(int, dims.split('x')); wrap = kind == 'cyl'
FZ = [int(x) for x in sys.argv[2].split(',')]; Tmax = int(sys.argv[3]); tag = sys.argv[4]
Bd = B(W, H, wrap); C = Cert(Bd, FZ)
zsq = [r * W + f for r in range(1, H - 1) for f in sorted(FZ)]
csq = [r * W + f for r in range(1, H - 1) for f in sorted(C.ctx)]
fzk = [r * W + f for r in range(H) for f in sorted(FZ)]
rows = []; n = 0
for bp in zsq:
  for wp in csq:
    for bk in fzk:
      for wk in fzk:
        if len({bp, wp, bk, wk}) < 4: continue
        Y = (wk, bk, frozenset([wp]), frozenset([bp]), 0, -1)
        if not Bd.legal_pos(Y): continue
        n += 1
        for kind_m, frm, to, promo, Qm in Bd.moves(Y):
            if promo or kind_m == 'P' and not C.inz(frm): continue
            for kind_r, frm2, to2, promo2, Q in Bd.moves(Qm):
                if promo2 or (kind_r == 'P' and not C.inz(frm2)) or (kind_r == 'K' and not C.inz(to2)): continue
                TP = C.minT(Q, Tmax, qs=True)
                if TP is None: continue
                m1 = C.mu(Q, True)
                for T in range(TP, Tmax + 1):
                    if m1 >= T + 1:
                        h, fl = C.L3(Q, T, qs=True)
                        if h:
                            rows.append(dict(Y=Bd.text(Y), m=Bd.name(frm) + Bd.name(to), r=Bd.name(frm2) + Bd.name(to2), Qm=Bd.text(Qm), Q=Bd.text(Q), T=T, mu=m1)); break
  if len(C.lmemo) > 2_000_000: C.lmemo.clear()
json.dump(rows, open(f"enum3_{tag}.json", "w"))
print(tag, "Y", n, "triples", len(rows), "tight", sum(1 for r in rows if r['mu'] == r['T'] + 1))
