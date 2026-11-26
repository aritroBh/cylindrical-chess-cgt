import sys,time
sys.path.insert(0,'delegate/out/L12_opencode')
from solver import *
for ep in ['aware','textbook','off']:
    e=make_env((ep,'count'), flat8)
    ks=raceKeys(e,posG)
    print(ep, "keys", len(ks))
    for (q,c) in ks:
        print("  ", COLOR_NAME[c], q.key())
