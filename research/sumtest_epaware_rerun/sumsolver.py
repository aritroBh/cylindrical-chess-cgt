"""Brute-force OUTCOME solver for disjunctive sums G + R.

Written from scratch for the sum-test cross-validation.  It does NOT import
cylcgt or crosscheck, and it computes no canonical forms: it only plays the
sum out by exhaustive minimax and reports the outcome class (L, R, N, P).

G : a pawn position on a board of any width, flat or cylindrical, 8 ranks.
R : an explicit abstract game tree (see `reference_set`).

Conventions (Elkies 1996, as fixed in the task spec):
  * White = Left, Black = Right.  Normal play: a player with no move in any
    component loses.
  * Pawns: single step; double step from the home rank (rank 2 for White,
    rank 7 for Black) when both squares are empty; diagonal captures (wrapping
    a<->last file on a cylinder); optional en passant (also across the seam).
  * As soon as a move leaves G in a position where exactly one side owns a
    passed pawn, G is worth +BIG (White) or -BIG (Black).  BIG dominates every
    R of the reference set, so the whole sum is then won by that side.
  * If both sides own passed pawns the race is resolved by RACE_RULE:
      count    : the opponent of the mover moves first in the race; whoever
                 needs fewer moves to promote wins; ties go to the opponent.
      mover    : the mover wins.
      opponent : the mover loses.

Choices the spec leaves open, exposed as options (defaults first):
  ep_scope  "component" : an e.p. right lives in G's state and is only
                          cleared by the next move made *in G* (this is what a
                          CGT component value implies);
            "global"    : any move anywhere (also in R) clears it (chess).
  ep_aware  True  : a pawn that can be captured en passant right now does not
                    count as passed;  False : the plain textbook definition.
  race_double True: a passed pawn still on its home rank needs one move less
                    (double step) when counting a race.
  mode      "whole" : G is one game; the first passer anywhere on the board
                      ends the whole sum (the literal spec).
            "comp"  : G is split into file-disjoint components at every node
                      (after the passer test), each component that acquires a
                      passer turns into the integer +-BIG, and those integers
                      add up (so +BIG and -BIG can cancel).  This mirrors how a
                      CGT engine that sums component values behaves.
"""

import sys

sys.setrecursionlimit(1_000_000)

FILES = "abcdefghijklmnopqrstuvwxyz"


# ----------------------------------------------------------------------------
# Abstract game trees (the R side)
# ----------------------------------------------------------------------------

class Trees:
    """Interned explicit game trees.  Node ids are topologically ordered:
    every option of node k has an id smaller than k."""

    def __init__(self):
        self.L = []          # list of tuples of child ids
        self.R = []
        self._index = {}
        self._sum = {}
        self._neg = {}

    def node(self, left=(), right=()):
        key = (tuple(sorted(set(left))), tuple(sorted(set(right))))
        if key not in self._index:
            self._index[key] = len(self.L)
            self.L.append(key[0])
            self.R.append(key[1])
        return self._index[key]

    def add(self, a, b):
        """Explicit (non-simplified) disjunctive sum a + b."""
        k = (a, b) if a <= b else (b, a)
        if k in self._sum:
            return self._sum[k]
        left = [self.add(x, b) for x in self.L[a]] + [self.add(a, y) for y in self.L[b]]
        right = [self.add(x, b) for x in self.R[a]] + [self.add(a, y) for y in self.R[b]]
        n = self.node(left, right)
        self._sum[k] = n
        return n

    def neg(self, a):
        if a in self._neg:
            return self._neg[a]
        n = self.node([self.neg(x) for x in self.R[a]], [self.neg(x) for x in self.L[a]])
        self._neg[a] = n
        return n

    def __len__(self):
        return len(self.L)


