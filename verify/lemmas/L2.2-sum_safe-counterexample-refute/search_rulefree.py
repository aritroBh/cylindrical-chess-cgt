"""Search (indep.py only) for single-component positions where S and W
outcomes differ and NO race is reachable at all (so the discrepancy cannot
depend on the race rule). 8 ranks, 6-8 files, flat or cylinder, e.p. off.
Usage: python3 search_rulefree.py SEED SECONDS"""
import random, sys, time
import indep as I
from indep import Bd, comps, gen, has_passer, oS, oW, clear, fmt

def races_reachable(B, w, k):
    seen, stack = {(w, k)}, [(w, k)]
    while stack:
        a, b = stack.pop()
        for side in "WB":
            for a2, b2, _ in gen(B, a, b, side, None):
                pw, pb = has_passer(B, a2, b2, "W"), has_passer(B, a2, b2, "B")
                if pw and pb:
                    return True
                if not (pw or pb) and (a2, b2) not in seen:
                    seen.add((a2, b2)); stack.append((a2, b2))
    return False

seed, secs = int(sys.argv[1]), float(sys.argv[2])
rng = random.Random(seed)
t0 = time.time(); tried = 0; found = 0
while time.time() - t0 < secs:
    n = rng.choice([6, 7, 8]); wrap = rng.random() < 0.6
    B = Bd(n, 8, wrap, False)
    nw, nb = rng.randint(2, 4), rng.randint(2, 4)
    sq = rng.sample([(f, r) for f in range(n) for r in range(2, 8)], nw + nb)
    w, k = frozenset(sq[:nw]), frozenset(sq[nw:])
    if has_passer(B, w, k, "W") or has_passer(B, w, k, "B") or len(comps(B, w, k)) != 1:
        continue
    tried += 1
    s, ww = oS(B, w, k, "count"), oW(B, w, k, "count"); clear()
    if s != ww and not races_reachable(B, w, k):
        found += 1
        print(f"{n}x8 {'cyl' if wrap else 'flat'} e.p. off {fmt(w, k)}: oS={s} oW={ww}, no race reachable", flush=True)
print(f"seed {seed}: tried {tried} single components in {time.time()-t0:.0f}s, {found} race-free counterexamples")
