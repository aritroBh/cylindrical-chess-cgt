"""Exhaustive falsification of Theorem 2.1 (claim L2.1-HSS-theorem) on small boards.

Uses ONLY indep.py (this directory; imports nothing from cylcgt/ or lemmas/).

For every placement of nw white and nb black pawns on ranks 2..m-1 of the
board (plus, with e.p. on, every such placement that carries a live e.p. right
from an immediately preceding double step), with no passer at the root:
  * HSS, condition (E), move bounds M_W, M_B (memoised recursion);
  * oW (whole-board alternating minimax) for the three race rules;
  * oS (sum-model game form F, plain minimax, no CGT) with
      BIG_t = max(M_W, M_B) + 1   (tightest value the theorem allows),
      BIG_t - 1                    (one below the hypothesis; probe only),
      BIG = 256                    (the project's value).
A counterexample to the theorem is: HSS and (E) and oS(BIG) != oW for some
BIG > max(M_W, M_B).

usage: python -I exhaust.py FILES RANKS WRAP(0/1) EP(0/1) NW NB [MAXSEC]
"""
import sys, time, itertools
from collections import Counter
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import indep as I

n, m, wrap, ep, nw, nb = map(int, sys.argv[1:7])
maxsec = float(sys.argv[7]) if len(sys.argv) > 7 else 1500
bd = I.Board(n, m, bool(wrap), bool(ep))
RULES = ("count", "mover", "opponent")
tau = I.tau_of(bd)

hss_memo, e_memo, nt_memo = {}, {}, {}


def nonterm(y):
    wp, bp = I.status(bd, y)
    return not (wp or bp)


def children(y):
    for side in ("W", "B"):
        for c in I.gen_moves(bd, y, side):
            yield c


def live(z):
    return bool(I.gen_moves(bd, z, "W") or I.gen_moves(bd, z, "B"))


def props(y):
    """(HSS, E, nontrivial) for a non-terminal position y, memoised.
    nontrivial: some non-terminal reachable node has >= 2 live components and
    at least one component with a non-empty threat set (i.e. the theorem says
    more than Theorem 2.3 / the one-sided special case)."""
    if y in hss_memo:
        return hss_memo[y]
    comps = I.components(bd, y)
    h = True
    e_ok = True
    nt = False
    if len(comps) >= 2:
        ts = [tau(c) for c in comps]
        for i, a in enumerate(ts):
            for j, b in enumerate(ts):
                if i != j and 1 in a and -1 in b:
                    h = False
        if I.ep_usable(bd, y):
            e_ok = False
        if sum(1 for c in comps if live(c)) >= 2 and any(ts):
            nt = True
    for c in children(y):
        if nonterm(c):
            ch, ce, cn = props(c)
            h &= ch
            e_ok &= ce
            nt |= cn
    r = (h, e_ok, nt)
    hss_memo[y] = r
    return r


squares = [(f, r) for f in range(n) for r in range(2, m)]
roots = []
for wset in itertools.combinations(squares, nw):
    rest = [s for s in squares if s not in wset]
    for bset in itertools.combinations(rest, nb):
        x = I.mkpos(wset, bset)
        if nonterm(x):
            roots.append(x)
        if False:  # plain roots only (no live right at the root)
            occ = set(wset) | set(bset)
            for (f, r) in wset:  # white just played f2-f4
                if r == 4 and (f, 3) not in occ and (f, 2) not in occ and m >= 5:
                    y = I.mkpos(wset, bset, ((f, 3), (f, 4), "B"))
                    if nonterm(y) and I.ep_usable(bd, y):
                        roots.append(y)
            for (f, r) in bset:  # black just played f(m-1)-f(m-3)
                if r == m - 3 and (f, m - 2) not in occ and (f, m - 1) not in occ and m >= 5:
                    y = I.mkpos(wset, bset, ((f, m - 2), (f, m - 3), "W"))
                    if nonterm(y) and I.ep_usable(bd, y):
                        roots.append(y)

stats = Counter()
cex, e_nec, big_nec = [], [], []
t0 = time.time()
done = 0
for x in roots:
    if time.time() - t0 > maxsec:
        stats["TIMEOUT_after_roots"] = done
        break
    h, e_ok, nt = props(x)
    mw, mbb = I.move_bound(bd, x)
    bt = max(mw, mbb) + 1
    for rule in RULES:
        try:
            ow = I.oW(bd, x, rule)
        except I.RaceRoot:
            continue
        os_t = I.oS(bd, x, rule, BIG=bt)
        key = ("HSS" if h else "notHSS", "E" if e_ok else "notE", "nontriv" if nt else "triv")
        stats[key + ("agree" if os_t == ow else "DISAGREE",)] += 1
        if h and e_ok and os_t != ow:
            cex.append((I.show(x), rule, "BIG", bt, os_t, ow))
        if h and not e_ok and os_t != ow:
            e_nec.append((I.show(x), rule, os_t, ow))
        if h and e_ok:
            # BIG = 256 (project value), must also agree
            os_256 = I.oS(bd, x, rule, BIG=256)
            if os_256 != ow:
                cex.append((I.show(x), rule, "BIG", 256, os_256, ow))
            stats["checked_BIG256"] += 1
            if nt and bt - 1 >= 1:
                os_m = I.oS(bd, x, rule, BIG=bt - 1)
                stats["below_bound_probe"] += 1
                if os_m != ow:
                    big_nec.append((I.show(x), rule, bt - 1, os_m, ow))
    done += 1

print(f"board {bd} nw={nw} nb={nb} roots={len(roots)} done={done} time={time.time()-t0:.1f}s")
for k in sorted(stats, key=str):
    print("   ", k, stats[k])
print("COUNTEREXAMPLES (HSS & E & oS != oW, BIG > max M):", len(cex))
for c in cex[:20]:
    print("    CEX", c)
print("HSS & not-E disagreements (tests necessity of E):", len(e_nec))
for c in e_nec[:10]:
    print("    notE", c)
print("HSS & E & nontrivial disagreements at BIG = max M (one below the hypothesis):", len(big_nec))
for c in big_nec[:10]:
    print("    lowBIG", c)
