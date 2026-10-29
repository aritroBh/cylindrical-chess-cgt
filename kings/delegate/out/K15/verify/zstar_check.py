import itertools, collections, sys
H=6
def moves(wp,bp,stm,om):
    res=[]; occ=wp|bp
    if stm==0:
        if om==0: res.append(('mv',wp,bp,1))
        for r in range(1,H-1):
            if wp>>r&1:
                if r+1==H-1: res.append(('promo',0,0,om))
                elif not occ>>(r+1)&1:
                    res.append(('mv',(wp&~(1<<r))|(1<<(r+1)),bp,om))
                    if r==1 and not occ>>(r+2)&1: res.append(('mv',(wp&~(1<<r))|(1<<(r+2)),bp,om))
    else:
        if om==0: res.append(('mv',wp,bp,om))   # Black passes in omega
        for r in range(1,H-1):
            if bp>>r&1:
                if r-1==0: res.append(('promo',0,0,om))
                elif not occ>>(r-1)&1:
                    res.append(('mv',wp,(bp&~(1<<r))|(1<<(r-1)),om))
                    if r==H-2 and not occ>>(r-2)&1: res.append(('mv',wp,(bp&~(1<<r))|(1<<(r-2)),om))
    return res
M=0b011110
states=[(w,b,s,o) for w in range(1<<H) for b in range(1<<H) if not (w&b) and not (w&~M) and not (b&~M) for s in (0,1) for o in (0,1)]
val={st:0 for st in states}
ch=True
while ch:
    ch=False
    for st in states:
        if val[st]!=0: continue
        w,b,s,o=st; win=False; allopp=True
        mv=moves(w,b,s,o)
        if not mv: val[st]=2; ch=True; continue   # no move: loses
        for k,nw,nb,no in mv:
            if k=='promo': win=True; break
            v=val[(nw,nb,1-s,no)]
            if v==2: win=True; break
            if v!=1: allopp=False
        if win: val[st]=1; ch=True
        elif allopp: val[st]=2; ch=True
def wp_(w,b,s,o):
    v=val[(w,b,s,o)]
    if v==0: return 'D'
    return 'W' if (v==1)==(s==0) else 'L'
grp="Kd5 kb5 Pa3 Pb2 Pd2 pa4 pc5 pd4"
for fl in sys.argv[1:]:
    pos=[];pred=[]
    for ctx in itertools.product('.WB',repeat=4):
        if sum(c!='.' for c in ctx)>3: continue
        w=b=0;s=''
        for i,c in enumerate(ctx):
            r=i+1
            if c=='W': w|=1<<r; s+=f' P{fl}{r+1}'
            if c=='B': b|=1<<r; s+=f' p{fl}{r+1}'
        for stm in (0,1):
            pos.append(f'{grp}{s} {"w" if stm==0 else "b"} -'); pred.append(wp_(w,b,stm,0))
    open(f'zs_{fl}_pos.in','w').write('\n'.join(pos)+'\n'); open(f'zs_{fl}_pred.txt','w').write('\n'.join(pred)+'\n')
    print(fl,len(pos),collections.Counter(pred))
