import sys, collections
sys.path.insert(0,'.')
from agg import configs, run
jobs=[("cyl:6x6","cyl_6x6_free.log.gz","free"),("cyl:7x6","cyl_7x6_free.log.gz","free"),("cyl:8x6","cyl_8x6_free.log.gz","free"),
("flat:7x6","flat_7x6_free.log.gz","free"),("flat:8x6","flat_8x6_free.log.gz","free"),
("flat:6x6","flat_6x6_m0.log.gz","0"),("flat:6x6","flat_6x6_m1.log.gz","1"),("flat:6x6","flat_6x6_m2.log.gz","2"),
("cyl:6x6","cyl_6x6_m0.log.gz","0"),("cyl:6x6","cyl_6x6_m1.log.gz","1"),("cyl:6x6","cyl_6x6_m2.log.gz","2")]
for b,l,m in jobs:
    tot=collections.Counter(); per={}
    for cfg,n,f in configs(l):
        r,h=run(b,cfg,m); tot.update(r)
        for k in ('+1','-1','*','{1|0}','{0|-1}','+2','-2','+3','-3','1/2','-1/2','up','down','over','under','up*','down*','*2'):
            if r.get(k): per.setdefault(k,[]).append((cfg,r[k]))
    print(b,m,dict(tot),'TOTAL',sum(tot.values()),flush=True)
    print('   INTERESTING',{k:v[:6] for k,v in per.items()},flush=True)
