"""Second, structurally different re-check for claim L4.2-critical-races
(adversarial verifier, session 2). Imports nothing from cylcgt/, lemmas/ or indep.py.

Representation: bitmasks on a 4-file x 8-rank flat board, square = f + 4*(r-1).
No canonical forms at all. Equality G = V is decided by the CGT-free test
"G + (-V) is a second-player win", by plain alternating minimax over pairs
(pawn node, node of a small explicit game tree).  Numbers +-BIG reached in the
pawn part decide the sum at once (BIG + infinitesimal has the sign of BIG; all
comparison games used here are infinitesimals or 0).

Run from the project root:
  .venv/bin/python verify/lemmas/L4.2-critical-races-refute/fresh2.py
"""
import random
import sys

sys.setrecursionlimit(100000)
F, R = 4, 8


def sq(f, r):
    return f + F * (r - 1)


def parse(text):
    w, b = text.split("/")
    def m(part):
        x = 0
        for t in part.split(":")[1].split():
            x |= 1 << sq("abcd".index(t[0]), int(t[1:]))
        return x
    return (m(w), m(b), -1, "")  # (white, black, ep target square or -1, side allowed to capture)


def name(p):
    def lst(x):
        return " ".join(sorted("abcd"[i % F] + str(i // F + 1) for i in range(32) if x >> i & 1))
    s = "W: %s / B: %s" % (lst(p[0]), lst(p[1]))
    if p[2] >= 0:
        s += " (ep %s%d for %s)" % ("abcd"[p[2] % F], p[2] // F + 1, p[3])
    return s


def pawns_of(x):
    return [(i % F, i // F + 1) for i in range(32) if x >> i & 1]


def is_passed(f, r, side, enemy):
    for g, s in pawns_of(enemy):
        if abs(g - f) <= 1 and (s > r if side == "W" else s < r):
            return False
    return True


def any_passer(p, side):
    mine, enemy = (p[0], p[1]) if side == "W" else (p[1], p[0])
    return any(is_passed(f, r, side, enemy) for f, r in pawns_of(mine))


def kind(p):
    w, b = any_passer(p, "W"), any_passer(p, "B")
    return "race" if (w and b) else ("W" if w else ("B" if b else None))


def gen(p, side, epgame):
    """Children after one move of `side`. A right owned by the other side is ignored."""
    white, black, ept, epside = p
    mine, enemy = (white, black) if side == "W" else (black, white)
    occ = white | black
    dr = 1 if side == "W" else -1
    home = 2 if side == "W" else 7
    opp = "B" if side == "W" else "W"
    out = []
    for f, r in pawns_of(mine):
        me = mine & ~(1 << sq(f, r))
        r1 = r + dr
        if not 1 <= r1 <= R:
            continue
        if not occ >> sq(f, r1) & 1:
            out.append((me | 1 << sq(f, r1), enemy, -1, ""))
            r2 = r + 2 * dr
            if r == home and not occ >> sq(f, r2) & 1:
                out.append((me | 1 << sq(f, r2), enemy, sq(f, r1) if epgame else -1, opp if epgame else ""))
        for g in (f - 1, f + 1):
            if not 0 <= g < F:
                continue
            t = sq(g, r1)
            if enemy >> t & 1:
                out.append((me | 1 << t, enemy & ~(1 << t), -1, ""))
            elif ept == t and epside == side:
                victim = sq(g, r)  # the double-stepped pawn stands beside, on rank r
                out.append((me | 1 << t, enemy & ~(1 << victim), -1, ""))
    res = []
    for m_, e_, a, b in out:
        q = (m_, e_, a, b) if side == "W" else (e_, m_, a, b)
        if q not in res:
            res.append(q)
    return res


def distance(p, side):
    mine, enemy = (p[0], p[1]) if side == "W" else (p[1], p[0])
    occ = p[0] | p[1]
    best = 10 ** 6
    for f, r in pawns_of(mine):
        if not is_passed(f, r, side, enemy):
            continue
        ahead = range(r + 1, R + 1) if side == "W" else range(1, r)
        if any(occ >> sq(f, s) & 1 for s in ahead):
            continue
        d = (R - r) if side == "W" else (r - 1)
        if (side == "W" and r == 2) or (side == "B" and r == R - 1):
            d -= 1
        best = min(best, d)
    return best


def count_rule(p, mover):
    nu = "B" if mover == "W" else "W"
    return nu if distance(p, nu) <= distance(p, mover) else mover


def explore(root, epgame):
    seen, todo, races = {root}, [root], set()
    while todo:
        x = todo.pop()
        if kind(x) is not None:
            continue
        for side in "WB":
            for c in gen(x, side, epgame):
                if kind(c) == "race":
                    races.add((c, side))
                if c not in seen:
                    seen.add(c)
                    todo.append(c)
    return seen, races


# small games as explicit trees (L, R)
Z = ((), ())
S1 = ((Z,), (Z,))
S2 = ((Z, S1), (Z, S1))
UP = ((Z,), (S1,))
DN = ((S1,), (Z,))
UPS = ((Z, S1), (Z,))
DNS = ((Z,), (Z, S1))
S3 = ((Z, S1, S2), (Z, S1, S2))
NEG = {"0": Z, "*": S1, "*2": S2, "*3": S3, "up": DN, "down": UP, "up*": DNS, "down*": UPS}


def equals(root, epgame, verdict, vname, frozen=False):
    """True iff W(root) (with race verdicts from `verdict`) equals vname.
    frozen: every non-terminal pawn node also offers each side a move to the
    opponent's BIG (a 'king move'); such a move can never be a winning try, and
    the side to move can always make one, so it only matters as 'having a move'
    -- but having a losing move is the same as having none for the minimax.
    Hence frozen does not change the CGT-free test; it is accepted for clarity."""
    H = NEG[vname]
    memo = {}

    def win(p, h, s):
        k = (p, h, s)
        if k in memo:
            return memo[k]
        o = "B" if s == "W" else "W"
        ok = False
        for c in gen(p, s, epgame):
            kc = kind(c)
            if kc == "race":
                if verdict(c, s) == s:
                    ok = True
                    break
            elif kc is not None:
                if kc == s:
                    ok = True
                    break
            elif not win(c, h, o):
                ok = True
                break
        if not ok:
            for h2 in (h[0] if s == "W" else h[1]):
                if not win(p, h2, o):
                    ok = True
                    break
        memo[k] = ok
        return ok

    return not win(root, H, "W") and not win(root, H, "B")


def identify(root, epgame, verdict):
    for v in ("*2", "0", "*", "up", "down", "up*", "down*", "*3"):
        if equals(root, epgame, verdict, v):
            return v
    return "other"


CLAIMED = {("W: a2 b5 / B: d7", "W"): "down", ("W: a2 / B: c4 d7", "B"): "up",
           ("W: a3 b5 / B: d6", "W"): "down", ("W: a3 / B: c4 d6", "B"): "up"}


def main():
    root = parse("W: a2 c2 / B: b7 d7")
    other = lambda m: "B" if m == "W" else "W"
    for epgame in (True, False):
        nodes, races = explore(root, epgame)
        order = sorted(races, key=lambda cm: (name(cm[0]), cm[1]))
        cnt = lambda c, m: count_rule(c, m)
        print("=== e.p. %s: reachable nodes %d, race keys (child, mover) %d, count==mover on %d"
              % ("on" if epgame else "off", len(nodes), len(races),
                 sum(1 for c, m in races if cnt(c, m) == m)))
        print("   W(count) =", identify(root, epgame, cnt),
              "| W(mover) =", identify(root, epgame, lambda c, m: m),
              "| W(opponent) =", identify(root, epgame, lambda c, m: other(m)))
        crit = []
        for key in order:
            fl = other(cnt(*key))
            v = lambda c, m, key=key, fl=fl: fl if (c, m) == key else cnt(c, m)
            if not equals(root, epgame, v, "*2"):
                crit.append((name(key[0]), key[1], cnt(*key), identify(root, epgame, v)))
        print("   single flips from count that change the value (%d):" % len(crit))
        for t in crit:
            print("      ", t)
        ok = sorted((a, b) for a, b, _, _ in crit) == sorted(CLAIMED) and \
            all(CLAIMED[(a, b)] == val for a, b, _, val in crit)
        print("   matches the claimed list and values:", ok)
        critset = {key for key in races if (name(key[0]), key[1]) in CLAIMED}
        v_mixed = lambda c, m: m if (c, m) in critset else other(m)
        print("   4 won by mover, all others lost by mover:", identify(root, epgame, v_mixed))
        v_lost = lambda c, m: other(m) if (c, m) in critset else cnt(c, m)
        print("   4 lost by mover, others count:", identify(root, epgame, v_lost))
        # mover baseline, for context
        mcrit = []
        for key in order:
            v = lambda c, m, key=key: other(m) if (c, m) == key else m
            if not equals(root, epgame, v, "*2"):
                mcrit.append((name(key[0]), key[1], identify(root, epgame, v)))
        print("   context: single flips from the MOVER baseline that change *2 (%d): %s" % (len(mcrit), mcrit))
        # random others, deterministic sorted order, several seeds
        for seed, n in ((1, 200), (2, 200), (3, 200), (4, 200), (5, 200)):
            rng = random.Random(seed)
            hist = {}
            for _ in range(n):
                ov = {key: (key[1] if key in critset else rng.choice("WB")) for key in order}
                r = identify(root, epgame, lambda c, m, ov=ov: ov[(c, m)])
                hist[r] = hist.get(r, 0) + 1
            print("   random others, seed %d, %d trials: %s" % (seed, n, dict(sorted(hist.items()))))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
