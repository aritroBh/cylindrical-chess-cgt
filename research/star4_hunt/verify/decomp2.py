import glob, itertools, os, re, subprocess, sys, collections
SD="/Users/aritro/Downloads/Research/Chessendgames/research/star4_hunt"
S2="./s2"
def parse(s):
    w,b=s.split('/')
    P=lambda t:[(ord(x[0])-97,int(x[1:])) for x in t.split(':')[1].split()]
    return sorted(P(w)),sorted(P(b))
def fmt(w,b):
    n=lambda s:" ".join(f"{chr(97+f)}{r}" for f,r in sorted(s))
    return f"W: {n(w)} / B: {n(b)}"
def canon(s):
    # up to mirror (within the occupied span) and colour reversal
    w,b=parse(s)
    def norm(w,b):
        m=min(f for f,_ in w+b); return sorted((f-m,r) for f,r in w),sorted((f-m,r) for f,r in b)
    def mirror(w,b):
        M=max(f for f,_ in w+b); return sorted((M-f,r) for f,r in w),sorted((M-f,r) for f,r in b)
    def rev(w,b): return sorted((f,9-r) for f,r in b),sorted((f,9-r) for f,r in w)
    c=[]
    w0,b0=norm(w,b)
    for (x,y) in (( w0,b0),mirror(w0,b0),rev(w0,b0),mirror(*rev(w0,b0))):
        c.append((tuple(x),tuple(y)))
    best=min(c)
    return fmt(list(best[0]),list(best[1]))
cache={}
def ev(poss):
    need=[p for p in set(poss) if p not in cache]
    for i in range(0,len(need),3000):
        chunk=need[i:i+3000]
        open("_dc_in.txt","w").write("\n".join(chunk)+"\n")
        out=subprocess.run([S2,"eval","8","_dc_in.txt"],capture_output=True,text=True).stdout.splitlines()[1:]
        for p,l in zip(chunk,out):
            t=l.split("\t"); cache[p]=(t[4] if len(t)>4 and t[3] in "NLRP" else t[3] if len(t)>3 else "?")
    return [cache[p] for p in poss]
def removals(c,k):
    w,b=parse(c); allp=[('W',p) for p in w]+[('B',p) for p in b]
    for comb in itertools.combinations(range(len(allp)),k):
        w2=[p for i,(s,p) in enumerate(allp) if s=='W' and i not in comb]
        b2=[p for i,(s,p) in enumerate(allp) if s=='B' and i not in comb]
        if w2 and b2:
            gw=[p for i,(s,p) in enumerate(allp) if s=='W' and i in comb]; gb=[p for i,(s,p) in enumerate(allp) if s=='B' and i in comb]
            yield fmt(w2,b2),(gw,gb)
mode=sys.argv[1]
if mode=="pairs13":
    cores=[l.strip() for l in open(f"{SD}/seeds/cores3_all.txt") if l.startswith("W:")]+[l.strip() for l in open(f"{SD}/seeds/w5p10_star3.txt") if l.startswith("W:")]
    print(len(cores),"cores"); bad=0
    for c in cores:
        rows=list(removals(c,2)); vals=ev([r[0] for r in rows]); self_val=ev([c])[0]
        hits=[(r,v) for r,v in zip(rows,vals) if v=="2"]
        # the removed groups
        gv=ev([fmt(g[0],g[1]) if g[0] and g[1] else "W: a2 / B: a2" for r,g in [(x[0],x[0][1]) for x in hits]]) if hits else []
        print(c,"| value",self_val,"| removals leaving *2:",len(hits),"| removed pair alone:",[ (fmt(*h[0][1][:2]) if True else '', g) for h,g in zip(hits,gv)][:3])
elif mode=="star2":
    cores=[l.strip() for l in open(f"{SD}/seeds/cores2_all.txt") if l.startswith("W:")]
    print(len(cores),"cores"); red=0
    for c in cores:
        v=ev([c])[0]
        if v!="2": print("NOT *2:",c,v)
        rows=list(removals(c,1))+list(removals(c,2)); vals=ev([r[0] for r in rows])
        if any(x=="2" for x in vals): red+=1; print("reducible:",c)
    print("reducible by 1-2 pawn removal to *2:",red)
elif mode=="w5p10_star2":
    PAT=re.compile(r'^W:( [a-h][1-8])+ / B:( [a-h][1-8])+$')
    pos=set()
    for fn in glob.glob(f"{SD}/out/w5p10/*.tsv"):
        for line in open(fn):
            p=line.rstrip("\n").split("\t")
            if p[0].startswith("W:") and len(p)>=5 and p[4]=="2" and PAT.match(p[0]): pos.add(canon(p[0]))
    print(len(pos),"distinct *2 positions (up to mirror/colour)")
    prim=0; red=[]
    for c in sorted(pos):
        v=ev([c])[0]
        assert v=="2",(c,v)
        rows=list(removals(c,1))+list(removals(c,2)); vals=ev([r[0] for r in rows])
        if any(x=="2" for x in vals): red.append(c)
        else: prim+=1
    print("primitive (no removal of 1-2 pawns leaves *2):",prim,"reducible:",len(red))
elif mode=="star3_all":
    PAT=re.compile(r'^W:( [a-h][1-8])+ / B:( [a-h][1-8])+$')
    found=set()
    for f in glob.glob(f"{SD}/out/*.out")+glob.glob(f"{SD}/out/w5p10/*.tsv")+glob.glob(f"{SD}/out/w4p11/*.tsv"):
        b_=os.path.basename(f)
        if b_.startswith(("r1_","r3_","r4_","rsa","j4_")): continue
        for line in open(f):
            p=line.rstrip("\n").split("\t")
            if len(p)>=5 and p[4]=="nim=3" and PAT.match(p[1]): found.add(canon(p[1]))
            elif len(p)>=5 and p[0].startswith("W:") and p[4]=="3" and not line.startswith("#") and PAT.match(p[0]): found.add(canon(p[0]))
    print(len(found),"distinct *3 positions (mine: up to mirror/colour)")
    vals=ev(sorted(found)); print("S2 values:",collections.Counter(vals))
    dec=0; nodec=[]; pairok=0; pairbad=[]; core_prim=0; core_red=[]
    for c in sorted(found):
        rows=list(removals(c,2)); vals=ev([r[0] for r in rows])
        hits=[(r,v) for r,v in zip(rows,vals) if v=="2"]
        if not hits: nodec.append(c); continue
        dec+=1
        # pair alone *1 ?  (pair must contain one W and one B)
        okp=False
        for (txt,(gw,gb)),v in hits:
            if len(gw)==1 and len(gb)==1:
                if ev([fmt(gw,gb)])[0]=="1": okp=True
        if okp: pairok+=1
        else: pairbad.append(c)
    print("decomposable by removing a pair to *2:",dec,"; not:",len(nodec)); print("  not decomposable:",nodec)
    print("of the decomposable: some W/B pair alone is *1 for",pairok,"; otherwise:",len(pairbad))
    for c in pairbad[:10]: print("   ",c)
