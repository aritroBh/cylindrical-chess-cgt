"""Referee: for a sample of real-kings hits (cyl:6x6), re-derive with MY solver (psolve) + MY D (dgame):
X: P=W, V1b,V2,V3,V4 hold, V1a fails; D(Black first)=Black.  Twins (black king on b(r+2) or b(r)): clean iff both
sides to move are legal, V1..V4 all hold at every reachable position, and P == D for both sides.
usage: twincheck.py <spec> <hits.json> <start> <step> <n>"""
import sys, json, re
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import psolve, vcheck
from dgame import *

def analyze(S, pb, bd, FZ, root):
    seen=set(); stack=[root]; res=dict(V1a=True,V1b=True,V2=True,V3=True,V4=True)
    while stack:
        p=stack.pop()
        if p in seen: continue
        seen.add(p); side=p[4]; me='W' if side==0 else 'B'
        ms=S.succ[p]
        if not ms: res['V1b']=False
        cp=vcheck.ctx_pos(pb,bd,p,FZ)
        if not vcheck._safe(bd,cp): res['V4']=False
        dopts={(c[0],c[1]):c for c in gen(bd,cp,me)}
        nonZ={}
        for kind_,q,lab in ms:
            if kind_=='P': res['V2']=False; continue
            isZ=(kind_=='K') or (kind_=='p' and vcheck.pawn_file(lab) in FZ)
            v={'W':'L','L':'W','D':'D'}[S.val[q]]
            if isZ:
                if v!='L': res['V3']=False
            else:
                cq=vcheck.ctx_pos(pb,bd,q,FZ); nonZ[(cq[0],cq[1])]=(q,v)
        if set(nonZ)!=set(dopts): res['V1a']=False
        for k,(q,v) in nonZ.items():
            if k not in dopts: continue
            c=dopts[k]; t=terminal(bd,c)
            if t is None:
                if q not in seen: stack.append(q)
            else:
                ben=('W' if t==1 else 'B') if t!=0 else race_winner(bd,c,me)
                if v!=('W' if ben==me else 'L'): res['V2']=False
    return res

def ctx_of(pb,bd,root,FZ):
    return vcheck.ctx_pos(pb,bd,root,FZ)

def main(spec,hitsf,start,step,n):
    kind,dims=spec.split(':'); w,h=map(int,dims.split('x')); pb=psolve.Board(w,h,kind=='cyl'); bd=Bd(w,h,kind=='cyl')
    alt=make_alt(bd); FZ={0,1}
    hits=json.load(open(hitsf))[start::step][:n]
    items=[]; texts=[]
    for t in hits:
        tk=t.split(); r=int(re.search(r'Pa(\d+)',t).group(1)); 
        for bkr in (r+2,r):
            if not (1<=bkr<=h): continue
            tt=re.sub(r'kb\d+','kb%d'%bkr,t)
            for side in ('b','w'):
                s=re.sub(r' [bw] -$',' %s -'%side,tt); texts.append(s)
        texts.append(t)
    roots={}
    for s in set(texts):
        try: roots[s]=psolve.parse(pb,s)
        except Exception as e: pass
    S=psolve.Solver(pb); S.explore(list(roots.values())); S.solve()
    nX=0; nclean=0
    for t in hits:
        r=int(re.search(r'Pa(\d+)',t).group(1))
        X=roots[t]; fx=analyze(S,pb,bd,FZ,X)
        cx=ctx_of(pb,bd,X,FZ); dB=alt(cx,'B')
        okX = S.white_view(X)=='W' and dB=='B' and fx['V1b'] and fx['V2'] and fx['V3'] and fx['V4'] and not fx['V1a']
        nX+=okX
        clean=False
        for bkr in (r+2,r):
            if not (1<=bkr<=h): continue
            tt=re.sub(r'kb\d+','kb%d'%bkr,t); good=True
            for side in ('b','w'):
                s=re.sub(r' [bw] -$',' %s -'%side,tt)
                if s not in roots: good=False; break
                R=roots[s]
                if not S.succ[R] and False: pass
                f=analyze(S,pb,bd,FZ,R)
                c=ctx_of(pb,bd,R,FZ); d=alt(c,'B' if side=='b' else 'W')
                pv=S.white_view(R); pw='B' if pv=='L' else ('W' if pv=='W' else '?')
                good&=all(f.values()) and pw==d
            clean|=good
        nclean+=clean
        print('hit',t,'| X ok:',okX,'| clean twin:',clean)
    print('SAMPLE',len(hits),'X ok',nX,'clean-twin',nclean)
if __name__=='__main__':
    main(sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]))
