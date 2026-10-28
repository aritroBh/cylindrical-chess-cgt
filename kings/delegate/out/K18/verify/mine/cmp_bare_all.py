import collections
ref={}
for l in open('posAll_ref3.txt'):
    if '|' not in l: continue
    p,v=l.rsplit('|',1); ref[p.strip()]=v.strip()
print('ref positions',len(ref), collections.Counter(ref.values()))
# per variant: the local value of a position = same for every (root,move) giving that position (position after m determines it)
for var in ('q0','q1'):
    plain={};pas={}
    for l in open(f'dumpall_{var}.txt'):
        pos,mv,rest=[x.strip() for x in l.split('|')]
        tp,ts,imm=map(int,rest.split())
        pl = tp>=0 or imm==1; ps = ts>=0 or imm==1
        plain[pos]=pl; pas[pos]=ps
    for nm,d in (('plain',plain),('pass',pas)):
        c=collections.Counter(ref[p] for p,v in d.items() if v)
        print(var,nm,'local win:',sum(c.values()),dict(c))
