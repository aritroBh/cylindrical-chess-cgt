import sys
sys.argv=[sys.argv[0],"none"]
exec(open("decomp2.py").read().split("mode=sys.argv[1]")[0])
P="W: a2 a3 b4 c2 c3 e3 f4 / B: b5 b7 d5 e7 f7"
Pp="W: a3 b4 c2 c3 e3 f4 / B: b5 d5 e7 f7"
print("P",ev([P])[0],"P'",ev([Pp])[0],"pair alone",ev(["W: a2 / B: b7"])[0])
import collections
for c in (Pp,P):
    allp=None
    print("== sub-positions of",c)
    for k in range(1,5):
        rows=list(removals(c,k)); vals=ev([r[0] for r in rows])
        cnt=collections.Counter(vals)
        nims=[(r[0],v) for r,v in zip(rows,vals) if v in ("1","2","3","4","5")]
        print(" k=%d: nimber census %s"%(k,dict(cnt)))
        for x in nims[:6]: print("     ",x)
