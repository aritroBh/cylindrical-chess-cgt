import sys, glob, os
tot_g=tot_r=0; allok=True; mind=99; hist={}
for f in sorted(glob.glob('../data/enum_*.txt')):
    name=os.path.basename(f)[5:-4]
    if name.endswith('_11') or name.endswith('_22'): continue
    r='data/r3e_%s.txt'%name
    if not os.path.exists(r): print(name,'no r3e yet'); continue
    g={}
    for l in open(f):
        z,d=l.strip().split(' | '); dw,db=map(int,d.split()); g[z]=(dw,db)
    q={}
    for l in open(r):
        z,d=l.strip().split(' | '); lw,lb=map(int,d.split()); q[z]=(lw,lb)
    same=set(g)==set(q)
    flagok=all((g[z][0]<=2)==bool(q[z][0]) and (g[z][1]<=2)==bool(q[z][1]) for z in g if z in q)
    both2=sum(1 for z in g if g[z][0]<=2 and g[z][1]<=2)
    mx=min(max(v) for v in g.values())
    print('%-16s grp %4d  ref3enum %4d  same set %s  depth<=2 flags agree %s  grp both<=2: %d  min over groups of max(dw,db): %d'%(name,len(g),len(q),same,flagok,both2,mx))
    tot_g+=len(g); tot_r+=len(q); allok&=same and flagok
print('total grp',tot_g,'ref3enum',tot_r,'all agree',allok)
