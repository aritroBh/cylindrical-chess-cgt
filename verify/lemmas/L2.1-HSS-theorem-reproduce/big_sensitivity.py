"""Sanity check that the BIG bound is not vacuous: for the seed-1 sample (HSS, nontrivial), find the
least BIG' >= 1 such that o(S) computed with BIG' equals o(W) for every BIG'' in [BIG', max(M)+1].
Reports how many positions need BIG' > 1, and whether any needs BIG' > max(M_W,M_B)+1 (would refute)."""
import sys
from collections import Counter
sys.path.insert(0, "verify/lemmas/L2.1-HSS-theorem-reproduce")
from indep_l21 import samples, analyse, o_S, o_W, mbound, show
st = Counter(); ex = []
for bd, x, rule in samples(1500, 1):
    h, E, nt = analyse(bd, x)
    if not (h and E and nt):
        continue
    ow = o_W(bd, x, rule)
    mw, mb = mbound(bd, x); top = max(mw, mb) + 1
    res = [o_S(bd, x, rule, k) for k in range(1, top + 1)]
    least = top + 1
    for k in range(top, 0, -1):
        if res[k - 1] == ow: least = k
        else: break
    st["n"] += 1
    if least > top: st["needs BIG > bound (REFUTES)"] += 1
    elif least > 1:
        st["needs BIG' > 1"] += 1
        if len(ex) < 5: ex.append((repr(bd), show(x), rule, "least BIG'", least, "bound", top))
print(dict(st))
for e in ex: print("  ", e)
