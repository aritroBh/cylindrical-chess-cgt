# mu_s of LOOPY Def 2.6 (L2) for Q after 1...Kd2 2.Kxb4, G1 and G2: BFS over Black king + context pawns, White never moves,
# White king and Z pawns deleted; the white context pawn stays unless captured. cyl:7x6.
from collections import deque
W,H=7,6
def nb(s):
    f,r=s
    for df in (-1,0,1):
        for dr in (-1,0,1):
            if (df or dr) and 0<=r+dr<H: yield ((f+df)%W,r+dr)
def mu(bk, wps, bps):
    start=(bk,frozenset(wps),frozenset(bps)); seen={start}; q=deque([(start,0)])
    while q:
        (k,wp,bp),d=q.popleft()
        nxt=[]
        for n in nb(k):
            if n in bp: continue
            # attacked by white pawn? white pawn at (f,r) attacks (f+-1,r+1)
            if any(n[1]==p[1]+1 and (n[0]-p[0])%W in (1,W-1) for p in wp): continue
            nxt.append((n,wp-{n},bp))
        for p in bp:
            t=(p[0],p[1]-1)
            if t==k or t in wp or t in bp: continue
            if t[1]==0: return d+1
            nxt.append((k,wp,(bp-{p})|{t}))
            if p[1]==H-2 and (p[0],p[1]-2) not in wp|bp and (p[0],p[1]-2)!=k: pass
        for p in bp:  # captures
            for df in (-1,1):
                t=((p[0]+df)%W,p[1]-1)
                if t in wp:
                    if t[1]==0: return d+1
                    nxt.append((k,wp-{t},(bp-{p})|{t}))
        for s in nxt:
            if s not in seen: seen.add(s); q.append((s,d+1))
    return None
d2=(3,1)
print('G2 mu_s', mu(d2,{(4,1)},{(4,2)}))   # Pe2, pe3
print('G1 mu_s', mu(d2,{(4,2)},{(4,3)}))   # Pe3, pe4
