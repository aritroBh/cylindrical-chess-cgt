import sys,time
sys.path.insert(0,'delegate/out/L12_opencode')
from solver import *
import itertools

def check_ep(ep):
    e0=make_env((ep,'count'), flat8)
    keys=raceKeys(e0,posG)
    k=len(keys)
    total=1<<k
    t0=time.time()
    count=0
    for mask in range(total):
        # build table: bit 1 -> white win? Let's use W if bit=1
        ws=[]
        for i in range(k):
            ws.append(W if (mask>>i)&1 else B)
        table=[]
        for (q,c),w in zip(keys,ws):
            table.append(((q.key(),c), w))
        def rf(pos,mover):
            key=(pos.key(),mover)
            for (k2,col) in table:
                if k2==key:
                    return col
            return None
        e=( (ep,'count'), flat8, 256, rf)
        if not isValue(e,400,posG,EIGHTH):
            print(f"  FAIL ep={ep} mask={mask}")
            return False
        count+=1
        if count%50==0:
            print(f"  ep={ep} {count}/{total} t={time.time()-t0:.1f}", flush=True)
    print(f"  ep={ep} all {total} pass t={time.time()-t0:.1f}")
    return True

for ep in ['aware','textbook','off']:
    print("ep",ep)
    ok=check_ep(ep)
    print("  result", ok)
