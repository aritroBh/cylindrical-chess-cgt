import re,sys,collections
def parse(files):
    cases={}
    for f in files:
        for l in open(f):
            m=re.match(r'CLS (\S+) (\d+)x(\d+) a(\d+) roots (\d+) p1 (\d+) m1 (\d+) notW/2 (\d+) oddrankdiff (\d+) races (\d+)',l)
            if m:
                b,W,H,r,rt,p,mm,nf,od,rc=m.groups(); cases[(int(W),int(H),int(r))]=(int(rt),int(p),int(mm),int(nf),int(od),int(rc))
    return cases
if __name__=='__main__':
    c=parse(sys.argv[1:])
    print('cases',len(c))
    ok=True
    rule_bad=[k for k,v in c.items() if ((k[0]%2==0 and k[0]>=6)!=(v[1]>0 and v[2]>0)) or ((v[1]>0)!=(v[2]>0))]
    print('rule violations',rule_bad[:10],len(rule_bad))
    print('roots +-1 total',sum(v[1]+v[2] for v in c.values()),'p1',sum(v[1] for v in c.values()),'m1',sum(v[2] for v in c.values()))
    print('with roots',sum(1 for v in c.values() if v[1]+v[2]>0),'without',sum(1 for v in c.values() if v[1]+v[2]==0))
    print('notW/2',sum(v[3] for v in c.values()),'oddrankdiff',sum(v[4] for v in c.values()),'races',sum(v[5] for v in c.values()))
    # colour symmetry
    bad=0
    for (W,H,r),v in c.items():
        o=c.get((W,H,H-r))
        if o is not None and v[1]!=o[2]: bad+=1
    print('colour symmetry violations',bad)
    # saturation
    sat={}
    for H in range(4,40):
        rows={}
        for (W,HH,r),v in c.items():
            if HH==H and W%2==0: rows.setdefault(W,{})[r]=(v[1],v[2])
        if not rows: continue
        Ws=sorted(rows); 
        last=tuple(sorted(rows[Ws[-1]].items()))
        const=[W for W in Ws if tuple(sorted(rows[W].items()))==last]
        sat[H]=(Ws[0],Ws[-1],min(const), 2*H-2, tuple(sorted(rows[2*H-4].items())) != last if 2*H-4 in rows else None)
    print('saturation (Wmin,Wmax,first W equal to last row, 2H-2, row at 2H-4 differs):')
    for H,v in sat.items(): print(' H',H,v)
