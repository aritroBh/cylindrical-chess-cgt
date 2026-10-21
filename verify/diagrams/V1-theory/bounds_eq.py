"""V1 theory check: is 7.2{a,b,h} (e.p. on) the same VALUE under every race resolution?
Compare count-rule value with the two monotone bounds (all races -> White, all races -> Black) using cgt.le.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/V1-theory/bounds_eq.py
"""
import sys, importlib.util
sys.setrecursionlimit(1_000_000)
spec = importlib.util.spec_from_file_location("tc", "verify/diagrams/V1-theory/theory_checks.py")
tc = importlib.util.module_from_spec(spec); spec.loader.exec_module(tc)
from cylcgt import cgt
T72 = "W: a2 b2 h3 / B: a6 b7 h7"
for b in (tc.CYL, tc.CYL0):
    v = {r: tc.val(b, T72, r)[0] for r in ("count", "mover", "opponent", "allW", "allB")}
    eq = lambda x, y: cgt.le(x, y) and cgt.le(y, x)
    print(f"ep={'on ' if b.ep else 'off'}", {r: f"{cgt.outcome(g)} mean {cgt.mean(g)} temp {cgt.temperature(g)}" for r, g in v.items()})
    print("   allB <= count <= allW:", cgt.le(v['allB'], v['count']), cgt.le(v['count'], v['allW']),
          "| count==allW:", eq(v['count'], v['allW']), " count==allB:", eq(v['count'], v['allB']),
          " allW==allB:", eq(v['allW'], v['allB']))
    pm1 = cgt.make([cgt.integer(1)], [cgt.integer(-1)])
    print("   any of the five equal to +-1:", [r for r, g in v.items() if eq(g, pm1)])
tc.set_rule("count")
