import collections
ref={}
for l in open('posAfterM_ref3.txt'):
    if '|' not in l: continue
    p,v=l.rsplit('|',1); ref[p.strip()]=v.strip()
for var in ('q1','q0'):
    c=collections.Counter(); seen=set()
    bad=[]
    for l in open(f'dump22_{var}.txt'):
        pos,mv,rest=[x.strip() for x in l.split('|')]
        if pos in seen: continue
        seen.add(pos)
        tp,ts,imm=map(int,rest.split())
        r=ref[pos]
        cls=('plain' if tp>=0 else '-')+('/pass' if ts>=0 else '/-')+('/imm' if imm else '')
        c[(cls,r)]+=1
        if tp>=0 and r!='L': bad.append((pos,'plain-not-L',r))
        if ts>=0 and r not in 'LD': bad.append((pos,'pass-not-LD',r))
        if imm and r!='L': bad.append((pos,'imm-not-L',r))
    print(var,len(seen),'distinct positions after m')
    for k,v in sorted(c.items()): print('  ',k,v)
    print('  violations',len(bad),bad[:5])
    pl=[1 for l in seen]
