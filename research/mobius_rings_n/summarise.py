import glob,re,collections,os,sys
rows=collections.defaultdict(lambda:{'chunks':{}, 'hits':collections.defaultdict(list)})
for f in sorted(glob.glob('results/n*_p*_c*of*.mob1.done')):
    b=f[:-len('.mob1.done')]
    m=re.match(r'results/n(\d+)_p(\d+)_c(\d+)of(\d+)',b); n,p,i,k=map(int,m.groups())
    if not os.path.exists(b+'.mob2.done'): continue
    r=rows[(n,p)]; r['K']=k
    o1=open(b+'.mob1.out').read(); o2=open(b+'.mob2.out').read()
    rings=int(re.search(r'RINGS (\d+)',o1).group(1))
    t=lambda x: float(re.search(r'real ([\d.]+)',open(b+'.'+x+'.time').read()).group(1))
    hs=[l.split(' ',2)[1:] for l in o1.splitlines() if l.startswith('HIT')]
    r['chunks'][i]=(rings,o1==o2,t('mob1'),t('mob2'),hs)
print('n pawns chunks rings *2orb *3orb agree mob1_s mob2_s')
for (n,p),r in sorted(rows.items()):
    ch=r['chunks']; rings=sum(c[0] for c in ch.values()); h=[x for c in ch.values() for x in c[4]]
    s2=sum(1 for x in h if x[0]=='NNPN'); s3=sum(1 for x in h if x[0]=='NNNP')
    print(n,p,f"{len(ch)}/{r['K']}",rings,s2,s3,all(c[1] for c in ch.values()),round(sum(c[2] for c in ch.values())),round(sum(c[3] for c in ch.values())))
if '-v' in sys.argv:
    for (n,p),r in sorted(rows.items()):
        for c in r['chunks'].values():
            for x in c[4]: print(n,p,x[0],x[1])
