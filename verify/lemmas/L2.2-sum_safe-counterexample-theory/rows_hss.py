"""HSS status (indep threat sets) of the nine L2.2 rows, and BIG-invariance of o(S) for each.
  .venv/bin/python -I verify/lemmas/L2.2-sum_safe-counterexample-theory/rows_hss.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep as I  # noqa: E402

for i, (bd, txt, rule, cS, cW) in enumerate(I.ROWS):
    p = I.parse(txt)
    I._BD[bd.key()] = bd
    bad = I.unsafe_nodes(bd, p)
    res = {}
    for big in (100, 256, 1000):
        I.BIG = big
        I.s_win.cache_clear(); I.w_win.cache_clear()
        res[big] = (I.oS(bd, p, rule), I.oW(bd, p, rule))
    I.BIG = 256
    I.s_win.cache_clear(); I.w_win.cache_clear()
    print(f"row {i+1}: comps={len(I.comps(bd, p))} HSS={not bad} (non-pairwise-safe reachable nodes: {len(bad)}) "
          f"(o(S),o(W)) by BIG: {res}", flush=True)
