"""V1 theory scratch: BIG-invariance compared STRUCTURALLY (options sorted; numbers with
|x| >= BIG/2 replaced by BIG-relative offsets), because cgt.show prints options in creation
order and string comparison gives false differences.  Also lists the 7.1ah summands on which
a first-passer-ends-the-game sum engine disagrees with the cylcgt disjunctive sum.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/V1-theory/big_struct.py
"""
import sys, importlib.util
sys.setrecursionlimit(1_000_000)
spec = importlib.util.spec_from_file_location("tc", "verify/diagrams/V1-theory/theory_checks.py")
tc = importlib.util.module_from_spec(spec); spec.loader.exec_module(tc)
from cylcgt import cgt, pawns
from cylcgt.pawns import Pos


def skey(g, memo):
    k = memo.get(g.id)
    if k is not None:
        return k
    if g.num is not None:
        B = pawns.BIG
        x = g.num
        k = ("B", x - B) if x >= B // 2 else (("-B", x + B) if x <= -(B // 2) else ("n", x))
    else:
        k = ("g", tuple(sorted(repr(skey(a, memo)) for a in g.L)), tuple(sorted(repr(skey(a, memo)) for a in g.R)))
    memo[g.id] = k
    return k


keys = {}
for big in (256, 1024, 2048):
    pawns.BIG = big
    for label, text, kind in tc.POS:
        for b in tc.boards(kind):
            for rule in ("count", "allW", "allB"):
                g, _ = tc.val(b, text, rule)
                keys[(big, label, b.ep, rule)] = (repr(skey(g, {})), cgt.outcome(g))
pawns.BIG = tc.ORIG_BIG; tc.set_rule("count")
for label, text, kind in tc.POS:
    for ep in (True, False):
        row = []
        for rule in ("count", "allW", "allB"):
            same = keys[(256, label, ep, rule)][0] == keys[(1024, label, ep, rule)][0] == keys[(2048, label, ep, rule)][0]
            oc = {keys[(bg, label, ep, rule)][1] for bg in (256, 1024, 2048)}
            row.append(f"{rule}: BIG-invariant={same} outcome {'/'.join(sorted(oc))}")
        bnd = keys[(256, label, ep, 'allW')][0] == keys[(256, label, ep, 'allB')][0]
        print(f"{label:7s} ep={'on ' if ep else 'off'} " + " | ".join(row) + f" | race bounds equal (BIG=256): {bnd}", flush=True)

b = tc.CYL; p = Pos.parse("W: a4 a5 h2 h3 / B: a7 h6")
G = pawns.value(b, p); T = tc.test_games(); mG = cgt.neg(G)
bat = dict(T); bat["-G"] = mG
for nm in ("*", "up", "down", "1/4", "-1/4", "1", "-1", "tiny1", "miny1"):
    bat[f"-G+{nm}"] = cgt.add(mG, T[nm])
model = tc.make_solver(b, "model")
for nm, X in bat.items():
    o1, o2 = cgt.outcome(cgt.add(G, X)), model(p, X)
    if o1 != o2:
        print(f"7.1ah + {nm}: cylcgt disjunctive sum {o1}; first-passer-ends engine {o2}")
