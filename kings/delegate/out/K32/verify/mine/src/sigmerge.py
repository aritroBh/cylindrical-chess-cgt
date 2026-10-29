import sys,re,collections
# merge SIG lines of several files (counts summed); print in K32's tally order: sorted by (lam,rho,LS,RS) numerically with inf last
tot=collections.Counter()
for f in sys.argv[1:]:
    for l in open(f):
        m=re.match(r'SIG lam=(\S+) rho=(\S+) LS=(\S+) RS=(\S+) count=(\d+)',l)
        if m: tot[m.group(1,2,3,4)]+=int(m.group(5))
def sv(s):
    if s=='+inf': return float('inf')
    if s=='-inf': return float('-inf')
    return int(s.split('/')[0])
def key(k): return (int(k[0]),int(k[1]),sv(k[2]),sv(k[3]))
for k in sorted(tot,key=key):
    la,rh,ls,rs=k
    print("lam=%s rho=%s LS=%s RS=%s count=%d"%("inf" if la=='99' else la,"inf" if rh=='99' else rh,ls,rs,tot[k]))
