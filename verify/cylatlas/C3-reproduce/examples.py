"""Values of the C3 example witnesses under the textbook and e.p.-aware passed tests.
  PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-reproduce/examples.py --root <cylcgt root>
"""
import sys, argparse
ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True); a = ap.parse_args()
sys.path.insert(0, a.root)
from cylcgt import cgt, pawns
print("module", pawns.__file__, "PASSED_RESPECTS_EP", getattr(pawns, "PASSED_RESPECTS_EP", None), "rule", pawns.RACE_RULE)
EX = [(3, True, "W: a2 b4 / B: b7 c6"), (3, True, "W: a2 b3 / B: a5 c7"), (3, True, "W: a2 b2 / B: c5 c6"),
      (3, True, "W: a2 a3 b2 / B: b6 c7"), (4, True, "W: a2 c2 / B: b7 d7"), (4, False, "W: a2 c2 / B: b7 d7")]
for n, wrap, s in EX:
    for ep in (True, False):
        pawns._value.cache_clear()
        g = pawns.value(pawns.Board(n, 8, wrap, ep), pawns.Pos.parse(s))
        print(f"{'cyl' if wrap else 'flat'}{n} ep={int(ep)} {s}: {cgt.show(g)}  outcome={cgt.outcome(g)}")
