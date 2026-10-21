"""Is the hypothesis BIG > max(M_W, M_B) of Theorem 2.1 ever needed?
For every non-terminal plain root (nw v nb pawns, ranks 2..m-1) that is HSS, satisfies (E)
and is non-trivial, compare oW with oS at small BIG values. Uses only indep.py.
usage: python -I probe_big.py FILES RANKS WRAP EP NW NB BIG1,BIG2,...
"""
import sys, itertools
from collections import Counter
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import indep as I
n, m, wrap, ep, nw, nb = map(int, sys.argv[1:7])
bigs = [int(v) for v in sys.argv[7].split(",")]
bd = I.Board(n, m, bool(wrap), bool(ep))
tau = I.tau_of(bd)
memo = {}
def live(z): return bool(I.gen_moves(bd, z, "W") or I.gen_moves(bd, z, "B"))
def props(y):
    if y in memo: return memo[y]
    comps = I.components(bd, y); h = e_ok = True; nt = False
    if len(comps) >= 2:
        ts = [tau(c) for c in comps]
        h = not any(1 in a and -1 in b for i, a in enumerate(ts) for j, b in enumerate(ts) if i != j)
        e_ok = not I.ep_usable(bd, y)
        nt = sum(1 for c in comps if live(c)) >= 2 and any(ts)
    for s in "WB":
        for c in I.gen_moves(bd, y, s):
            if not any(I.status(bd, c)):
                a, b2, c2 = props(c); h &= a; e_ok &= b2; nt |= c2
    memo[y] = (h, e_ok, nt); return memo[y]
sqs = [(f, r) for f in range(n) for r in range(2, m)]
st = Counter(); ex = {}
for ws in itertools.combinations(sqs, nw):
    rest = [s for s in sqs if s not in ws]
    for bs in itertools.combinations(rest, nb):
        x = I.mkpos(ws, bs)
        if any(I.status(bd, x)): continue
        h, e_ok, nt = props(x)
        if not (h and e_ok and nt): continue
        mw, mb = I.move_bound(bd, x)
        for rule in ("count", "mover", "opponent"):
            ow = I.oW(bd, x, rule)
            for B in bigs:
                os_ = I.oS(bd, x, rule, BIG=B)
                st[(B, "agree" if os_ == ow else "DISAGREE")] += 1
                if os_ != ow and B not in ex:
                    ex[B] = (I.show(x), rule, "maxM", max(mw, mb), "oS", os_, "oW", ow)
print(bd, f"{nw}v{nb}", "nontrivial HSS&E plain roots x rules")
for k in sorted(st): print("   ", k, st[k])
for B, e in sorted(ex.items()): print("    first disagreement at BIG", B, e)
