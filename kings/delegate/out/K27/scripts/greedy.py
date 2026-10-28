"""greedy.py -- build a small proof DAG: every winner node uses a DTW-decreasing move (so no cycles), chosen to
reuse nodes already in the DAG."""
import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm
sys.setrecursionlimit(100000)
_d={}
def D(p):
    """dtw of position p (side to move wins) or None"""
    if p in _d: return _d[p]
    r=pm.dtw(p,31)
    _d[p]=r
    return r

def options(p):
    """winning moves of the side to move at p that decrease dtw: list of (lab, q or 'PROMO', replies)"""
    n=D(p)
    out=[]
    ms=pm.moves(p)
    for lab,q in ms:
        if q=='PROMO': return [(lab,'PROMO',[])]
    for lab,q in ms:
        # q: opponent to move must lose within n-1
        qs=pm.moves(q)
        if not qs:
            if pm.in_check(q,q[5]): out.append((lab,q,[])) 
            continue
        ok=True; reps=[]
        for l2,q2 in qs:
            if q2=='PROMO': ok=False;break
            d2=D(q2)
            if d2 is None or d2>n-2: ok=False;break
            reps.append((l2,q2))
        if ok: out.append((lab,q,reps))
    return out

S={}   # chosen: p -> (lab, q, reps)
_cost={}
def cost(p, depth=0):
    """number of new nodes needed to certify p, given S (no sharing inside this estimate except S and memo)"""
    if p in S: return 0
    key=p
    if key in _cost: return _cost[key]
    opts=options(p)
    best=None
    for lab,q,reps in opts:
        if q=='PROMO': best=1; break
        c=1+sum(cost(q2) for l2,q2 in reps)
        if best is None or c<best: best=c
    _cost[key]=best
    return best

def add(p):
    if p in S: return
    opts=options(p)
    best=None
    for lab,q,reps in opts:
        if q=='PROMO': best=(1,lab,q,reps); break
        c=1+sum(cost(q2) for l2,q2 in reps)
        if best is None or c<best[0]: best=(c,lab,q,reps)
    _,lab,q,reps=best
    S[p]=(lab,q,reps)
    _cost.clear()
    for l2,q2 in reps: add(q2)

if __name__=='__main__':
    tops=[]
    for line in open(sys.argv[1]):
        p=pm.parse(line.split('#')[0].strip())
        tops.append(p)
    # process hardest first so smaller ones reuse
    tops.sort(key=lambda p:-D(p))
    for p in tops:
        add(p)
    nonterm=[p for p,(lab,q,r) in S.items() if q!='PROMO']
    print('nodes',len(S),'non-terminal',len(nonterm))

def render(tops):
    ids={}
    order=[]
    def visit(p):
        if p in ids: return
        ids[p]=len(ids)+1
        order.append(p)
        lab,q,reps=S[p]
        for l2,q2 in reps: visit(q2)
    for p in tops: visit(p)
    lines=[]
    for p in order:
        lab,q,reps=S[p]
        side='White' if p[5]==0 else 'Black'
        if q=='PROMO':
            lines.append('N%d  %s | %s: %s wins'%(ids[p],pm.show(p)[:-4],side,lab)); continue
        if not reps:
            lines.append('N%d  %s | %s: %s mate'%(ids[p],pm.show(p)[:-4],side,lab)); continue
        rs=[]
        for l2,q2 in reps:
            lab2,qq,_=S[q2]
            rs.append('%s -> N%d'%(l2,ids[q2]))
        lines.append('N%d  %s | %s: %s ; %s'%(ids[p],pm.show(p)[:-4],side,lab,'; '.join(rs)))
    return lines
