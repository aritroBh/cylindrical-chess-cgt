"""Independent re-check of claim L4.2-critical-races (adversarial verifier, lens REPRODUCE).

Written from scratch: its own pawn move generator, passed-pawn test, promotion
distance and race rule, and NO combinatorial-game library. Values are tested by
the CGT identity  G = X  <=>  G + (-X) is a second-player win (P-position),
decided by plain alternating minimax on the sum of the whole-board convention
game G (4 files, 8 ranks, flat) and a small explicit game H:
    G = *2   <=> G + *2 is P        G = down <=> G + up   is P
    G = up   <=> G + down is P      G = 0    <=> G        is P
Leaves where exactly one side has a passer are +-BIG; since H is infinitesimal,
BIG + H is a win for that side whoever moves, so such a leaf decides the sum.
E.p. semantics follow the model under test: a double step gives the opponent a
right; it stays attached to the component until someone moves IN THE COMPONENT;
if the double-stepper moves there again, the right lapses.

Run:  cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/lemmas/L4.2-critical-races-reproduce/indep.py
"""
from __future__ import annotations

import random
import sys
from collections import Counter

sys.setrecursionlimit(100000)

NF, NR = 4, 8

def other(s):
    return "B" if s == "W" else "W"

# position = (frozenset white, frozenset black, ep) ; ep = (target, victim, owner) or None

def parse(text):
    w, b = text.split("/")
    sqs = lambda part: frozenset(("abcd".index(t[0]), int(t[1:])) for t in part.split(":")[1].split())
    return (sqs(w), sqs(b), None)

def show(p):
    nm = lambda s: "abcd"[s[0]] + str(s[1])
    out = "W: " + " ".join(sorted(map(nm, p[0]))) + " / B: " + " ".join(sorted(map(nm, p[1])))
    if p[2]:
        out += f" (ep {nm(p[2][0])} for {p[2][2]})"
    return out

def has_passer(p, side):
    mine, theirs = (p[0], p[1]) if side == "W" else (p[1], p[0])
    for (f, r) in mine:
        ok = True
        for (g, s) in theirs:
            if abs(g - f) <= 1 and ((s > r) if side == "W" else (s < r)):
                ok = False
                break
        if ok:
            return True
    return False

def status(p):
    w, b = has_passer(p, "W"), has_passer(p, "B")
    if w and b:
        return "race"
    if w:
        return "W"
    if b:
        return "B"
    return None

def dist(p, side):
    mine, theirs = (p[0], p[1]) if side == "W" else (p[1], p[0])
    occ = p[0] | p[1]
    best = 10**6
    for (f, r) in mine:
        # passed?
        if any(abs(g - f) <= 1 and ((s > r) if side == "W" else (s < r)) for (g, s) in theirs):
            continue
        ahead = range(r + 1, NR + 1) if side == "W" else range(1, r)
        if any((f, s) in occ for s in ahead):
            continue
        if side == "W":
            d = (NR - r) - (1 if r == 2 else 0)
        else:
            d = (r - 1) - (1 if r == NR - 1 else 0)
        best = min(best, d)
    return best

def count_verdict(p, mover):
    opp = other(mover)
    return opp if dist(p, opp) <= dist(p, mover) else mover

def gen(p, side, ep_on):
    """children after `side` moves in the component p (lapsing a foreign right)."""
    W, B, ep = p
    if ep and ep[2] != side:
        ep = None
    mine, theirs = (W, B) if side == "W" else (B, W)
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else NR - 1
    occ = W | B
    kids = set()
    def put(m, t, e=None):
        kids.add((frozenset(m), frozenset(t), e) if side == "W" else (frozenset(t), frozenset(m), e))
    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if not 1 <= r1 <= NR:
            continue
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs)
            if r == start and (f, r1 + d) not in occ:
                e = ((f, r1), (f, r1 + d), other(side)) if ep_on else None
                put(rest | {(f, r1 + d)}, theirs, e)
        for g in (f - 1, f + 1):
            if not 0 <= g < NF:
                continue
            if (g, r1) in theirs:
                put(rest | {(g, r1)}, theirs - {(g, r1)})
            elif ep and ep[0] == (g, r1):
                put(rest | {(g, r1)}, theirs - {ep[1]})
    return kids

SMALL = {  # name: (Left options, Right options)
    "0": ((), ()),
    "*": (("0",), ("0",)),
    "*2": (("0", "*"), ("0", "*")),
    "up": (("0",), ("*",)),
    "down": (("*",), ("0",)),
}

