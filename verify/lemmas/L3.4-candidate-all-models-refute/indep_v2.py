"""Independent re-check of claim L3.4 (the *2 candidate W a2 c2 / B b7 d7).

Written from scratch by the adversarial verifier (2026-10-16). It imports NOTHING
from cylcgt/, lemmas/ or crosscheck/. Pure stdlib.

Method (no canonical forms needed):
  G = *2  <=>  G - *2 = G + *2 is a second-player win (outcome P).
  G = 0   <=>  G is a second-player win.
So for each model (W, WF, S) we run an exact alternating-play minimax on the
disjunctive sum  model(X) + *k  (k = 0, 1, 2, 3) with CGT semantics: a move in
the nim heap leaves the pawn component's state (including any e.p. right)
untouched; a frozen +-BIG is an integer summand (Left may move n -> n-1 if n > 0,
Right n -> n+1 if n < 0).

Models (as defined in notes/lemmas.md section 0, re-implemented here):
  W : whole board, first passer ends the game (+-BIG), race scored by rule.
  WF: W plus a losing "king move" for each side at every non-terminal node.
  S : sum model: components separated by empty files; a component that gets a
      passer (or a race) is frozen into +-BIG and play continues elsewhere;
      e.p. rights live inside their component.

Usage:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python -I verify/lemmas/L3.4-candidate-all-models-refute/indep_v2.py
"""
from __future__ import annotations

import sys
from functools import lru_cache

sys.setrecursionlimit(100000)

BIG = 256
RANKS = 8


# ---------------------------------------------------------------- board / moves
class Bd:
    def __init__(self, files, wrap, ep):
        self.files, self.wrap, self.ep = files, wrap, ep

    def adj(self, f):
        out = []
        for g in (f - 1, f + 1):
            if self.wrap:
                out.append(g % self.files)
            elif 0 <= g < self.files:
                out.append(g)
        return out

    def key(self):
        return (self.files, self.wrap, self.ep)


def sqn(s):
    return "abcdefgh"[s[0]] + str(s[1])


def parse(t):
    w, b = t.split("/")
    p = lambda part: frozenset(("abcdefgh".index(x[0]), int(x[1:])) for x in part.split(":")[1].split())
    return (p(w), p(b), None)


def is_passed(bd, pos, side):
    """Some pawn of `side` has no enemy pawn ahead on its own or an adjacent file."""
    w, b, _ = pos
    mine, opp = (w, b) if side == "W" else (b, w)
    for (f, r) in mine:
        fs = {f, *bd.adj(f)}
        if side == "W":
            if not any(g in fs and s > r for (g, s) in opp):
                return True
        else:
            if not any(g in fs and s < r for (g, s) in opp):
                return True
    return False


def gen(bd, pos, side):
    """Pawn moves of `side` from pos. A right belonging to the other side is ignored
    (it expires when `side` moves). Children never inherit a right except one
    freshly created by a double step (for the opponent)."""
    w, b, ep = pos
    mine, opp = (w, b) if side == "W" else (b, w)
    occ = w | b
    dr = 1 if side == "W" else -1
    start = 2 if side == "W" else RANKS - 1
    other = "B" if side == "W" else "W"
    my_ep = ep if (ep is not None and ep[2] == side) else None
    res = []

    def put(nm, no, e=None):
        res.append((frozenset(nm), frozenset(no), e) if side == "W" else (frozenset(no), frozenset(nm), e))

    for p in mine:
        f, r = p
        rest = mine - {p}
        r1 = r + dr
        if not 1 <= r1 <= RANKS:
            continue
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, opp)
            r2 = r + 2 * dr
            if r == start and (f, r2) not in occ and 1 <= r2 <= RANKS:
                e = ((f, r1), (f, r2), other) if bd.ep else None
                put(rest | {(f, r2)}, opp, e)
        for g in bd.adj(f):
            t = (g, r1)
            if t in opp:
                put(rest | {t}, opp - {t})
            elif my_ep is not None and my_ep[0] == t:
                put(rest | {t}, opp - {my_ep[1]})
    # dedupe preserving order
    seen, out = set(), []
    for x in res:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def dist(bd, pos, side):
    """Smallest promotion distance among passed FRONT pawns of side (double step = 1)."""
    w, b, _ = pos
    mine = w if side == "W" else b
    occ = w | b
    best = None
    for (f, r) in mine:
        single = (frozenset([(f, r)]), b, None) if side == "W" else (w, frozenset([(f, r)]), None)
        if not is_passed(bd, single, side):
            continue
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, RANKS + 1)):
                continue
            d = RANKS - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            d = r - 1 - (1 if r == RANKS - 1 else 0)
        best = d if best is None else min(best, d)
    return 10 ** 6 if best is None else best


