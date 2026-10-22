import time
from mysolve import solve_text
ROOTS=[("C3 W a2 a3 b2 / B b7 c6 c7",3,"W: a2 a3 b2 / B: b7 c6 c7"),("C4 W a4 b2 c2 / B b6 c5 d6 d7",4,"W: a4 b2 c2 / B: b6 c5 d6 d7")]
SET=[("count ep-on aware","count",True,True),("count ep-on textbook","count",True,False),("count ep-off","count",False,False),
("mover ep-on aware","mover",True,True),("mover ep-on textbook","mover",True,False),("mover ep-off","mover",False,False),
("opponent ep-on aware","opponent",True,True),("opponent ep-on textbook","opponent",True,False),("opponent ep-off","opponent",False,False)]
for label,F,t in ROOTS:
    print("==",label)
    for nm,race,ep,aw in SET:
        t0=time.time()
        oc,k,s=solve_text(F,t,race,ep,aw,kmax=6)
        print(f"  {nm:26s} outcome {oc} nimber {('*'+str(k)) if k is not None else 'none<=*5'}  states {len(s.memo)}  {time.time()-t0:.1f}s",flush=True)
