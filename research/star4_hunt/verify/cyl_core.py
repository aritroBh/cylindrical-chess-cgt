import sys, time
from cylcgt import cgt, pawns
pawns.RACE_RULE="count"; pawns.PASSED_RESPECTS_EP=True
b=pawns.Board(5,8,False,True)
for text in ["W: a2 a5 c2 d2 e2 / B: a3 a7 b5 d4 e6","W: a2 a5 c2 d3 e2 / B: a4 b7 c7 d6 e5","W: a2 b2 c2 c5 e2 / B: a6 b4 c7 d5 e3"]:
    pos=pawns.Pos.parse(text)
    for mode in ("sum","whole"):
        t=time.time(); pawns._value.cache_clear()
        if mode=="whole":
            old=pawns.components; pawns.components=lambda bd,p:[p]
        g=pawns.value(b,pos)
        print(text,mode,"value",cgt.show(g)[:60],"outcomes G+*k k=0..4:",[cgt.outcome(cgt.add(g,cgt.nimber(k))) for k in range(5)],f"{time.time()-t:.0f}s",flush=True)
        if mode=="whole": pawns.components=old
