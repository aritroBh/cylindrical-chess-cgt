"""Which race nodes does G = *2 depend on? Flip each distinct race resolution (count rule) alone.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/sumtest/C2-theory/race_sensitivity.py [ep]
"""
import sys
from functools import lru_cache
sys.path.insert(0, "verify/sumtest/C2-theory")
from indep import Model, sqs, BIG
from cylcgt import cgt

ep = len(sys.argv) > 1 and sys.argv[1] == "ep"
aware = len(sys.argv) > 2 and sys.argv[2] == "aware"
root = (sqs("a2 c2"), sqs("b7 d7"), None)

class Flip(Model):
    def __init__(self, flip=None, **kw):
        super().__init__(**kw)
        self.flip, self.seen = flip, set()
    def resolve(self, st, mover):
        d = super().resolve(st, mover)
        if d is not None and self.passed(st, "W") and self.passed(st, "B"):
            key = (st, mover)
            self.seen.add(key)
            if key == self.flip:
                return -d
        return d

def canon(m):
    @lru_cache(maxsize=None)
    def val(st, mover):
        d = m.resolve(st, mover)
        if d is not None:
            return cgt.integer(d)
        L = [val(c, "W") for c in m.moves(m.strip_ep_for(st, "W"), "W")]
        R = [val(c, "B") for c in m.moves(m.strip_ep_for(st, "B"), "B")]
        return cgt.make(L, R)
    return val(root, None)

def fmt(st):
    W, B, e = st
    n = lambda s: " ".join(sorted("abcd"[f] + str(r) for f, r in s))
    return f"W {n(W)} / B {n(B)}" + (f" ep" if e else "")

base = Flip(ep=ep, aware=aware, race="count")
g0 = canon(base)
races = sorted(base.seen, key=str)
print("ep", ep, "aware", aware, "base value", cgt.show(g0), "distinct race nodes", len(races))
changed = []
for key in races:
    m = Flip(flip=key, ep=ep, aware=aware, race="count")
    g = canon(m)
    if g is not g0:
        changed.append((key, cgt.show(g)))
print("single flips that change the root:", len(changed))
for (st, mover), v in changed:
    print("  ", fmt(st), "after", mover, "count-winner", "W" if Model(ep, aware, "count").resolve(st, mover) > 0 else "B", "-> root", v)
