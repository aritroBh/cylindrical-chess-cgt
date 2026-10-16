"""Sanity checks for the own CGT and own sum minimax in refute_n1.py (so a P result is not vacuous).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/N1-refute/sanity.py
"""
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location("r", pathlib.Path(__file__).with_name("refute_n1.py"))
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

R = r.Rules()
checks = []
def chk(label, got, want):
    checks.append(got == want)
    print(f"{'ok ' if got == want else 'BAD'} {label}: got {got}, want {want}")

# pure CGT identities
chk("tiny(1) > 0", r.le(r.ZERO, r.TINY1) and not r.le(r.TINY1, r.ZERO), True)
chk("tiny(1) < up? (tiny(1) is smaller than up)", r.le(r.TINY1, r.UP) and not r.le(r.UP, r.TINY1), True)
chk("neg(tiny(1)) is miny(1)", r.neg(r.TINY1) is r.MINY1, True)
chk("{0,{0|-257*} || 0|-1} canonicalises to tiny(1)",
    r.make([r.ZERO, r.make([r.ZERO], [r.make([r.integer(-257)], [r.integer(-257)])])], [r.SW_0_M1]) is r.TINY1, True)
chk("{0|-1} is not tiny(1) and not 0", (r.eq(r.SW_0_M1, r.TINY1), r.eq(r.SW_0_M1, r.ZERO)), (False, False))
# raw-sum minimax on known pawn components
m1 = r.parse("W: f4 / B: f5 f7")     # -1
st = r.parse("W: f4 / B: f6")        # *
chk("pawn(-1) value", r.show(R.value(m1)), "-1")
chk("pawn(*) value", r.show(R.value(st)), "*")
chk("pawn(-1) + 1 is P", R.sum_outcome(m1, r.RI(1)), "P")
chk("pawn(-1) + 0 is R", R.sum_outcome(m1, r.R0), "R")
chk("pawn(*) + * is P", R.sum_outcome(st, r.RSTAR), "P")
chk("pawn(*) + 0 is N", R.sum_outcome(st, r.R0), "N")
chk("pawn(*) + tiny(1) is N", R.sum_outcome(st, r.RTINY1), "N")
chk("pawn(-1) + tiny(1) is R", R.sum_outcome(m1, r.RTINY1), "R")
g = r.parse(r.POS)
chk("G + 0 is L", R.sum_outcome(g, r.R0), "L")
chk("G + miny(1) is P", R.sum_outcome(g, r.RMINY1), "P")
chk("G + (-1) is R (would be P if G = 1)", R.sum_outcome(g, r.RM1), "R")
# a P result is not vacuous: G + miny(1) + extra * must be N
RMINY2 = ("g", (("g", (r.RI(2),), (r.R0,)),), (r.R0,))   # {2|0 || 0} = -tiny(2)
chk("G + miny(2) is L (tiny(1) > tiny(2)), so the sum test can tell tinies apart", R.sum_outcome(g, RMINY2), "L")
chk("G + down is R (tiny(1) < up)", R.sum_outcome(g, r.RMUP), "R")
print("all ok" if all(checks) else "SOME CHECK FAILED")
