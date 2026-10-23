import random, sys
random.seed(int(sys.argv[1])); N=int(sys.argv[2]); out=sys.argv[3]
def fmt(W,B):
    n=lambda s:" ".join(sorted(f"{chr(97+f)}{r}" for f,r in s))
    return f"W: {n(W)} / B: {n(B)}"
def valid(W,B):
    if W&B: return False
    for f,r in W:
        if not any(abs(g-f)<=1 and s>r for g,s in B): return False
    for f,r in B:
        if not any(abs(g-f)<=1 and s<r for g,s in W): return False
    return True
res=set()
while len(res)<N:
    wd=random.choice([6,7,8])
    gap=random.randint(1,wd-2)           # one empty file, both sides non-empty
    files=[f for f in range(wd) if f!=gap]
    nw=random.randint(2,5); nb=random.randint(2,5)
    W=set();B=set()
    while len(W)<nw: W.add((random.choice(files),random.randint(2,6)))
    while len(B)<nb: B.add((random.choice(files),random.randint(3,7)))
    W=frozenset(W);B=frozenset(B)
    if not valid(W,B): continue
    # both parts must be non-empty
    if not any(f<gap for f,_ in W|B) or not any(f>gap for f,_ in W|B): continue
    res.add(fmt(W,B))
open(out,"w").write("\n".join(sorted(res))+"\n")
