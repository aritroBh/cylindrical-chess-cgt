import sys
sys.argv=[sys.argv[0],"none"]
exec(open("decomp2.py").read().split("mode=sys.argv[1]")[0])
for c in ["W: a2 a3 b4 c2 c3 e3 f4 / B: b5 b7 d5 e7 f7","W: a2 a3 c3 d4 e2 e3 f4 / B: b5 c7 d7 f5 f7","W: a2 a4 c2 c3 e3 f4 / B: a5 b6 b7 d5 e7 f7"]:
    print("==",c,"value",ev([c])[0])
    rows=list(removals(c,2)); vals=ev([r[0] for r in rows])
    for (txt,(gw,gb)),v in zip(rows,vals):
        if v=="2":
            grp=fmt(gw,gb) if gw and gb else None
            print("  removing W",[f"{chr(97+f)}{r}" for f,r in gw],"B",[f"{chr(97+f)}{r}" for f,r in gb],"-> *2 remainder:",txt,"| removed group alone:",ev([grp])[0] if grp else "(one colour only)")
    # 1-pawn removals
    rows1=list(removals(c,1)); v1=ev([r[0] for r in rows1])
    print("  single-pawn removals giving a nimber:",[(r[1],v) for r,v in zip(rows1,v1) if v in "0123"])
