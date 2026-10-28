import sys, json
sys.path.insert(0, '.')
from dgame import *
from reprod_real import contexts, nm
import psolve
for spec, files, maxp in [('cyl:6x6',[3,4],3),('flat:6x6',[3,4,5],2),('cyl:7x6',[3,4,5],2),('cyl:5x6',[3],3)]:
    kind,dims=spec.split(':'); w,h=map(int,dims.split('x')); bd=Bd(w,h,kind=='cyl'); alt=make_alt(bd)
    pb=psolve.Board(w,h,kind=='cyl')
    cand=[p for p in contexts(bd,files,maxp) if alt(p,'B')=='B']
    roots=[]
    for p in cand:
        toks=['Ka1','kb4','Pa3','pa4']+['P'+nm(s) for s in sorted(p[0])]+['p'+nm(s) for s in sorted(p[1])]
        roots.append(psolve.parse(pb,' '.join(toks)+' b -'))
    S=psolve.Solver(pb,frozen=True); S.explore(roots); S.solve()
    res=[S.white_view(r) for r in roots]
    nlegal=[len(S.succ[r]) for r in roots]
    print(spec,'cands',len(cand),'P(X)=W:',res.count('W'),'with no legal move:',nlegal.count(0))
