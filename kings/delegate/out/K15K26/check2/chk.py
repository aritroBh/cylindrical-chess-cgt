import sys
def parse(fn, kpp):
    out={}
    for ln in open(fn):
        pos,rest=ln.split(' | ',1)
        parts=rest.split(' | ')
        val=parts[0].split()[0]
        mv=parts[-1].split() if kpp else rest.split()[1:]
        out[pos]=(val,sorted(mv))
    return out
for g in sys.argv[1:]:
    a=parse(g+'.kpp.out',True); b=parse(g+'.ref.out',False)
    same = a==b
    exact=True; nmv=0; ndraw=0
    for pos,(v,mv) in a.items():
        stm=pos.split()[-2]
        lose='L' if stm=='w' else 'W'
        d=[m for m in mv if m.endswith(':D')]
        bad=[m for m in mv if not (m.endswith(':D') or m.endswith(':'+lose))]
        nmv+=len(mv); ndraw+=len(d)
        if v!='D' or len(d)!=1 or bad or not d[0].startswith('K'): exact=False; print(' non-exact at',pos,v,d,bad)
    print(g,'roots',len(a),'solvers agree',same,'moves',nmv,'draw',ndraw,'exact',exact)
