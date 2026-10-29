import sys, collections
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]; model=sys.argv[2]
B=Board(spec)
roots=[parse(B,'Ke6 Pd7 kd8 pe7 w -')]
index,plist,val,moves=solve(B,model,roots)
# reachable under "White plays any non-losing move after a sortie (Ke5,Kd5,Kf5); Black plays anything"
start=[]
i0=index[roots[0]]
for lab,k,t in moves[i0]:
    if lab in ('e6e5','e6d5','e6f5'):
        start.append(t)
seen=set(start); dq=collections.deque(start)
while dq:
    i=dq.popleft(); p=plist[i]
    for lab,k,t in moves[i]:
        if k=='p': continue
        if p[0]==0 and val[t]!='D': continue   # White only plays moves that keep D
        if t not in seen: seen.add(t); dq.append(t)
print(spec,model,'reachable positions:',len(seen))
c=collections.Counter()
for i in seen:
    p=plist[i]; c[(p[0],len(p[3]),len(p[4]))]+=1
print(c)
# classify White-king squares (White to move) by pawn rank, for positions without white pawn
pos=collections.defaultdict(set)
for i in seen:
    p=plist[i]
    if p[0]==0 and not p[3] and p[4]:
        pos[B.r(p[4][0])+1].add(B.name(p[1]))
for r in sorted(pos): print('pawn rank',r,sorted(pos[r]))
