import random, subprocess, sys
from kpgen import Board
random.seed(5)
def rand_pos(B, npw, npb):
    W,H=B.W,B.H
    while True:
        sqs = random.sample(range(B.N), 2+npw+npb)
        wk,bk = sqs[0],sqs[1]
        wp=frozenset(sqs[2:2+npw]); bp=frozenset(sqs[2+npw:])
        stm=random.randint(0,1)
        pos=(wk,bk,wp,bp,stm,-1)
        if B.legal_pos(pos): return pos
for (W,H,wrap) in [(7,6,True),(5,4,False),(6,5,True)]:
    B=Board(W,H,wrap)
    poss=[]
    while len(poss)<400:
        pos=rand_pos(B,random.randint(0,3),random.randint(0,3))
        poss.append(pos)
    # add some e.p. positions
    inp="\n".join(B.to_text(p) for p in poss)+"\n"
    out=subprocess.run(["./kp","--board",("cyl" if wrap else "flat")+f":{W}x{H}","--ep","on","--promote","Q","--pmodel","--moves"],input=inp,capture_output=True,text=True).stdout.splitlines()
    bad=0
    for p,line in zip(poss,out):
        parts=line.split("|")
        if "X" in parts[1]: 
            print("X",line); bad+=1; continue
        ks=set(m.split(":")[0] for m in parts[2].split()) if len(parts)>2 and parts[2].strip() else set()
        mine=set()
        for m in B.moves(p):
            s=m['kind']+B.fname(m['frm'])+B.fname(m['to'])+("=Q" if m['promo'] else "")
            mine.add(s)
        if ks!=mine:
            bad+=1
            if bad<5: print("DIFF",B.to_text(p),sorted(ks^mine))
    print(W,H,wrap,"bad",bad)
