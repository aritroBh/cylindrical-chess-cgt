import itertools, os, subprocess, sys
sys.argv=[sys.argv[0],"none"]
exec(open("decomp2.py").read().split("mode=sys.argv[1]")[0])
def evr(poss, width=7):
    need=[p for p in set(poss) if p not in cache]
    for i in range(0,len(need),3000):
        chunk=need[i:i+3000]
        open("_dc_in.txt","w").write("\n".join(chunk)+"\n")
        env=dict(os.environ,S2_WRAP="1")
        out=subprocess.run(["./s2w","eval",str(width),"_dc_in.txt"],capture_output=True,text=True,env=env).stdout.splitlines()[1:]
        for p,l in zip(chunk,out):
            t=l.split("\t"); cache[p]=(t[4] if len(t)>4 and t[3] in "NLRP" else t[3] if len(t)>3 else "?")
    return [cache[p] for p in poss]
nm=lambda s,p:f"{s}{chr(97+p[0])}{p[1]}"
for c in [l.strip() for l in open("/Users/aritro/Downloads/Research/Chessendgames/research/star4_hunt/seeds/c7_reps.txt") if l.startswith("W:")]:
    v=evr([c])[0]; found=[]
    w,b=parse(c); allp=[('W',p) for p in w]+[('B',p) for p in b]
    for k in (1,2,3,4):
        rows=[]
        for comb in itertools.combinations(range(len(allp)),k):
            w2=[p for i,(s,p) in enumerate(allp) if s=='W' and i not in comb]; b2=[p for i,(s,p) in enumerate(allp) if s=='B' and i not in comb]
            if w2 and b2: rows.append((fmt(w2,b2),[nm(*allp[i]) for i in comb]))
        vals=evr([r[0] for r in rows])
        found+=[(r[1],x) for r,x in zip(rows,vals) if x in ("2","3")]
    print(c,"| value",v,"| removals (1-4 pawns) leaving *2/*3:",found if found else "none")
