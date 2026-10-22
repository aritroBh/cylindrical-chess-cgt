from collections import deque
from mysolve import Solver, parse, name, sq
F=3
def mk(ep_on, aware=True):
    s=Solver(F,"count",ep_on,aware)
    z=s.zero(); m1=s.add_node([],[z]); m2=s.add_node([],[m1])
    s.negsw = s.add_node([m1],[m2])      # -{2|1} = {-1|-2}
    s.neg1star = s.add_node([m1],[m1])   # -(1*) = {-1|-1}
    s.neg_star_ = None
    return s,z
# position with e.p. marker: W a2 a3 c5 / B b5 c7, ep target b6 victim b5, W may capture
W,B=parse("W: a2 a3 c5 / B: b5 c7")
EPm=(((1,6),(1,5),"W"),)
s_on,z=mk(True)
print("ON  W a2 a3 c5/B b5 c7 (ep b6): equals {2|1}=3/2+-1/2 ?", s_on.outcome_with(W,B,EPm,s_on.negsw)=="P",
      "| equals 1* ?", s_on.outcome_with(W,B,EPm,s_on.neg1star)=="P")
s_off,z=mk(False)
print("OFF same pawns, no marker:   equals {2|1} ?", s_off.outcome_with(W,B,(),s_off.negsw)=="P",
      "| equals 1* ?", s_off.outcome_with(W,B,(),s_off.neg1star)=="P")
# a5xb6 position: W a2 a5 b2 / B b5 c5 c7 (ep b6)
W2,B2=parse("W: a2 a5 b2 / B: b5 c5 c7")
s1,z1=mk(True); s2,z2=mk(False)
print("a5xb6 position: on==0 ?", s1.outcome_with(W2,B2,EPm,z1)=="P", " off==0 ?", s2.outcome_with(W2,B2,(),z2)=="P")
# earliest depth of each e.p. capture event, my own BFS
W0,B0=parse("W: a2 a3 b2 / B: b7 c6 c7")
s=Solver(3,"count",True,True)
seen={(W0,B0,(),"W")}; fr=[(W0,B0,(),"W")]; first={}
for depth in range(0,8):
    nxt=[]
    for (w,b,ep,side) in fr:
        opp="B" if side=="W" else "W"
        for (nw,nb,nep) in s.pawn_moves(w,b,ep,side):
            to=(b if side=="W" else w); tn=(nb if side=="W" else nw)
            mo=(w if side=="W" else b); mn=(nw if side=="W" else nb)
            if set(to)-set(tn):
                t=(set(mn)-set(mo)).pop(); f=(set(mo)-set(mn)).pop()
                if t not in to:
                    first.setdefault((side,name(f)+"x"+name(t)),depth+1)
            if s.verdict(nw,nb,nep,side) is not None: continue
            k=(nw,nb,nep,opp)
            if k not in seen: seen.add(k); nxt.append(k)
    fr=nxt
print("earliest ply at which each e.p. capture can be played:", dict(sorted(first.items(), key=lambda x:x[1])))