def reference_set(T):
    """Return an ordered dict name -> node id for the 15 reference games.

    Each is written from its textbook definition; up* and double-up* are
    built as explicit sums (up + *, up + up + *) so that no canonical-form
    knowledge is needed."""
    z = T.node()
    star = T.node([z], [z])
    star2 = T.node([z, star], [z, star])
    star3 = T.node([z, star, star2], [z, star, star2])
    up = T.node([z], [star])
    down = T.node([star], [z])
    upstar = T.add(up, star)
    dupstar = T.add(T.add(up, up), star)
    one = T.node([z], [])
    mone = T.node([], [z])
    half = T.node([z], [one])
    mhalf = T.node([mone], [z])
    sw10 = T.node([one], [z])
    pm1 = T.node([one], [mone])
    tiny1 = T.node([z], [T.node([z], [mone])])
    return {
        "0": z, "*": star, "*2": star2, "*3": star3,
        "up": up, "down": down, "up*": upstar, "dup*": dupstar,
        "1/2": half, "-1/2": mhalf, "1": one, "-1": mone,
        "{1|0}": sw10, "+-1": pm1, "tiny1": tiny1,
    }


def canonical_alternatives(T):
    """Hand-written canonical forms of the two composite games, used only as
    an internal consistency test (outcomes must not depend on the tree)."""
    z = T.node()
    star = T.node([z], [z])
    up = T.node([z], [star])
    return {"up*": T.node([z, star], [z]), "dup*": T.node([z], [up])}


# ----------------------------------------------------------------------------
# Pawn board geometry and rules
# ----------------------------------------------------------------------------

