"""Step 4a: every non-8-rank position the paper names, outcome class by (original minimax, fixed minimax, cylcgt engine).
Run: nice -n 15 .venv/bin/python delegate/out/L1_minimax_rank_audit/step4_named_positions.py"""
import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "crosscheck_fixed")); sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
import minimax_orig as mo, minimax_fixed as mf
from cylcgt import cgt, pawns

NAMED = [  # (label, files, ranks, wrap, ep_on, text, ep_right, expected_class_of_G_alone, source)
 ("tall R7 F3 *2", 3, 7, False, True, "W: a2 c2 / B: c3 b6", None, "N", "main Sec.8 / S6.5 / T80"),
 ("tall R7 F4 *3", 4, 7, False, True, "W: a2 c2 d3 / B: c3 b6 c6", None, "N", "main Sec.8 / S6.5 / T80"),
 ("tall R7 F4 *2", 4, 7, False, True, "W: a2 c2 / B: d4 b6", None, "N", "S6.5 / T80"),
 ("tall R7 C3 *2", 3, 7, True, True, "W: c2 a3 / B: b5 c5", None, "N", "S6.5 / T80"),
 ("tall R6 F4 *2 (a)", 4, 6, False, True, "W: a2 b2 d2 / B: a5 c5 d5", None, "N", "main Sec.8 / S6.5 / T80"),
 ("tall R6 F4 *2 (b)", 4, 6, False, True, "W: a2 d2 b3 / B: c4 a5 d5", None, "N", "S6.5 / T80"),
 ("tall R6 C4 *2", 4, 6, True, True, "W: c2 d2 a3 / B: b4 c5 d5", None, "N", "S6.5 / T80"),
 ("tall R9 C3 *2", 3, 9, True, True, "W: a2 b2 c2 / B: a8 b8 c8", None, "N", "S6.5 / T80"),
 ("(E) witness F5 R7", 5, 7, False, True, "W: a4 b3 e2 / B: a5 b4 e4", ((0, 3), (0, 4), "B"), "N", "S12.1 A.7 Remark (whole board W(X) = first player wins)"),
 ("condE prop F6 R6 (pure game; minimax has the passed rule, so only indicative)", 6, 6, False, True, "W: a4 f4 / B: b4 e5", ((0, 3), (0, 4), "B"), None, "S3 Prop. condE"),
]
def run(m, files, ranks, wrap, ep, text, epr):
    b = m.Board(files, ranks, wrap, ep); p = m.parse_position(text, epr)
    return m.outcome_class(b, p)
print(f"{'position':72s} {'orig':5s} {'fixed':5s} {'engine':6s} {'expected'}")
for lab, files, ranks, wrap, ep, text, epr, exp, src in NAMED:
    t0 = time.time()
    o = run(mo, files, ranks, wrap, ep, text, epr); f = run(mf, files, ranks, wrap, ep, text, epr)
    b = pawns.Board(files, ranks, wrap, ep); pp = pawns.Pos.parse(text)
    pp = pawns.Pos(pp.white, pp.black, epr)
    try: e = cgt.outcome(pawns.value(b, pp))
    except Exception as ex: e = type(ex).__name__
    flag = "" if o == f else "  <-- original differs from fixed"
    print(f"{lab + ' ' + text:72s} {o:5s} {f:5s} {str(e):6s} {exp}{flag}   [{src}] {time.time()-t0:.1f}s")
