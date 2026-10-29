# independent exhaustive file-g context test for G8a / G8b on cyl:8x6 : prediction by own pawn-only game with free passes
import itertools, subprocess, sys, collections
H=6
# ---- own predictor: pawns on one file, both sides may pass at will, promotion wins, infinite play = draw
def moves(wp,bp,stm):
    res=[('pass',wp,bp)]
    occ=wp|bp
    if stm==0:
        for r in range(1,H):            # rank index 1..H-1 (0-based ranks 1..4 hold pawns) ; pawn at 0-based rank r
            if wp>>r&1:
                if r+1==H-1: res.append(('promo',0,0)); 
                elif not occ>>(r+1)&1:
                    res.append(('mv',(wp&~(1<<r))|(1<<(r+1)),bp))
                    if r==1 and not occ>>(r+2)&1: res.append(('mv',(wp&~(1<<r))|(1<<(r+2)),bp))
    else:
        for r in range(1,H-1):
            if bp>>r&1:
                if r-1==0: res.append(('promo',0,0))
                elif not occ>>(r-1)&1:
                    res.append(('mv',wp,(bp&~(1<<r))|(1<<(r-1))))
                    if r==H-2 and not occ>>(r-2)&1: res.append(('mv',wp,(bp&~(1<<r))|(1<<(r-2))))
    return res
# states: (wp,bp,stm); value for mover: 1 win, 2 loss, 0 draw
states=[(w,b,s) for w in range(1<<H) for b in range(1<<H) if not (w&b) and not (w&~0b011110) and not (b&~0b011110) for s in (0,1)]
val={st:0 for st in states}
changed=True
while changed:
    changed=False
    for st in states:
        if val[st]!=0: continue
        w,b,s=st; allopp=True; win=False
        for k,nw,nb in moves(w,b,s):
            if k=='promo': win=True; break
            v=val[(nw,nb,1-s)]
            if v==2: win=True; break
            if v!=1: allopp=False
        if win: val[st]=1; changed=True
        elif allopp: val[st]=2; changed=True   # every move (incl. pass) loses
def whitepov(w,b,s):
    v=val[(w,b,s)]
    if v==0: return 'D'
    return 'W' if (v==1)==(s==0) else 'L'
groups={'G8a':[("b2","c2"),("c4","d4"),"Pa3 Pe2 pa4 pe3"],'G8b':[("b3","c3"),("c5","d5"),"Pa4 Pe3 pa5 pe4"]}
pos=[];pred=[]
for gname,(wks,bks,paw) in groups.items():
    for wk in wks:
        for bk in bks:
            for ctx in itertools.product('.WB',repeat=4):
                w=b=0; s=''
                for i,c in enumerate(ctx):
                    r=i+1  # ranks 2..5 -> 0-based 1..4
                    if c=='W': w|=1<<r; s+=f' Pg{r+1}'
                    if c=='B': b|=1<<r; s+=f' pg{r+1}'
                for stm in (0,1):
                    pos.append(f'K{wk} k{bk} {paw}{s} {"w" if stm==0 else "b"} -')
                    pred.append(whitepov(w,b,stm))
open('ctx_g8_pos.in','w').write('\n'.join(pos)+'\n')
open('ctx_g8_pred.txt','w').write('\n'.join(pred)+'\n')
print(len(pos),collections.Counter(pred))
