"""Decisive checks for claim L2.2 using ONLY indep2.py (no project code).

Run from the project root:
  .venv/bin/python -I verify/lemmas/L2.2-sum_safe-counterexample-refute/run2/run_checks.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep2 as I  # noqa: E402

HEAD = "W: b2 d4 g3 h5 / B: a7 c7 f7 g4"
CASES = [
    ((8, 8, True, False), HEAD, "count", "R", "N"),
    ((8, 8, True, False), "W: b3 f4 g5 / B: a5 b6 f5 h6", "count", "N", "L"),
    ((8, 8, True, False), "W: b2 c5 d4 f3 / B: c7 d6 e7 g6", "count", "L", "N"),
    ((8, 8, True, True), "W: a2 c4 e4 h2 / B: a6 b5 d7 e7", "count", "R", "N"),
    ((8, 8, True, True), "W: a5 b6 d2 e2 / B: a7 c7 e7", "count", "L", "N"),
    ((8, 7, True, False), "W: c2 g2 h4 / B: a5 b6 f5 g6", "count", "R", "N"),
    ((7, 6, False, True), "W: b2 d3 f2 / B: c4 c5 e5 g5", "count", "N", "R"),
    ((8, 8, True, True), "W: a3 e2 e4 h6 / B: a4 a5 f5 g7", "opponent", "N", "L"),
    ((6, 8, False, False), "W: b2 d4 f4 / B: b7 c5 e5 e7", "opponent", "R", "N"),
]

print("== the 9 table rows: threshold S, brute-force S, W, and S with globally expiring e.p. ==")
for bd, text, rule, cS, cW in CASES:
    B = I.Board(*bd)
    x = I.parse(text)
    t = time.time()
    ncomp = len(I.comp_files(B, *x))
    s, s2, w = I.oS(B, x, rule), I.oS2(B, x, rule), I.oW(B, x, rule)
    sg = I.oS(B, x, rule, global_ep=True) if B.ep else "-"
    ok = (s == cS and s2 == cS and w == cW)
    print(f"{B!r:20s} {text:34s} {rule:8s} comps={ncomp} oS={s} oS2={s2} oW={w} oS_globalEP={sg} "
          f"claimed S={cS} W={cW} {'MATCH' if ok else 'MISMATCH'} [{time.time()-t:.1f}s]")

print()
print("== headline: other race rules, BIG, e.p. on ==")
B0 = I.Board(8, 8, True, False)
x0 = I.parse(HEAD)
for ep in (False, True):
    for rule in ("count", "mover", "opponent"):
        B = I.Board(8, 8, True, ep)
        print(f"  ep={ep} rule={rule}: oS={I.oS(B, x0, rule)} oW={I.oW(B, x0, rule)}")
for big in (64, 1000):
    I.BIG = big
    print(f"  BIG={big} ep=off count: oS={I.oS(B0, x0, 'count')} oS2={I.oS2(B0, x0, 'count')} oW={I.oW(B0, x0, 'count')}")
I.BIG = 256

print()
print("== headline root: passers / components ==")
w, k = x0
print("  passer W", I.has_passer(B0, w, k, "W"), "passer B", I.has_passer(B0, w, k, "B"),
      "component files", [sorted(I.LET[f] for f in c) for c in I.comp_files(B0, w, k)])

print()
print("== headline root children ==")
for side in "WB":
    for w2, k2, _ in I.gen(B0, w, k, side, None):
        pw, pb = I.has_passer(B0, w2, k2, "W"), I.has_passer(B0, w2, k2, "B")
        if pw or pb:
            print(f"  {side} -> {I.fmt(w2, k2)}: terminal (W passer {pw}, B passer {pb})")
            continue
        s, ww = I.oS(B0, (w2, k2), "count"), I.oW(B0, (w2, k2), "count")
        print(f"  {side} -> {I.fmt(w2, k2)}: comps={len(I.comp_files(B0, w2, k2))} oS={s} oW={ww}"
              f"{'  <-- differ' if s != ww else ''}")

print()
print("== mechanism node W: b5 d4 g3 / B: c6 f6 g4 h6 ==")
xm = I.parse("W: b5 d4 g3 / B: c6 f6 g4 h6")
memo = {}
for files in I.comp_files(B0, *xm):
    zw = frozenset(p for p in xm[0] if p[0] in files)
    zk = frozenset(p for p in xm[1] if p[0] in files)
    print(f"  component {sorted(I.LET[f] for f in files)}: {I.fmt(zw, zk)} threats {sorted(I.threats(B0, zw, zk, memo))}")
print(f"  oS={I.oS(B0, xm, 'count')} oS2={I.oS2(B0, xm, 'count')} oW={I.oW(B0, xm, 'count')}")

# is the mechanism node reachable from the headline (any move order, stopping at passers)?
seen, stack = set(), [(w, k)]
while stack:
    p = stack.pop()
    if p in seen:
        continue
    seen.add(p)
    if I.has_passer(B0, *p, "W") or I.has_passer(B0, *p, "B"):
        continue
    for side in "WB":
        for w2, k2, _ in I.gen(B0, *p, side, None):
            stack.append((w2, k2))
print(f"  reachable from headline (either side, any order): {xm in seen}; reachable positions {len(seen)}")

# does the headline discrepancy need race scoring at all?  Count race events in W's tree.
races = 0
for p in seen:
    if I.has_passer(B0, *p, "W") or I.has_passer(B0, *p, "B"):
        continue
    for side in "WB":
        for w2, k2, _ in I.gen(B0, *p, side, None):
            if I.has_passer(B0, w2, k2, "W") and I.has_passer(B0, w2, k2, "B"):
                races += 1
print(f"  race-creating moves among reachable non-terminal positions: {races}")
