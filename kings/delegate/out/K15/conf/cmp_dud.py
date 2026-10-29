import json,os,sys
from collections import Counter,defaultdict
rows=json.load(open('conf/dud/rows.json'))
ORD={"L":0,"D":1,"W":2}
out=[]; summ=defaultdict(Counter); missing=defaultdict(int)
for gi,gr in enumerate(rows):
    for k in range(0,len(gr),2):
        fn=f'conf/dud/g{gi}_c{k//2:02d}.out'
        if not os.path.exists(fn): missing[gr[0]['gname']]+=1; continue
        ls=[l.rstrip('\n') for l in open(fn)]
        if len(ls)<2: missing[gr[0]['gname']]+=1; continue
        for r,l in zip(gr[k:k+2],ls):
            pos,ab=l.split(' | '); A,B=ab.split(); assert pos==r['pos']
            st='agree' if A==B==r['pred'] else ('DISAGREE' if A==B else ('inexact-consistent' if ORD[B]<=ORD[r['pred']]<=ORD[A] else 'inexact-DISAGREE'))
            r2=dict(r); r2.update(A=A,B=B,status=st); out.append(r2); summ[r['gname']][st]+=1
json.dump(out,open('conf/dud_table.json','w'))
for g,v in summ.items(): print(g,dict(v),'contexts missing:',missing.get(g,0))
for g in missing:
    if g not in summ: print(g,'none done; missing',missing[g])
# disagreements by group
for g in summ:
    bad=[r for r in out if r['gname']==g and r['status']!='agree']
    ctxs=sorted({r['ctx'] for r in bad})
    print(g,'disagree contexts:',ctxs[:40])
