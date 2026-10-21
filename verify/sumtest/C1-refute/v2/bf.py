"""Independent brute-force outcome solver for  G + X  (verifier v2, C1-refute).

Written from the task spec only. Imports neither cylcgt nor sumtest (nor crosscheck).

Model (pawns only, 8 ranks, `F` files, flat or cylinder):
  * White = Left, Black = Right, normal play (no move anywhere => you lose).
  * Moves in G: single step, double step from home rank (2 / 7), diagonal capture
    (wrapping on a cylinder), optional en passant.
  * After every G-move: if exactly one side has a passed pawn (textbook test: no enemy
    pawn strictly ahead on the same or an adjacent file; e.p. rights ignored), that side
    wins the WHOLE sum at once ("whole-board" semantics: the first passer ends play).
    If both sides do, it is a race decided by `rule`:
        mover    : mover wins
        opponent : mover loses
        count    : opponent of the mover moves first; d(side) = min over passed pawns of
                   moves-to-promote (home-rank pawn with two empty squares ahead gets one
                   move of credit); opponent wins iff d(opp) <= d(mover).
  * X is a multiset of explicit textbook game trees (no canonical-form arithmetic).
  * e.p. rights (frozenset of (target, captured, capturer)) and three scopes:
        pcomp  : a right dies at the next move in the PAWN COMPONENT (files separated by
                 an empty file) that holds it; moves elsewhere (other pawn components, X)
                 keep it.  (This is the semantics a sum of per-component games has.)
        G      : a right dies at the next pawn move anywhere; X moves keep it.
        global : a right dies at the next move anywhere (chess-like).
"""
from __future__ import annotations

import itertools
import sys

sys.setrecursionlimit(10000)
RANKS = 8


class Geo:
    def __init__(self, F: int, wrap: bool):
        self.F, self.wrap = F, wrap
        # span[side][sq] = mask of squares strictly ahead on files f, f-1, f+1
        self.span = {"W": {}, "B": {}}
        for f in range(F):
            fs = {f}
            for df in (-1, 1):
                g = self.nb(f, df)
                if g is not None:
                    fs.add(g)
            for r in range(1, RANKS + 1):
                s = self.sq(f, r)
                self.span["W"][s] = sum(1 << self.sq(g, t) for g in fs for t in range(r + 1, RANKS + 1))
                self.span["B"][s] = sum(1 << self.sq(g, t) for g in fs for t in range(1, r))

    def nb(self, f, df):
        g = f + df
        if self.wrap:
            return g % self.F
        return g if 0 <= g < self.F else None

    @staticmethod
    def sq(f, r):
        return f * RANKS + (r - 1)

    @staticmethod
    def fr(s):
        return divmod(s, RANKS)[0], s % RANKS + 1

    def show(self, W, B):
        def names(m):
            return " ".join(sorted("abcdefgh"[self.fr(s)[0]] + str(self.fr(s)[1]) for s in bits(m)))
        return f"W: {names(W)} / B: {names(B)}"

    def groups(self, occ_files):
        """map file -> frozenset(files of its component) for occupied files."""
        occ = sorted(occ_files)
        runs = []
        for f in occ:
            if runs and f == runs[-1][-1] + 1:
                runs[-1].append(f)
            else:
                runs.append([f])
        if self.wrap and len(runs) > 1 and runs[0][0] == 0 and runs[-1][-1] == self.F - 1:
            runs[0] = runs.pop() + runs[0]
        out = {}
        for run in runs:
            fs = frozenset(run)
            for f in run:
                out[f] = fs
        return out


def bits(m):
    while m:
        low = m & -m
        yield low.bit_length() - 1
        m ^= low


def passed(geo, W, B, side):
    mine, theirs = (W, B) if side == "W" else (B, W)
    sp = geo.span[side]
    return any((theirs & sp[s]) == 0 for s in bits(mine))


def dist(geo, W, B, side):
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = W | B
    best = 10 ** 6
    for s in bits(mine):
        if theirs & geo.span[side][s]:
            continue
        f, r = geo.fr(s)
        if side == "W":
            d = RANKS - r
            if r == 2 and not (occ >> geo.sq(f, 3)) & 1 and not (occ >> geo.sq(f, 4)) & 1:
                d -= 1
        else:
            d = r - 1
            if r == RANKS - 1 and not (occ >> geo.sq(f, RANKS - 2)) & 1 and not (occ >> geo.sq(f, RANKS - 3)) & 1:
                d -= 1
        best = min(best, d)
    return best


