# referee: r(over + C) for a pawn-only context C on cyl:WxH (pawn moves only, e.p. on, a promotion is a terminal win; Definition 1.2/1.3)
import sys
from collections import deque
W,H=10,6
def sq(f,r): return (r,f%W)
def parse(s):
    wp=set(); bp=set()
    for t in s.split():
        f=ord(t[1])-97; r=int(t[2:])-1
        (wp if t[0]=='P' else bp).add((r,f))
    return (frozenset(wp),frozenset(bp),None)
def moves(p,c):  # returns list of (newpos or 'WIN')
    wp,bp,ep=p; own,opp=(wp,bp) if c==0 else (bp,wp); d=1 if c==0 else -1; last=H-1 if c==0 else 0; start=1 if c==0 else H-2
    occ=wp|bp; out=[]
    for (r,f) in own:
        r1=r+d
        def mk(to,cap=None,newep=None):
            o=set(own); o.discard((r,f)); x=set(opp)
            if cap: x.discard(cap)
            if to[0]==last: out.append('WIN'); return
            o.add(to); np=(frozenset(o),frozenset(x),newep) if c==0 else (frozenset(x),frozenset(o),newep); out.append(np)
        if (r1,f) not in occ:
            mk((r1,f))
            if r==start and (r1+d,f) not in occ: mk((r1+d,f),None,(r1,f))
        for df in (-1,1):
            t=(r1,(f+df)%W)
            if t in opp: mk(t,t)
            elif ep==t: mk(t,(r,(f+df)%W))
    return out
def solve(c0):
    # product with over: over node o in {0:'omega',1:'zero'}; state (p,o,side)
    start=(parse(c0),0)
    states=set(); Q=deque([start]); succ={}
    while Q:
        s=Q.popleft()
        if s in states: continue
        states.add(s); p,o=s
        for c in (0,1):
            L=[]
            for m in moves(p,c):
                if m=='WIN': L.append('WIN')
                else: L.append((m,o)); Q.append((m,o))
            # over: White omega->zero; Black omega->omega (pass). A move in over clears e.p.
            pc=(p[0],p[1],None)
            if o==0:
                if c==0: L.append((pc,1)); Q.append((pc,1))
                else: L.append((pc,0)); Q.append((pc,0))
            succ[(s,c)]=L
    val={}
    changed=True
    while changed:
        changed=False
        for (s,c),L in succ.items():
            if (s,c) in val: continue
            win='W' if c==0 else 'L'; lose='L' if c==0 else 'W'
            vs=[win if m=='WIN' else val.get((m,1-c)) for m in L]
            if win in vs: val[(s,c)]=win; changed=True
            elif all(v==lose for v in vs): val[(s,c)]=lose; changed=True
    return val.get((start,0),'D'), val.get((start,1),'D')
for c in sys.argv[1:]:
    print(c, 'over+C: w %s b %s'%solve(c))
