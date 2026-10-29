import sys, collections, pickle
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]
B=Board(spec)
E=4
def mkT(rows_files):
    # rows_files: list of (drow, [file offsets]) : squares (rank r - drow, file e+off)
    def T(rank):
        out=set()
        for d,offs in rows_files:
            rr=rank-d
            if 1<=rr<=B.H:
                for o in offs:
                    f=E+o
                    if B.cyl: f%=B.W
                    elif not (0<=f<B.W): continue
                    out.add((rr-1)*B.W+f)
        return out
    return T
def run(T,name):
    def flt(B,p,m):
        lab,k,np_=m
        if k=='p': return True
        bp=np_[4]
        if not bp: return True
        rank=B.r(bp[0])+1
        return np_[1] in T(rank)
    root=parse(B,'Ke6 Pd7 kd8 pe7 w -')
    idx,pl,val,mv=solve(B,'P',[root],wfilter=flt)
    i=idx[root]
    print(spec,name,[(lab,(val[t] if k=='n' else t)) for lab,k,t in mv[i]], len(pl))
run(mkT([(1,[0]),(2,[-1,0,1])]),'T4: e(r-1), d/e/f(r-2)')
run(mkT([(1,[0]),(2,[-1,0,1]),(3,[-1,0,1])]),'T7: + d/e/f(r-3)')
run(mkT([(1,[0]),(2,[-1,0,1]),(3,[0])]),'T5: + e(r-3)')
run(mkT([(1,[0]),(2,[0])]),'T2: e(r-1),e(r-2)')
run(mkT([(1,[0]),(2,[0,-1])]),'T3L')
run(mkT([(1,[0]),(2,[0,1])]),'T3R')
