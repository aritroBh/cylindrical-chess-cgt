import sys
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]; model=sys.argv[2]
B=Board(spec)
root=parse(B,'Ke6 Pd7 kd8 pe7 w -')
def mk(files):
    S=set('abcdefgh'.index(x) for x in files)
    def flt(B,p,m):
        lab,k,np_=m
        if k=='p': return True
        return (np_[1]%B.W) in S
    return flt
for files in ['e','def','cdefg','bcdefgh','abcdefgh']:
    idx,pl,val,mv=solve(B,model,[root],wfilter=mk(files))
    i=idx[root]
    print(spec,model,files,[ (lab,(val[t] if k=='n' else t)) for lab,k,t in mv[i]])
