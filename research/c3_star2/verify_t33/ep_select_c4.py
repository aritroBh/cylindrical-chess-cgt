from collections import deque
from mysolve import Solver, parse, name
F=4
W,B=parse("W: a4 b2 c2 / B: b6 c5 d6 d7")
s=Solver(F,"count",True,True)
seen={(W,B,(),"W")}; q=deque(seen); events={}
while q:
    w,b,ep,side=q.popleft(); opp="B" if side=="W" else "W"
    for (nw,nb,nep) in s.pawn_moves(w,b,ep,side):
        to=(b if side=="W" else w); tn=(nb if side=="W" else nw); mo=(w if side=="W" else b); mn=(nw if side=="W" else nb)
        if set(to)-set(tn):
            t=(set(mn)-set(mo)).pop(); f=(set(mo)-set(mn)).pop()
            if t not in to: events[(side,f,t)]=events.get((side,f,t),0)+1
        if s.verdict(nw,nb,nep,side) is not None: continue
        k=(nw,nb,nep,opp)
        if k not in seen: seen.add(k); q.append(k)
evs=sorted(events); print("states",len(seen),"e.p. capture types",len(evs))
def root(filt):
    sv=Solver(F,"count",True,True,filt); return sv.nim_of(W,B,(),6), sv.outcome_with(W,B,(),sv.zero())
print("all:",root(None)," none:",root(lambda *a:False))
need=[]
for e in evs:
    r=root(lambda sd,fr,to,e=e:(sd,fr,to)!=e)
    flag = "" if r[0]==2 else "   <-- needed (removing it destroys *2)"
    print("  disable",e[0],name(e[1])+"x"+name(e[2]),"->",r,flag)
    if r[0]!=2: need.append(e)
print("individually needed:",[(e[0],name(e[1])+"x"+name(e[2])) for e in need])
if need:
    print("only the needed ones:",root(lambda sd,fr,to:(sd,fr,to) in set(need)))
