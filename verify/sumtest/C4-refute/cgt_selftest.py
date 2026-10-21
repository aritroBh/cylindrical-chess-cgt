"""Sanity tests of my own CGT kernel in c4_indep.py (no project imports)."""
import importlib.util, os, sys
from fractions import Fraction as Fr
spec = importlib.util.spec_from_file_location("c4", os.path.join(os.path.dirname(__file__), "c4_indep.py"))
c4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c4)
num, make, show, le, eq, outcome, neg = c4.num, c4.make, c4.show, c4.le, c4.eq, c4.outcome, c4.neg
z = num(0)
star = make([z], [z]); star2 = make([z, star], [z, star])
up = make([z], [star])
def add(a, b):
    La, Ra = c4.opts(a); Lb, Rb = c4.opts(b)
    if a.num is not None and b.num is not None: return num(a.num + b.num)
    return make([add(x, b) for x in La] + [add(a, y) for y in Lb], [add(x, b) for x in Ra] + [add(a, y) for y in Rb])
checks = {
  "{0|0}=*": show(star) == "*",
  "*2+*2=0": add(star2, star2) is z,
  "*+*2 != 0": outcome(add(star, star2)) == "N",
  "{0|1}=1/2": make([z],[num(1)]) is num(Fr(1,2)) if False else show(make([z],[num(1)])) == "1/2",
  "{1|}=2": make([num(1)],[]) is num(2),
  "{0|2}=1": make([z],[num(2)]) is num(1),
  "{-1|-3} shows -2±1": show(make([num(-1)],[num(-3)])) == "-2±1",
  "{256|-256} shows ±256": show(make([num(256)],[num(-256)])) == "±256",
  "up>0": outcome(up) == "L",
  "up+down=0": add(up, neg(up)) is z,
  "1/2+1/2=1": add(make([z],[num(1)]), make([z],[num(1)])) is num(1),
  "{0,*|0}=up*": eq(make([z, star],[z]), add(up, star)),
  "pm1+pm1=0": add(make([num(1)],[num(-1)]), make([num(1)],[num(-1)])) is z,
  "{256|pm256} - 256 = tiny-like >0": outcome(add(make([num(256)],[make([num(256)],[num(-256)])]), num(-256))) == "L",
  "simplest(3/4,1)=7/8": c4.simplest_between(Fr(3,4), Fr(1)) == Fr(7,8),
  "simplest(-5/2,-2)=-9/4": c4.simplest_between(Fr(-5,2), Fr(-2)) == Fr(-9,4),
  "{-4|-2}=-3": make([num(-4)],[num(-2)]) is num(-3),
  "{2|3/2}? hot": show(make([num(2)],[num(Fr(3,2))])) == "7/4±1/4",
}
from fractions import Fraction as Fr
for k, v in checks.items(): print(("ok  " if v else "FAIL"), k)
print("ALL OK" if all(checks.values()) else "SOME FAILED")
