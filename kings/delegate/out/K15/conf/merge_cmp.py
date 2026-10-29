import json,glob,os,sys
sys.path.insert(0,'.')
rows=json.load(open('conf/c86.rows.json'))
ORD={"L":0,"D":1,"W":2}
# group index -> rows (12 per group, in order)
groups=[]
for r in rows:
    if not groups or groups[-1][0]!=r['group']: groups.append([r['group'],[]])
    groups[-1][1].append(r)
res=[];missing=[]
for i,(g,rs) in enumerate(groups):
    fn=f'conf/pm/g{i:03d}.out'
    if not os.path.exists(fn): missing.append(g); continue
    lines=[l.rstrip('\n') for l in open(fn)]
    if len(lines)!=len(rs): missing.append(g); continue
    for r,l in zip(rs,lines):
        pos,ab=l.split(' | '); A,B=ab.split()
        assert pos==r['pos']
        st='agree' if (A==B==r['pred']) else ('DISAGREE' if A==B else ('inexact-consistent' if ORD[B]<=ORD[r['pred']]<=ORD[A] else 'inexact-DISAGREE'))
        r2=dict(r); r2.update(A=A,B=B,status=st); res.append(r2)
json.dump(res,open('conf/pm_table.json','w'))
from collections import Counter,defaultdict
summ=defaultdict(Counter); byctx=defaultdict(Counter)
for r in res:
    summ[r['cls']][r['status']]+=1; byctx[(r['cls'],r['ctx'])][r['status']]+=1
for c,v in summ.items(): print(c,dict(v))
print('groups done',len(groups)-len(missing),'of',len(groups),'missing',len(missing))
for k,v in sorted(byctx.items()): print(k,dict(v))
json.dump(missing,open('conf/pm_missing.json','w'))
