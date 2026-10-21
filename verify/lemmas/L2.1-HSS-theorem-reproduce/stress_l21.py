"""Targeted stress test of Theorem 2.1 with the independent implementation indep_l21.py.

Generates positions with 2-3 pawn groups separated by empty files (so the sum model really
splits), e.p. on/off, flat/cylinder, all three race rules, and checks
    HSS and (E)  =>  o(S) == o(W)
with BIG at the theorem's minimum allowed value max(M_W, M_B)+1 AND at 256.
Also reports HSS positions that violate (E) and whether they disagree (informative only).

Run from the project root:
  PYTHONPATH=. .venv/bin/python verify/lemmas/L2.1-HSS-theorem-reproduce/stress_l21.py --seed 5 --seconds 1200
"""
import argparse
import random
import sys
import time
from collections import Counter

sys.path.insert(0, "verify/lemmas/L2.1-HSS-theorem-reproduce")
import indep_l21 as IL  # noqa: E402
from indep_l21 import B, analyse, comps, mbound, o_S, o_W, show, term, threats  # noqa: E402


def gen_pos(rng):
    n = rng.choice([5, 6, 7, 8])
    m = rng.choice([6, 7, 8])
    bd = B(n, m, rng.random() < 0.5, rng.random() < 0.6)
    # choose occupied file set with at least one gap
    k = rng.choice([2, 3])
    for _ in range(100):
        occ = sorted(rng.sample(range(n), rng.randint(k + 1, min(n - 1, 2 * k + 2))))
        if len(comps(bd, (frozenset((f, 3) for f in occ), frozenset(), None))) >= 2:
            break
    else:
        return None
    nw, nb = rng.randint(1, 4), rng.randint(1, 4)
    sq = [(f, r) for f in occ for r in range(2, m)]
    if len(sq) < nw + nb:
        return None
    for _ in range(200):
        pick = rng.sample(sq, nw + nb)
        p = (frozenset(pick[:nw]), frozenset(pick[nw:]), None)
        if term(bd, p) is None:
            return bd, p
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=5)
    ap.add_argument("--seconds", type=float, default=1200)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    t0 = time.time()
    st = Counter()
    fails = []
    eviol = []
    while time.time() - t0 < a.seconds:
        g = gen_pos(rng)
        if g is None:
            continue
        bd, x = g
        rule = rng.choice(("count", "mover", "opponent"))
        hss, E, nontriv = analyse(bd, x)
        st["total"] += 1
        if not hss:
            st["notHSS"] += 1
            continue
        both = threats(bd, x) == frozenset({1, -1})
        mw, mb = mbound(bd, x)
        bmin = max(mw, mb) + 1
        ow = o_W(bd, x, rule)
        smin = o_S(bd, x, rule, bmin)
        s256 = o_S(bd, x, rule, 256)
        st[("HSS", "E" if E else "notE", "nontrivial" if nontriv else "trivial",
            "bothsigns" if both else "onesign")] += 1
        if E and (smin != ow or s256 != ow):
            fails.append((repr(bd), show(x), rule, bmin, smin, s256, ow))
            print("FAIL", fails[-1], flush=True)
        if not E:
            st[("HSS notE", "agree" if s256 == ow else "DISAGREE")] += 1
            if s256 != ow:
                eviol.append((repr(bd), show(x), rule, s256, ow))
        if len(IL._Fm) + len(IL._Wm) + len(IL._Tm) > 3_000_000:
            IL._Fm.clear(); IL._Wm.clear(); IL._Tm.clear()
        if st["total"] % 200 == 0:
            print(f"[{time.time()-t0:.0f}s]", dict(st), flush=True)
    print("FINAL", f"{time.time()-t0:.0f}s")
    for k in sorted(st, key=str):
        print(k, st[k])
    print("HSS & (E) failures:", len(fails))
    for f in fails[:20]:
        print("   ", f)
    print("HSS & not (E) disagreements (not covered by the theorem):", len(eviol))
    for f in eviol[:10]:
        print("   ", f)


if __name__ == "__main__":
    main()
