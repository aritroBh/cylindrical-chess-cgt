import sys, subprocess, itertools, collections
from hc import Geo, Cert
geo = sys.argv[1]; kind, wh = geo.split(':'); W,H = map(int, wh.split('x'))
FZ=[int(x) for x in sys.argv[2].split(',')]; target_mu=int(sys.argv[3]); ctxrank=int(sys.argv[4]); maxrows=int(sys.argv[5])
g = Geo(W,H,kind=='cyl'); C=Cert(g,FZ)
rows=[]
for f in FZ:
  wpsq=(H-2)*W+f
  for cf in C.ctxfiles:
    bpsq=ctxrank*W+cf
    for wk in [r*W+x for r in range(H) for x in FZ]:
      for bk in range(g.N):
        Q=(wk,bk,frozenset([wpsq]),frozenset([bpsq]),1,-1)
        if not g.legal(Q): continue
        if C.L1_T(Q,True,1)!=1: continue
        if C.mu(Q,6,True)!=target_mu: continue
        if not C.L3(Q,1,True)[0]: continue
        rows.append(Q)
import random
random.seed(5)
random.shuffle(rows); rows=rows[:maxrows]
print(len(rows),"LC_1 (queen clause) positions with mu=",target_mu)
inp="\n".join(g.text(q) for q in rows)+"\n"
P=subprocess.run(['./kpm','--board',geo,'--ep','on','--pmodel','--promote','Q'],input=inp,capture_output=True,text=True).stdout.splitlines()
Cr=subprocess.run(['./kpreal','--board',geo,'--ep','on','--cap','2'],input=inp,capture_output=True,text=True)
print(Cr.stderr[-300:])
Cr=Cr.stdout.splitlines()
cnt=collections.Counter()
for q,p,c in zip(rows,P,Cr):
    pv=p.split('|')[1].split(); cv=c.split('|')[1].split()
    cnt[(tuple(pv),tuple(cv))]+=1
print(cnt)
for tag,key in (("draw",['D','D']),("Black wins",['L','L'])):
    k=0
    for q,c in zip(rows,Cr):
        if c.split('|')[1].split()==key and k<5: k+=1; print("C",tag,g.text(q))
