from collections import deque
from mysolve import Solver, parse, name
def bfs(F, start_text, target_text, maxdepth=30):
    s = Solver(F, "count", True, True)
    W0,B0 = parse(start_text); TW,TB = parse(target_text)
    tcount = len(TW)+len(TB)
    k0=(W0,B0,(),"W"); par={k0:None}; q=deque([(k0,0)]); hits=[]
    while q:
        k,d=q.popleft(); w,b,ep,side=k
        if (w,b)==(TW,TB): hits.append((k,d)); continue
        if d>=maxdepth: continue
        for nw,nb,nep in s.pawn_moves(w,b,ep,side):
            if any(r==8 for f,r in nw) or any(r==1 for f,r in nb): continue
            if len(nw)+len(nb)<tcount: continue
            nk=(nw,nb,nep,"B" if side=="W" else "W")
            if nk in par: continue
            par[nk]=(k,(side,w,b,nw,nb)); q.append((nk,d+1))
    return s,par,hits
def lab(side,w,b,nw,nb):
    mo,mn=((w,nw) if side=="W" else (b,nb)); to,tn=((b,nb) if side=="W" else (w,nw))
    f=(set(mo)-set(mn)).pop(); t=(set(mn)-set(mo)).pop()
    cap = len(set(to)-set(tn))>0
    return f"{side}:{name(f)}{'x' if cap else '-'}{name(t)}"
print("== C3 (3 files, 6 pawns): reach W a2 a3 b2 / B b7 c6 c7")
s,par,hits=bfs(3,"W: a2 b2 c2 / B: a7 b7 c7","W: a2 a3 b2 / B: b7 c6 c7")
print("  states",len(par),"hits",len(hits))
print("== C4: reach W a4 b2 c2 / B b6 c5 d6 d7")
s,par,hits=bfs(4,"W: a2 b2 c2 d2 / B: a7 b7 c7 d7","W: a4 b2 c2 / B: b6 c5 d6 d7")
print("  states",len(par),"hits",len(hits), "min depth", min(d for k,d in hits))
k,d=min(hits,key=lambda x:x[1]); path=[]
cur=k
while par[cur]: pk,info=par[cur]; path.append((pk,info)); cur=pk
path.reverse()
print("  shortest:", " ".join(lab(*i) for _,i in path))
# passed pawns along the history
for pk,(side,w,b,nw,nb) in path:
    pw=s.passed_pawns(nw,nb,pk[2],"W"); pb=s.passed_pawns(nw,nb,(),"B")
    print("   after",lab(side,w,b,nw,nb),"passed W:",pw,"B:",pb)
# explicit hand history, legality check
hist=[("W","d2","d4"),("B","b7","b6"),("W","d4","d5"),("B","c7","c5"),("W","d5","d6"),("B","a7","d6"),("W","a2","a4")]
W,B=parse("W: a2 b2 c2 d2 / B: a7 b7 c7 d7"); EP=(); S=Solver(4,"count",True,True)
from mysolve import sq
for side,f,t in hist:
    ok=False
    for nw,nb,nep in S.pawn_moves(W,B,EP,side):
        mo,mn=((W,nw) if side=="W" else (B,nb))
        if sq(f) in set(mo)-set(mn) and sq(t) in set(mn)-set(mo):
            W,B,EP=nw,nb,nep; ok=True; break
    print("  ",side,f,"->",t,"legal" if ok else "ILLEGAL")
print("  final:", W, B)
# all capture events on any <=9 ply history? Material argument:
print("material: start 8 pawns, target 7 -> exactly one capture on any history")
