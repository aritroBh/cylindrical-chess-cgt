import sys, time
from cylcgt import cgt, pawns
pawns.RACE_RULE="count"; pawns.PASSED_RESPECTS_EP=True
text="W: a2 b2 b3 c2 e2 / B: b5 b6 b7 c4 e6"
pos=pawns.Pos.parse(text)
b=pawns.Board(5,8,False,True)
def star(n):
    return cgt.nimber(n)
for mode in ("whole","sum"):
    t=time.time()
    pawns._value.cache_clear()
    if mode=="whole":
        old=pawns.components; pawns.components=lambda bd,p:[p]
    g=pawns.value(b,pos)
    res=[]
    for k in range(0,4):
        res.append(cgt.outcome(cgt.add(g,star(k))))
    print(mode, cgt.show(g), res, f"{time.time()-t:.1f}s", flush=True)
    if mode=="whole": pawns.components=old
