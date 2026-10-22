import sys, subprocess, collections
from hc import Geo, Cert
geo='flat:6x6'; W=H=6
g=Geo(6,6,False); C=Cert(g,[0,1,2])
rows=[]
for target_mu, ctxrank in ((2,2),(3,3)):
  for f in [0,1,2]:
    wpsq=(H-2)*W+f
    for cf in C.ctxfiles:
      bpsq=ctxrank*W+cf
      for wk in [r*W+x for r in range(H) for x in [0,1,2]]:
        for bk in range(g.N):
          Q=(wk,bk,frozenset([wpsq]),frozenset([bpsq]),1,-1)
          if not g.legal(Q): continue
          if C.L1_T(Q,True,1)!=1: continue
          if C.mu(Q,6,True)!=target_mu: continue
          if not C.L3(Q,1,True)[0]: continue
          rows.append((target_mu,Q))
inp="\n".join(g.text(q) for _,q in rows)+"\n"
Cr=subprocess.run(['./kpreal','--board',geo,'--ep','on','--cap','2'],input=inp,capture_output=True,text=True).stdout.splitlines()
def d(a,b): return max(abs(a%W-b%W),abs(a//W-b//W))
out=[]
for (mu,q),c in zip(rows,Cr):
    cv=c.split('|')[1].split()
    if cv==['D','D']:
        wk,bk=q[0],q[1]; wp=list(q[2])[0]; bp=list(q[3])[0]
        out.append((mu, d(wk,bp)+d(bk,wp), g.text(q)))
out.sort(key=lambda x:(x[0],-x[1]))
for mu in (2,3):
    print("mu",mu,[o[2] for o in out if o[0]==mu][:12])
