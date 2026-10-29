import sys, collections, pickle
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]
B=Board(spec)
E=4
sp,V=pickle.load(open('kpkT_%s.pkl'%spec.replace(':','_'),'rb'))
def T(rank):
    out=set()
    for d,offs in [(1,[0]),(2,[-1,0,1])]:
        rr=rank-d
        if 1<=rr<=B.H:
            for o in offs:
                f=E+o
                if B.cyl: f%=B.W
                elif not (0<=f<B.W): continue
                out.add((rr-1)*B.W+f)
    return out
def flt(B,p,m):
    lab,k,np_=m
    if k=='p': return True
    bp=np_[4]
    if not bp: return True
    rank=B.r(bp[0])+1
    return np_[1] in T(rank)
# full model from X
root=parse(B,'Ke6 Pd7 kd8 pe7 w -')
idx,pl,val,mv=solve(B,'P',[root],wfilter=flt)
i0=idx[root]
start=[t for lab,k,t in mv[i0] if lab in('e6e5','e6d5','e6f5')]
seen=set(start); dq=collections.deque(start)
while dq:
    i=dq.popleft(); p=pl[i]
    for lab,k,t in mv[i]:
        if k=='p': continue
        if p[0]==0 and val[t]!='D': continue
        if t not in seen: seen.add(t); dq.append(t)
print('reachable',len(seen))
tail=collections.defaultdict(lambda: collections.defaultdict(set))
for i in seen:
    p=pl[i]
    if p[0]==1 and not p[3] and p[4]:
        r=B.r(p[4][0])+1
        tail[r][B.name(p[1])].add(B.name(p[2]))
for r in (3,2):
    print('pawn rank',r)
    for w in sorted(tail[r]): print('  White K',w,'Black K',sorted(tail[r][w]))
