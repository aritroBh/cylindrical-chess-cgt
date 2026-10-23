import sys
sys.argv=[sys.argv[0],"none"]
exec(open("decomp2.py").read().split("mode=sys.argv[1]")[0])
c="W: a2 a3 a4 c2 d2 e4 / B: a7 b6 c5 d6 f6 f7"
print(c,ev([c])[0])
for k in (1,2,3,4):
    rows=list(removals(c,k)); vals=ev([r[0] for r in rows])
    for (txt,(gw,gb)),v in zip(rows,vals):
        if v in ("2","3"):
            g=fmt(gw,gb) if gw and gb else None
            print(" k=%d remove W%s B%s -> %s value *%s | removed group alone: %s"%(k,[f'{chr(97+f)}{r}' for f,r in gw],[f'{chr(97+f)}{r}' for f,r in gb],txt,v,ev([g])[0] if g else "n/a"))
