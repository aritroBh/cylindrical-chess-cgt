# Targeted family on cyl:6x6: exactly one white and one black context pawn on the same file (d, e or f), every rank pair 2..5,
# all six trebuchets, both sides to move (the family in which P4/P13 of K23 live). Output data/sB.txt + data/sB_meta.json
import json
FILES='abcdef'
def S(f,r): return FILES[f]+str(r)
recs=[]
for r in (2,3,4):
    for mirror in (False,True):
        fa,fc=(0,2) if not mirror else (2,0)
        K,P,k,p=S(fa,r+1),S(1,r),S(fc,r),S(1,r+1)
        for f in (3,4,5):
            for rw in range(2,6):
                for rb in range(2,6):
                    if rw==rb: continue
                    for stm in 'wb':
                        W=[S(f,rw)];B=[S(f,rb)]
                        # pawns must not give check: black pawn at rb attacks (f+-1, rb-1); white at rw attacks (f+-1,rw+1)
                        bad=False
                        for (kk,col) in ((K,'w'),(k,'b')):
                            kf=FILES.index(kk[0]);kr=int(kk[1])
                            if col=='w' and any((kf-(f+d))%6==0 and kr==rb-1 for d in(-1,1)): bad=True
                            if col=='b' and any((kf-(f+d))%6==0 and kr==rw+1 for d in(-1,1)): bad=True
                        if bad: continue
                        if stm=='w' and any(((FILES.index(k[0])-(f+d))%6==0) and int(k[1])==rw+1 for d in(-1,1)): continue
                        if stm=='b' and any(((FILES.index(K[0])-(f+d))%6==0) and int(K[1])==rb-1 for d in(-1,1)): continue
                        s=f"K{K} P{P} P{W[0]} k{k} p{p} p{B[0]} {stm} -"
                        recs.append(dict(pos=s,r=r,mir=mirror,W=W,B=B,stm=stm))
open('data/sB.txt','w').write('\n'.join(x['pos'] for x in recs)+'\n')
json.dump(recs,open('data/sB_meta.json','w'))
print(len(recs))
