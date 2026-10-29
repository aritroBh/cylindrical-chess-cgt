import collections
P={}
for ln in open('d2.kpp.out'):
    pos,root,mv=[p.strip() for p in ln.split('|')]
    P[pos]=dict(m.split(':') for m in mv.split())
C={}
roots={}
for ln in open('../r3/logs/chess_cyl7_c1_mv.out'):
    pos,root,rest=[p.strip() for p in ln.split('|',2)]
    roots[pos]=root
    a,b=rest.split('| B:')
    A=dict(m.split(':') for m in a.replace('A:','').split()); B=dict(m.split(':') for m in b.split())
    C[pos]=(A,B)
cnt=collections.Counter()
for pos in P:
    grp='D2' if 'Pb4 Pc3 pb3 pc4' in pos else 'D2m'
    stm=pos.split()[-2]
    for m,v in P[pos].items():
        a=C[pos][0][m]; b=C[pos][1][m]
        # P value from White view v in W/L/D ; mover loses if (stm w and L) or (stm b and W)
        ploses=(stm=='w' and v=='L') or (stm=='b' and v=='W')
        if v=='D': cnt[(grp,'Pdraw','chess exact draw' if a==b=='D' else 'other:%s%s'%(a,b))]+=1
        elif ploses:
            if a==b=='D': cnt[(grp,'Ploses','chess draw exact')]+=1
            elif a==b==v: cnt[(grp,'Ploses','chess loses exact')]+=1
            else: cnt[(grp,'Ploses','undecided %s%s'%(a,b))]+=1
        else: cnt[(grp,'Pwins?',v)]+=1
for k,v in sorted(cnt.items()): print(k,v)
print(collections.Counter(roots.values()))
