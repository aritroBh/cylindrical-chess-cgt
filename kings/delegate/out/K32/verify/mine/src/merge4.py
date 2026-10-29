import re,glob,sys
fs=sorted(glob.glob(sys.argv[1]))
lab=cls=0; nodes=0
acc={}
pat=[('graphs',r'graphs (\d+) nodes (\d+)  cyc-errors (\d+)  D2-vs-D1 bad nodes (\d+)  monotone-bad (\d+)  number-ambiguous (\d+)  bigstops (\d+)'),
     ('nodelev',r'node-level corrected violations lam (\d+) rho (\d+) ; infinity-pairing violations lam (\d+) rho (\d+) ; literal violations \(finite stop\) lam (\d+) rho (\d+)'),
     ('rootlev',r'root-level: corrected violations lam (\d+) rho (\d+) ; literal violations lam (\d+) rho (\d+) either (\d+)')]
tot={k:None for k,_ in pat}
for f in fs:
    t=open(f).read()
    m=re.search(r'labelled-rooted-stoppers (\d+) classes (\d+)',t); lab+=int(m.group(1)); cls+=int(m.group(2))
    for k,p in pat:
        v=list(map(int,re.search(p,t).groups()))
        tot[k]=v if tot[k] is None else [a+b for a,b in zip(tot[k],v)]
print("files",len(fs),"labelled rooted stoppers",lab,"classes",cls)
print("graphs,nodes,cyc,d2bad,mono,amb,big =",tot['graphs'])
print("node-level: corr lam,rho; inf lam,rho; literal lam,rho =",tot['nodelev'])
print("root-level: corr lam,rho; literal lam,rho,either =",tot['rootlev'])