class Geometry:
    def __init__(self, files, wrap, ranks=8):
        assert files >= 1 and ranks >= 5
        self.F, self.NR, self.wrap = files, ranks, wrap
        self.N = files * ranks

        def adj(f):
            out = []
            for g in (f - 1, f + 1):
                if wrap:
                    g %= files
                if 0 <= g < files and g != f and g not in out:
                    out.append(g)
            return out

        self.adj = [adj(f) for f in range(files)]
        sq = self.sq
        self.fileof = [s // ranks for s in range(self.N)]
        self.rankof = [s % ranks + 1 for s in range(self.N)]
        self.filemask = [sum(1 << sq(f, r) for r in range(1, ranks + 1)) for f in range(files)]
        self.capW, self.capB, self.frontW, self.frontB = [], [], [], []
        self.adjrank = {}     # (file, rank) -> mask of squares on adjacent files at that rank
        for f in range(files):
            for r in range(1, ranks + 1):
                self.adjrank[(f, r)] = sum(1 << sq(g, r) for g in self.adj[f])
        for s in range(self.N):
            f, r = self.fileof[s], self.rankof[s]
            self.capW.append([sq(g, r + 1) for g in self.adj[f]] if r < ranks else [])
            self.capB.append([sq(g, r - 1) for g in self.adj[f]] if r > 1 else [])
            span = [f] + self.adj[f]
            self.frontW.append(sum(1 << sq(g, t) for g in span for t in range(r + 1, ranks + 1)))
            self.frontB.append(sum(1 << sq(g, t) for g in span for t in range(1, r)))

    def sq(self, f, r):
        return f * self.NR + (r - 1)

    def name(self, s):
        return FILES[self.fileof[s]] + str(self.rankof[s])

    def parse(self, text):
        """'W: a2 c2 / B: b7 d7' -> (Wmask, Bmask)."""
        W = B = 0
        for part in text.split("/"):
            part = part.strip()
            side, _, sqs = part.partition(":")
            side = side.strip().upper()
            m = 0
            for t in sqs.split():
                f = FILES.index(t[0].lower())
                r = int(t[1:])
                assert 0 <= f < self.F and 1 <= r <= self.NR, t
                m |= 1 << self.sq(f, r)
            if side == "W":
                W |= m
            elif side == "B":
                B |= m
            else:
                raise ValueError(text)
        assert W & B == 0
        return W, B

    def show(self, W, B):
        ws = " ".join(self.name(s) for s in bits(W))
        bs = " ".join(self.name(s) for s in bits(B))
        return f"W: {ws} / B: {bs}"


def bits(x):
    while x:
        low = x & -x
        yield low.bit_length() - 1
        x ^= low


class Rules:
    def __init__(self, geo, ep=True, ep_aware=True, race_rule="count", race_double=True):
        assert race_rule in ("count", "mover", "opponent")
        self.g, self.ep, self.ep_aware = geo, ep, ep_aware
        self.race_rule, self.race_double = race_rule, race_double
        self.race_hits = 0

    # --- move generation ---------------------------------------------------
    def moves(self, W, B, ep, white):
        """All positions (W', B', ep') reachable by one move of the side."""
        g = self.g
        NR = g.NR
        occ = W | B
        out = []
        if white:
            for s in bits(W):
                r = g.rankof[s]
                if r < NR and not (occ >> (s + 1)) & 1:
                    out.append((W ^ (1 << s) ^ (1 << (s + 1)), B, -1))
                    if r == 2 and not (occ >> (s + 2)) & 1:
                        t = s + 2
                        nep = -1
                        if self.ep and (B & g.adjrank[(g.fileof[s], 4)]):
                            nep = s + 1
                        out.append((W ^ (1 << s) ^ (1 << t), B, nep))
                for t in g.capW[s]:
                    if (B >> t) & 1:
                        out.append((W ^ (1 << s) ^ (1 << t), B ^ (1 << t), -1))
            if ep >= 0 and g.rankof[ep] == NR - 2:          # black skipped this square
                victim = ep - 1
                for s in bits(W & g.adjrank[(g.fileof[ep], NR - 3)]):
                    out.append((W ^ (1 << s) ^ (1 << ep), B ^ (1 << victim), -1))
        else:
            for s in bits(B):
                r = g.rankof[s]
                if r > 1 and not (occ >> (s - 1)) & 1:
                    out.append((W, B ^ (1 << s) ^ (1 << (s - 1)), -1))
                    if r == NR - 1 and not (occ >> (s - 2)) & 1:
                        t = s - 2
                        nep = -1
                        if self.ep and (W & g.adjrank[(g.fileof[s], NR - 3)]):
                            nep = s - 1
                        out.append((W, B ^ (1 << s) ^ (1 << t), nep))
                for t in g.capB[s]:
                    if (W >> t) & 1:
                        out.append((W ^ (1 << t), B ^ (1 << s) ^ (1 << t), -1))
            if ep >= 0 and g.rankof[ep] == 3:                # white skipped this square
                victim = ep + 1
                for s in bits(B & g.adjrank[(g.fileof[ep], 4)]):
                    out.append((W ^ (1 << victim), B ^ (1 << s) ^ (1 << ep), -1))
        return out

    # --- passed pawns and races --------------------------------------------
    def passers(self, W, B, ep, white):
        g = self.g
        mine, theirs = (W, B) if white else (B, W)
        if self.ep_aware and ep >= 0:
            if white and g.rankof[ep] == 3:
                mine &= ~(1 << (ep + 1))
            if not white and g.rankof[ep] == g.NR - 2:
                mine &= ~(1 << (ep - 1))
        front = g.frontW if white else g.frontB
        return [s for s in bits(mine) if not (theirs & front[s])]

    def steps(self, sqs, white):
        g = self.g
        best = 99
        for s in sqs:
            r = g.rankof[s]
            if white:
                n = g.NR - r - (1 if (self.race_double and r == 2) else 0)
            else:
                n = r - 1 - (1 if (self.race_double and r == g.NR - 1) else 0)
            best = min(best, n)
        return best

    def resolve(self, W, B, ep, mover_white):
        """None if no passed pawn; else 'L' or 'R' (winner of G)."""
        wp = self.passers(W, B, ep, True)
        bp = self.passers(W, B, ep, False)
        if not wp and not bp:
            return None
        if wp and not bp:
            return "L"
        if bp and not wp:
            return "R"
        self.race_hits += 1
        mover = "L" if mover_white else "R"
        opp = "R" if mover_white else "L"
        if self.race_rule == "mover":
            return mover
        if self.race_rule == "opponent":
            return opp
        sw, sb = self.steps(wp, True), self.steps(bp, False)
        sm, so = (sw, sb) if mover_white else (sb, sw)
        return opp if so <= sm else mover

    def has_initial_passer(self, W, B):
        return bool(self.passers(W, B, -1, True) or self.passers(W, B, -1, False))

    # --- components -----------------------------------------------------------
    def split(self, W, B, ep):
        """Split into maximal runs of occupied files (cyclic on a cylinder)."""
        g = self.g
        occ = [bool((W | B) & g.filemask[f]) for f in range(g.F)]
        if not any(occ):
            return []
        runs = []
        if g.wrap and all(occ):
            runs = [list(range(g.F))]
        else:
            start = 0
            if g.wrap:
                start = occ.index(False)          # rotate so we begin on an empty file
            cur = []
            for i in range(g.F):
                f = (start + i) % g.F
                if occ[f]:
                    cur.append(f)
                elif cur:
                    runs.append(cur)
                    cur = []
            if cur:
                runs.append(cur)
        out = []
        for run in runs:
            m = 0
            for f in run:
                m |= g.filemask[f]
            e = ep if (ep >= 0 and (m >> ep) & 1) else -1
            out.append((W & m, B & m, e))
        return out


# ----------------------------------------------------------------------------
# The sum solver
# ----------------------------------------------------------------------------

class SumSolver:
    """win masks over all R-nodes of a Trees object.

    solve(state) -> (wl, wr): bit k of wl is set iff Left, moving first in
    state + node_k, wins; bit k of wr iff Right, moving first, wins.
    """

    BIGC = 64        # stand-in for BIG inside "comp" mode (see module doc)

    def __init__(self, rules, trees, mode="whole", ep_scope="component"):
        assert mode in ("whole", "comp") and ep_scope in ("component", "global")
        if mode == "comp":
            assert ep_scope == "component"
        self.rules, self.T, self.mode, self.ep_scope = rules, trees, mode, ep_scope
        n = len(trees)
        self.n = n
        self.ALL = (1 << n) - 1
        self.NLm = [sum(1 << c for c in trees.L[k]) for k in range(n)]
        self.NRm = [sum(1 << c for c in trees.R[k]) for k in range(n)]
        self.memo = {}
        self.nodes = 0

    # ---- outcome helpers ----
    @staticmethod
    def outcome(wl, wr, k):
        lf, rf = (wl >> k) & 1, (wr >> k) & 1
        return {(1, 0): "L", (0, 1): "R", (1, 1): "N", (0, 0): "P"}[(lf, rf)]

    def start_state(self, W, B):
        """Initial state for a position with no passed pawn and no e.p. right."""
        assert not self.rules.has_initial_passer(W, B)
        if self.mode == "whole":
            return (W, B, -1)
        return self._comp_state(self.rules.split(W, B, -1), 0)

    def outcomes(self, W, B, nodes):
        wl, wr = self.solve(self.start_state(W, B))
        return [self.outcome(wl, wr, k) for k in nodes]

    # ---- whole mode ----
    def _after_move_whole(self, st, mover_white):
        W, B, ep = st
        res = self.rules.resolve(W, B, ep, mover_white)
        return res if res else st

    def _children(self, state, white):
        if self.mode == "whole":
            W, B, ep = state
            return [self._after_move_whole(c, white) for c in self.rules.moves(W, B, ep, white)]
        return self._comp_children(state, white)

    def _cleared(self, state, mover_white):
        """State of G after a move made in R (only differs in global e.p. scope)."""
        if self.ep_scope == "component" or self.mode != "whole":
            return state
        W, B, ep = state
        if ep < 0:
            return state
        return self._after_move_whole((W, B, -1), mover_white)

    def solve(self, state):
        if state == "L":          # G is +BIG: Left wins whoever moves first
            return self.ALL, 0
        if state == "R":          # G is -BIG
            return 0, self.ALL
        m = self.memo.get(state)
        if m is not None:
            return m
        self.nodes += 1
        ALL = self.ALL
        gl = 0
        for c in self._children(state, True):
            gl |= ALL & ~self.solve(c)[1]
            if gl == ALL:
                break
        gr = 0
        for c in self._children(state, False):
            gr |= ALL & ~self.solve(c)[0]
            if gr == ALL:
                break
        n = self.n
        NLm, NRm = self.NLm, self.NRm
        if self.mode == "whole" and self.ep_scope == "global" and state[2] >= 0:
            # a move in R clears the e.p. right
            cl_L = self.solve(self._cleared(state, True))     # after Left moved in R
            cl_R = self.solve(self._cleared(state, False))    # after Right moved in R
            wl, wr = gl, gr
            for k in range(n):
                if NLm[k] & ~cl_L[1]:
                    wl |= 1 << k
                if NRm[k] & ~cl_R[0]:
                    wr |= 1 << k
        else:
            wl, wr = gl, gr
            for k in range(n):
                bit = 1 << k
                if not wl & bit and NLm[k] & ~wr:
                    wl |= bit
                if not wr & bit and NRm[k] & ~wl:
                    wr |= bit
        res = (wl, wr)
        self.memo[state] = res
        return res

    # ---- comp mode ----
    def _comp_state(self, comps, bank):
        live = []
        for (W, B, ep) in comps:
            if self.rules.moves(W, B, ep, True) or self.rules.moves(W, B, ep, False):
                live.append((W, B, ep))
        if not live and abs(bank) > 8:
            return "L" if bank > 0 else "R"
        return (tuple(sorted(live)), bank)

    def _comp_children(self, state, white):
        comps, bank = state
        out = []
        for i, (W, B, ep) in enumerate(comps):
            rest = comps[:i] + comps[i + 1:]
            for (W2, B2, ep2) in self.rules.moves(W, B, ep, white):
                res = self.rules.resolve(W2, B2, ep2, white)
                if res:
                    nb = bank + (self.BIGC if res == "L" else -self.BIGC)
                    out.append(self._comp_state(rest, nb))
                else:
                    out.append(self._comp_state(rest + tuple(self.rules.split(W2, B2, ep2)), bank))
        if white and bank > 0:
            out.append(self._comp_state(comps, bank - 1))
        if not white and bank < 0:
            out.append(self._comp_state(comps, bank + 1))
        return out


# ----------------------------------------------------------------------------
# Convenience
# ----------------------------------------------------------------------------

def make(files, wrap, ep=True, race_rule="count", mode="whole", ep_scope="component",
         ep_aware=True, race_double=True):
    geo = Geometry(files, wrap)
    rules = Rules(geo, ep=ep, ep_aware=ep_aware, race_rule=race_rule, race_double=race_double)
    T = Trees()
    ref = reference_set(T)
    solver = SumSolver(rules, T, mode=mode, ep_scope=ep_scope)
    return geo, rules, T, ref, solver


REF_NAMES = ["0", "*", "*2", "*3", "up", "down", "up*", "dup*",
             "1/2", "-1/2", "1", "-1", "{1|0}", "+-1", "tiny1"]


def outcome_vector(text, files, wrap, **kw):
    geo, rules, T, ref, solver = make(files, wrap, **kw)
    W, B = geo.parse(text)
    return dict(zip(REF_NAMES, solver.outcomes(W, B, [ref[n] for n in REF_NAMES])))


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("position", help='e.g. "W: a2 c2 / B: b7 d7"')
    ap.add_argument("--files", type=int, default=4)
    ap.add_argument("--wrap", action="store_true")
    ap.add_argument("--no-ep", action="store_true")
    ap.add_argument("--race", default="count")
    ap.add_argument("--mode", default="whole")
    ap.add_argument("--ep-scope", default="component")
    a = ap.parse_args()
    v = outcome_vector(a.position, a.files, a.wrap, ep=not a.no_ep, race_rule=a.race,
                       mode=a.mode, ep_scope=a.ep_scope)
    print(" ".join(f"{k}:{o}" for k, o in v.items()))
