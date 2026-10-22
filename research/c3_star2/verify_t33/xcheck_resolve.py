"""Verifier: classify the 33 xcheck disagreements. Reuses the agent's position generator (same seed) but its own analysis."""
import random, subprocess, sys, pathlib
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from cylcgt import pawns, cgt
import research.c3_star2.xcheck_cyl as X
SC=str(HERE)
rng=random.Random(20261022)
cases=[]
for files in (3,4):
    made=0
    while made<25:
        pos=X.random_position(rng,files)
        b=pawns.Board(files,8,True,True)
        if pawns.passed(b,pos,"W") and pawns.passed(b,pos,"B"): continue
        cases.append((files,pos)); made+=1
total=0; bad=[]; root_passed_total=0
rows_by_w={}
for files in (3,4):
    grp=[(f,p) for f,p in cases if f==files]
    path=f"{SC}/xin_{files}.tsv"
    open(path,"w").write("\n".join(f"{X.text(p)}\t{f}" for f,p in grp)+"\n")
    out=subprocess.run([str(HERE.parent/"cyl_eval"),"--eval",path,"--cylinder"],capture_output=True,text=True,check=True).stdout
    rows=[l.split("\t") for l in out.strip().split("\n") if not l.startswith("#")]
    rows_by_w[files]=(grp,rows)
n_ok_nopass=n_nopass=0; classes={}
for files,(grp,rows) in rows_by_w.items():
    for (f,p),row in zip(grp,rows):
        for si,setting in enumerate(X.SETTINGS):
            race,ep_on,aware=setting
            g=X.cylcgt_setting(f,p,setting)
            oc,k=X.cgt_class(g)
            ccls,cnim=row[3+si].split(",")
            agree=(oc==ccls and k==int(cnim))
            b=pawns.Board(f,8,True,ep_on)
            pawns.PASSED_RESPECTS_EP=aware
            rp = pawns.passed(b,p,"W") or pawns.passed(b,p,"B")   # root already has a passed pawn (one-sided)
            total+=1
            key=("root has passer" if rp else "root has no passer", "agree" if agree else "DISAGREE")
            classes[key]=classes.get(key,0)+1
            if not agree and not rp: bad.append((f,X.text(p),setting,cgt.show(g),oc,k,row[3+si]))
print("settings x positions:",total)
for k,v in sorted(classes.items()): print("  ",k,v)
print("disagreements with NO passed pawn at the root:",len(bad))
for b in bad[:10]: print("  ",b)
