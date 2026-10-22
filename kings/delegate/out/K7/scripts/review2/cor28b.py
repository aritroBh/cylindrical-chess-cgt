import collections
from kb import B
from cert import Cert
def run(kind,W,H,FZ):
    wrap = kind=='cyl'; Bd=B(W,H,wrap); C=Cert(Bd,FZ)
    res=collections.defaultdict(lambda:[0,0,0,0])   # (d-D) -> [tot, L1_P holds, L1 with queen clause holds]
    for s in (0,):
        sb=1-s
        for p in [r*W+f for r in range(1,H-1) for f in FZ]:
            d = 1 if sb==0 else -1; last = H-1 if sb==0 else 0
            D = abs(last - p//W); q = last*W + p%W
            path = {p + d*W*i for i in range(0,D+1)}
            for bk in [r*W+f for r in range(H) for f in FZ]:
                if bk in path: continue
                for sk in range(Bd.N):
                    if sk in path or sk==bk or sk in Bd.kn[bk]: continue
                    dd = Bd.kdist(sk,q)
                    if dd < D-1 or dd > D+3: continue
                    wk,bkk = (sk,bk)
                    pos=(wk,bkk,frozenset(),frozenset([p]),0,-1) if sb==1 else (wk,bkk,frozenset([p]),frozenset(),1,-1)
                    pos=(sk,bk,frozenset(),frozenset([p]),0,-1)   # s=White, s-bar=Black
                    if not Bd.legal_pos(pos): continue
                    a=C.lg(C.proj(pos),D,1,False); b=C.lg(C.proj(pos),D,1,True)
                    r=res[dd-D]; r[0]+=1; r[1]+=a; r[2]+=b
    for k in sorted(res): print(kind,W,H,"d-D =",k,"total",res[k][0],"L1_P holds",res[k][1],"L1 holds",res[k][2])
run('flat',6,6,[0,1,2]); run('cyl',7,6,[0,1,2])
