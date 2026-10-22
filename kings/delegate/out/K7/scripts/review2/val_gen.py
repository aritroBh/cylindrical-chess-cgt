import random, subprocess, sys
from hc import Geo
random.seed(int(sys.argv[1]))
def rand_pos(g, withep):
    while True:
        N=g.N; W=g.W; H=g.H
        sq=random.sample(range(N), 2+random.randint(0,3)+random.randint(0,3))
        k=random.randint(0,3); wk,bk=sq[0],sq[1]
        npw=random.randint(0,3); npb=random.randint(0,3)
        pool=[s for s in range(N) if 0< s//W <H-1 and s not in (wk,bk)]
        random.shuffle(pool)
        wp=frozenset(pool[:npw]); bp=frozenset(pool[npw:npw+npb])
        stm=random.randint(0,1); ep=-1
        if withep and random.random()<0.9:
            # black just double-stepped (stm white) or vice versa
            them=1-stm
            f=random.randrange(W)
            land=3 if them==0 else H-4
            if them==0:
                lsq=land*W+f; skip=(land-1)*W+f; orig=(land-2)*W+f
                wp=wp|{lsq}
            else:
                lsq=land*W+f; skip=(land+1)*W+f; orig=(land+2)*W+f
                bp=bp|{lsq}
            ep=skip
            pos=(wk,bk,wp,bp,stm,ep)
            occ=[wk,bk]+list(wp)+list(bp)
            if skip in occ or orig in occ: continue
        pos=(wk,bk,wp,bp,stm,ep)
        if not g.legal(pos): continue
        if ep>=0:
            # require a capturer so that kp keeps the right
            pass
        return pos
for geo in sys.argv[2:]:
    kind,wh=geo.split(':'); W,H=map(int,wh.split('x'))
    g=Geo(W,H,kind=='cyl')
    pos_list=[rand_pos(g, i%2==0) for i in range(600)]
    inp="\n".join(g.text(p) for p in pos_list)+"\n"
    out=subprocess.run(['./kp','--board',geo,'--ep','on','--moves','--promote','Q','--pmodel'],input=inp,capture_output=True,text=True).stdout.splitlines()
    out=[l for l in out]
    bad=0
    for p,l in zip(pos_list,out):
        mv=l.split('|')[-1].split()
        ks=set(m.split(':')[0] for m in mv)
        mine=set()
        for kind_,frm,to,promo,npos,after in g.moves(p):
            nm=("K" if kind_=='K' else "P") if True else ""
            mine.add(("K" if kind_=='K' else "P")+g.name(frm)+g.name(to)+("=Q" if promo else ""))
        if ks!=mine:
            bad+=1
            if bad<5: print("MISMATCH",g.text(p),sorted(ks^mine))
    print(geo,len(pos_list),"bad",bad)
