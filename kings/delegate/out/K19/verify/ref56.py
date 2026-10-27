from lg import *
for q in (True,False):
  for c in (True,False):
    G=Game(8,8,False,'b',{5,6,7},queen=q,mate=True,confine=c)
    print('queen',q,'confine',c,[G.T(parse('Ke6 kg4 pg5'),k,tmax=9) for k in (0,1,2,3,4,None)],flush=True)
# mu_W: BFS over white king + context pawns only, black king & Z pawns deleted: Ke6, Pc3 ; black context pawn d6
from collections import deque
def mu():
    W=H=8
    start=((4,5),frozenset([(2,2)]))  # Ke6, Pc3
    bp={(3,5)}
    def nbs(s):
        f,r=s
        for df in (-1,0,1):
            for dr in (-1,0,1):
                if (df or dr) and 0<=f+df<W and 0<=r+dr<H: yield (f+df,r+dr)
    def attacked_by_bp(t): # black pawn at (f,r) attacks (f±1,r-1)
        return any(abs(t[0]-p[0])==1 and t[1]==p[1]-1 for p in bp)
    seen={start:0}; dq=deque([start])
    while dq:
        s=dq.popleft(); d=seen[s]; k,ps=s
        # king moves
        for t in nbs(k):
            if t in ps or attacked_by_bp(t): continue
            n2=(t,ps-({t}&bp))
            # king captures black pawn
            nb=n2
            if (nb) not in seen: seen[nb]=d+1; dq.append(nb)
        for p in ps:
            f,r=p
            if r==H-2 and (f,r+1) not in bp and (f,r+1)!=k:
                return d+1
            t=(f,r+1)
            if t!=k and t not in bp and t not in ps:
                n2=(k,(ps-{p})|{t})
                if n2 not in seen: seen[n2]=d+1; dq.append(n2)
            if r==1:
                t2=(f,r+2)
                if t!=k and t2!=k and t not in bp and t2 not in bp:
                    n2=(k,(ps-{p})|{t2})
                    if n2 not in seen: seen[n2]=d+1; dq.append(n2)
            for df in (-1,1):
                tt=(f+df,r+1)
                if tt in bp: pass  # black pawn captured by white pawn (black pawns stay put, capturing allowed)
    return None
print('mu_W =',mu(),' (k.u. BFS ignoring bp captures by pawns)')
