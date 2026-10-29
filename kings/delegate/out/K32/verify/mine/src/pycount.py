"""Referee-2: independent Python class count of rooted terminal-free stoppers (root node 0, all nodes reachable),
isomorphism = relabelling of the non-root nodes (itertools.permutations, set of canonical tuples). n=1..3 (n=4 needs 2^32 labelled graphs, done in C)."""
import itertools,sys
sys.path.insert(0,'.')
def stopper(n,L,R):
    # Kahn-style removal of (node,mover) with no live successor
    aL=set(range(n)); aR=set(range(n)); ch=True
    while ch:
        ch=False
        for v in list(aL):
            if not (set(L[v])&aR): aL.discard(v); ch=True
        for v in list(aR):
            if not (set(R[v])&aL): aR.discard(v); ch=True
    return not aL and not aR
for n in (1,2,3):
    subsets=[tuple(u for u in range(n) if m>>u&1) for m in range(1<<n)]
    perms=[(0,)+p for p in itertools.permutations(range(1,n))]
    seen=set(); lab=0
    for Ls in itertools.product(subsets,repeat=n):
        for Rs in itertools.product(subsets,repeat=n):
            # reachability from 0
            r={0}; st=[0]
            while st:
                v=st.pop()
                for u in Ls[v]+Rs[v]:
                    if u not in r: r.add(u); st.append(u)
            if len(r)!=n: continue
            if not stopper(n,Ls,Rs): continue
            lab+=1
            best=None
            for p in perms:
                nl=[None]*n; nr=[None]*n
                for v in range(n):
                    nl[p[v]]=tuple(sorted(p[u] for u in Ls[v])); nr[p[v]]=tuple(sorted(p[u] for u in Rs[v]))
                key=(tuple(nl),tuple(nr))
                if best is None or key<best: best=key
            seen.add(best)
    print("n=%d labelled rooted stoppers %d classes %d"%(n,lab,len(seen)))
