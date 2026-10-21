"""Verifier's own third outcome solver (written for C1 checking), plus two side checks.

  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
    .venv/bin/python verify/sumtest/C1-reproduce/rerun2/vthird.py

(a) own enumeration of the families (own passer test) -> position counts and key-set equality;
(b) own brute-force outcome of G + X for every family position, all 3 race rules, e.p. on/off
    (textbook passer test, e.p. right kept until the next move in G), with X given in CANONICAL
    form (up* = {0,*|0}, dup* = {0|up}) instead of the worker's explicit sums; compared with
    the freshly recomputed cylcgt vectors in rerun2/data;
(c) the worker's solver with race_double=False (no double-step credit in "count") vs cylcgt.
"""
import gzip
import itertools
import json
import multiprocessing as mp
import os
import sys

sys.setrecursionlimit(100000)
ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
FRESH = os.path.join(ROOT, "verify/sumtest/C1-reproduce/rerun2/data")
BOARDS = {"flat3": (3, False), "flat4": (4, False), "cyl3": (3, True), "cyl4": (4, True), "cyl5": (5, True)}
RULES = ["count", "mover", "opponent"]
NR = 8
FL = "abcdefghij"

# ---- X games, canonical forms, as (L-tuple, R-tuple) ----
Z = ((), ())
S = ((Z,), (Z,))
S2 = ((Z, S), (Z, S))
S3 = ((Z, S, S2), (Z, S, S2))
UP = ((Z,), (S,))
DN = ((S,), (Z,))
UPS = ((Z, S), (Z,))
DUPS = ((Z,), (UP,))
ONE = ((Z,), ())
MONE = ((), (Z,))
HALF = ((Z,), (ONE,))
MHALF = ((MONE,), (Z,))
SW = ((ONE,), (Z,))
PM1 = ((ONE,), (MONE,))
TINY = ((Z,), (((Z,), (MONE,)),))
XS = [Z, S, S2, S3, UP, DN, UPS, DUPS, HALF, MHALF, ONE, MONE, SW, PM1, TINY]


class Pawns:
    def __init__(self, files, wrap, ep, rule):
        self.F, self.wrap, self.ep, self.rule = files, wrap, ep, rule

    def nbrs(self, f):
        out = set()
        for g in (f - 1, f + 1):
            if self.wrap:
                g %= self.F
            if 0 <= g < self.F and g != f:
                out.add(g)
        return out

    def passers(self, mine, theirs, white):
        res = []
        for (f, r) in mine:
            span = {f} | self.nbrs(f)
            if white:
                blocked = any(g in span and s > r for (g, s) in theirs)
            else:
                blocked = any(g in span and s < r for (g, s) in theirs)
            if not blocked:
                res.append((f, r))
        return res

    def dist(self, ps, white):
        if white:
            return min(NR - r - (1 if r == 2 else 0) for f, r in ps)
        return min(r - 1 - (1 if r == NR - 1 else 0) for f, r in ps)

    def settle(self, W, B, ep, mover_white):
        """terminal 'L'/'R' or the state itself."""
        wp = self.passers(W, B, True)
        bp = self.passers(B, W, False)
        if not wp and not bp:
            return (W, B, ep)
        if wp and not bp:
            return "L"
        if bp and not wp:
            return "R"
        mover, opp = ("L", "R") if mover_white else ("R", "L")
        if self.rule == "mover":
            return mover
        if self.rule == "opponent":
            return opp
        dw, db = self.dist(wp, True), self.dist(bp, False)
        dm, do = (dw, db) if mover_white else (db, dw)
        return opp if do <= dm else mover

    def moves(self, st, white):
        W, B, ep = st
        occ = W | B
        mine, theirs = (W, B) if white else (B, W)
        d = 1 if white else -1
        home = 2 if white else NR - 1
        out = []
        for (f, r) in mine:
            rest = mine - {(f, r)}
            r1 = r + d
            if not 1 <= r1 <= NR:
                continue
            if (f, r1) not in occ:
                out.append((rest | {(f, r1)}, theirs, None))
                if r == home and (f, r + 2 * d) not in occ:
                    nep = ((f, r1), (f, r + 2 * d), not white) if self.ep else None
                    out.append((rest | {(f, r + 2 * d)}, theirs, nep))
            for g in self.nbrs(f):
                t = (g, r1)
                if t in theirs:
                    out.append((rest | {t}, theirs - {t}, None))
                elif ep is not None and ep[2] == white and ep[0] == t:
                    out.append((rest | {t}, theirs - {ep[1]}, None))
        res = []
        for m, th, e in out:
            nW, nB = (m, th) if white else (th, m)
            res.append(self.settle(frozenset(nW), frozenset(nB), e, white))
        return res


