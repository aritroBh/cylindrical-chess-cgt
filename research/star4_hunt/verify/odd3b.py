import sys
sys.argv=[sys.argv[0],"none"]
exec(open("decomp2.py").read().split("mode=sys.argv[1]")[0])
SD="/Users/aritro/Downloads/Research/Chessendgames/research/star4_hunt"
known=set(canon(l.strip()) for l in open(f"{SD}/seeds/cores3_all.txt") if l.startswith("W:"))|set(canon(l.strip()) for l in open(f"{SD}/seeds/w5p10_star3.txt") if l.startswith("W:"))
for c in ["W: a2 a3 b4 c2 c3 e3 f4 / B: b5 b7 d5 e7 f7","W: a2 a3 c3 d4 e2 e3 f4 / B: b5 c7 d7 f5 f7","W: a2 a4 c2 c3 e3 f4 / B: a5 b6 b7 d5 e7 f7"]:
    print("==",c)
    best=None
    for k in range(1,7):
        rows=list(removals(c,k)); vals=ev([r[0] for r in rows])
        hits=[r[0] for r,v in zip(rows,vals) if v=="3"]
        if hits:
            print("  k=%d: %d sub-positions with value *3, e.g. %s ; in the 13-core list: %s"%(k,len(hits),hits[0],[canon(h) in known for h in hits][:5]))
            best=k
        else:
            if best is not None: break
