import glob, re, random, itertools, collections
SD="/Users/aritro/Downloads/Research/Chessendgames/research/star4_hunt"
PAT=re.compile(r'^W:( [a-h][1-8])+ / B:( [a-h][1-8])+$')
def parse(s):
    w,b=s.split('/')
    P=lambda t:[(ord(x[0])-97,int(x[1:])) for x in t.split(':')[1].split()]
    return frozenset(P(w)),frozenset(P(b))
def fmt(W,B):
    n=lambda s:" ".join(sorted(f"{chr(97+f)}{r}" for f,r in s))
    return f"W: {n(W)} / B: {n(B)}"
hits=set()
for d in ["w5p10","w4p11"]:
    for fn in glob.glob(f"{SD}/out/{d}/*.tsv"):
        for line in open(fn):
            if line.startswith('#'): continue
            p=line.rstrip('\n').split('\t')
            cand=None
            if p[0].startswith('NEAR'): cand=p[1]
            elif p[0].startswith('W:') and len(p)>=5 and p[4].lstrip('-').isdigit() and int(p[4])>=2: cand=p[0]
            if cand and PAT.match(cand): hits.add(cand)
for fn in ["star2_flat_all.txt","cores3_all.txt","s3_ext_all_pos.txt","cores2_all.txt","star3_found_ext.txt"]:
    for line in open(f"{SD}/seeds/{fn}"):
        c=line.rstrip('\n').split('\t')[0]
        if PAT.match(c): hits.add(c)
print(len(hits),"base positions")
base=[parse(h) for h in hits]
def width(W,B): return 1+max(f for f,_ in list(W)+list(B))
def valid(W,B):
    if W&B: return False
    if any(not(2<=r<=6) for f,r in W) or any(not(3<=r<=7) for f,r in B): return False
    for f,r in W:
        if not any(abs(g-f)<=1 and s>r for g,s in B): return False
    for f,r in B:
        if not any(abs(g-f)<=1 and s<r for g,s in W): return False
    return True
random.seed(5)
def reloc(W,B,wd):
    res=[]
    pawns=[(0,p) for p in W]+[(1,p) for p in B]
    for col,(f,r) in pawns:
        for df in (-1,0,1):
            for dr in (-2,-1,0,1,2):
                if df==0 and dr==0: continue
                g,s=f+df,r+dr
                if not(0<=g<wd): continue
                if col==0: W2=(W-{(f,r)})|{(g,s)}; B2=B
                else: B2=(B-{(f,r)})|{(g,s)}; W2=W
                res.append((frozenset(W2),frozenset(B2)))
    return res
one=set(); two=set()
for W,B in base:
    wd=max(5,width(W,B))
    first=[x for x in reloc(W,B,wd) if len(x[0])==len(W)]
    for W1,B1 in first:
        if valid(W1,B1): one.add((wd,fmt(W1,B1)))
    for (W1,B1) in random.sample(first,min(len(first),40)):
        second=[x for x in reloc(W1,B1,wd) if len(x[0])==len(W1)]
        for (W2,B2) in random.sample(second,min(len(second),25)):
            if valid(W2,B2): two.add((wd,fmt(W2,B2)))
print(len(one),"one-move neighbours",len(two),"two-move neighbours")
by=collections.defaultdict(set)
for wd,s in one|two: by[wd].add(s)
for wd,l in sorted(by.items()):
    open(f"nb_w{wd}.txt","w").write("\n".join(sorted(l))+"\n"); print(wd,len(l))
by2=collections.defaultdict(list)
for h in hits:
    W,B=parse(h); by2[max(5,width(W,B))].append(h)
for wd,l in by2.items(): open(f"hits_w{wd}.txt","w").write("\n".join(sorted(l))+"\n"); print("hits",wd,len(l))
