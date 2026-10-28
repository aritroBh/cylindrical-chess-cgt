import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm, tree
sys.setrecursionlimit(100000)
for line in open(sys.argv[1]):
    p=pm.parse(line)
    for lab,q in pm.moves(p):
        if q=='PROMO': continue
        n=pm.dtw(q,21)
        if n is None: continue
        r=tree._w(q,n)
        print('%-70s %-10s win in %2d size %3d'%(pm.show(p),lab,n,r[0]))
