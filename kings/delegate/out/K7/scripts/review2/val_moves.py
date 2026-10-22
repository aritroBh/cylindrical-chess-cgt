import random, subprocess, sys
from kb import B
random.seed(5)
def rnd(Bd):
    while True:
        npw, npb = random.randint(0,3), random.randint(0,3)
        sqs = random.sample(range(Bd.N), 2+npw+npb)
        wk, bk = sqs[:2]; wp = frozenset(sqs[2:2+npw]); bp = frozenset(sqs[2+npw:])
        stm = random.randint(0,1)
        ep = -1
        pos = (wk,bk,wp,bp,stm,ep)
        if random.random()<0.5:
            # make an ep right: pawn of 1-stm just double stepped
            them = 1-stm
            pw = bp if them==1 else wp
            land = 3 if them==0 else Bd.H-4
            cand=[p for p in pw if p//Bd.W==land]
            if cand:
                p=random.choice(cand); skip = p-Bd.W if them==0 else p+Bd.W
                orig = p-2*Bd.W if them==0 else p+2*Bd.W
                if skip in (wk,bk) or skip in wp or skip in bp or orig in (wk,bk) or orig in wp or orig in bp: continue
                pos=(wk,bk,wp,bp,stm,skip)
        if Bd.legal_pos(pos): return pos
for spec in [(7,6,True),(6,6,False),(7,5,True),(5,4,False)]:
    Bd=B(*spec); tot=0; bad=0
    ps=[rnd(Bd) for _ in range(400)]
    inp="\n".join(Bd.text(p) for p in ps)+"\n"
    out=subprocess.run(["./kp","--board",("cyl" if spec[2] else "flat")+f":{spec[0]}x{spec[1]}","--ep","on","--promote","Q","--pmodel","--moves"],input=inp,capture_output=True,text=True).stdout.splitlines()
    for p,l in zip(ps,out):
        mv=l.split("|")[2].split()
        mine=Bd.moves(p)
        # kpsolve lists promotions per promo type (Q only) so counts equal
        if len(mv)!=len(mine):
            bad+=1
            if bad<4: print(spec, Bd.text(p), len(mv), len(mine), l)
        tot+=1
    print(spec,"checked",tot,"count mismatches",bad)
