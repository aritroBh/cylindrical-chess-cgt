from sumsolver import *
T = SumSolver(3); S = T.S
star = S.nimber(1); zero=S.zero(); two=S.nimber(2)
ROOT = "W: a2 a3 b2 / B: b7 c6 c7"
# O = a2-a4 (ep a3) option inside P1:  W a4 b2 / B b5 c7
O = "W: a4 b2 / B: b5 c7"
W,B = parse(O)
print("O = W a4 b2 / B b5 c7 : outcome", T.outcome(O), " O<=G:", T.le(O,ROOT))
for (nW,nB,nEP) in S.pawn_moves(W,B,(),"B"):
    t = "W: "+" ".join(sorted(name(s) for s in nW))+" / B: "+" ".join(sorted(name(s) for s in nB))
    vd=S.verdict(nW,nB,nEP,"B")
    if vd: print("  B reply",t,"decided",vd); continue
    print(f"  B reply {t:30s} oc={T.outcome(t,nEP):2s}  reply<=G(root): {T.le(t,ROOT,nEP)}")
