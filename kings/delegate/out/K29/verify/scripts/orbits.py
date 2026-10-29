# own orbit count of the ref3enum candidate lists under colour swap + rank flip (r -> H+1-r) and the file reflection of F_Z
import glob, os, re
cfg={'cyl7x6_f3':('cyl',7,6,0,3),'cyl7x6_f4':('cyl',7,6,0,4),'cyl8x6_f3':('cyl',8,6,0,3),'cyl8x6_f4':('cyl',8,6,0,4),
 'flat7x6_f3_z0':('flat',7,6,0,3),'flat7x6_f4_z0':('flat',7,6,0,4),'flat7x6_f3_z2':('flat',7,6,2,3),
 'flat8x6_f3_z0':('flat',8,6,0,3),'flat8x6_f4_z0':('flat',8,6,0,4),'flat8x6_f3_z2':('flat',8,6,2,3)}
tot=0
for name,(kind,W,H,zs,fz) in cfg.items():
    cands=[l.split(' | ')[0] for l in open('data/r3e_%s.txt'%name)]
    def canon(z):
        return tuple(sorted((t[0],t[1:]) for t in z.split()))
    def parse(z): return [(t[0],ord(t[1])-97,int(t[2:])) for t in z.split()]
    def key(p): return tuple(sorted(p))
    sw={'K':'k','k':'K','P':'p','p':'P'}
    def colour(p): return [(sw[c],f,H+1-r) for c,f,r in p]
    def refl(p): return [(c,(2*zs+fz-1-f)%W if kind=='cyl' else 2*zs+fz-1-f,r) for c,f,r in p]
    refl_ok = kind=='cyl' or (2*zs+fz-1==W-1)
    seen=set(); n=0
    S={key(parse(z)) for z in cands}
    for z in cands:
        p=parse(z)
        imgs=[p,colour(p)]
        if refl_ok: imgs+= [refl(p),refl(colour(p))]
        ks=[key(i) for i in imgs]
        assert all(k in S for k in ks), (name,z)   # symmetry closure of the list
        rep=min(ks)
        if rep not in seen: seen.add(rep); n+=1
    rep=len(open('../data/rep_%s.txt'%name.replace('_z0','_z0')).read().strip().split('\n'))
    print('%-16s candidates %4d  classes (own) %3d  K29 rep file %3d'%(name,len(cands),n,rep)); tot+=n
print('total classes',tot)
