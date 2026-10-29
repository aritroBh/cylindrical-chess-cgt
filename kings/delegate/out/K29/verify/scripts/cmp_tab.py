import re
# grp table lines: T <z> | <ctx> | P=ab F=cd same/DIFF   ; ref3 pairs
def load(f): return [l.rsplit(' | ',1)[1].strip() for l in open(f)]
P=load('data/zt_P.ref3'); A=load('data/zt_park0.ref3'); ins=[l.strip() for l in open('data/zt_P.in')]
ref={}
for c in range(885):
    ctx=' '.join(sorted(t for t in ins[2*c].split() if t[0] in 'Pp' and t[1] in 'ef'))
    ref[ctx]=(P[2*c]+P[2*c+1], A[2*c]+A[2*c+1])
g={}
for l in open('data/grp_zt_table.out'):
    if not l.startswith('T '): continue
    m=re.match(r'T (.*?) \|(.*?) \| P=(\w\w) F=(\w\w) (\w+)',l)
    ctx=' '.join(sorted(m.group(2).split()))
    g[ctx]=(m.group(3),m.group(4))
print(len(g),len(ref))
bad=[c for c in ref if g.get(c)!=ref[c]]
print('per-context (Phi,Psi) mismatches grp vs ref3:',len(bad), bad[:3])
