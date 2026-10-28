import sys, collections
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm, greedy
S=greedy.S
tops=[(pm.parse(l.split('#')[0].strip()), l.split('#')[2].strip(), l.split('#')[1].strip()) for l in open(sys.argv[1])]
tops.sort(key=lambda t:-greedy.D(t[0]))
for p,_,_ in tops: greedy.add(p)
def kind(p):
    lab,q,reps=S[p]
    if q=='PROMO': return 'Q'
    if reps and all(S[q2][1]=='PROMO' for l2,q2 in reps): return 'R'
    return 'N'
use=collections.Counter()
for p,lab,root in tops:
    reach=set()
    def vis(x):
        if x in reach: return
        reach.add(x)
        if kind(x)=='N':
            for l2,q2 in S[x][2]: vis(q2)
    vis(p)
    for x in reach:
        if kind(x)=='N': use[x]+=1
multi=[x for x,c in use.items() if c>=2]
print(len(use),'N nodes; used by >=2 cases:',len(multi), ' sum of per-case N:',sum(use.values()))
