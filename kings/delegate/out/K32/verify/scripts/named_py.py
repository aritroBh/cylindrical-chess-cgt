import sys; sys.path.insert(0,'scripts')
from pyref import run, fmt
def G(L,R): n=len(L); return dict(n=n,L=[list(x) for x in L],R=[list(x) for x in R])
games={
 'on':G([[0]],[[]]),'off':G([[]],[[0]]),'0':G([[]],[[]]),
 'over':G([[1],[]],[[0],[]]),'under':G([[1],[]],[[],[]]) ,
 '*':G([[1],[]],[[1],[]]),
 '1':G([[1],[]],[[],[]]),
 '2':G([[1],[2],[]],[[],[],[]]),
 '-1':G([[],[]],[[1],[]]),
 '-2':G([[],[],[]],[[1],[2],[]]),
 '1/2':G([[1],[],[1]] if False else [[1],[],[1]],[[2],[],[]]) ,
 'up':G([[1],[],[1]],[[2],[],[]]),
}
# fix definitions explicitly
games['under']=G([[0 ]if False else [1],[]],[[],[]])
games['under']=G([[0,1],[]],[[1],[]])      # under = {under | 0}: L option itself?? placeholder replaced below
games['under']=G([[0],[]],[[1],[]])        # under = {under | 0}: node0: L->0 (itself), R->1 (the zero node)
games['over']=G([[1],[]],[[0],[]])         # over = {0 | over}
games['1/2']=G([[1,],[],[ ]] if False else [[1],[],[1]],[[2],[],[]])
# 1/2 = {0|1}: nodes: 0=root, 1=zero, 2=one ; one={0|}
games['1/2']=G([[1],[],[1]],[[2],[],[]])
# up = {0|*}: nodes 0=up,1=zero,2=star ; star={0|0}
games['up']=G([[1],[],[1]],[[2],[],[1]])
games['down']=G([[2],[],[1]],[[1],[],[1]])
games['up']=G([[1],[],[1]],[[2],[],[1]])
games['+-1']=G([[1],[3],[],[]],[[2],[],[3],[]])   # root {1|-1}; node1 = {0|}; node2={|0}; node3 = 0
# fix: node1 L->3 (zero), node2 R->3 ; node3 zero
games['+-1']=G([[1],[3],[],[]],[[2],[],[3],[]])
games['{on|off}']=G([[1],[1],[]],[[2],[],[2]])
games['{0|off}']=G([[1],[],[]],[[2],[],[2]])
games['{on|0}']=G([[1],[1],[]],[[2],[],[]])
games['K21 tempo']=G([[2],[],[1,2]],[[1,2],[0,1],[]])
for k,g in games.items():
    # sanity: stopper check by evaluating run (would recurse forever otherwise)
    out=run(g)
    print(k, ' '.join('(lam=%s rho=%s LS=%s RS=%s)'%(a if a is not None else 'inf',b if b is not None else 'inf',fmt(c),fmt(d)) for a,b,c,d in out[:1]))
