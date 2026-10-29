import re,glob,sys
BIG=1000000
tot=dict(lab=0,cl=0); sig={}
root=dict(nodes=0,corrL=0,corrR=0,litL=0,litR=0,inf=0,d12=0,amb=0,uns=0,litOut=0,litIn=0)
allr=dict(root); n=0
for f in sorted(glob.glob('logs/enum4/chunk_*.txt')):
    n+=1
    for ln in open(f):
        m=re.match(r'ENUM4 .* labelled-rooted-stoppers (\d+) canonical-classes (\d+)',ln)
        if m: tot['lab']+=int(m[1]); tot['cl']+=int(m[2])
        m=re.match(r'(all nodes of the classes|root only): nodes (\d+)  corrected-viol lam (\d+) rho (\d+)  literal-viol lam (\d+) rho (\d+)  infinity-pair-viol (\d+)  D2-grid-viol (\d+)  ambiguous-number (\d+)  unsolved (\d+)  literal-fails-outside-RS>=2 (\d+)  literal-holds-inside (\d+)',ln)
        if m:
            d=root if m[1]=='root only' else allr
            for k,v in zip(['nodes','corrL','corrR','litL','litR','inf','d12','amb','uns','litOut','litIn'],m.groups()[1:]): d[k]+=int(v)
        if ln.startswith('SIG'):
            a=list(map(int,ln.split()[1:])); sig[tuple(a[:4])]=sig.get(tuple(a[:4]),0)+a[4]
print('chunks',n); print('labelled rooted stoppers (4 nodes, all reachable from node 0):',tot['lab']); print('classes (canonical under permutations of 1..3):',tot['cl'])
print('root only:',root); print('all nodes of the classes:',allr)
def f(v,one): return '+inf' if v==BIG else '-inf' if v==-BIG else '%d/16'%(v*2)
mine={}
for (lam,rho,LS,RS),c in sig.items():
    k='lam=%s rho=%s LS=%s RS=%s'%('inf' if lam<0 else lam,'inf' if rho<0 else rho,f(LS,8),f(RS,8)); mine[k]=c
print('signatures',len(mine))
theirs={}
for ln in open('../logs/A_enum4_root.txt'):
    m=re.match(r'(lam=\S+ rho=\S+ LS=\S+ RS=\S+) count=(\d+)',ln)
    if m: theirs[m[1]]=int(m[2])
print('their signatures',len(theirs),'identical tables:',mine==theirs)
if mine!=theirs:
    for k in sorted(set(mine)|set(theirs)):
        if mine.get(k)!=theirs.get(k): print('DIFF',k,mine.get(k),theirs.get(k))
