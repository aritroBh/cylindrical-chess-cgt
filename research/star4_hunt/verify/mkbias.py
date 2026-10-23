import random, sys
random.seed(int(sys.argv[1])); N=int(sys.argv[2]); out=sys.argv[3]
def fmt(W,B):
    n=lambda s:" ".join(sorted(f"{chr(97+f)}{r}" for f,r in s))
    return f"W: {n(W)} / B: {n(B)}"
def valid(W,B,wd):
    if W&B: return False
    for f,r in W:
        if not any(abs(g-f)<=1 and s>r for g,s in B): return False
    for f,r in B:
        if not any(abs(g-f)<=1 and s<r for g,s in W): return False
    return all(any(g==f for g,_ in W|B) for f in range(wd))
res=set()
wr=[2,2,2,3,4,4,5,6]; br=[7,7,7,6,5,5,4,3]
while len(res)<N:
    wd=random.choice([4,5,5,6])
    nw=random.randint(3,6); nb=random.randint(3,6)
    W=set();B=set()
    while len(W)<nw: W.add((random.randrange(wd),random.choice(wr)))
    while len(B)<nb: B.add((random.randrange(wd),random.choice(br)))
    W=frozenset(W);B=frozenset(B)
    if valid(W,B,wd): res.add((wd,fmt(W,B)))
for wd in (4,5,6):
    open(f"{out}_w{wd}.txt","w").write("\n".join(sorted(s for w,s in res if w==wd))+"\n")
    print(wd,sum(1 for w,s in res if w==wd))
