import time, random
from engine import parse_ring, make_engine
random.seed(1)
lines=open('research/c9_rings/codex/enumerated/rings_4_5.txt').read().splitlines()
sample=random.sample(lines, 20)
times=[]
states=[]
sigs=[]
for ring in sample:
    toks=ring.split()
    pos=parse_ring(toks,9)
    t=time.time()
    eng=make_engine(9,True)
    sig=eng['signature'](pos,4)
    dt=time.time()-t
    st=eng['wins'].cache_info().currsize
    times.append(dt); states.append(st); sigs.append(sig)
    print(f'{ring} -> {sig} states={st} time={dt:.3f}')
print('max states',max(states),'max time',max(times),'total',sum(times))
