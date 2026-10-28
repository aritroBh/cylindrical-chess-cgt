import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm, tree
sys.setrecursionlimit(100000)
def dag(p, n, seen):
    """collect positions (winner-to-move nodes with chosen move) reachable in chosen tree"""
    if (p) in seen: return
    r = tree._w(p, n)
    lab, rr = r[1][0]
    seen[p] = (n, lab)
    if rr is None or rr == 'MATE': return
    q = [qq for l, qq in pm.moves(p) if l == lab][0]
    for l2, q2, r2 in rr[1]:
        dag(q2, n - 2, seen)
if __name__=='__main__':
    tot={}
    for line in open(sys.argv[1]):
        p=pm.parse(line)
        if p[5]==0: continue
    allseen={}
    for line in open(sys.argv[1]):
        p=pm.parse(line)
        for lab,q in pm.moves(p):
            if q=='PROMO': continue
            n=pm.dtw(q,21)
            if n is None: continue
            s={}
            dag(q,n,s)
            print(pm.show(p),lab,'dag nodes',len(s), 'of which non-terminal', sum(1 for v in s.values() if 'promotes' not in v[1]))
            allseen.update({k:v for k,v in s.items()})
    print('distinct winner positions overall',len(allseen))
