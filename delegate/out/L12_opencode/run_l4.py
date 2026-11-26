import sys
sys.path.insert(0,'delegate/out/L12_opencode')
from solver import *
import time

# shape
print("A comps", len(flat8.components(posA)))
print("B comps", len(flat8.components(posB)))

env_default = make_env(('aware','count'), flat8)
t0=time.time()
print("A default isValue *2:", isValue(env_default, 400, posA, star(2)))
print("B default isValue *2:", isValue(env_default, 400, posB, star(2)))
print("time", time.time()-t0)

# not ep off: for each race rule, NotValue
for r in ['count','mover','opponent']:
    e=make_env(('off',r), flat8)
    print(f"A ep-off {r} notValue:", notValue(e,400,posA,star(2)))
    print(f"B ep-off {r} notValue:", notValue(e,400,posB,star(2)))

# not opponent: for each ep option
for ep in ['aware','textbook','off']:
    e=make_env((ep,'opponent'), flat8)
    print(f"A opponent {ep} notValue:", notValue(e,400,posA,star(2)))
    print(f"B opponent {ep} notValue:", notValue(e,400,posB,star(2)))
