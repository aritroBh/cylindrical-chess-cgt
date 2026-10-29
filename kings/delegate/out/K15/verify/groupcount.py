import sys,glob,collections
from canon import parse_state
def key(s): return (s[0],s[1],tuple(sorted(s[2])),tuple(sorted(s[3])))
def transform(s,W,H,sh,mi,fl,cyl,FW):
    wk,bk,wp,bp=s
    def g(p):
        f,r=p
        if mi: f=(-f) if cyl else (FW-1-f)
        f=f+sh
        if cyl: f%=W
        if fl: r=H-1-r
        return (f,r)
    t=(g(wk),g(bk),frozenset(map(g,wp)),frozenset(map(g,bp)))
    if fl: t=(t[1],t[0],t[3],t[2])
    return t
def run(W,H,cyl,files,FW=3):
    items=[]
    for fn in files:
        for ln in open(fn):
            root,cl=ln.rstrip('\n').split('\t')
            items.append((root,frozenset(parse_state(x,W,H) for x in cl.split('|'))))
    par={}
    def find(x):
        while par.setdefault(x,x)!=x:
            par[x]=par[par[x]]; x=par[x]
        return x
    for r,c in items:
        c=list(c)
        for s in c[1:]: par[find(s)]=find(c[0])
        find(c[0])
    comps={}
    for r,c in items: comps.setdefault(find(next(iter(c))),set()).update(c)
    comps=list(comps.values())
    def canon(c,shifts,mirrors,flips):
        best=None
        for sh in shifts:
            for mi in mirrors:
                for fl in flips:
                    k=tuple(sorted(key(transform(s,W,H,sh,mi,fl,cyl,FW)) for s in c))
                    if best is None or k<best: best=k
        return best
    res={}
    res['roots']=len(items); res['closures']=len(set(c for r,c in items)); res['components']=len(comps)
    res['flip']=len(set(canon(c,[0],[0],[0,1]) for c in comps))
    res['all_sym']=len(set(canon(c,range(W) if cyl else [0],[0,1],[0,1]) for c in comps))
    res['translate_mirror_only']=len(set(canon(c,range(W) if cyl else [0],[0,1],[0]) for c in comps))
    return res,comps
if __name__=='__main__':
    W=int(sys.argv[1]);H=int(sys.argv[2]);cyl=sys.argv[3]=='cyl'
    res,comps=run(W,H,cyl,sys.argv[4:])
    print(res)
