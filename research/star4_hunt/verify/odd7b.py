import sys, collections
sys.argv=[sys.argv[0],"none"]
exec(open("decomp2.py").read().split("mode=sys.argv[1]")[0])
SD="/Users/aritro/Downloads/Research/Chessendgames/research/star4_hunt"
known=set(canon(l.strip()) for l in open(f"{SD}/seeds/cores3_all.txt") if l.startswith("W:"))|set(canon(l.strip()) for l in open(f"{SD}/seeds/w5p10_star3.txt") if l.startswith("W:"))
c="W: a2 a3 a4 c2 d2 e4 / B: a7 b6 c5 d6 f6 f7"
for k in range(1,7):
    rows=list(removals(c,k)); vals=ev([r[0] for r in rows])
    cnt=collections.Counter(vals)
    h=[r[0] for r,v in zip(rows,vals) if v=="3"]
    print("k=%d census %s | *3 sub-positions: %d %s"%(k,dict(cnt),len(h),[(x,canon(x) in known) for x in h[:3]]))
rem="W: a4 c2 d2 e4 / B: b6 c5 d6 f6 f7"
print("remainder",rem,ev([rem])[0],"; in 35-core list? (it has 9 pawns)")
for k in (1,2,3):
    rows=list(removals(rem,k)); vals=ev([r[0] for r in rows]); print(" remainder k=%d:"%k,dict(collections.Counter(vals)),[ (r[0],v) for r,v in zip(rows,vals) if v=="2"][:3])
