from sumsolver import *
import time
T = SumSolver(4); S = T.S
star = S.nimber(1); zero=S.zero(); two=S.nimber(2)
def oc(t, ep=(), h=None): return T.outcome(t, ep, h)
def ge_nim(t, h, ep=()):   # a >= *k  (since -*k = *k): Left wins a + *k moving second
    return not T.wins((T.G(t,ep), ("H",h)), 0, "B")
t0=time.time()
print("== C4 root options (W a4 b2 c2 / B b6 c5 d6 d7)")
print("W01 b2-b3 = * :", oc("W: a4 b3 c2 / B: b6 c5 d6 d7",(),star)=="P")
print("W05 c2-c4 (ep c3) = 0 :", oc("W: a4 b2 c4 / B: b6 c5 d6 d7")=="P")
print("W02 b2-b4 <= * (dominated by b2-b3):", T.le_H("W: a4 b4 c2 / B: b6 c5 d6 d7", star))
print("W04 c2-c3 <= * (dominated by b2-b3):", T.le_H("W: a4 b2 c3 / B: b6 c5 d6 d7", star))
Ya="W: a5 b2 c2 / B: b5 c5 d6 d7"
print("W03 a4-a5 : <=0",T.le_H("W: a5 b2 c2 / B: b6 c5 d6 d7",zero)," <=*",T.le_H("W: a5 b2 c2 / B: b6 c5 d6 d7",star)," (not dominated by 0 or *: need reversal)")
print("Ya (a4-a5, b6-b5) <= *2 (a4-a5 reversible):", T.le_H(Ya, two))
print("B02 c5-c4 = 0 :", oc("W: a4 b2 c2 / B: b6 c4 d6 d7")=="P")
Yb="W: b2 b5 c2 / B: c5 d6 d7"
print("Yb (b6-b5, a4xb5) outcome:", oc(Yb), " >= *2:", ge_nim(Yb,two))
for t in ["W: b2 b5 c2 / B: c4 d6 d7","W: b2 b5 c2 / B: c5 d5 d7"]:
    print("   reply",t,"outcome",oc(t)," >= 0:", ge_nim(t,zero)," >= *:",ge_nim(t,star))
Yd="W: b2 c2 d5 / B: b6 c5 d7"
print("Yd (d6-d5, a4xd5) >= *2 (d6-d5 reversible):", ge_nim(Yd,two))
for nm,t in [("b6-b5","W: b2 c2 d5 / B: b5 c5 d7"),("c5-c4","W: b2 c2 d5 / B: b6 c4 d7"),("d7-d6","W: b2 c2 d5 / B: b6 c5 d6")]:
    print(f"   reply {nm}: outcome {oc(t)}  =* : {oc(t,(),star)=='P'}  >=*: {ge_nim(t,star)}")
# B01 b6-b5 and B03 d6-d5 outcomes
print("B01 b6-b5 outcome:", oc("W: a4 b2 c2 / B: b5 c5 d6 d7"), " >=0:",ge_nim("W: a4 b2 c2 / B: b5 c5 d6 d7",zero)," >=*:",ge_nim("W: a4 b2 c2 / B: b5 c5 d6 d7",star))
print("B03 d6-d5 outcome:", oc("W: a4 b2 c2 / B: b6 c5 d5 d7"), " >=0:",ge_nim("W: a4 b2 c2 / B: b6 c5 d5 d7",zero)," >=*:",ge_nim("W: a4 b2 c2 / B: b6 c5 d5 d7",star))
print("elapsed %.1fs"%(time.time()-t0))
