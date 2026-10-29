import json,re,glob,sys
sys.path.insert(0,'.')
from summarize import parse
mine=parse(sorted(glob.glob('out/s_h*.txt'))+['out/ext.txt'])
grid=[(W,H,r) for H in range(4,13) for W in range(3,27) for r in range(2,H-1)]
print('grid',len(grid),'covered by mine',sum(1 for k in grid if k in mine))
k31={}
for f in ['sweep_main.jsonl','sweep_h4.jsonl','sweep_small.jsonl','sweep_wide.jsonl','sweep_ext.jsonl']:
    for l in open('../../logs/'+f):
        d=json.loads(l)
        if d['board'].startswith('cyl:'): k31[(d['W'],d['H'],d['rank'])]=(d['roots'],d['lk_p1'],d['lk_m1'])
bad=[(k,k31[k],mine[k][:3]) for k in k31 if k in mine and k31[k]!=mine[k][:3]]
print('K31 cases',len(k31),'compared',sum(1 for k in k31 if k in mine),'differences',len(bad),bad[:5])
ref={}
for f in glob.glob('../mine_*.txt'):
    for l in open(f):
        m=re.match(r'cyl:(\d+)x(\d+) a(\d+) roots (\d+) races (\d+)\s+\+1 (\d+)\s+-1 (\d+)',l)
        if m: W,H,r,rt,rc,p,mm=map(int,m.groups()); ref[(W,H,r)]=(rt,p,mm)
bad2=[(k,ref[k],mine[k][:3]) for k in ref if k in mine and ref[k]!=mine[k][:3]]
print('first referee cases',len(ref),'compared',sum(1 for k in ref if k in mine),'differences',len(bad2),bad2[:5])
gap=[k for k in grid if k not in k31]
print('gap cases',len(gap),'in first referee files',sum(1 for k in gap if k in ref),'and in mine',sum(1 for k in gap if k in mine))
