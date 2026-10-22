from sumsolver import *
T = SumSolver(3)
S = T.S
ROOT = "W: a2 a3 b2 / B: b7 c6 c7"
star = S.nimber(1); two = S.nimber(2)
def oc(text, ep=(), h=None):
    return T.outcome(text, ep, h)
print("== root options, outcome class (L>0, R<0, N fuzzy, P=0)")
for nm, t in [("W01 b2-b3","W: a2 a3 b3 / B: b7 c6 c7"),("W02 b2-b4","W: a2 a3 b4 / B: b7 c6 c7"),("W03 a3-a4","W: a2 a4 b2 / B: b7 c6 c7"),
              ("B01 b7-b6","W: a2 a3 b2 / B: b6 c6 c7"),("B02 b7-b5","W: a2 a3 b2 / B: b5 c6 c7"),("B03 c6-c5","W: a2 a3 b2 / B: b7 c5 c7")]:
    print(f"  {nm:12s} outcome {oc(t):2s}  =0? {oc(t)=='P'}  =*? {oc(t,(),S.nimber(1))=='P'}")
print("== reversal / value claims (explicit sum tests)")
Q1="W: a2 a4 b2 / B: b5 c6 c7"
print("Q1 (a3-a4 b7-b5) <= G(root):", T.le(Q1, ROOT))
print("Q1 <= *2 :", T.le_H(Q1, two))
print("W a2 a4 b3 / B b5 c6 c7 (b2-b3 reply) = * :", oc("W: a2 a4 b3 / B: b5 c6 c7",(),star)=="P")
P1="W: a2 b2 / B: b5 c7"
print("P1 (X after c6xb5) <= G(root):", T.le(P1, ROOT), " <= *2:", T.le_H(P1, two))
print("W a2 b4 / B b5 c7 (b2-b4 in P1) = 0 :", oc("W: a2 b4 / B: b5 c7")=="P")
X="W: a2 b2 b5 / B: c6 c7"
print("X (a4xb5) outcome:", oc(X), " (X>0 expected 'L')")
print("-- Black side")
V="W: a2 a3 b4 / B: b7 c5 c7"
print("V (c6-c5 b2-b4) >= G(root):", T.ge(V, ROOT), " >= *2:", T.le_H("W: a2 a3 b4 / B: b7 c5 c7", two) , "(le_H is V<=*2, ignore)")
print("V b7-b6 reply = * :", oc("W: a2 a3 b4 / B: b6 c5 c7",(),star)=="P")
Y2="W: a2 a3 / B: b4 b7 c7"
Z="W: a2 b4 / B: b7 c7"
print("Z (a3xb4) >= G(root):", T.ge(Z, ROOT))
print("Z b7-b5 reply W a2 b4 / B b5 c7 = 0 :", oc("W: a2 b4 / B: b5 c7")=="P")
print("Y2 (c5xb4) >= * ?", None)
print("Y2 outcome:", oc(Y2), "(R expected: Y2 < 0 ... )")
print("V-options vs Y2: (right dominance means option >= Y2)")
for nm,t in [("b7-b6","W: a2 a3 b4 / B: b6 c5 c7"),("b7-b5 ep","W: a2 a3 b4 / B: b5 c5 c7"),("c5-c4","W: a2 a3 b4 / B: b7 c4 c7"),("c7-c6","W: a2 a3 b4 / B: b7 c5 c6")]:
    print(f"   V {nm:9s} >= Y2: {T.ge(t,Y2)}   >= *: {not T.le_H(t, star) if False else None}")
