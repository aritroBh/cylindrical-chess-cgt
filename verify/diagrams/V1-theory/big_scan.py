"""V1 theory scratch: BIG-dependence of 7.2{a,b,h} canonical forms, and which 7.1ah summands
my sum engine disagrees with cylcgt on (expected: those with -BIG options, i.e. the +BIG/-BIG
cancellation that the first-passer-ends-the-game rule forbids).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/V1-theory/big_scan.py
"""
import sys, importlib.util
sys.setrecursionlimit(1_000_000)
spec = importlib.util.spec_from_file_location("tc", "verify/diagrams/V1-theory/theory_checks.py")
tc = importlib.util.module_from_spec(spec); spec.loader.exec_module(tc)
from cylcgt import cgt, pawns
from cylcgt.pawns import Pos
T72 = "W: a2 b2 h3 / B: a6 b7 h7"
forms = {}
for big in (64, 128, 256, 512, 1024, 2048, 4096):
    pawns.BIG = big
    for b in (tc.CYL, tc.CYL0):
        for rule in ("count", "allW", "allB"):
            g, n = tc.val(b, T72, rule)
            f = tc.rshow(g)
            forms[(big, b.ep, rule)] = f
            print(f"BIG={big:5d} ep={'on ' if b.ep else 'off'} {rule:5s} outcome {cgt.outcome(g)} mean {cgt.mean(g)} "
                  f"temp {cgt.temperature(g)} len {len(f)}  form-id {abs(hash(f)) % 10**6:06d}", flush=True)
pawns.BIG = tc.ORIG_BIG; tc.set_rule("count")
for ep in (True, False):
    for rule in ("count", "allW", "allB"):
        ids = [forms[(big, ep, rule)] == forms[(4096, ep, rule)] for big in (64, 128, 256, 512, 1024, 2048, 4096)]
        print(f"ep={'on ' if ep else 'off'} {rule:5s} equal to BIG=4096 form at BIG=64..4096: {ids}")
print("BIG=4096 ep=off count form:", forms[(4096, False, 'count')])
# 7.1ah mismatches
b = tc.CYL; p = Pos.parse("W: a4 a5 h2 h3 / B: a7 h6")
G = pawns.value(b, p); T = tc.test_games(); mG = cgt.neg(G)
bat = dict(T); bat["-G"] = mG
for nm in ("*", "up", "down", "1/4", "-1/4", "1", "-1", "tiny1", "miny1"):
    bat[f"-G+{nm}"] = cgt.add(mG, T[nm])
model = tc.make_solver(b, "model")
for nm, X in bat.items():
    o1, o2 = cgt.outcome(cgt.add(G, X)), model(p, X)
    if o1 != o2:
        print(f"7.1ah + {nm}: cylcgt {o1}  first-passer-ends engine {o2}")
