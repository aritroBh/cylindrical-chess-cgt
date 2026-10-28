import json,re,subprocess,collections,itertools
nf=3
def msq(s): return chr(97+nf-1-(ord(s[0])-97))+s[1:]
def canon(y):
    t=y.split(); a=tuple(sorted(t[:-2])); b=tuple(sorted(x[0]+msq(x[1:]) for x in t[:-2])); return min(a,b)
# groups: NOESC roots in my own search output, Q variant, one pawn a side
groups={}
for l in open('../mine/s22_q1.txt'):
    if l.startswith('#'): continue
    p=[x.strip() for x in l.split('|')]
    if p[3]!='NOESC': continue
    Y=p[1]; toks=Y.split()
    nP=sum(1 for t in toks if t[0]=='P'); nb=sum(1 for t in toks if t[0]=='p')
    if (nP,nb)!=(1,1): continue
    k=canon(Y)
    if k in groups: continue
    sorts=[]
    for s in re.findall(r"\[([^\]]*)\]",p[4]):
        t=s.split()
        if t[1]=='PLAIN-ONLY' and t[0].startswith('K'): sorts.append(t[0])
    groups[k]=(Y,sorts)
print('groups with one pawn a side, NOESC (Q):',len(groups),' plain-only king sorties:',sum(len(v[1]) for v in groups.values()),' groups with >=1 plain-only king sortie:',sum(1 for v in groups.values() if v[1]))
json.dump(list(groups.values()),open('es_groups.json','w'))
