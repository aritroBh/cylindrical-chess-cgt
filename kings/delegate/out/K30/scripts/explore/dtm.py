import sys, collections
sys.path.insert(0,'.')
from kpm import *
# depth-to-win analysis for P model: BFS layers by ply
def solve_depth(B, model, roots):
    index, plist, val, moves = solve(B, model, roots)
    n=len(plist)
    # compute depth: win for mover = 1+min over (loss successors depth, promo win =1); loss = 1+max over successors
    INF=10**9
    dep=[None]*n
    # value from mover's view
    def mv(i):
        p=plist[i]; v=val[i]
        if v=='D': return 0
        return 1 if (v=='W')==(p[0]==0) else -1
    # iterate layers
    preds=[[] for _ in range(n)]
    for i in range(n):
        for lab,k,t in moves[i]:
            if k=='n': preds[t].append(i)
    cnt=[0]*n
    q=collections.deque()
    for i in range(n):
        m=mv(i)
        if m==0: continue
        if not moves[i]:
            dep[i]=0; q.append(i); continue
        # terminal promo win?
        win_prom=any(k=='p' and ((t==W_)==(plist[i][0]==0)) for lab,k,t in moves[i])
        if m==1 and win_prom:
            dep[i]=1; q.append(i)
        cnt[i]=sum(1 for lab,k,t in moves[i] if k=='n')
    # simple fixpoint iteration by depth
    # process in increasing depth using repeated sweeps (graph small)
    changed=True
    while changed:
        changed=False
        for i in range(n):
            m=mv(i)
            if m==0 or dep[i] is not None and False: continue
            ms=moves[i]
            if not ms: continue
            if m==1:
                best=INF
                for lab,k,t in ms:
                    if k=='p':
                        if (t==W_)==(plist[i][0]==0): best=min(best,1)
                    else:
                        if mv(t)==-1 and dep[t] is not None: best=min(best,dep[t]+1)
                if best<INF and (dep[i] is None or best<dep[i]): dep[i]=best; changed=True
            else:
                worst=0; ok=True
                for lab,k,t in ms:
                    if k=='p': worst=max(worst,1)   # losing promotion by mover: 1 ply
                    else:
                        if mv(t)==1 and dep[t] is not None: worst=max(worst,dep[t]+1)
                        else: ok=False;break
                if ok and (dep[i] is None or worst!=dep[i]): dep[i]=worst; changed=True
    return index,plist,val,moves,dep,mv
if __name__=='__main__':
    spec=sys.argv[1]; model=sys.argv[2]
    B=Board(spec)
    root=parse(B,'Ke6 Pd7 kd8 pe7 w -')
    index,plist,val,moves,dep,mv=solve_depth(B,model,[root])
    i0=index[root]
    for lab,k,t in moves[i0]:
        if k=='n': print(lab,val[t],dep[t])
    # principal line after Kf7
    def line(i):
        out=[]
        while True:
            p=plist[i]; m=mv(i)
            if m==1:
                cands=[(dep_t,lab,t,k) for lab,k,t in moves[i] for dep_t in [ (1 if k=='p' else (dep[t]+1 if mv(t)==-1 and dep[t] is not None else 10**9))]]
                cands.sort(key=lambda x:x[0]); d,lab,t,k=cands[0]
            else:
                # loser: pick move maximizing depth
                cands=[]
                for lab,k,t in moves[i]:
                    d=1 if k=='p' else (dep[t]+1 if mv(t)==1 and dep[t] is not None else -1)
                    cands.append((d,lab,t,k))
                cands.sort(key=lambda x:-x[0]); d,lab,t,k=cands[0]
            out.append((fmt(B,p),lab,d))
            if k=='p': break
            i=t
        return out
    for lab,k,t in moves[i0]:
        if lab=='e6f7':
            for l in line(t): print(l)
