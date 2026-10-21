"""Root options of G = W a2 c2 / B b7 d7 (4 files flat) in the independent model, all three e.p. settings, count rule.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/sumtest/C2-theory/root_options_aware.py
"""
import sys
from functools import lru_cache
sys.path.insert(0, "verify/sumtest/C2-theory")
import indep
from cylcgt import cgt

def fmt(st):
    W, B, e = st
    n = lambda s: " ".join(sorted("abcd"[f] + str(r) for f, r in s))
    return f"W {n(W)} / B {n(B)}" + (" +ep" if e else "")

root = (indep.sqs("a2 c2"), indep.sqs("b7 d7"), None)
for ep, aware, lab in ((False, False, "ep off"), (True, False, "ep on, textbook"), (True, True, "ep on, ep-aware")):
    m = indep.Model(ep, aware, "count")
    @lru_cache(maxsize=None)
    def val(st, mover):
        d = m.resolve(st, mover)
        if d is not None:
            return cgt.integer(d)
        return cgt.make([val(c, "W") for c in m.moves(m.strip_ep_for(st, "W"), "W")],
                        [val(c, "B") for c in m.moves(m.strip_ep_for(st, "B"), "B")])
    print(f"{lab}: G = {cgt.show(val(root, None))}")
    for side in ("W", "B"):
        for c in m.moves(root, side):
            print(f"   {side}-> {fmt(c):28s} {cgt.show(val(c, side))}")
    X = (indep.sqs("a2 c2"), indep.sqs("b4 d7"), None)
    print(f"   X = W a2 c2 / B b4 d7 (no ep): {cgt.show(val(X, 'B'))};  after a2-a4 in X:",
          cgt.show(val(m.moves(X, 'W')[1] if False else [c for c in m.moves(X, 'W') if (0, 4) in c[0]][0], 'W')))
