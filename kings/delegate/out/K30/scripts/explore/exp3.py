import sys, collections, itertools
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]; model=sys.argv[2]
B=Board(spec)
root=parse(B,'Ke6 Pd7 kd8 pe7 w -')
def mk(files,lo,hi,allow_row_ge_pawn=False):
    S=set('abcdefgh'.index(x) for x in files)
    def flt(B,p,m):
        lab,k,np_=m
        if k=='p': return True
        wk=np_[1]
        if (wk%B.W) not in S: return False
        # pawn rank (black pawn) after the move; if no black pawn: anything
        bp=np_[4]
        if not bp: return True
        pr=B.r(bp[0])
        wr=B.r(wk)
        d=pr-wr   # distance in front (>=1 in front)
        return lo<=d<=hi
    return flt
for lo,hi in [(1,2),(1,3),(1,4),(2,3),(2,2),(1,5),(0,3),(-1,3),(-9,9)]:
    idx,pl,val,mv=solve(B,model,[root],wfilter=mk('def',lo,hi))
    i=idx[root]
    print(spec,model,lo,hi,[ (lab,(val[t] if k=='n' else t)) for lab,k,t in mv[i]])
