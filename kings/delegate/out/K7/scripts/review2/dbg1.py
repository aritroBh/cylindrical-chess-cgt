from kb import B
from cert import Cert
Bd=B(7,6,True); C=Cert(Bd,[0,1,2])
Q=Bd.parse("Kg4 ka1 Pa2 Pf3 Pc4 pb2 pf4 pe5 w -")
print(C.minT(Q,6), C.mu(Q), C.mu(Q,False))
sb=1
# search for spromo path
def rg(pos,t,path):
    mv=Bd.moves(pos)
    for kind,frm,to,promo,nxt in mv:
        if promo:
            print("S PROMO at", Bd.text(pos), "t",t, "path", path, Bd.name(frm),Bd.name(to)); return True
        if rf(nxt,t,path+[Bd.text(pos)+" -> "+Bd.name(frm)+Bd.name(to)]): return True
    return False
def rf(pos,t,path):
    for kind,frm,to,promo,nxt in Bd.moves(pos):
        if kind=='K' and not C.inz(to): continue
        if promo: continue
        pj=C.proj(nxt)
        if Bd.check(pj,0) and not Bd.moves(pj): continue
        if t>=2 and C.lg(pj,t-1,sb,False):
            if rg(nxt,t-1,path+["  sb: "+Bd.name(frm)+Bd.name(to)]): return True
    return False
rg(Q,4,[])