RACE_LOG = {}


def race_winner(bd, child, mover, rule):
    other = "B" if mover == "W" else "W"
    if rule == "mover":
        return mover
    if rule == "opponent":
        return other
    if rule == "count":
        return other if dist(bd, child, other) <= dist(bd, child, mover) else mover
    if rule == "count_tie_mover":  # sensitivity variant, not part of the claim
        return other if dist(bd, child, other) < dist(bd, child, mover) else mover
    raise ValueError(rule)


def classify(bd, pos):
    """None (no passer), 'W', 'B', or 'race'."""
    a, c = is_passed(bd, pos, "W"), is_passed(bd, pos, "B")
    if a and c:
        return "race"
    if a:
        return "W"
    if c:
        return "B"
    return None


def components(bd, pos):
    w, b, ep = pos
    files = sorted({f for f, _ in w | b})
    groups = []
    for f in files:
        if groups and f == groups[-1][-1] + 1:
            groups[-1].append(f)
        else:
            groups.append([f])
    if bd.wrap and len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == bd.files - 1:
        groups[0] = groups.pop() + groups[0]
    out = []
    for g in groups:
        fs = set(g)
        e = ep if (ep is not None and ep[0][0] in fs) else None
        out.append((frozenset(p for p in w if p[0] in fs), frozenset(p for p in b if p[0] in fs), e))
    return out


# ---------------------------------------------------------------- W / WF  (+ *k)
def make_W(bd, rule, kings):
    @lru_cache(maxsize=None)
    def wins(pos, k, tm):
        """True iff side `tm` to move wins  W(pos) + *k  (pos non-terminal)."""
        other = "B" if tm == "W" else "W"
        for c in gen(bd, pos, tm):
            cl = classify(bd, c)
            if cl == "race":
                if race_winner(bd, c, tm, rule) == tm:
                    return True  # +-BIG + *k: sign decides
                continue
            if cl is not None:
                if cl == tm:
                    return True
                continue
            if not wins(c, k, other):
                return True
        for j in range(k):
            if not wins(pos, j, other):
                return True
        # king move (kings=True) is a move to -BIG/+BIG for the mover's opponent: always losing
        return False
    return wins


def outcome_from(wins_fn, pos, k):
    lw = wins_fn(pos, k, "W")
    rw = wins_fn(pos, k, "B")
    return {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(lw, rw)]


