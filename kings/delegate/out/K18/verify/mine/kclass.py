import re,gzip,collections,sys
nf=3
def msq(s): return chr(97+nf-1-(ord(s[0])-97))+s[1:]
def canon(y):
    t=y.split(); a=tuple(sorted(t[:-2])); b=tuple(sorted(x[0]+msq(x[1:]) for x in t[:-2])); return min(a,b)
def load(opener,fn):
    d={}
    for l in opener(fn):
        if l.startswith('#'): continue
        p=[x.strip() for x in l.split('|')]
        if p[0]!='Q' or p[3]!='NOESC': continue
        k=canon(p[1])
        if k in d: continue
        mv={}
        for s in re.findall(r"\[([^\]]*)\]",p[4]):
            t=s.split(); name=t[0]; cls=t[1]
            kv=None
            for x in t[2:]:
                if x.startswith('k='): kv=[None if y=='-' else int(y) for y in x[2:].split(',')][:7]
            mv[name]=(cls,kv)
        d[k]=(p[1],mv)
    return d
mine=load(lambda f:open(f,'rt'),'s22_k6_q1.txt')
theirs=load(lambda f:gzip.open(f,'rt'),'../../keep/searchk_c8x6_f3_22.out.gz')
print('noesc classes mine',len(mine),'theirs',len(theirs))
diff=0
# mirror reps may differ: compare by sorted multiset of (class,kvec) for each canon key
for k in mine:
    a=sorted((v[0],tuple(-1 if x is None else x for x in (v[1] or ()))) for v in mine[k][1].values()); b=sorted((v[0],tuple(-1 if x is None else x for x in (v[1] or ()))) for v in theirs[k][1].values())
    if a!=b: diff+=1
print('classes with differing (class,kvec) multisets:',diff)
def cls(f):
    if all(f): return 'finite for every k<=6'
    if f[0] and not any(f[1:]): return 'k*=0'
    if all(f[k]==(k%2==0) for k in range(7)): return 'even k only'
    return 'other finite pattern'
C=collections.Counter(); sub=collections.Counter(); n=0
for k,(Y,mv) in mine.items():
    for name,(c,kv) in mv.items():
        if c=='PLAIN-ONLY' and name.startswith('K'):
            n+=1; f=[x is not None for x in kv]; C[cls(f)]+=1
            if cls(f)=='other finite pattern':
                fin=[i for i in range(7) if f[i]]
                if fin==list(range(len(fin))): sub['prefix k<=%d'%max(fin)]+=1
                elif f[0] and all(f[i] for i in (1,3,5)) and not any(f[i] for i in (2,4,6)): sub['k=0 and odd k']+=1
                else: sub['other:'+''.join('1' if x else '0' for x in f)]+=1
print(n,'plain-only king sorties',dict(C)); print(dict(sub))
