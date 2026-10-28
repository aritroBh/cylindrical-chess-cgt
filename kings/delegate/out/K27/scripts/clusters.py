import sys, collections
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm, tree, dag
sys.setrecursionlimit(100000)
allseen={}
for line in open(sys.argv[1]):
    p=pm.parse(line)
    for lab,q in pm.moves(p):
        if q=='PROMO': continue
        n=pm.dtw(q,21)
        if n is None: continue
        s={}
        dag.dag(q,n,s)
        allseen.update(s)
cl=collections.defaultdict(list)
for p,(n,lab) in allseen.items():
    if 'promotes' in lab: continue
    key=(' '.join('P'+pm.nm(s) for s in p[2]),' '.join('p'+pm.nm(s) for s in p[3]),p[5])
    cl[key].append((pm.nm(p[0]),pm.nm(p[1]),lab,n))
for k,v in sorted(cl.items(), key=lambda kv:-len(kv[1])):
    print(k,len(v))
    for x in sorted(v): print('    ',x)
