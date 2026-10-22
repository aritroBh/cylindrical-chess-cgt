import sys, subprocess, itertools
from hc import Geo, Cert
geo = sys.argv[1]; kind, wh = geo.split(':'); W,H = map(int, wh.split('x'))
g = Geo(W,H,kind=='cyl'); FZ=[0,1,2]; C=Cert(g,FZ)
# s = Black (stm 1), sbar = White.  White pawn on penultimate rank in F_Z, Black context pawn mu = 2.
rows=[]
for f in FZ:
  wpsq=(H-2)*W+f
  for cf in C.ctxfiles:
    bpsq=2*W+cf        # rank index 2 -> mu = 2 on any H (needs 2 moves: idx1, idx0)
    for wk in [r*W+x for r in range(H) for x in FZ]:
      for bk in range(g.N):
        Q=(wk,bk,frozenset([wpsq]),frozenset([bpsq]),1,-1)
        if not g.legal(Q): continue
        T=C.L1_T(Q,True,1)
        if T!=1: continue
        mu=C.mu(Q,5,True)
        if mu!=2: continue
        ok,an=C.L3(Q,1,True)
        if not ok: continue
        rows.append(Q)
print(len(rows),"LC_1 positions with mu=2")
inp="\n".join(g.text(q) for q in rows)+"\n"
P=subprocess.run(['./kpm','--board',geo,'--ep','on','--pmodel','--promote','Q'],input=inp,capture_output=True,text=True).stdout.splitlines()
Cr=subprocess.run(['./kpreal','--board',geo,'--ep','on','--cap','2'],input=inp,capture_output=True,text=True)
print(Cr.stderr[-300:])
Cr=Cr.stdout.splitlines()
import collections
cnt=collections.Counter()
ex=[]
for q,p,c in zip(rows,P,Cr):
    pv=p.split('|')[1].split(); cv=c.split('|')[1].split()
    cnt[(tuple(pv),tuple(cv))]+=1
    if cv!=['L','L'] and len(ex)<10: ex.append((g.text(q),pv,cv))
print(cnt)
for e in ex: print(e)
print("--- L / D examples")
nl=nd=0
for q,p,c in zip(rows,P,Cr):
    cv=c.split('|')[1].split()
    if cv==['L','L'] and nl<6: nl+=1; print("C=Black wins:",g.text(q))
    if cv==['D','D'] and nd<6: nd+=1; print("C=draw:",g.text(q))
