import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames')
# reuse analyze from analyze_w10 but import? Just exec
exec(open('/tmp/scratchpad/analyze_w10.py').read().split('lines=open')[0])
# now lines handling
lines=open('/Users/aritro/Downloads/Research/Chessendgames/research/ring_n_plus_2/ext_w10_k2.out').read().splitlines()
nim2=[l for l in lines if l.startswith('NIM') and '\t2\t' in l]
from collections import Counter
groups=Counter()
examples={}
for l in nim2:
    pos=l.split('\t')[1]
    r=analyze(pos,10)
    if r is None:
        key=('NONE',None)
    else:
        ph,ln,st,wf,core,cp=r
        key=(ph,ln,cp,core)
    groups[key]+=1
    if key not in examples: examples[key]=pos
for key,v in groups.items():
    print(v, key, 'ex:', examples[key])
