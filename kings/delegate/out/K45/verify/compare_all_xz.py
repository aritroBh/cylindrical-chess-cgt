import re,glob,sys
def canon(k): return tuple(sorted(re.findall(r'[Pp][a-z]\d+',k)))
def parse(path):
    L={};H=set()
    import lzma
    for line in lzma.open(path+'.xz','rt'):
        if line.startswith('LAYER'):
            p=line.split(); L[(canon(p[1]),int(p[2][3:]))]=tuple(int(x.split('=')[1]) for x in p[3:] if '=' in x)
        elif line.startswith('HIT'):
            p=line.split(); sh=int(p[1][3:])
            toks=[t for t in p[2:] if re.match(r'^[KkPp][a-z]\d+$',t)]
            sq=[t for t in toks if t[0] in 'Kk']; pw=tuple(sorted(t for t in toks if t[0] in 'Pp'))
            sh_idx=p.index('shuttle'); H.add((sh,tuple(sorted(sq)),pw,p[sh_idx+1]))
    return L,H
tot=0;bad=0
for W in (10,11,12):
    for f in sorted(glob.glob('../logs/A_cyl%dx6_f*.out.xz'%W)):
        tag=f.split('A_')[1][:-3]
        g='../logs/Ball_'+tag
        try: LA,HA=parse(f[:-3]); LB,HB=parse(g)
        except FileNotFoundError: print('missing',g); continue
        n=len(LA); tot+=n
        d=[k for k in set(LA)|set(LB) if LA.get(k)!=LB.get(k)]
        bad+=len(d)
        print(tag,'layer lines A',len(LA),'B',len(LB),'differences',len(d),'hits A',len(HA),'B',len(HB),'hit sets equal',HA==HB)
print('total A lines',tot,'differences',bad)
