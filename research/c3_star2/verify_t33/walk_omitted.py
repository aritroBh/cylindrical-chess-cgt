from sumsolver import *
T = SumSolver(3); S = T.S
star = S.nimber(1); zero=S.zero()
ROOT = "W: a2 a3 b2 / B: b7 c6 c7"
def rel(a, b):
    return ("<=" if T.le(a,b) else "  ") , (">=" if T.ge(a,b) else "  ")
def opts(pos_text, side):
    W,B = parse(pos_text)
    out=[]
    for (nW,nB,nEP) in S.pawn_moves(W,B,(),side):
        vd = S.verdict(nW,nB,nEP,side)
        t = "W: "+" ".join(sorted(name(s) for s in nW))+" / B: "+" ".join(sorted(name(s) for s in nB))
        out.append((t,nEP,vd))
    return out
print("Left options of Q1 = W a2 a4 b2 / B b5 c6 c7 (after a3-a4 b7-b5):")
Q1="W: a2 a4 b2 / B: b5 c6 c7"
X="W: a2 b2 b5 / B: c6 c7"
for t,ep,vd in opts(Q1,"W"):
    if vd: print("  ",t,"decided",vd); continue
    d_star = T.le_H(t, star, ep)
    d_zero = T.le_H(t, zero, ep)
    d_X = T.le(t, X, ep)
    print(f"   {t:34s} oc={T.outcome(t,ep):2s}  <=0:{d_zero}  <=*:{d_star}  <=X(a4xb5):{d_X}")
print("Left options of P1 = W a2 b2 / B b5 c7 (replacement set when X reverses):")
P1="W: a2 b2 / B: b5 c7"
for t,ep,vd in opts(P1,"W"):
    if vd: print("  ",t,"decided",vd); continue
    print(f"   {t:34s} oc={T.outcome(t,ep):2s}  <=0:{T.le_H(t,zero,ep)}  <=*:{T.le_H(t,star,ep)}  =0:{T.outcome(t,ep)=='P'}")
