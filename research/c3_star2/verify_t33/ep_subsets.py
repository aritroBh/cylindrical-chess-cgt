import itertools
from mysolve import Solver, parse, name, sq
F=3
W,B=parse("W: a2 a3 b2 / B: b7 c6 c7")
EV=[("B","a4","b3"),("B","b4","a3"),("B","c4","a3"),("B","c4","b3"),("W","a5","b6"),("W","a5","c6"),("W","b5","c6"),("W","c5","b6")]
EVs=[(a,sq(b),sq(c)) for a,b,c in EV]
def root(allowed):
    sv=Solver(F,"count",True,True,lambda sd,fr,to: (sd,fr,to) in allowed)
    return sv.nim_of(W,B,(),6), sv.outcome_with(W,B,(),sv.zero())
need=[EVs[1],EVs[6]]
print("only b4xa3 + b5xc6:",root(set(need)))
print("only b4xa3:",root({EVs[1]}),"only b5xc6:",root({EVs[6]}))
print("all minus c5xb6:",root(set(EVs)-{EVs[7]}))
# which subsets give *2 ?  (2^8 = 256 subsets)
good=[]
for mask in range(256):
    sub={EVs[i] for i in range(8) if mask>>i&1}
    k,oc=root(sub)
    if k==2: good.append(sub)
mins=[g for g in good if not any(h<g for h in good)]
print("subsets giving *2:",len(good),"of 256; minimal ones:")
for m in mins: print("  ",sorted(f"{a} {name(b)}x{name(c)}" for a,b,c in m))
