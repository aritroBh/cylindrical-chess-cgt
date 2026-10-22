import sys, time
from collections import deque
from mysolve import Solver, parse, name
PY=sys.argv[1] if len(sys.argv)>1 else "aware"
aware = (PY=="aware")
F=3
W,B=parse("W: a2 a3 b2 / B: b7 c6 c7")
s=Solver(F,"count",True,aware)
# enumerate all reachable states (stop at decided) and collect e.p. capture events
seen={(W,B,(),"W")}; q=deque(seen); events={}
while q:
    w,b,ep,side=q.popleft()
    opp="B" if side=="W" else "W"
    # find ep captures: moves where a marker with cap==side is consumed
    mine=(w if side=="W" else b)
    for (nw,nb,nep) in s.pawn_moves(w,b,ep,side):
        # detect e.p.: some victim pawn removed that is not on the target square of the mover
        theirs_old=(b if side=="W" else w); theirs_new=(nb if side=="W" else nw)
        mine_old=mine; mine_new=(nw if side=="W" else nb)
        lost=set(theirs_old)-set(theirs_new)
        if lost:
            moved_to=(set(mine_new)-set(mine_old)).pop(); moved_from=(set(mine_old)-set(mine_new)).pop()
            if moved_to not in theirs_old:  # landed on empty square => e.p.
                events[(side,moved_from,moved_to)]=events.get((side,moved_from,moved_to),0)+1
        vd=s.verdict(nw,nb,nep,side)
        if vd is not None: continue
        key=(nw,nb,nep,opp)
        if key not in seen:
            seen.add(key); q.append(key)
print("reachable states",len(seen))
evs=sorted(events)
print("e.p. capture events in tree (%s test):"%PY)
for e in evs: print("  ",e[0],name(e[1]),"x",name(e[2]),"  (occurrences",events[e],")")
def root(filt, ep_on=True):
    sv=Solver(F,"count",ep_on,aware,filt)
    return sv.nim_of(W,B,(),6), sv.outcome_with(W,B,(),sv.zero())
print("all e.p. allowed  :",root(None))
print("none allowed (filter False):",root(lambda *a: False))
print("-- disable exactly one event")
for e in evs:
    r=root(lambda sd,fr,to,e=e: (sd,fr,to)!=e)
    print("  disable",e[0],name(e[1])+"x"+name(e[2]),"->",r)
print("-- allow exactly one event")
for e in evs:
    r=root(lambda sd,fr,to,e=e: (sd,fr,to)==e)
    print("  only   ",e[0],name(e[1])+"x"+name(e[2]),"->",r)
