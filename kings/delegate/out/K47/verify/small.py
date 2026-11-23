# referee: r(G + T) for small D-games G, T (normal play, Definition 1.2; no terminals), by retrograde with counters.
import sys, itertools
from collections import deque
def readT(fn):
    out=[]
    for line in open(fn):
        if not line.strip() or line[0]=='#': continue
        name,n,rest=[x.strip() for x in line.split('|',2)]; n=int(n); L=[[] for _ in range(n)]; R=[[] for _ in range(n)]
        for part in rest.split(';'):
            part=part.strip(); i=int(part.split(':')[0]); l=part.split('L=')[1].split()[0] if 'L= ' not in part and not part.split('L=')[1].startswith(' ') else ''
            r=part.split('R=')[1].strip()
            L[i]=[int(x) for x in l.split(',') if x!=''] if l else []; R[i]=[int(x) for x in r.split(',') if x!=''] if r else []
        out.append((name,(L,R)))
    return out
def summ(*gs):
    sizes=[len(g[0]) for g in gs]; states=list(itertools.product(*[range(s) for s in sizes])); idx={s:i for i,s in enumerate(states)}
    L=[[] for _ in states]; R=[[] for _ in states]
    for s in states:
        for k,g in enumerate(gs):
            for x in g[0][s[k]]: L[idx[s]].append(idx[s[:k]+(x,)+s[k+1:]])
            for x in g[1][s[k]]: R[idx[s]].append(idx[s[:k]+(x,)+s[k+1:]])
    return (L,R)
def solve(g):
    L,R=g; n=len(L); val={}; cnt={}; pred={}
    for i in range(n):
        for s,opts in ((0,L[i]),(1,R[i])):
            cnt[(i,s)]=len(opts)
            for j in opts: pred.setdefault((j,1-s),[]).append((i,s))
    Q=deque()
    for k,c in cnt.items():
        if c==0: val[k]='L' if k[1]==0 else 'W'; Q.append(k)
    while Q:
        k=Q.popleft(); v=val[k]
        for p in pred.get(k,[]):
            if p in val: continue
            win='W' if p[1]==0 else 'L'
            if v==win: val[p]=win; Q.append(p)
            else:
                cnt[p]-=1
                if cnt[p]==0: val[p]='L' if p[1]==0 else 'W'; Q.append(p)
    return lambda i,s: val.get((i,s),'D')
G={}
G['0']=([[]],[[]]); G['*']=([[1],[]],[[1],[]]); G['up']=([[2],[2],[]],[[1],[2],[]]); G['down']=([[1],[2],[]],[[2],[2],[]])
G['over']=([[1],[]],[[0],[]]); G['under']=([[0],[]],[[1],[]])
G['over+*']=summ(G['over'],G['*']); G['over+down']=summ(G['over'],G['down']); G['over+up']=summ(G['over'],G['up'])
G['{0|*}']=G['up']
G['{0|over}']=([[1],[]],[[0],[]])  # identical to over
G['{over|0}']=([[1],[2],[]],[[2],[1],[]])  # node1 = over, node2 = 0
G['{0|0,over}']=([[1],[]],[[1,0],[]])   # over with a Black move to 0 as well
G['{0,*|over}']=([[1,2],[],[1]],[[0],[],[1]])  # 2 = *
G['tiny1']=([[1],[],[],[]],[[2],[],[3],[]]) # {0||0|-1}: 2 = {0|-1}, -1 = {|0}
G['tiny1']=([[1],[],[1],[]],[[2],[],[3],[1]])
G['miny1']=([[2],[],[3],[1]],[[1],[],[1],[]])
tests=readT(sys.argv[1])
names=sys.argv[2].split(';')
for tn,T in tests:
    row=[tn]
    for gn in names:
        f=solve(summ(G[gn],T)); row.append(gn+'='+f(0,0)+f(0,1))
    print(' | '.join(row))
