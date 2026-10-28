import sys, json
from k17lib import *
from check2 import parse_ctx
spec="cyl:6x6"; b=board_of(spec); p=parse_ctx("W: d2 e3 / B: e5")
Zx=dict(wk="b6",bk="b3",wz=["a2"],bz=["a3"],FZ={0,1}); Zt=dict(Zx,bk="b2")
rcB=reach(b,p,"B"); rcW=reach(b,p,"W")
qX=chess_str(p,"B",Zx)
qT=sorted(set(all_queries(b,p,"B",Zt,rcB))|set(all_queries(b,p,"W",Zt,rcW)))
res,err=run_kp(KPP,spec,[qX]+qT,flags=("--pmodel","--moves"))
print(err.strip())
okX,nX=verify(b,spec,p,"B",Zx,res,rc={(p,"B"):rcB[(p,"B")]},model="real")
print("X",qX,res[qX],okX)
for s,rc in (("W",rcW),("B",rcB)):
    ok,notes=verify(b,spec,p,s,Zt,res,rc=rc,model="real")
    print("twin",s,len(rc),chess_str(p,s,Zt),res[chess_str(p,s,Zt)][:2],ok,notes[:2], "D_whole",D_whole(b,p))
print("D_fix",D_fix(b,p),"D_S",D_S(b,p),"HSS",v4_hss_exact(b,p,"B"),v4_strong(b,p))
