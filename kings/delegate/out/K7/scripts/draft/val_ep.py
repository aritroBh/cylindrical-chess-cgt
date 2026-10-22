import random, subprocess
from kpgen import Board
random.seed(9)
def rand_pos(B, npw, npb):
    while True:
        sqs = random.sample(range(B.N), 2+npw+npb)
        pos=(sqs[0],sqs[1],frozenset(sqs[2:2+npw]),frozenset(sqs[2+npw:]),random.randint(0,1),-1)
        if B.legal_pos(pos): return pos
for (W,H,wrap) in [(7,6,True),(5,4,False),(6,6,False)]:
    B=Board(W,H,wrap); poss=[]
    tries=0
    while len(poss)<300 and tries<200000:
        tries+=1
        p=rand_pos(B,random.randint(1,3),random.randint(1,3))
        for m in B.moves(p):
            if m['pos'] and m['pos'][5]>=0: poss.append(m['pos'])
    inp="\n".join(B.to_text(p) for p in poss)+"\n"
    out=subprocess.run(["./kp","--board",("cyl" if wrap else "flat")+f":{W}x{H}","--ep","on","--promote","Q","--pmodel","--moves"],input=inp,capture_output=True,text=True).stdout.splitlines()
    bad=0
    for p,line in zip(poss,out):
        parts=line.split("|")
        if "X" in parts[1]: bad+=1; print("X",line); continue
        ks=set(m.split(":")[0] for m in parts[2].split()) if len(parts)>2 and parts[2].strip() else set()
        mine=set(m['kind']+B.fname(m['frm'])+B.fname(m['to'])+("=Q" if m['promo'] else "") for m in B.moves(p))
        if ks!=mine:
            bad+=1
            if bad<5: print("DIFF",B.to_text(p),sorted(ks^mine))
    print(W,H,wrap,len(poss),"bad",bad)
