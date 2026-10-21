"""Independent check of claim C2 (verifier run 2, REFUTE lens).

Written from scratch for this check. Imports nothing from cylcgt, sumtest,
crosscheck, or the earlier verifier scripts in ../. Pure stdlib.

Decisive quantity: the outcome class of G + X, by exhaustive minimax, for
G = W a2 c2 / B b7 d7 on a 4-file flat 8-rank board and X from a reference set
of explicit game trees. G = *2 iff G + *2 is a P-position (-*2 = *2).

Model (Elkies 1996 as stated in the task):
  - White = Left, Black = Right; normal play (no move anywhere = loss).
  - As soon as a state has exactly one side owning a passed pawn, that side
    wins the whole sum (BIG = 256 dominates every X used).
  - Both sides passed: race, decided by RACE rule against the player who made
    the last move ("mover").
  - passed test "textbook": no enemy pawn strictly ahead on own/adjacent file.
    "aware": additionally, the pawn that just double-stepped is NOT passed
    while the opponent holds a usable e.p. capture of it.
  - e.p. scope "local": the right survives moves made in X and dies with the
    next move made in G (what a CGT component value implies);
    "global": any move anywhere kills it (chess).

Run:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/sumtest/C2-refute/run2/mine.py
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(1_000_000)

# ---------------------------------------------------------------- abstract X
ZERO = ((), ())


def gm(L, R):
    return (tuple(L), tuple(R))


STAR = gm([ZERO], [ZERO])
STAR2 = gm([ZERO, STAR], [ZERO, STAR])
STAR3 = gm([ZERO, STAR, STAR2], [ZERO, STAR, STAR2])
UP = gm([ZERO], [STAR])
DOWN = gm([STAR], [ZERO])
ONE = gm([ZERO], [])
MONE = gm([], [ZERO])
HALF = gm([ZERO], [ONE])
MHALF = gm([MONE], [ZERO])
HOT10 = gm([ONE], [ZERO])
PM1 = gm([ONE], [MONE])
TINY1 = gm([ZERO], [gm([ZERO], [MONE])])

REF = [("0", ()), ("*", (STAR,)), ("*2", (STAR2,)), ("*3", (STAR3,)),
       ("up", (UP,)), ("down", (DOWN,)), ("up*", (UP, STAR)),
       ("dup*", (UP, UP, STAR)), ("1/2", (HALF,)), ("-1/2", (MHALF,)),
       ("1", (ONE,)), ("-1", (MONE,)), ("{1|0}", (HOT10,)), ("+-1", (PM1,)),
       ("tiny1", (TINY1,))]


def norm(X):
    return tuple(sorted(c for c in X if c != ZERO))


def x_moves(X, side):
    k = 0 if side == "W" else 1
    for i, c in enumerate(X):
        for o in c[k]:
            yield norm(X[:i] + (o,) + X[i + 1:])


# ---------------------------------------------------------------- pawn model
class Cfg:
    files = 4
    ranks = 8
    wrap = False
    ep = True
    aware = False
    scope = "local"
    race = "count"


C = Cfg()
OTHER = {"W": "B", "B": "W"}
race_states = set()
split_states = set()


def adj(f):
    out = []
    for d in (-1, 1):
        g = f + d
        if C.wrap:
            out.append(g % C.files)
        elif 0 <= g < C.files:
            out.append(g)
    return out


def ep_capture_possible(W, B, ep):
    if ep is None:
        return False
    target, victim, holder = ep
    mine = W if holder == "W" else B
    return any((g, victim[1]) in mine for g in adj(victim[0]))


def pawn_passed(p, side, W, B, ep):
    f, r = p
    enemy = B if side == "W" else W
    files = {f, *adj(f)}
    for (g, s) in enemy:
        if g in files and ((s > r) if side == "W" else (s < r)):
            return False
    if C.aware and ep is not None and ep[1] == p and ep[2] != side \
            and ep_capture_possible(W, B, ep):
        return False
    return True


def has_passer(side, W, B, ep):
    return any(pawn_passed(p, side, W, B, ep) for p in (W if side == "W" else B))


def dist(side, W, B, ep):
    occ = W | B
    best = 10 ** 6
    for p in (W if side == "W" else B):
        if not pawn_passed(p, side, W, B, ep):
            continue
        f, r = p
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, C.ranks + 1)):
                continue
            d = C.ranks - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            d = r - 1 - (1 if r == C.ranks - 1 else 0)
        best = min(best, d)
    return best


def terminal(W, B, ep, mover):
    """'W'/'B' if the state is decided, else None."""
    wp = has_passer("W", W, B, ep)
    bp = has_passer("B", W, B, ep)
    if wp and bp:
        race_states.add((W, B, ep, mover))
        if C.race == "mover":
            return mover
        if C.race == "opponent":
            return OTHER[mover]
        opp = OTHER[mover]
        return opp if dist(opp, W, B, ep) <= dist(mover, W, B, ep) else mover
    if wp:
        return "W"
    if bp:
        return "B"
    return None


def pawn_moves(W, B, ep, side):
    mine, theirs = (W, B) if side == "W" else (B, W)
    d = 1 if side == "W" else -1
    home = 2 if side == "W" else C.ranks - 1
    occ = W | B
    res = []

    def put(nm, nt, nep):
        res.append((nm, nt, nep) if side == "W" else (nt, nm, nep))

    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if not 1 <= r1 <= C.ranks:
            continue
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs, None)
            r2 = r + 2 * d
            if r == home and (f, r2) not in occ:
                nep = ((f, r1), (f, r2), OTHER[side]) if C.ep else None
                put(rest | {(f, r2)}, theirs, nep)
        for g in adj(f):
            t = (g, r1)
            if t in theirs:
                put(rest | {t}, theirs - {t}, None)
            elif ep is not None and ep[2] == side and ep[0] == t:
                put(rest | {t}, theirs - {ep[1]}, None)
    return res


def gapped(W, B):
    fs = sorted({f for f, _ in W | B})
    if len(fs) < 2:
        return False
    if not C.wrap:
        return fs[-1] - fs[0] + 1 != len(fs)
    return len(fs) < C.files and sum(1 for i, f in enumerate(fs)
                                     if (fs[(i + 1) % len(fs)] - f) % C.files != 1) > 1


@lru_cache(maxsize=None)
def wins(W, B, ep, X, tomove):
    """True iff the player to move wins G + X."""
    t = terminal(W, B, ep, OTHER[tomove])
    if t is not None:
        return t == tomove
    if gapped(W, B):
        split_states.add((W, B, ep))
    nxt = OTHER[tomove]
    for (W2, B2, ep2) in pawn_moves(W, B, ep, tomove):
        if not wins(W2, B2, ep2, X, nxt):
            return True
    ep_after_x = ep if C.scope == "local" else None
    for X2 in x_moves(X, tomove):
        if not wins(W, B, ep_after_x, X2, nxt):
            return True
    return False


def outcome(W, B, X):
    lw = wins(W, B, None, X, "W")
    rw = wins(W, B, None, X, "B")
    return {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(lw, rw)]


def parse(text):
    wp, bp = text.split("/")
    def sqs(part):
        return frozenset(("abcdefghijklmnop".index(t[0]), int(t[1:])) for t in part.split(":")[1].split())
    return sqs(wp), sqs(bp)


def vector(W, B):
    return "".join(outcome(W, B, norm(X)) for _, X in REF)


def configure(**kw):
    for k, v in kw.items():
        setattr(C, k, v)
    wins.cache_clear()
    race_states.clear()
    split_states.clear()


def main():
    pos = "W: a2 c2 / B: b7 d7"
    W, B = parse(pos)
    configure(ep=False, aware=False, scope="local", race="count")
    E = frozenset()
    zero_vec = vector(E, E)
    target = "".join(outcome(E, E, norm((STAR2,) + X)) for _, X in REF)
    print("reference order:", " ".join(n for n, _ in REF))
    print("0 + X vector  (G empty):", zero_vec)
    print("*2 + X vector (G empty):", target)
    print(f"G = {pos}, {C.files} files, flat, {C.ranks} ranks")
    print("race     ep   test      scope  | G  G+* G+*2 G+*3 | vector          | =*2 | =0  | race states | split non-terminal states")
    settings = [("off", False, False, "local"),
                ("on", True, False, "local"), ("on", True, False, "global"),
                ("on", True, True, "local"), ("on", True, True, "global")]
    for race in ("count", "mover", "opponent"):
        for epn, ep, aware, scope in settings:
            configure(ep=ep, aware=aware, scope=scope, race=race)
            v = vector(W, B)
            test = "aware" if aware else "textbook"
            print(f"{race:8s} {epn:4s} {test:9s} {scope:6s} | {v[0]}  {v[1]}   {v[2]}    {v[3]}    | {v} | "
                  f"{'yes' if v == target else 'no ':3s} | {'yes' if v == zero_vec else 'no ':3s} | {len(race_states):11d} | {len(split_states)}")


if __name__ == "__main__":
    main()
