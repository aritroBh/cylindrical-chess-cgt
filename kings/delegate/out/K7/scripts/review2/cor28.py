import sys, itertools
from kb import B
from cert import Cert
def run(kind,W,H,FZ):
    wrap = kind=='cyl'; Bd=B(W,H,wrap); C=Cert(Bd,FZ)
    bad=0; tot=0
    for s in (0,1):
        sb=1-s
        for p in [r*W+f for r in range(1,H-1) for f in FZ]:
            d = 1 if sb==0 else -1; last = H-1 if sb==0 else 0
            D = abs(last - p//W)
            q = (last*W + p%W)
            path = {p + d*W*i for i in range(0,D+1)}
            for bk in [r*W+f for r in range(H) for f in FZ]:
                if bk in path: continue
                for sk in range(Bd.N):
                    if sk in path or sk==bk or sk in Bd.kn[bk]: continue
                    if Bd.kdist(sk,q) < D+2: continue
                    wk,bkk = (sk,bk) if s==0 else (bk,sk)
                    wp = frozenset([p]) if sb==0 else frozenset(); bp = frozenset([p]) if sb==1 else frozenset()
                    pos=(wk,bkk,wp,bp,s,-1)
                    if not Bd.legal_pos(pos): continue
                    tot+=1
                    ok = C.lg(C.proj(pos), D, sb, True)
                    if not ok:
                        bad+=1
                        if bad<=5: print("COR2.8 FAIL", kind,W,H,Bd.text(pos),"D",D)
    print(kind,W,H,FZ,"checked",tot,"fail",bad)
run('flat',6,6,[0,1,2]); run('cyl',7,6,[0,1,2]); run('cyl',7,5,[0,1]); run('flat',5,7,[1,2])