# ---------------------------------------------------------------- S (+ *k)
def make_S(bd, rule):
    def freeze_or_split(c, mover):
        """child component c after `mover` moved in it -> (delta_N, [components])"""
        cl = classify(bd, c)
        if cl == "race":
            return (BIG if race_winner(bd, c, mover, rule) == "W" else -BIG), []
        if cl == "W":
            return BIG, []
        if cl == "B":
            return -BIG, []
        return 0, components(bd, c)

    def norm(comps):
        return tuple(sorted(comps, key=lambda p: (sorted(p[0]), sorted(p[1]), str(p[2]))))

    @lru_cache(maxsize=None)
    def wins(comps, N, k, tm):
        other = "B" if tm == "W" else "W"
        for i, z in enumerate(comps):
            rest = comps[:i] + comps[i + 1:]
            for c in gen(bd, z, tm):
                dN, new = freeze_or_split(c, tm)
                if not wins(norm(rest + tuple(new)), N + dN, k, other):
                    return True
        if tm == "W" and N > 0 and not wins(comps, N - 1, k, other):
            return True
        if tm == "B" and N < 0 and not wins(comps, N + 1, k, other):
            return True
        for j in range(k):
            if not wins(comps, N, j, other):
                return True
        return False

    def root(pos, k, tm):
        cl = classify(bd, pos)
        if cl == "W":
            comps, N = (), BIG
        elif cl == "B":
            comps, N = (), -BIG
        else:
            assert cl is None
            comps, N = norm(components(bd, pos)), 0
        return wins(comps, N, k, tm)
    return root, wins


# ---------------------------------------------------------------- tree statistics
def reach(bd, pos):
    """All positions reachable by moves of either side in any order, not expanding
    positions with a passer (terminal or race)."""
    seen = {pos}
    st = [pos]
    while st:
        x = st.pop()
        if classify(bd, x) is not None:
            continue
        for side in ("W", "B"):
            for c in gen(bd, x, side):
                if c not in seen:
                    seen.add(c)
                    st.append(c)
    return seen


def race_nodes(bd, pos):
    """Distinct (child, mover) race events in the reachable tree."""
    ev = set()
    for x in reach(bd, pos):
        if classify(bd, x) is not None:
            continue
        for side in ("W", "B"):
            for c in gen(bd, x, side):
                if classify(bd, c) == "race":
                    ev.add((c, side))
    return ev


def main():
    X4 = parse("W: a2 c2 / B: b7 d7")
    X8 = parse("W: a2 c2 g4 / B: b7 d7 g5")
    rules = ("count", "mover", "opponent", "count_tie_mover")
    print("Independent check of L3.4 (verifier script, no project imports)")
    for ep in (True, False):
        b4, b8 = Bd(4, False, ep), Bd(8, False, ep)
        r4 = reach(b4, X4)
        nt4 = [x for x in r4 if classify(b4, x) is None]
        multi = [x for x in nt4 if len(components(b4, x)) > 1]
        r8 = reach(b8, X8)
        nt8 = [x for x in r8 if classify(b8, x) is None]
        multi8 = [x for x in nt8 if len([c for c in components(b8, x) if c[0] | c[1]]) > 2]
        print(f"\n== e.p. {'on' if ep else 'off'} ==")
        print(f"4-file: reachable {len(r4)}, non-terminal {len(nt4)}, non-terminal with >=2 components: {len(multi)}")
        print(f"8x8 (+g4/g5): reachable {len(r8)}, non-terminal {len(nt8)}, non-terminal with >2 components: {len(multi8)}")
        print(f"race events (child, mover) on 4 files: {len(race_nodes(b4, X4))}")
        for rule in rules:
            row = []
            for name, bd, X in (("4", b4, X4), ("8", b8, X8)):
                Wf = make_W(bd, rule, False)
                WFf = make_W(bd, rule, True)
                Sroot, _ = make_S(bd, rule)
                for model, fn in (("W", Wf), ("WF", WFf)):
                    oc = [outcome_from(fn, X, k) for k in range(4)]
                    row.append(f"{model}{name}:" + "".join(oc))
                oc = []
                for k in range(4):
                    lw, rw = Sroot(X, k, "W"), Sroot(X, k, "B")
                    oc.append({(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(lw, rw)])
                row.append(f"S{name}:" + "".join(oc))
            print(f"  {rule:16s} outcomes of model+*k for k=0,1,2,3: " + "  ".join(row))
    print("\nReading: value = *2 iff the k=2 letter is P; value = 0 iff the k=0 letter is P.")


if __name__ == "__main__":
    main()
