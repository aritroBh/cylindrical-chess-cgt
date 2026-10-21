"""Independent nimber scan (no cylcgt import).

Enumerates RAW (no symmetry reduction) single components ("atoms": every file
of the strip/cylinder occupied, pawns on ranks 2..7, no passed pawn at the
root) and decides, for each, whether its model value equals *k for k = 1..5,
using G == *k  iff  G + *k is a second-player win.

The solver reproduces the cylcgt *model* semantics exactly, including sums:
  * state = live pawn components (split at empty files) + an integer t + X;
  * a move that leaves a component with passer(s) for exactly one side, or a
    race (both sides) resolved by RACE_RULE, removes it and adds +-256 to t;
  * integer t > 0 gives Left the move t -> t-1 (t < 0: Right, t -> t+1);
  * an e.p. right lives in its component until the next move made there.
Fast path (provably correct): if t != 0 and no live component can ever
produce a BIG of the opposite sign, then |t| >= 256 > (game depth <= 30) + |X|,
so the side favoured by t wins.

Atoms suffice for single components: a component never acquires a pawn on a
file outside its span, and an empty file / board edge are equivalent, so every
single component with k pawns on any board is an atom of a flat strip of
width <= k or a cylinder ring of width <= k.

Run (examples):
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python -I verify/cylatlas/C5-reproduce/indep_scan.py --maxpawns 4 --settings all
  .venv/bin/python -I verify/cylatlas/C5-reproduce/indep_scan.py --minpawns 5 --maxpawns 5 --settings count/1
"""
import argparse
import itertools
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache

sys.setrecursionlimit(200000)
RANKS = 8
BIG = 256

ZERO = ((), ())


def G(L, R):
    return (tuple(L), tuple(R))


def nim(k):
    opts = [nim(i) for i in range(k)]
    return G(opts, opts)


NIMS = {k: nim(k) for k in range(0, 6)}

# ---------------- pawn rules ----------------
CFG = {}


def adj(f):
    n, wrap = CFG["n"], CFG["wrap"]
    out = []
    for d in (-1, 1):
        g = f + d
        if wrap:
            out.append(g % n)
        elif 0 <= g < n:
            out.append(g)
    return out


def is_passed(side, f, r, W, B):
    files = {f, *adj(f)}
    if side == "W":
        return not any(g in files and s > r for g, s in B)
    return not any(g in files and s < r for g, s in W)


def has_passer(side, W, B):
    return any(is_passed(side, f, r, W, B) for f, r in (W if side == "W" else B))


def dist(side, W, B):
    best = 10 ** 6
    mine = W if side == "W" else B
    for f, r in mine:
        if not is_passed(side, f, r, W, B):
            continue
        if side == "W":
            if any((f, s) in mine for s in range(r + 1, RANKS + 1)):
                continue
            d = (RANKS - r) - (1 if r == 2 else 0)
        else:
            if any((f, s) in mine for s in range(1, r)):
                continue
            d = (r - 1) - (1 if r == RANKS - 1 else 0)
        best = min(best, d)
    return best


def pawn_moves(side, W, B, ep):
    W, B = frozenset(W), frozenset(B)
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = W | B
    fwd = 1 if side == "W" else -1
    home = 2 if side == "W" else RANKS - 1
    other = "B" if side == "W" else "W"
    res = set()

    def put(m2, t2, e2=None):
        res.add((m2, t2, e2) if side == "W" else (t2, m2, e2))

    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + fwd
        if not 1 <= r1 <= RANKS:
            continue
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs)
            r2 = r + 2 * fwd
            if r == home and (f, r2) not in occ:
                put(rest | {(f, r2)}, theirs, ((f, r1), (f, r2), other) if CFG["ep"] else None)
        for g in adj(f):
            t = (g, r1)
            if t in theirs:
                put(rest | {t}, theirs - {t})
            elif ep is not None and ep[2] == side and ep[0] == t:
                put(rest | {t}, theirs - {ep[1]})
    return res


def decided(mover, W, B):
    wp, bp = has_passer("W", W, B), has_passer("B", W, B)
    if wp and bp:
        rule = CFG["rule"]
        if rule == "mover":
            win = mover
        elif rule == "opponent":
            win = "B" if mover == "W" else "W"
        else:
            opp = "B" if mover == "W" else "W"
            win = opp if dist(opp, W, B) <= dist(mover, W, B) else mover
        return 1 if win == "W" else -1
    return 1 if wp else (-1 if bp else 0)


def comp_key(W, B, ep):
    return (tuple(sorted(W)), tuple(sorted(B)), ep)


