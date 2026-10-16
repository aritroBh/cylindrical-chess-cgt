"""Verifier driver: for every row of the notes/lemmas.md section 2 table,
compute with the independent implementation (indep.py) the whole-board outcome
and the sum-model outcome; compare with cylcgt (pawns.value, pawns.sum_safe,
lemmas.common.W/alt_outcome) and crosscheck/minimax.py.

Run from project root:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python \
      verify/lemmas/L2.2-sum_safe-counterexample-reproduce/check_table.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep  # noqa: E402

from cylcgt import cgt, pawns  # noqa: E402
from cylcgt.pawns import Board, Pos  # noqa: E402
from crosscheck import minimax as mm  # noqa: E402
from lemmas.common import S, W, alt_outcome, hereditarily_safe  # noqa: E402

ROWS = [
    # files ranks wrap ep position rule claimed_oS claimed_oW
    (8, 8, True, False, "W: b2 d4 g3 h5 / B: a7 c7 f7 g4", "count", "R", "N"),
    (8, 8, True, False, "W: b3 f4 g5 / B: a5 b6 f5 h6", "count", "N", "L"),
    (8, 8, True, False, "W: b2 c5 d4 f3 / B: c7 d6 e7 g6", "count", "L", "N"),
    (8, 8, True, True, "W: a2 c4 e4 h2 / B: a6 b5 d7 e7", "count", "R", "N"),
    (8, 8, True, True, "W: a5 b6 d2 e2 / B: a7 c7 e7", "count", "L", "N"),
    (8, 7, True, False, "W: c2 g2 h4 / B: a5 b6 f5 g6", "count", "R", "N"),
    (7, 6, False, True, "W: b2 d3 f2 / B: c4 c5 e5 g5", "count", "N", "R"),
    (8, 8, True, True, "W: a3 e2 e4 h6 / B: a4 a5 f5 g7", "opponent", "N", "L"),
    (6, 8, False, False, "W: b2 d4 f4 / B: b7 c5 e5 e7", "opponent", "R", "N"),
]

allok = True
for n, m, wrap, ep, text, rule, cS, cW in ROWS:
    t0 = time.time()
    b = Board(n, m, wrap, ep)
    x = Pos.parse(text)
    ncomp = len(pawns.components(b, x))
    ss = pawns.sum_safe(b, x)
    s = S(b, x, rule)
    oS = cgt.outcome(s)
    oW = cgt.outcome(W(b, x, rule))
    oalt = alt_outcome(b, x, rule)
    xc = None
    if m == 8 and rule == "count":
        xc = mm.outcome_class(mm.Board(n, m, wrap, ep), mm.Position(x.white, x.black, None))
    hss = hereditarily_safe(b, x)
    bd = indep.Bd(n, m, wrap, ep)
    p = indep.parse(text)
    iW = indep.w_outcome(bd, p, rule)
    iS = indep.s_outcome(bd, p, rule)
    icomp = len(indep.comps(bd, p))
    ok = (ncomp == 1 and icomp == 1 and ss and oS == cS == iS and oW == cW == oalt == iW
          and (xc is None or xc == cW) and not hss)
    allok &= ok
    print(f"{'OK ' if ok else 'BAD'} {n}x{m} {'cyl' if wrap else 'flat'} ep={'on' if ep else 'off'} {rule:8s} {text}\n"
          f"     comps={ncomp}/{icomp} sum_safe={ss} HSS={hss} | o(S): pawns={oS} indep={iS} claimed={cS}"
          f" | o(W): common.W={oW} alt={oalt} xc={xc} indep={iW} claimed={cW} | {time.time() - t0:.1f}s",
          flush=True)
print("ALL ROWS OK" if allok else "SOME ROW FAILED")
