"""Larger-sample estimate of P(value = *2) when the 4 critical races are won by
the mover and every other race verdict is a fair coin (independent solver)."""
import os, random, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep_check as ic
root = ic.parse("W: a2 c2 / B: b7 d7")
N = 2000
for mode in ("always", "off"):
    races, _ = ic.race_nodes(root, mode)
    order = sorted(races, key=lambda k: (ic.show(k[0]), k[1]))
    crit = {k for k in order if ic.show(k[0]) in ("W: a2 b5 / B: d7", "W: a3 b5 / B: d6") and k[1] == "W"
            or ic.show(k[0]) in ("W: a2 / B: c4 d7", "W: a3 / B: c4 d6") and k[1] == "B"}
    assert len(crit) == 4
    rng = random.Random(2026); hist = {}
    for _ in range(N):
        ov = {k: (k[1] if k in crit else rng.choice("WB")) for k in order}
        v = ic.value_name(ic.make_solver(mode, ov), root)
        hist[v] = hist.get(v, 0) + 1
    p = hist.get("*2", 0) / N
    print(mode, N, sorted(hist.items()), f"P(*2) = {p:.3f} +- {1.96*math.sqrt(p*(1-p)/N):.3f} (95%)", flush=True)
