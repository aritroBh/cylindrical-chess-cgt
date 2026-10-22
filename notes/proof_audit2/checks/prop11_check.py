"""Prop. 11 of the paper: cyl(8), e.p. off, count rule, X = W b2 d4 g3 h5 / B a7 c7 f7 g4.
Claim: S(X) is a black win whoever starts (R), W(X) is a first-player win (N).
Independent CGT-free minimax (indep_sum_model.py).  BIG = 24 > max(M_W, M_B) = 21.
Run from the project root:  python3 notes/proof_audit2/checks/prop11_check.py
"""
import sys, time
sys.path.insert(0, "notes/proof_audit2/checks")
import indep_sum_model as M
M.configure(8, 8, True, False, "count", True, big=24)
W, B = M.parse("W: b2 d4 g3 h5 / B: a7 c7 f7 g4")
mw = sum(8 - r for _, r in W); mb = sum(r - 1 for _, r in B)
print("move bounds M_W, M_B =", mw, mb, flush=True)
t = time.time()
print("W(X) outcome:", M.W_outcome(W, B), f"({time.time()-t:.0f}s, cache {M.W_win.cache_info().currsize})", flush=True)
t = time.time()
print("S(X) outcome:", M.S_outcome(W, B), f"({time.time()-t:.0f}s, cache {M.S_win.cache_info().currsize})", flush=True)