def solve_config(args):
    board, rule, ep = args
    files, wrap = BOARDS[board]
    P = Pawns(files, wrap, ep, rule)
    memo = {}

    def wins(st, x, left):
        """does the player to move win in st + x?"""
        if st == "L":
            return left
        if st == "R":
            return not left
        k = (st, x, left)
        r = memo.get(k)
        if r is not None:
            return r
        res = False
        for c in P.moves(st, left):
            if not wins(c, x, not left):
                res = True
                break
        if not res:
            for y in (x[0] if left else x[1]):
                if not wins(st, y, not left):
                    res = True
                    break
        memo[k] = res
        return res

    # own enumeration
    sqs = [(f, r) for f in range(files) for r in range(2, 8)]
    out = {}
    for nw, nb in [(1, 1), (2, 1), (1, 2), (2, 2)]:
        for ws in itertools.combinations(sqs, nw):
            rest = [s for s in sqs if s not in ws]
            for bs in itertools.combinations(rest, nb):
                W, B = frozenset(ws), frozenset(bs)
                if P.passers(W, B, True) or P.passers(B, W, False):
                    continue
                key = ("W: " + " ".join(FL[f] + str(r) for f, r in sorted(W)) +
                       " / B: " + " ".join(FL[f] + str(r) for f, r in sorted(B)))
                st = (W, B, None)
                vec = ""
                for x in XS:
                    lf = wins(st, x, True)
                    rf = wins(st, x, False)
                    vec += {(True, False): "L", (False, True): "R", (True, True): "N", (False, False): "P"}[(lf, rf)]
                out[key] = vec
    return board, rule, ep, out


def canon_key(text):
    """normalise 'W: a2 c2 / B: b7' ordering (worker's show() sorts by square index = file-major)."""
    w, b = text.split("/")
    ws = sorted(w.split(":")[1].split(), key=lambda t: (t[0], int(t[1:])))
    bs = sorted(b.split(":")[1].split(), key=lambda t: (t[0], int(t[1:])))
    return "W: " + " ".join(ws) + " / B: " + " ".join(bs)


def load(name):
    with gzip.open(os.path.join(FRESH, name), "rt") as fh:
        return json.load(fh)["outcomes"]


def race_double_off(args):
    board, rule, ep = args
    from sumtest.sumsolver import Geometry, Rules, SumSolver, Trees, reference_set, REF_NAMES
    from sumtest.enum_positions import positions
    files, wrap = BOARDS[board]
    geo, pos = positions(files, wrap)
    T = Trees()
    ref = reference_set(T)
    idx = [ref[n] for n in REF_NAMES]
    s = SumSolver(Rules(geo, ep=ep, ep_aware=False, race_rule=rule, race_double=False), T, mode="whole")
    res = {}
    for W, B in pos:
        wl, wr = s.solve(s.start_state(W, B))
        res[geo.show(W, B)] = "".join(s.outcome(wl, wr, k) for k in idx)
    return board, rule, ep, res


def main():
    mp.set_start_method("fork", force=True)
    tasks = [(b, r, e) for b in BOARDS for r in RULES for e in (True, False)]
    tot_pred = tot_diff = 0
    npos = {}
    with mp.Pool(12) as pool:
        for board, rule, ep, out in pool.imap_unordered(solve_config, tasks):
            cy = load(f"cylcgt__{board}__{rule}__{'ep' if ep else 'noep'}.json.gz")
            cyn = {canon_key(k): v for k, v in cy.items()}
            assert len(cyn) == len(cy)
            same_keys = set(cyn) == set(out)
            d = sum(1 for k in out for x, y in zip(out[k], cyn.get(k, "?" * 15)) if x != y)
            dpos = sum(1 for k in out if out[k] != cyn.get(k))
            tot_pred += 15 * len(out)
            tot_diff += d
            npos[board] = len(out)
            print(f"third-solver {board:5s} {rule:8s} ep={ep!s:5s} positions={len(out)} keys_equal={same_keys} "
                  f"positions_differing={dpos} pairs_differing={d}", flush=True)
        print("own enumeration counts:", npos, "total", sum(npos.values()))
        print("third solver vs cylcgt: predictions", tot_pred, "differing", tot_diff)

        print("\n(c) worker solver with race_double=False vs cylcgt (count rule only matters):")
        tasks2 = [(b, r, e) for b in BOARDS for r in RULES for e in (True, False)]
        agg = {}
        for board, rule, ep, res in pool.imap_unordered(race_double_off, tasks2):
            cy = load(f"cylcgt__{board}__{rule}__{'ep' if ep else 'noep'}.json.gz")
            dpos = sum(1 for k in res if res[k] != cy[k])
            agg.setdefault((rule, ep), 0)
            agg[(rule, ep)] += dpos
        for k in sorted(agg):
            print("   rule=%s ep=%s positions differing: %d" % (k[0], k[1], agg[k]))


if __name__ == "__main__":
    main()