def split(W, B, ep):
    n, wrap = CFG["n"], CFG["wrap"]
    occ = sorted({f for f, _ in W} | {f for f, _ in B})
    groups = []
    for f in occ:
        if groups and f == groups[-1][-1] + 1:
            groups[-1].append(f)
        else:
            groups.append([f])
    if wrap and len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == n - 1:
        groups[0] = groups.pop() + groups[0]
    out = []
    for gr in groups:
        fs = set(gr)
        e = ep if (ep and ep[0][0] in fs) else None
        out.append(comp_key([p for p in W if p[0] in fs], [p for p in B if p[0] in fs], e))
    return out


@lru_cache(maxsize=None)
def comp_children(c, side):
    """list of (sign, newcomps): sign != 0 means component resolved to sign*BIG."""
    W, B, ep = c
    out = []
    for (W2, B2, e2) in pawn_moves(side, W, B, ep):
        d = decided(side, W2, B2)
        if d:
            out.append((d, ()))
        else:
            out.append((0, tuple(split(W2, B2, e2))))
    return out


@lru_cache(maxsize=None)
def can_produce(c, sign):
    """Can component c (from any reachable state) resolve to sign*BIG?"""
    for side in ("W", "B"):
        for d, sub in comp_children(c, side):
            if d == sign:
                return True
            if d == 0 and any(can_produce(s, sign) for s in sub):
                return True
    return False


@lru_cache(maxsize=None)
def wins(comps, t, X, side):
    sgn = 1 if side == "W" else -1
    other = "B" if side == "W" else "W"
    if t != 0:
        s = 1 if t > 0 else -1
        if not any(can_produce(c, -s) for c in comps):
            return s == sgn
    for i, c in enumerate(comps):
        rest = comps[:i] + comps[i + 1:]
        for d, sub in comp_children(c, side):
            nc = tuple(sorted(rest + sub))
            if not wins(nc, t + d * BIG, X, other):
                return True
    if sgn * t > 0:
        if not wins(comps, t - sgn, X, other):
            return True
    for X2 in (X[0] if side == "W" else X[1]):
        if not wins(comps, t, X2, other):
            return True
    return False


def nim_value(c):
    """k if the component equals *k (k in 0..5), else None."""
    comps = (c,)
    lf, rf = wins(comps, 0, ZERO, "W"), wins(comps, 0, ZERO, "B")
    if not lf and not rf:
        return 0
    if not (lf and rf):
        return None
    for k in range(1, 6):
        X = NIMS[k]
        if not wins(comps, 0, X, "W") and not wins(comps, 0, X, "B"):
            return k
    return None


def atoms(n, wrap, npawns):
    sqs = [(f, r) for f in range(n) for r in range(2, RANKS)]
    for S in itertools.combinations(sqs, npawns):
        if len({f for f, _ in S}) != n:
            continue
        for mask in range(1, 2 ** npawns - 1):
            W = [S[i] for i in range(npawns) if mask >> i & 1]
            B = [S[i] for i in range(npawns) if not mask >> i & 1]
            yield W, B


def task(args):
    n, wrap, npawns, rule, ep = args
    CFG.clear()
    CFG.update(n=n, wrap=wrap, ep=ep, rule=rule)
    for f in (comp_children, can_produce, wins):
        f.cache_clear()
    t0 = time.time()
    found = []
    tot = 0
    for W, B in atoms(n, wrap, npawns):
        Wf, Bf = frozenset(W), frozenset(B)
        if has_passer("W", Wf, Bf) or has_passer("B", Wf, Bf):
            continue
        tot += 1
        k = nim_value(comp_key(W, B, None))
        if k is not None and k >= 1:
            found.append((k, W, B))
    return args, tot, found, time.time() - t0


def fmt(W, B):
    nm = lambda p: "abcdefgh"[p[0]] + str(p[1])
    return "W: " + " ".join(map(nm, sorted(W))) + " / B: " + " ".join(map(nm, sorted(B)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--minpawns", type=int, default=2)
    ap.add_argument("--maxpawns", type=int, default=4)
    ap.add_argument("--settings", default="all")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    settings = ([(r, e) for r in ("count", "mover", "opponent") for e in (True, False)]
                if a.settings == "all" else
                [(s.split("/")[0], s.split("/")[1] == "1") for s in a.settings.split(",")])
    tasks = []
    for rule, ep in settings:
        for np_ in range(a.minpawns, a.maxpawns + 1):
            for n in range(1, np_ + 1):
                tasks.append((n, False, np_, rule, ep))
            for n in range(3, np_ + 1):
                tasks.append((n, True, np_, rule, ep))
    tasks.sort(key=lambda t: -t[2] * t[0])
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        for (n, wrap, np_, rule, ep), tot, found, dt in ex.map(task, tasks):
            ks = sorted({k for k, _, _ in found})
            print(f"{rule}/ep{int(ep)} {'cyl' if wrap else 'flat'}{n} pawns={np_} raw_atoms={tot} "
                  f"nimbers_k>=1={len(found)} k>=2: {[(k, fmt(W, B)) for k, W, B in found if k >= 2]} "
                  f"ks={ks} ({dt:.0f}s)", flush=True)
