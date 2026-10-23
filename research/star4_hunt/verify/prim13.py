import sys
sys.argv=[sys.argv[0],"none"]
exec(open("decomp2.py").read().split("mode=sys.argv[1]")[0])
SD="/Users/aritro/Downloads/Research/Chessendgames/research/star4_hunt"
cores=[l.strip() for l in open(f"{SD}/seeds/cores3_all.txt") if l.startswith("W:")]+[l.strip() for l in open(f"{SD}/seeds/w5p10_star3.txt") if l.startswith("W:")]
star2=set(canon(l.strip()) for l in open(f"{SD}/seeds/cores2_all.txt") if l.startswith("W:"))
allprim=0; inlist=0
for c in cores:
    rows=list(removals(c,2)); vals=ev([r[0] for r in rows])
    rem=[r[0] for r,v in zip(rows,vals) if v=="2"]
    assert len(rem)==1
    r=rem[0]
    sub=list(removals(r,1))+list(removals(r,2)); sv=ev([x[0] for x in sub])
    prim=not any(v=="2" for v in sv)
    allprim+=prim; inlist+= canon(r) in star2
    print(c,"-> remainder",r,"primitive:",prim,"| in the 35-core list:",canon(r) in star2)
print("primitive remainders:",allprim,"of",len(cores),"; remainders in the 35-core list:",inlist)