class Solver:
    def __init__(self, F, wrap, ep, rule, scope="pcomp"):
        self.geo = Geo(F, wrap)
        self.ep, self.rule, self.scope = ep, rule, scope
        self.gm = {}      # (W,B,rights,side) -> list of results
        self.memo = {}
        self.race_hits = 0
        self.seam_ep = True   # default = full rules; False only in mutate.py

    # ---- pawn moves -------------------------------------------------------
    def classify(self, W, B, mover):
        geo = self.geo
        wp, bp = passed(geo, W, B, "W"), passed(geo, W, B, "B")
        if wp and bp:
            self.race_hits += 1
            other = "B" if mover == "W" else "W"
            if self.rule == "mover":
                return mover
            if self.rule == "opponent":
                return other
            assert self.rule == "count"
            return other if dist(geo, W, B, other) <= dist(geo, W, B, mover) else mover
        if wp:
            return "W"
        if bp:
            return "B"
        return None

    def gmoves(self, W, B, rights, side):
        key = (W, B, rights, side)
        hit = self.gm.get(key)
        if hit is not None:
            return hit
        geo = self.geo
        mine, theirs = (W, B) if side == "W" else (B, W)
        occ = W | B
        d = 1 if side == "W" else -1
        home = 2 if side == "W" else RANKS - 1
        other = "B" if side == "W" else "W"
        grp = geo.groups({geo.fr(s)[0] for s in bits(occ)}) if self.scope == "pcomp" else None
        out = []
        for s in bits(mine):
            f, r = geo.fr(s)
            r1 = r + d
            assert 1 <= r1 <= RANKS, "promotion square reached in a non-terminal state"
            # rights that survive this move
            if self.scope == "pcomp":
                keep = frozenset(x for x in rights if grp[geo.fr(x[0])[0]] != grp[f])
                mine_rights = [x for x in rights if x[2] == side and grp[geo.fr(x[0])[0]] == grp[f]]
            else:
                keep = frozenset()
                mine_rights = [x for x in rights if x[2] == side]
            rest = mine & ~(1 << s)
            t1 = geo.sq(f, r1)
            cand = []
            if not (occ >> t1) & 1:
                cand.append((rest | (1 << t1), theirs, keep))
                r2 = r + 2 * d
                if r == home:
                    t2 = geo.sq(f, r2)
                    if not (occ >> t2) & 1:
                        nk = keep | {(t1, t2, other)} if self.ep else keep
                        cand.append((rest | (1 << t2), theirs, frozenset(nk)))
            for df in (-1, 1):
                g = geo.nb(f, df)
                if g is None:
                    continue
                t = geo.sq(g, r1)
                if (theirs >> t) & 1:
                    cand.append((rest | (1 << t), theirs & ~(1 << t), keep))
                else:
                    if not self.seam_ep and abs(g - f) > 1:
                        continue  # mutation used only by mutate.py: no e.p. across the seam
                    for (tg, cap, _) in mine_rights:
                        if tg == t:
                            cand.append((rest | (1 << t), theirs & ~(1 << cap), keep))
            for nm, nt, nk in cand:
                nW, nB = (nm, nt) if side == "W" else (nt, nm)
                res = self.classify(nW, nB, side)
                if res is not None:
                    out.append(res)
                else:
                    # drop rights whose captured pawn has vanished or that are now unusable
                    nk = frozenset(x for x in nk if ((nW | nB) >> x[1]) & 1)
                    out.append((nW, nB, nk))
        self.gm[key] = out
        return out

    # ---- sum search -------------------------------------------------------
    def win(self, W, B, rights, x, side):
        """Does `side` (to move) win G + X?  x = sorted tuple of X-node ids (no zeros)."""
        key = (W, B, rights, x, side)
        v = self.memo.get(key)
        if v is not None:
            return v
        other = "B" if side == "W" else "W"
        res = False
        for c in self.gmoves(W, B, rights, side):
            if c == side:
                res = True
                break
            if c == other:
                continue
            if not self.win(c[0], c[1], c[2], x, other):
                res = True
                break
        if not res:
            r2 = frozenset() if self.scope == "global" else rights
            for nx in xmoves(x, side):
                if not self.win(W, B, r2, nx, other):
                    res = True
                    break
        self.memo[key] = res
        return res

    def outcome(self, W, B, x):
        lf = self.win(W, B, frozenset(), x, "W")
        rf = self.win(W, B, frozenset(), x, "B")
        return {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(lf, rf)]


# ---- explicit X game trees (textbook definitions) ---------------------------
NODES = []  # id -> (L ids, R ids)


def node(L, R):
    NODES.append((tuple(L), tuple(R)))
    return len(NODES) - 1


Z = node([], [])
S = node([Z], [Z])
S2 = node([Z, S], [Z, S])
S3 = node([Z, S, S2], [Z, S, S2])
UP = node([Z], [S])
DN = node([S], [Z])
ONE = node([Z], [])
MONE = node([], [Z])
HALF = node([Z], [ONE])
MHALF = node([MONE], [Z])
HOT = node([ONE], [Z])
PM1 = node([ONE], [MONE])
_inner = node([Z], [MONE])
TINY1 = node([Z], [_inner])

REF_NAMES = ["0", "*", "*2", "*3", "up", "down", "up*", "dup*", "1/2", "-1/2", "1", "-1",
             "{1|0}", "+-1", "tiny1"]
REF = {"0": (), "*": (S,), "*2": (S2,), "*3": (S3,), "up": (UP,), "down": (DN,),
       "up*": (UP, S), "dup*": (UP, UP, S), "1/2": (HALF,), "-1/2": (MHALF,), "1": (ONE,),
       "-1": (MONE,), "{1|0}": (HOT,), "+-1": (PM1,), "tiny1": (TINY1,)}
REF = {k: tuple(sorted(v)) for k, v in REF.items()}


def xmoves(x, side):
    out = set()
    for i, n in enumerate(x):
        L, R = NODES[n]
        for o in (L if side == "W" else R):
            rest = x[:i] + x[i + 1:]
            nx = tuple(sorted(rest + ((o,) if o != Z else ())))
            out.add(nx)
    return out


# ---- families -----------------------------------------------------------------
BOARDS = {"flat3": (3, False), "flat4": (4, False), "cyl3": (3, True), "cyl4": (4, True), "cyl5": (5, True)}
COUNTS = [(1, 1), (2, 1), (1, 2), (2, 2)]


def family(F, wrap):
    geo = Geo(F, wrap)
    sqs = [geo.sq(f, r) for f in range(F) for r in range(2, 8)]
    out = []
    for nw, nb in COUNTS:
        for ws in itertools.combinations(sqs, nw):
            W = sum(1 << s for s in ws)
            rest = [s for s in sqs if s not in ws]
            for bs in itertools.combinations(rest, nb):
                B = sum(1 << s for s in bs)
                if not passed(geo, W, B, "W") and not passed(geo, W, B, "B"):
                    out.append((W, B))
    return geo, out
