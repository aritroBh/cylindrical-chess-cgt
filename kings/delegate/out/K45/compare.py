import re,sys,glob,collections
W=sys.argv[1]
def canon(k): return tuple(sorted(re.findall(r'[Pp][a-z]\d+',k)))
def files(k): return set(re.match(r'[Pp]([a-z])',t).group(1) for t in k)
def parse(path):
    d={}
    grp=None; out=[]
    for line in open(path):
        if line.startswith('G '): grp=line.split()[1]; continue
        if not line.startswith('LAYER'): continue
        p=line.split()
        key=canon(p[1]); sh=int(p[2][3:]); rest=[x for x in p[3:] if '=' in x]
        vals=tuple(int(x.split('=')[1]) for x in rest)
        blocked = 'B' in p[3:4]
        out.append((grp,key,sh,blocked,vals))
    return out
B=parse('logs/B_%s.out'%W)
A={}
for f in glob.glob('logs/A_cyl%sx6_f*.out'%W):
    tri=re.search(r'_f([0-9_]+)\.out',f).group(1).split('_')
    for line in open(f):
        if not line.startswith('LAYER'): continue
        p=line.split(); key=canon(p[1]); sh=int(p[2][3:])
        vals=tuple(int(x.split('=')[1]) for x in p[3:] if '=' in x)
        A[(tuple(tri),key,sh)]=vals
letters=lambda tri: set(chr(97+int(t)) for t in tri)
tris=sorted(set(k[0] for k in A))
nb=nm=nmiss=0; Bkeys=set()
for grp,key,sh,blocked,vals in B:
    gt=tuple(grp.split(',')) if grp else None
    Bkeys.add((key,sh))
    found=None
    for t in tris:
        if files(key)<=letters(t) and (t,key,sh) in A: found=A[(t,key,sh)]; break
    # blocked layers always printed by A; non-blocked B lines have f1>0 so A has them too
    nb+=1
    if found is None: nmiss+=1; print('MISSING in A',key,sh,vals) if nmiss<10 else None
    elif found!=vals: nm+=1; print('MISMATCH',key,sh,vals,found) if nm<10 else None
print('W',W,'B lines',nb,'mismatch',nm,'missing in A',nmiss)
# reverse: A lines with key reachable in B (key in B reach) must be in B
reach=set(canon(l.strip()) for l in open('logs/B_%s_reach.txt'%W))
nr=nbad=0
for (t,key,sh),vals in A.items():
    if key in reach:
        nr+=1
        if (key,sh) not in Bkeys: nbad+=1; print('A line reachable but not printed by B',t,key,sh,vals) if nbad<10 else None
print('A lines whose layer is B-reachable',nr,'not printed by B',nbad)
tot=collections.Counter()
for grp,key,sh,blocked,vals in B:
    tot['f1']+=vals[1]; tot['f2']+=vals[4]; tot['f3']+=vals[5]; tot['f4']+=vals[6]
print('B totals (printed layers):',dict(tot))
