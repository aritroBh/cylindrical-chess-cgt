import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames')
from cylcgt.pawns import Pos

PHASES = {'W2/B4':{'W':2,'B':4},'W3/B5':{'W':3,'B':5}}

def file_pawns(pos):
    d={}
    for (f,r) in pos.white: d.setdefault(f,[]).append(('W',r))
    for (f,r) in pos.black: d.setdefault(f,[]).append(('B',r))
    return d

def analyze(pos_str, n):
    pos=Pos.parse(pos_str)
    fp=file_pawns(pos)
    best_overall=None
    for phname,phase in PHASES.items():
        iswall=[False]*n; color=[None]*n
        for f in range(n):
            ps=fp.get(f,[])
            if len(ps)==1:
                c,r=ps[0]
                if r==phase[c]:
                    iswall[f]=True; color[f]=c
        dw=iswall+iswall; dc=color+color
        runs=[]; cur=[]
        for idx in range(2*n):
            if dw[idx] and (not cur or dc[idx]!=dc[cur[-1]]):
                cur.append(idx)
            else:
                if cur: runs.append(list(cur)); cur=[]
                if dw[idx]: cur=[idx]
        if cur: runs.append(list(cur))
        for run in runs:
            if len(run)>n: run=run[:n]
            if len(run)<1: continue
            fset=set(x%n for x in run)
            if len(fset)!=len(run): continue
            if best_overall is None or len(run)>best_overall[1]:
                best_overall=(phname,len(run),run[0]%n,frozenset(fset))
    if best_overall is None:
        return None
    phname,length,start,fset=best_overall
    core=[f for f in range(n) if f not in fset]
    corep=sum(len(fp.get(f,[])) for f in core)
    letters='abcdefghij'[:n]
    return phname,length,letters[start],''.join(letters[f] for f in sorted(fset)),''.join(letters[f] for f in core),corep

lines=open('/Users/aritro/Downloads/Research/Chessendgames/research/ring_n_plus_2/ext_w10_k2.out').read().splitlines()
nim2=[l for l in lines if l.startswith('NIM') and '\t2\t' in l]
from collections import Counter
c=Counter()
for l in nim2:
    pos=l.split('\t')[1]
    r=analyze(pos,10)
    print(f"{pos}  -> {r}")
    if r: c[(r[0],r[1])]+=1
print("wallrun counts:", c)
