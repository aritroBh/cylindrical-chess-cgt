import itertools,sys,json
comps={'zero':{'W':[],'B':[]},'on':{'W':['on'],'B':[]},'off':{'W':[],'B':['off']},'dud':{'W':['dud'],'B':['dud']},
       'over':{'W':['zero'],'B':['over']},'under':{'W':['under'],'B':['zero']}}
# tempo: ctx bit0 private W, bit1 private B, bit2 shared
def moves(c,ctx,s):
    res=[]
    for n in comps[c]['W' if s==0 else 'B']: res.append((n,ctx))
    pb=1 if s==0 else 2
    if ctx&pb: res.append((c,ctx&~pb))
    if ctx&4: res.append((c,ctx&~4))
    return res
states=[(c,ctx,s) for c in comps for ctx in range(8) for s in (0,1)]
val={st:0 for st in states}   # 0 draw 1 mover wins 2 mover loses
ch=True
while ch:
    ch=False
    for st in states:
        if val[st]!=0: continue
        c,ctx,s=st; mv=moves(c,ctx,s)
        if not mv: val[st]=2; ch=True; continue
        win=False; allopp=True
        for n,c2 in mv:
            v=val[(n,c2,1-s)]
            if v==2: win=True;break
            if v!=1: allopp=False
        if win: val[st]=1; ch=True
        elif allopp: val[st]=2; ch=True
def sig(c):
    out=''
    for ctx in range(8):
        for s in (0,1):
            v=val[(c,ctx,s)]
            out+= 'D' if v==0 else ('W' if (v==1)==(s==0) else 'L')
    return out
SIG={c:sig(c) for c in comps}
if __name__=='__main__':
    for c,v in SIG.items(): print(c,v)