class Model:
    def __init__(self, root, ep_on):
        self.root, self.ep_on = root, ep_on
        self.kids = {}
        self.races = set()
        # explore every position reachable by any sequence of moves (CGT tree)
        stack, seen = [root], {root}
        while stack:
            x = stack.pop()
            for side in "WB":
                ks = gen(x, side, ep_on)
                self.kids[(x, side)] = ks
                for c in ks:
                    st = status(c)
                    if st == "race":
                        self.races.add((c, side))
                    elif st is None and c not in seen:
                        seen.add(c)
                        stack.append(c)
        self.positions = seen

    def outcome_is_P(self, h, verdict):
        memo = {}
        def win(x, hh, s):
            k = (x, hh, s)
            r = memo.get(k)
            if r is not None:
                return r
            r = False
            for c in self.kids[(x, s)]:
                st = status(c)
                if st == "race":
                    if verdict(c, s) == s:
                        r = True
                        break
                elif st is not None:
                    if st == s:
                        r = True
                        break
                elif not win(c, hh, other(s)):
                    r = True
                    break
            if not r:
                for h2 in SMALL[hh][0 if s == "W" else 1]:
                    if not win(x, h2, other(s)):
                        r = True
                        break
            memo[k] = r
            return r
        return (not win(self.root, h, "W")) and (not win(self.root, h, "B"))

    def classify(self, verdict):
        for name, h in (("*2", "*2"), ("0", "0"), ("↓", "up"), ("↑", "down")):
            if self.outcome_is_P(h, verdict):
                return name
        return "other"

def make_verdict(override):
    def v(c, mover):
        w = override.get((c, mover))
        return w if w is not None else count_verdict(c, mover)
    return v

CLAIMED = [("W: a2 b5 / B: d7", "W", "↓"), ("W: a2 / B: c4 d7", "B", "↑"),
           ("W: a3 b5 / B: d6", "W", "↓"), ("W: a3 / B: c4 d6", "B", "↑")]

def main():
    root = parse("W: a2 c2 / B: b7 d7")
    for ep_on in (True, False):
        m = Model(root, ep_on)
        print(f"== e.p. {'on' if ep_on else 'off'}: {len(m.positions)} non-terminal positions, "
              f"{len(m.races)} race nodes (child incl. ep field, mover)")
        stripped = Counter((c[0], c[1], s) for c, s in m.races)
        print(f"   race nodes after dropping the ep field: {len(stripped)} "
              f"({sum(1 for v in stripped.values() if v > 1)} of them have an ep twin)")
        print("   count verdict == mover on", sum(1 for c, s in m.races if count_verdict(c, s) == s))
        base = m.classify(make_verdict({}))
        print("   base value (count rule):", base)
        crit = []
        for c, s in sorted(m.races, key=lambda t: (show(t[0]), t[1])):
            w = count_verdict(c, s)
            val = m.classify(make_verdict({(c, s): other(w)}))
            if val != "*2":
                crit.append((show(c), s, w, val))
        print("   single flips that change the value:")
        for t in crit:
            print("     ", t)
        print("   matches claimed list:", sorted(crit) == sorted((a, b, b, d) for a, b, d in CLAIMED))
        # grouped flips: flip a race together with its ep twins
        groups = {}
        for c, s in m.races:
            groups.setdefault((c[0], c[1], s), []).append((c, s))
        gcrit = []
        for key, members in groups.items():
            if len(members) < 2:
                continue
            ov = {(c, s): other(count_verdict(c, s)) for c, s in members}
            val = m.classify(make_verdict(ov))
            if val != "*2":
                gcrit.append((show((key[0], key[1], None)), key[2], val))
        print("   flipping ep-twin groups together, groups that change the value:", gcrit)
        critset = {(parse(a), b) for a, b, _ in CLAIMED}
        mixed = {(c, s): (s if (c, s) in critset else other(s)) for c, s in m.races}
        print("   4 critical won by mover, all others lost by mover:", m.classify(make_verdict(mixed)))
        lost4 = {(c, s): other(s) for c, s in critset}
        print("   4 critical lost by mover, rest count:", m.classify(make_verdict(lost4)))
        allmover = {(c, s): s for c, s in m.races}
        allopp = {(c, s): other(s) for c, s in m.races}
        print("   all mover:", m.classify(make_verdict(allmover)),
              " all opponent:", m.classify(make_verdict(allopp)))
        # random trials, order made deterministic by sorting
        order = sorted(m.races, key=lambda t: (show(t[0]), t[1]))
        for seed, trials in ((1, 200), (2, 200), (3, 200), (12345, 1000)):
            rng = random.Random(seed)
            hist = Counter()
            for _ in range(trials):
                ov = {(c, s): (s if (c, s) in critset else rng.choice("WB")) for c, s in order}
                hist[m.classify(make_verdict(ov))] += 1
            print(f"   random rest, seed {seed}, {trials} trials:", dict(hist))

if __name__ == "__main__":
    main()
