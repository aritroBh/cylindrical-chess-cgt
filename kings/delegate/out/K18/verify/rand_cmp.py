import sys,time
sys.path.insert(0,'.')
from vlg import *
tot=bad=0
for W,H,fn in [(8,6,'rand_8x6_a'),(7,6,'rand_7x6_a')]:
    B=Board(W,H,True,[0,1,2])
    G={(qc,k):Game(B,0,qc) for qc in (False,True) for k in (0,None)}
    A={l.split(' | ')[0]:l.split(' | ')[1].split() for l in open('../keep/%s.lg'%fn)}
    for key,theirs in A.items():
        toks=key.split()
        pos=parse(B,' '.join(toks[:-2]))
        ep=toks[-1]
        if ep!='-':
            pos=pos[:4]+(((int(ep[1:])-1)*W+ord(ep[0])-97),)
        vals=[]
        for (qc,k) in ((False,0),(True,0),(False,None),(True,None)):   # plain/P plain/Q pass/P pass/Q
            T=G[(qc,k)].least_T(pos,k,20)
            vals.append('inf' if T is None else str(T))
        mine=['plain/P=%s'%vals[0],'plain/Q=%s'%vals[1],'pass/P=%s'%vals[2],'pass/Q=%s'%vals[3]]
        tot+=1
        if mine!=theirs:
            bad+=1; print('MISMATCH',key,mine,theirs)
    print(fn,len(A),'positions, finite:',sum(1 for t in A.values() if any('inf' not in x for x in t)),'with ep:',sum(1 for k in A if k.split()[-1]!='-'))
print('total',tot,'mismatches',bad)
