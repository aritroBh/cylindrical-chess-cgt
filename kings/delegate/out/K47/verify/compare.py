# compare the referee's r(Z_O + T) (logs/main_N.out) and over + T (logs/small_candidates.out) with the investigator's ../logs/full_A_N.out
import re
inv={}
for l in open('../logs/full_A_N.out'):
    p=[x.strip() for x in l.split('|')]
    t,root,s,z,o=p[0],p[1],p[2],p[3].split()[1],p[4].split()[1]
    inv[(t,'A' if 'kd4' in root else 'B',s)]=(z,o)
alias={'over+*':'*+over'}
ov={}
for l in open('logs/small_candidates.out'):
    ov[l.split(' | ')[0].strip()]=re.search(r'\| over=(\w\w)',l).group(1)
n=agree=nover=0; diffs=[]; zo=[]
for l in open('logs/main_N.out'):
    p=[x.strip() for x in l.split('|')]; t=p[0]
    for root,v in (('A',p[1]),('B',p[2])):
        for s,c in (('w',v[0]),('b',v[1])):
            key=(alias.get(t,t),root,s); n+=1
            iz,io=inv[key]; o=ov[t][0 if s=='w' else 1]
            if iz==c: agree+=1
            else: diffs.append((key,c,iz))
            if io==o: nover+=1
            else: diffs.append(('over',key,o,io))
            if c!=o: zo.append((t,root,s,'Z='+c,'over='+o))
print('results',n,'Z agree with investigator',agree,'over agree',nover); print('disagreements',diffs)
print('Z != over at',len(zo)); [print(' ',x) for x in zo]
