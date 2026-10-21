"""The nine rows of the L2.2 table under the e.p.-aware passed test adopted on 2026-10-16
(a pawn that may still be taken e.p. is not passed).
  indep part : .venv/bin/python -I verify/lemmas/L2.2-sum_safe-counterexample-theory/ep_aware_rows.py indep
  branch part: .venv/bin/python -I verify/lemmas/L2.2-sum_safe-counterexample-theory/ep_aware_rows.py branch <ep-wt root>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import indep as I  # noqa: E402

mode = sys.argv[1]
if mode == "indep":
    I.EP_AWARE = True
    for i, (bd, txt, rule, cS, cW) in enumerate(I.ROWS):
        p = I.parse(txt)
        print(f"row {i+1} {bd.key()} {txt} [{rule}] EP_AWARE: o(S)={I.oS(bd, p, rule)} "
              f"o(S_glob)={I.oS(bd, p, rule, glob=True) if bd.ep else '-'} o(W)={I.oW(bd, p, rule)}", flush=True)
else:
    sys.path.insert(0, os.path.abspath(sys.argv[2]))
    from cylcgt import cgt, pawns
    assert hasattr(pawns, "PASSED_RESPECTS_EP") and pawns.PASSED_RESPECTS_EP
    for i, (bd, txt, rule, cS, cW) in enumerate(I.ROWS):
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        b = pawns.Board(bd.nf, bd.nr, bd.wrap, bd.ep)
        x = pawns.Pos.parse(txt)
        print(f"row {i+1} {bd.key()} {txt} [{rule}] branch pawns.value outcome={cgt.outcome(pawns.value(b, x))} "
              f"sum_safe={pawns.sum_safe(b, x)}", flush=True)
