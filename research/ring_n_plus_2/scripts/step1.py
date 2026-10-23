import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames')
from cylcgt.pawns import Board, Pos

PHASES = {
 'W2/B4': {'W':2,'B':4},
 'W3/B5': {'W':3,'B':5},
}

def file_pawns(pos):
    d={}
    for (f,r) in pos.white:
        d.setdefault(f,[]).append(('W',r))
    for (f,r) in pos.black:
        d.setdefault(f,[]).append(('B',r))
    return d

def analyze(pos_str, n):
    pos=Pos.parse(pos_str)
    fp=file_pawns(pos)
    best_overall=None
    for phname,phase in PHASES.items():
        iswall=[False]*n
        color=[None]*n
        for f in range(n):
            ps=fp.get(f,[])
            if len(ps)==1:
                c,r=ps[0]
                if r==phase[c]:
                    iswall[f]=True
                    color[f]=c
        dw=iswall+iswall
        dc=color+color
        runs=[]
        cur=[]
        for idx in range(2*n):
            if dw[idx] and (not cur or dc[idx]!=dc[cur[-1]]):
                cur.append(idx)
            else:
                if cur:
                    runs.append(list(cur)); cur=[]
                if dw[idx]:
                    cur=[idx]
        if cur:
            runs.append(list(cur))
        for run in runs:
            if len(run)>n:
                run=run[:n]
            if len(run)<1: continue
            fset=set(x%n for x in run)
            if len(fset)!=len(run): continue
            if best_overall is None or len(run)>best_overall[1]:
                best_overall=(phname,len(run),run[0]%n,frozenset(fset))
    if best_overall is None:
        return None
    phname,length,start,fset=best_overall
    core_files=[f for f in range(n) if f not in fset]
    core_pawns=sum(len(fp.get(f,[])) for f in core_files)
    return phname,length,start,sorted(fset),core_files,core_pawns

lines=[l.strip() for l in open('/Users/aritro/Downloads/Research/Chessendgames/research/star26_rings/c8/p10_5_5_hits.tsv') if l.strip()]
for ln in lines:
    if 'N,2' not in ln:
        continue
    posstr=ln.split('\t')[0]
    res=analyze(posstr,8)
    letters='abcdefgh'
    if res is None:
        print(f"{posstr}\n   NO WALL RUN"); continue
    ph,length,start,fset,core,corep=res
    core_letters=''.join(letters[f] for f in core)
    wall_letters=''.join(letters[f] for f in sorted(fset))
    print(f"{posstr}")
    print(f"   phase={ph} wallrun_len={length} start_file={letters[start]} wall_files={wall_letters} core_files={core_letters} core_pawns={corep}")
