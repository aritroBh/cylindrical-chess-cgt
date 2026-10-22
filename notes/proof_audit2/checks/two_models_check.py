"""Section V 'two models' claim: under the opponent rule with the e.p.-aware test,
   W a3 b3 c2 e2 / B a6 c5 d5 e3  (ordinary board, 5 files, 8 ranks, e.p. on) is 'up-double' (outcome L) as a sum
   but *2 (outcome N) on the whole board.
Independent CGT-free minimax for outcomes; also reports whether the Theorem-10 hypotheses (HSS, (E)) hold,
which they must NOT if the paper's Theorem 10 is right.
Run from the project root: python3 notes/proof_audit2/checks/two_models_check.py [rule]
"""
import sys, time
sys.path.insert(0, "notes/proof_audit2/checks")
import indep_sum_model as M
import hss_search as H
rule = sys.argv[1] if len(sys.argv) > 1 else "opponent"
M.configure(5, 8, False, True, rule, True, big=24)
W, B = M.parse("W: a3 b3 c2 e2 / B: a6 c5 d5 e3")
print("rule", rule, "move bounds", sum(8 - r for _, r in W), sum(r - 1 for _, r in B), flush=True)
t = time.time(); print("W outcome", M.W_outcome(W, B), f"{time.time()-t:.0f}s", flush=True)
t = time.time(); hss, E = H.analyse(W, B); print("HSS", hss, " (E)", E, f"{time.time()-t:.0f}s", flush=True)
t = time.time(); print("S outcome", M.S_outcome(W, B), f"{time.time()-t:.0f}s cache {M.S_win.cache_info().currsize}", flush=True)
