import sys,collections
def norm(pos):
    t=pos.split()
    ks=[x for x in t if x[0] in 'Kk' and x not in ('w','b')]
    pieces=sorted(x for x in t if x[0] in 'KkPp' and len(x)>=3)
    return ' '.join(pieces)
def load(fn):
    d={}
    for ln in open(fn):
        p,c=ln.rstrip('\n').split('\t'); d[norm(p)]=c
    return d
a=load(sys.argv[1]); b=load(sys.argv[2])
print('grp roots',len(a),'my roots',len(b))
conf=collections.Counter(); ex={}
for k,c in b.items():
    g=a.get(k)
    if g!=c:
        conf[(g,c)]+=1; ex.setdefault((g,c),k)
print('mismatches (grp,mine): count',dict(conf))
for k,v in ex.items(): print(k,v)
only=[k for k in a if k not in b]
print('in grp not mine',len(only), collections.Counter(a[k] for k in only))
