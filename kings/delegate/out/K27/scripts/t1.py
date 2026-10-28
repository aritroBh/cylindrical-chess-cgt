import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm
sys.setrecursionlimit(10000)
for line in open(sys.argv[1]):
    p=pm.parse(line)
    ms=pm.moves(p)
    out=[]
    for lab,q in ms:
        if q=='PROMO': v='PROMO'
        else:
            v=pm.dtw(q,int(sys.argv[2]))
            v = 'oppwins@%d'%v if v else '-'
        out.append(lab+':'+v)
    print(pm.show(p),'|',' '.join(out))
