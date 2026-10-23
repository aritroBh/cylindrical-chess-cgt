import random, re, sys
SD="/Users/aritro/Downloads/Research/Chessendgames/research/star4_hunt"
random.seed(11)
PAT=re.compile(r'^W:( [a-h][1-8])+ / B:( [a-h][1-8])+$')
def parse(s):
    w,b=s.split('/')
    P=lambda t:[(ord(x[0])-97,int(x[1:])) for x in t.split(':')[1].split()]
    return P(w),P(b)
def fmt(w,b):
    n=lambda s:" ".join(f"{chr(97+f)}{r}" for f,r in sorted(s))
    return f"W: {n(w)} / B: {n(b)}"
def shift(c,d): w,b=c; return [(f+d,r) for f,r in w],[(f+d,r) for f,r in b]
def mirror(c):
    w,b=c; M=max(f for f,_ in w+b); return [(M-f,r) for f,r in w],[(M-f,r) for f,r in b]
def width(c): w,b=c; return 1+max(f for f,_ in w+b)-min(f for f,_ in w+b)
cores=[]   # (position, nimber)
for fn,nim in [("cores2_all.txt",2)]:
    for l in open(f"{SD}/seeds/{fn}"):
        l=l.strip()
        if PAT.match(l): cores.append((parse(l),nim))
for fn in ["cores3_all.txt","w5p10_star3.txt"]:
    for l in open(f"{SD}/seeds/{fn}"):
        l=l.strip()
        if PAT.match(l): cores.append((parse(l),3))
small1=[];small0=[]
for l in open("small_all.tsv"):
    p,o=l.rstrip("\n").split("\t")
    if o=="NPNNNNNN": small1.append(parse(p))
    elif o=="PNNNNNNN": small0.append(parse(p))
small0=random.sample(small0,200)
def norm(c):
    m=min(f for f,_ in c[0]+c[1]); return shift(c,-m)
rows=[]
for c,a in cores:
    c=norm(c)
    for cc in (c,mirror(c)):
        cc=norm(cc)
        wc=width(cc)
        for sm,b in [(s,1) for s in small1]+[(s,0) for s in small0]:
            sm=norm(sm)
            for sc in (sm,norm(mirror(sm))):
                if wc+1+width(sc)>8: continue
                s2=shift(sc,wc+1)
                rows.append((fmt(cc[0]+s2[0],cc[1]+s2[1]),a^b,a,b))
rows=list(dict.fromkeys(rows))
print(len(rows),"combos",file=sys.stderr)
open("gapsum_in.txt","w").write("\n".join(r[0] for r in rows)+"\n")
open("gapsum_exp.tsv","w").write("\n".join(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}" for r in rows)+"\n")
