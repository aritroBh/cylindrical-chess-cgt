import json, sys, time
sys.path.insert(0,'kings/delegate/out/K12')
import checker as C
import brute as B
roots=json.load(open('kings/delegate/out/K12/roots.json'))
meta=json.load(open('kings/delegate/out/K12/meta.json'))
assert len(roots)==len(meta)
mism=0; cert1=0; cert2=0; t0=time.time()
for i,(r,m) in enumerate(zip(roots,meta)):
    W=r['W'];H=r['H'];Wp=r['Wp'];Bp=r['Bp'];ep=r['ep'];stm=r['stm'];beta=m['beta']
    c1=C.check_certified(W,H,Wp,Bp,ep,stm,beta)
    c2=B.check_certified_brute(W,H,Wp,Bp,ep,stm,beta)
    if c1: cert1+=1
    if c2: cert2+=1
    if c1!=c2:
        mism+=1
        if mism<=10:
            print('MISMATCH',i,W,H,c1,c2, flush=True)
    if i%50000==0:
        print(i, 'cert1',cert1,'cert2',cert2,'mism',mism,'time',round(time.time()-t0,1), flush=True)
print('FINAL', 'n',len(roots),'cert1',cert1,'cert2',cert2,'mismatches',mism,'time',round(time.time()-t0,1), flush=True)
