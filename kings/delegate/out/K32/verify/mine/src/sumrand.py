import re,sys
g=n=cyc=d2=mono=amb=big=0; corr=[0,0]; inf=[0,0]; lit=[0,0]; rl=[0,0]
for l in open(sys.argv[1]):
    m=re.match(r'\[rand\] graphs (\d+) nodes (\d+)  cyc-errors (\d+)  D2-vs-D1 bad nodes (\d+)  monotone-bad (\d+)  number-ambiguous (\d+)  bigstops (\d+)',l)
    if m: a=list(map(int,m.groups())); g+=a[0];n+=a[1];cyc+=a[2];d2+=a[3];mono+=a[4];amb+=a[5];big+=a[6]
    m=re.match(r'\[rand\] node-level corrected violations lam (\d+) rho (\d+) ; infinity-pairing violations lam (\d+) rho (\d+) ; literal violations \(finite stop\) lam (\d+) rho (\d+)',l)
    if m: a=list(map(int,m.groups())); corr[0]+=a[0];corr[1]+=a[1];inf[0]+=a[2];inf[1]+=a[3];lit[0]+=a[4];lit[1]+=a[5]
print("graphs",g,"nodes",n,"cyc-errors",cyc,"D2-vs-D1 bad nodes",d2,"monotone-bad",mono,"ambiguous",amb,"big stops",big)
print("corrected violations lam,rho",corr,"infinity-pairing violations lam,rho",inf,"literal violations (finite stop) lam,rho",lit)
