# Sample trebuchet + context positions on cyl:6x6 (files a..f, ranks 1..6). Output: data/s6x6.txt (kpsolve format) and data/s6x6_meta.json
import random,json,sys
random.seed(20261029)
FILES='abcdef'
def S(f,r): return FILES[f]+str(r)
def trebuchets():
    out=[]
    for r in (2,3,4):
        for mirror in (False,True):
            fa,fc=(0,2) if not mirror else (2,0)
            out.append(dict(r=r,mir=mirror,
              K=S(fa,r+1),P=S(1,r),k=S(fc,r),p=S(1,r+1)))
    return out
T=trebuchets()
def adj(a,b):
    fa,ra=FILES.index(a[0]),int(a[1]);fb,rb=FILES.index(b[0]),int(b[1])
    df=min((fa-fb)%6,(fb-fa)%6)
    return max(df,abs(ra-rb))<=1
def attacked_by_pawns(sqr,pawns_w,pawns_b,king_color):
    # is a king of king_color on sqr attacked by an enemy pawn
    f=FILES.index(sqr[0]);r=int(sqr[1])
    if king_color=='w':  # black pawns attack downward: pawn at (f+-1,r+1)
        return any(S((f+d)%6,r+1) in pawns_b for d in(-1,1))
    return any(S((f+d)%6,r-1) in pawns_w for d in(-1,1))
seen=set();recs=[]
ctxsq=[S(f,r) for f in (3,4,5) for r in (2,3,4,5)]
tries=0
while len(recs)<2000 and tries<200000:
    tries+=1
    t=random.choice(T)
    n=random.choice([1,2,2,3,3,3])
    nw=random.randint(0,n);nb=n-nw
    if nw+nb==0: continue
    sq=random.sample(ctxsq,n)
    W=sq[:nw];B=sq[nw:]
    stm=random.choice('wb')
    wp=[t['P']]+W;bp=[t['p']]+B
    occ=set(wp)|set(bp)|{t['K'],t['k']}
    # kings not adjacent / not attacked by pawns
    if attacked_by_pawns(t['K'],wp,bp,'w') or attacked_by_pawns(t['k'],wp,bp,'b'):continue
    # side not to move must not be in check by pawn: (stm side's opponent king attacked by stm pawn)
    if stm=='w' and attacked_by_pawns(t['k'],wp,bp,'b'):continue
    key=(t['r'],t['mir'],tuple(sorted(W)),tuple(sorted(B)),stm)
    if key in seen:continue
    seen.add(key)
    s=f"K{t['K']} "+' '.join('P'+x for x in [t['P']]+sorted(W))+f" k{t['k']} "+' '.join('p'+x for x in [t['p']]+sorted(B))+f" {stm} -"
    recs.append(dict(pos=s,r=t['r'],mir=t['mir'],W=sorted(W),B=sorted(B),stm=stm))
open('data/s6x6.txt','w').write('\n'.join(x['pos'] for x in recs)+'\n')
json.dump(recs,open('data/s6x6_meta.json','w'))
print(len(recs),'positions in',tries,'tries')
