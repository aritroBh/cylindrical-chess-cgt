import sys, json
sys.path.insert(0, '.')
from dgame import *
from reprod_real import contexts
for spec, files, maxp, logn in [('cyl:6x6',[3,4],3,'A_cyl_6x6'),('flat:6x6',[3,4,5],2,'A_flat_6x6'),('cyl:7x6',[3,4,5],2,'A_cyl_7x6'),('cyl:5x6',[3],3,'A_cyl_5x6')]:
    kind,dims=spec.split(':'); w,h=map(int,dims.split('x')); bd=Bd(w,h,kind=='cyl'); alt=make_alt(bd)
    ctxs=list(contexts(bd,files,maxp)); cand=[p for p in ctxs if alt(p,'B')=='B']
    L=json.load(open('../logs/'+logn+'.json'))
    print(spec,files,maxp,'mine: n_ctx',len(ctxs),'cand',len(cand),'| agent: n_ctx',L['n_ctx'],'n_cand',L['n_cand'])
