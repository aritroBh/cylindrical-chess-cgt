import glob,collections
for fl in 'fg':
    pos=[l.strip() for l in open(f'zs_{fl}_pos.in')]; pred=[l.strip() for l in open(f'zs_{fl}_pred.txt')]
    d={p:r for p,r in zip(pos,pred)}
    done=0;bad=[]
    for f in sorted(glob.glob(f'zs/{fl}_*.out')):
        for ln in open(f):
            if '|' not in ln: continue
            p,v=[x.strip() for x in ln.split('|')]
            done+=1
            if d[p]!=v: bad.append((p,d[p],v))
    print(fl,'done',done,'/',len(pos),'differ',len(bad))
    for b in bad: print('  ',b)
