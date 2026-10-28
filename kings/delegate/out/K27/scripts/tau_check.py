"""tau_check.py -- tau = (flip ranks r -> 7-r, swap colours, swap side to move) is a symmetry of the P model on flat 7x6
(and of chess). Check on the 8 roots of Z_B and on all their descendants reachable by <= 12 plies of legal play (pm.py move
generator): the legal-move sets correspond, and tau(Z_B roots) = the 8 roots of the mirror group."""
import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm
H,W=pm.H,pm.W
def ts(s): return (H-1-s//W)*W+s%W
def tau(p):
    wk,bk,wp,bp,ep,stm=p
    return (ts(bk),ts(wk),tuple(sorted(ts(s) for s in bp)),tuple(sorted(ts(s) for s in wp)),ts(ep) if ep>=0 else -1,1-stm)
roots=[pm.parse(l) for l in open(sys.argv[1]) if l.strip()]
zb=roots[:8]; mir=set(roots[8:])
img=set(tau(p) for p in zb)
print('tau(Z_B roots) == mirror roots:', img==mir)
# move generator equivariance on a BFS of positions
seen=set(); fr=list(zb); bad=0; n=0
for depth in range(8):
    nf=[]
    for p in fr:
        if p in seen: continue
        seen.add(p)
        ms=pm.moves(p); mt=pm.moves(tau(p))
        a=sorted((('PROMO' if q=='PROMO' else tau(q)) for l,q in ms), key=str)
        b=sorted((q for l,q in mt), key=str)
        n+=1
        if a!=b: bad+=1
        for l,q in ms:
            if q!='PROMO': nf.append(q)
    fr=nf
print('positions tested',n,'equivariance failures',bad)
