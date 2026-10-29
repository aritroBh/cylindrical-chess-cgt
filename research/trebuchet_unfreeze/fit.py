# Exhaustive one- and two-feature threshold rules (depth-1 stump, depth-2 tree over a feature pair), pure python.
import itertools,collections
def stump_candidates(rows,f):
    vals=sorted({r[f] for r in rows})
    return [(f,v) for v in vals[:-1]]   # rule: x<=v
def acc(pred,y): return sum(p==t for p,t in zip(pred,y))/len(y)
def best_stump(rows,feats,y):
    best=None
    for f in feats:
        for (_,v) in stump_candidates(rows,f):
            for pol in (0,1):   # pol: predict 1 when x<=v else 0 ; or reverse
                pred=[(r[f]<=v)==bool(pol) for r in rows]
                a=acc(pred,y)
                if best is None or a>best[0]: best=(a,f,v,pol)
    return best
def best_pair(rows,feats,y):
    best=None
    for f,g in itertools.combinations(feats,2):
        vf=sorted({r[f] for r in rows})[:-1]; vg=sorted({r[g] for r in rows})[:-1]
        for a in vf:
            for b in vg:
                cells=collections.defaultdict(lambda:[0,0])
                for r,t in zip(rows,y): cells[(r[f]<=a,r[g]<=b)][int(t)]+=1
                correct=sum(max(c) for c in cells.values())/len(y)
                if best is None or correct>best[0]:
                    best=(correct,f,a,g,b,{k:int(v[1]>=v[0]) for k,v in cells.items()})
    return best
def confusion(pred,y):
    c=collections.Counter((int(t),int(p)) for p,t in zip(pred,y))
    return {'TP':c[(1,1)],'FN':c[(1,0)],'FP':c[(0,1)],'TN':c[(0,0)]}
