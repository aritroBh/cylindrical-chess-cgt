import sys, subprocess
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm
import importlib
lines=[l.split('#') for l in open(sys.argv[1])]
for ln in lines:
    import greedy
    importlib.reload(greedy)
    p=pm.parse(ln[0].strip())
    greedy.add(p)
    S=greedy.S
    def kind(p):
        lab,q,reps=S[p]
        if q=='PROMO': return 'Q'
        if reps and all(S[q2][1]=='PROMO' for l2,q2 in reps): return 'R'
        return 'N'
    reach=set()
    def vis(p):
        if p in reach: return
        reach.add(p)
        if kind(p)=='N':
            for l2,q2 in S[p][2]: vis(q2)
    vis(p)
    c={'Q':0,'R':0,'N':0}
    for x in reach: c[kind(x)]+=1
    print('%-34s %-8s %-40s dtw %2d N=%3d R=%3d'%(ln[1].strip()[:34],ln[2].strip(),pm.show(p)[:-4],greedy.D(p),c['N'],c['R']),flush=True)
