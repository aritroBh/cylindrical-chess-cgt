from collections import deque
from mysolve import Solver, parse, name
def lab(side,w,b,nw,nb):
    mo,mn=((w,nw) if side=="W" else (b,nb)); to,tn=((b,nb) if side=="W" else (w,nw))
    f=(set(mo)-set(mn)).pop(); t=(set(mn)-set(mo)).pop()
    cap = len(set(to)-set(tn))>0
    return f"{side}:{name(f)}{'x' if cap else '-'}{name(t)}", (cap and t not in to)
s=Solver(3,"count",True,True)
W0,B0=parse("W: a2 a3 b2 / B: b7 c6 c7")
k0=(W0,B0,(),"W"); par={k0:None}; q=deque([k0]); found={}
while q:
    k=q.popleft(); w,b,ep,side=k
    for nw,nb,nep in s.pawn_moves(w,b,ep,side):
        l,isep=lab(side,w,b,nw,nb)
        nk=(nw,nb,nep,"B" if side=="W" else "W")
        if isep and l not in found:
            path=[l]; cur=k
            while par[cur]: pk,pl=par[cur]; path.append(pl); cur=pk
            found[l]=list(reversed(path))
        if s.verdict(nw,nb,nep,side) is not None: continue
        if nk not in par: par[nk]=(k,l); q.append(nk)
for l,p in sorted(found.items(), key=lambda x: len(x[1])):
    print(len(p),"plies:"," ".join(p))
