import sys, subprocess, collections
from hc import Geo, Cert
geo=sys.argv[1]; kind,wh=geo.split(':'); W,H=map(int,wh.split('x'))
g=Geo(W,H,kind=='cyl'); FZ=[0,1,2]; C=Cert(g,FZ)
rows=[]
for f in FZ:
  wpsq=(H-2)*W+f
  for wk in [r*W+x for r in range(H) for x in FZ]:
    for bk in range(g.N):
      Q=(wk,bk,frozenset([wpsq]),frozenset(),1,-1)
      if not g.legal(Q): continue
      if C.L1_T(Q,True,1)!=1: continue
      if C.mu(Q,9,True)<=9-1+0 and False: pass
      if not C.L3(Q,1,True)[0]: continue
      rows.append(Q)
inp="\n".join(g.text(q) for q in rows)+"\n"
P=subprocess.run(['./kpm','--board',geo,'--ep','on','--pmodel','--promote','Q'],input=inp,capture_output=True,text=True).stdout.splitlines()
Cr=subprocess.run(['./kpreal','--board',geo,'--ep','on','--cap','1'],input=inp,capture_output=True,text=True).stdout.splitlines()
cnt=collections.Counter(); ex=[]
for q,p,c in zip(rows,P,Cr):
    pv=tuple(p.split('|')[1].split()); cv=tuple(c.split('|')[1].split())
    cnt[(pv,cv)]+=1
    if cv!=('W','W') and len(ex)<8: ex.append(g.text(q))
print(len(rows),cnt); print(ex)
