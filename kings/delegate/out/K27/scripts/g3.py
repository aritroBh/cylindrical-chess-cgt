import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm, greedy
tops=[pm.parse(l.split('#')[0].strip()) for l in open(sys.argv[1])]
tops.sort(key=lambda p:-greedy.D(p))
for p in tops: greedy.add(p)
S=greedy.S
def kind(p):
    lab,q,reps=S[p]
    if q=='PROMO': return 'Q'
    if reps and all(S[q2][1]=='PROMO' for l2,q2 in reps): return 'R'
    return 'N'
cnt={'Q':0,'R':0,'N':0}
reach=set()
def vis(p):
    if p in reach: return
    reach.add(p)
    if kind(p)=='N':
        for l2,q2 in S[p][2]: vis(q2)
for p in tops: vis(p)
for p in reach: cnt[kind(p)]+=1
print(cnt)
import collections
cl=collections.defaultdict(list)
for p in reach:
    if kind(p)!='N': continue
    key=(' '.join('P'+pm.nm(s) for s in p[2]),' '.join('p'+pm.nm(s) for s in p[3]),'W' if p[5]==0 else 'B')
    cl[key].append('K'+pm.nm(p[0])+' k'+pm.nm(p[1])+' '+S[p][0])
for k,v in sorted(cl.items(), key=lambda kv:-len(kv[1])):
    print(k,len(v),'; '.join(sorted(v)))
