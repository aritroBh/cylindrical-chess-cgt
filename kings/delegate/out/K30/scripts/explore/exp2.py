import sys, collections
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]; model=sys.argv[2]; files=sys.argv[3]
B=Board(spec)
root=parse(B,'Ke6 Pd7 kd8 pe7 w -')
S=set('abcdefgh'.index(x) for x in files)
def flt(B,p,m):
    lab,k,np_=m
    if k=='p': return True
    return (np_[1]%B.W) in S
idx,pl,val,mv=solve(B,model,[root],wfilter=flt)
i0=idx[root]
start=[t for lab,k,t in mv[i0] if lab in('e6e5','e6d5','e6f5')]
seen=set(start); dq=collections.deque(start)
while dq:
    i=dq.popleft(); p=pl[i]
    for lab,k,t in mv[i]:
        if k=='p': continue
        if p[0]==0 and val[t]!='D': continue
        if t not in seen: seen.add(t); dq.append(t)
print(spec,model,files,'reachable',len(seen))
pos=collections.defaultdict(set)
for i in seen:
    p=pl[i]
    if p[0]==0 and not p[3] and p[4]:
        pos[B.r(p[4][0])+1].add(B.name(p[1]))
for r in sorted(pos): print('pawn rank',r,sorted(pos[r]))
