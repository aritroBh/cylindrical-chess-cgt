import sys, json, random, itertools
sys.path.insert(0,'.')
import confirm as c
random.seed(1515)
board=(8,6); W,H=board
groups=[("Z_B-cyl","Kb2 ka4 Pa3 Pb4 pb3 pc4"),("D2","Ka1 ka4 Pb4 Pc3 pb3 pc4"),("D3","Ka1 ka6 Pa3 Pb4 Pc3 pa4 pb3 pc4"),("Z_C(tempo-fail)","Ka2 kc4 Pa4 Pc2 pa5 pc3"),
        ("Z_B-mirror","Ka3 kb5 Pb4 Pc3 pa4 pb3"),("D2-mirror","Ka1 ka6 Pa3 Pb4 pa4 pb3")]
named=c.contexts(board)
# random context sample on files e,g (non adjacent) and f: <=2 pawns per side, <=3 in total
sq_eg=[f"{f}{r}" for f in "eg" for r in range(2,6)]
sq_f=[f"f{r}" for r in range(2,6)]
rand={}
def pawn_ok(wl,bl):
    # no pawn may attack another pawn / share squares; pawns on e,g only or f only
    return True
tries=0
while len(rand)<30 and tries<10000:
    tries+=1
    pool=sq_eg if random.random()<0.7 else sq_f
    nw=random.randint(0,2); nb=random.randint(0,2)
    if nw+nb==0 or nw+nb>3: continue
    sel=random.sample(pool,nw+nb); wl=sorted(sel[:nw]); bl=sorted(sel[nw:])
    name="R_"+"".join(wl)+"_"+"".join(bl)
    # skip contexts where a pawn is already past the other (immediately promoting) - keep them, they test races
    rand[name]=(wl,bl)
ctxs=dict(named); ctxs.update(rand)
rows=[]; import os; os.makedirs('conf/dud',exist_ok=True)
for gi,(gname,grp) in enumerate(groups):
    toks=[t for t in grp.split() if len(t)>=3]
    lines=[]; gr=[]
    for cname,(cw,cb) in ctxs.items():
        cwp=[c.sq(x) for x in cw]; cbp=[c.sq(x) for x in cb]
        pw,pb=c.solve_d(H,cwp,cbp,"dud")
        ctoks=[f"P{x}" for x in cw]+[f"p{x}" for x in cb]
        for stm,pred in (("w",pw),("b",pb)):
            p=" ".join(toks+ctoks)+f" {stm} -"
            lines.append(p); gr.append({"cls":"dud","gname":gname,"group":" ".join(toks),"ctx":cname,"stm":stm,"pos":p,"z":"dud","pred":pred})
    open(f'conf/dud/g{gi}.in','w').write("\n".join(lines)+"\n")
    rows.append(gr)
json.dump(rows,open('conf/dud/rows.json','w'))
print([len(r) for r in rows])
