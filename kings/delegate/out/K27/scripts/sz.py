import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm, tree
sys.setrecursionlimit(100000)
for line in open(sys.argv[1]):
    p=pm.parse(line)
    for lab,q in pm.moves(p):
        if q=='PROMO': continue
        n=pm.dtw(q,21)
        if n is None or n<9: continue
        out=[]
        for m in (n,n+2,n+4):
            r=tree._w(q,m)
            out.append((m,r[0] if r else None))
        print(pm.show(p),lab,out, flush=True)
