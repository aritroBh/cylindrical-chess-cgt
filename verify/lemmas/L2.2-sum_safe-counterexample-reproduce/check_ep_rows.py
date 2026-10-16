"""Verifier: for the e.p.-on rows of the section-2 table, is the S != W
disagreement still there when stale e.p. rights are removed from the sum model?
Run from project root:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python \
      verify/lemmas/L2.2-sum_safe-counterexample-reproduce/check_ep_rows.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep

ROWS = [
    (8, 8, True, True, "W: a2 c4 e4 h2 / B: a6 b5 d7 e7", "count"),
    (8, 8, True, True, "W: a5 b6 d2 e2 / B: a7 c7 e7", "count"),
    (7, 6, False, True, "W: b2 d3 f2 / B: c4 c5 e5 g5", "count"),
    (8, 8, True, True, "W: a3 e2 e4 h6 / B: a4 a5 f5 g7", "opponent"),
]
for n, m, wrap, ep, text, rule in ROWS:
    bd = indep.Bd(n, m, wrap, ep)
    p = indep.parse(text)
    print(f"{n}x{m} {'cyl' if wrap else 'flat'} ep=on {rule:8s} {text}: o(W)={indep.w_outcome(bd, p, rule)} "
          f"o(S local ep)={indep.s_outcome(bd, p, rule)} o(S global ep)={indep.s_outcome_global_ep(bd, p, rule)}",
          flush=True)
