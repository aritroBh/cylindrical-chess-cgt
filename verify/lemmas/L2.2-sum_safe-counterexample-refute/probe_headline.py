"""Adversarial probes of the headline counterexample, using ONLY indep.py.

  - root move lists, and oS / oW of every child (so the 'three of four White
    moves, one of six Black moves' sub-claim can be checked);
  - the nested node W: b5 d4 g3 / B: c6 f6 g4 h6 and its components' threat sets;
  - robustness: all three race rules, e.p. on/off, BIG = 64 / 1000;
  - whether any race node is reached at all from the headline position.
"""
import indep as I
from indep import Bd, parse, fmt, comps, gen, has_passer, oS, oW, clear

X = "W: b2 d4 g3 h5 / B: a7 c7 f7 g4"


def threats(B, w, k, memo):
    key = (w, k)
    if key in memo:
        return memo[key]
    out = set()
    if has_passer(B, w, k, "W"):
        out.add("+")
    if has_passer(B, w, k, "B"):
        out.add("-")
    if not out:
        for side in "WB":
            for w2, k2, _ in gen(B, w, k, side, None):
                out |= threats(B, w2, k2, memo)
    memo[key] = frozenset(out)
    return memo[key]


def child_table(B, w, k, rule):
    for side in "WB":
        print(f"  {side} moves:")
        for w2, k2, nr in gen(B, w, k, side, None):
            pw, pb = has_passer(B, w2, k2, "W"), has_passer(B, w2, k2, "B")
            if pw or pb:
                print(f"    {fmt(w2, k2)}: terminal/race pw={pw} pb={pb}")
                continue
            s, ww = oS(B, w2, k2, rule), oW(B, w2, k2, rule)
            print(f"    {fmt(w2, k2)}: comps={len(comps(B, w2, k2))} oS={s} oW={ww}"
                  f"{'  <-- differ' if s != ww else ''}")
            clear()


def count_races(B, w, k):
    """Number of distinct (child, mover) race events reachable (any move order)."""
    seen, stack, races = {(w, k)}, [(w, k)], set()
    while stack:
        a, b = stack.pop()
        if has_passer(B, a, b, "W") or has_passer(B, a, b, "B"):
            continue
        for side in "WB":
            for a2, b2, _ in gen(B, a, b, side, None):
                if has_passer(B, a2, b2, "W") and has_passer(B, a2, b2, "B"):
                    races.add((a2, b2, side))
                elif (a2, b2) not in seen:
                    seen.add((a2, b2))
                    stack.append((a2, b2))
    return len(seen), len(races)


if __name__ == "__main__":
    B = Bd(8, 8, True, False)
    w, k = parse(X)
    print("headline", X, "8x8 cyl e.p. off, count")
    child_table(B, w, k, "count")
    nr, nrace = count_races(B, w, k)
    print(f"  reachable positions (e.p. off, any order, stop at passer): {nr}; race events: {nrace}")

    Y = "W: b5 d4 g3 / B: c6 f6 g4 h6"
    w2, k2 = parse(Y)
    memo = {}
    print("nested node", Y)
    for cf in comps(B, w2, k2):
        zw = frozenset(p for p in w2 if p[0] in cf)
        zk = frozenset(p for p in k2 if p[0] in cf)
        print(f"   component files {sorted(I.LET[f] for f in cf)}: {fmt(zw, zk)} threats={sorted(threats(B, zw, zk, memo))}")
    print(f"   oS={oS(B, w2, k2, 'count')} oW={oW(B, w2, k2, 'count')}")
    clear()

    print("robustness of the headline:")
    for ep in (False, True):
        for rule in ("count", "mover", "opponent"):
            B = Bd(8, 8, True, ep)
            print(f"   ep={'on' if ep else 'off'} rule={rule}: oS={oS(B, w, k, rule)} oW={oW(B, w, k, rule)}")
            clear()
    for big in (64, 1000):
        I.BIG = big
        B = Bd(8, 8, True, False)
        print(f"   BIG={big} ep=off count: oS={oS(B, w, k, 'count')} oW={oW(B, w, k, 'count')}")
        clear()
    I.BIG = 256
