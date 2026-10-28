import time
from engine import parse_ring, make_engine
toks='B3 B3 W2 B3 B3 W2 B3 W2 W2'.split()
pos=parse_ring(toks,9)
t=time.time()
eng=make_engine(9,True)
print('sig', eng['signature'](pos,4), 'states', eng['wins'].cache_info().currsize, 'time', round(time.time()-t,3))
