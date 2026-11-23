import sys,json,collections; sys.path.insert(0,'.')
from fam import *
bases = {
 'n7p8': 'B6 W2 W3 B6 B7 W3 W6B7',
 'n8p8': 'B7 W3 W3 B6 W3 B6 B6 W2',
 'n10a': 'B4 W2 B6 W2 W3 B6 B7 W3 B7 W5',
 'n10b': 'B6 W3 B7 W2 W3 B6 B7 W2 B6 W3',
}
st1 = json.load(open('results/fam_stage1.json'))
groups = collections.defaultdict(dict)
for name, rows in st1.items():
    for sg,k,b,m,r in rows: groups[(name,k,b)][m]=sg
out=[]
MAXF=32
for (name,k,b),d in groups.items():
    if not (1 in d and 2 in d): continue
    t=bases[name].split(); blk=b.split()
    ms=[m for m in range(1,40) if len(t)+len(blk)*m<=MAXF]
    rings=[' '.join(ins(t,k,blk,m)) for m in ms]
    s1=solve(rings); s2=solve(rings,'bin/mob1_32')
    assert s1==s2,(name,k,b)
    first_bad=next((m for m,x in zip(ms,s1) if x not in ('NNPN','NNNP')),None)
    out.append((name,k,b,s1[0],ms[-1],first_bad,sorted(set(s1))))
    print(name,'cut',k,'block',b,'sig',s1[0],'maxm_tested',ms[-1],'first_fail_m',first_bad,set(s1),flush=True)
json.dump(out,open('results/fam_stage2.json','w'))
