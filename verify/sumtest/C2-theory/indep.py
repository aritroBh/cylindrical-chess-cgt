"""Theory-lens verifier for claim C2: a third, independent pawn model written from the spec
(does not import cylcgt.pawns or sumtest). Uses cylcgt.cgt only for canonical forms, and also
does a canonical-form-free direct search of G + *n (nim heap) to test the outcome class.

Run:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/sumtest/C2-theory/indep.py
"""
import sys
from functools import lru_cache
from itertools import product

from cylcgt import cgt

BIG = 256
FILES, RANKS = 4, 8


def sqs(s):
    return frozenset(("abcdefgh".index(t[0]), int(t[1])) for t in s.split())


class Model:
    def __init__(self, ep, aware, race, files=FILES, ranks=RANKS, wrap=False, credit=True):
        self.ep, self.aware, self.race = ep, aware, race
        self.F, self.H, self.wrap, self.credit = files, ranks, wrap, credit
        self.races = 0

    def adj(self, f):
        out = []
        for d in (-1, 1):
            g = f + d
            if self.wrap:
                out.append(g % self.F)
            elif 0 <= g < self.F:
                out.append(g)
        return out

    # state: (W, B, ep) ; ep = None or (capturer_side, target_sq, victim_sq)
    def pawn_passed(self, st, side, p):
        W, B, ep = st
        f, r = p
        enemy = B if side == "W" else W
        fs = {f, *self.adj(f)}
        for g, s in enemy:
            if g in fs and ((s > r) if side == "W" else (s < r)):
                return False
        if self.aware and ep is not None and ep[2] == p:
            # the opponent may capture this pawn en passant right now
            cap = ep[0]
            capt = W if cap == "W" else B
            for g in self.adj(f):
                if (g, r) in capt:
                    return False
        return True

    def passed(self, st, side):
        mine = st[0] if side == "W" else st[1]
        return any(self.pawn_passed(st, side, p) for p in mine)

    def dist(self, st, side):
        W, B, _ = st
        mine = W if side == "W" else B
        occ = W | B
        best = 10 ** 6
        for p in mine:
            if not self.pawn_passed(st, side, p):
                continue
            f, r = p
            if side == "W":
                if any((f, s) in occ for s in range(r + 1, self.H + 1)):
                    continue
                d = self.H - r - (1 if (self.credit and r == 2) else 0)
            else:
                if any((f, s) in occ for s in range(1, r)):
                    continue
                d = r - 1 - (1 if (self.credit and r == self.H - 1) else 0)
            best = min(best, d)
        return best

    def moves(self, st, side):
        W, B, ep = st
        mine, theirs = (W, B) if side == "W" else (B, W)
        occ = W | B
        dr = 1 if side == "W" else -1
        home = 2 if side == "W" else self.H - 1
        other = "B" if side == "W" else "W"
        res = []

        def put(nm, nt, nep=None):
            res.append((nm, nt, nep) if side == "W" else (nt, nm, nep))

        for p in mine:
            f, r = p
            rest = mine - {p}
            r1 = r + dr
            if not 1 <= r1 <= self.H:
                continue
            if (f, r1) not in occ:
                put(rest | {(f, r1)}, theirs)
                r2 = r + 2 * dr
                if r == home and (f, r2) not in occ:
                    nep = (other, (f, r1), (f, r2)) if self.ep else None
                    put(rest | {(f, r2)}, theirs, nep)
            for g in self.adj(f):
                t = (g, r1)
                if t in theirs:
                    put(rest | {t}, theirs - {t})
                elif ep is not None and ep[0] == side and ep[1] == t:
                    put(rest | {t}, theirs - {ep[2]})
        return list(dict.fromkeys(res))

    def resolve(self, st, mover):
        """Return +BIG/-BIG if decided, else None."""
        wp, bp = self.passed(st, "W"), self.passed(st, "B")
        if wp and bp:
            if mover is None:
                raise RuntimeError("race at root")
            self.races += 1
            opp = "B" if mover == "W" else "W"
            if self.race == "mover":
                win = mover
            elif self.race == "opponent":
                win = opp
            else:
                win = opp if self.dist(st, opp) <= self.dist(st, mover) else mover
            return BIG if win == "W" else -BIG
        if wp:
            return BIG
        if bp:
            return -BIG
        return None

    def strip_ep_for(self, st, side):
        """e.p. right is usable only by its owner on the very next move in this component."""
        W, B, ep = st
        if ep is not None and ep[0] != side:
            return (W, B, None)
        return st


def canon(m, root):
    @lru_cache(maxsize=None)
    def val(st, mover):
        d = m.resolve(st, mover)
        if d is not None:
            return cgt.integer(d)
        L = [val(c, "W") for c in m.moves(m.strip_ep_for(st, "W"), "W")]
        R = [val(c, "B") for c in m.moves(m.strip_ep_for(st, "B"), "B")]
        return cgt.make(L, R)
    return val(root, None)


def direct_outcome(m, root, heap):
    """Outcome class of G + *heap by plain minimax, no canonical forms.
    A resolved +-BIG ends the whole sum (BIG dominates a nim heap). Normal play otherwise.
    e.p. right local to G (survives a move in the heap)."""
    @lru_cache(maxsize=None)
    def win(st, mover_last, h, side):
        # does `side` (to move) win?
        d = m.resolve(st, mover_last) if mover_last != "done" else None
        if d is not None:
            # decided: winner is sign of d (BIG dominates *h)
            return (d > 0) == (side == "W")
        other = "B" if side == "W" else "W"
        for c in m.moves(m.strip_ep_for(st, side), side):
            if not win(c, side, h, other):
                return True
        for k in range(h):
            if not win(st, "done", k, other):
                return True
        return False
    lw = win(root, None, heap, "W")
    rw = win(root, None, heap, "B")
    return {(True, True): "N", (False, False): "P", (True, False): "L", (False, True): "R"}[(lw, rw)]


def main():
    root = (sqs("a2 c2"), sqs("b7 d7"), None)
    print("W a2 c2 / B b7 d7, 4 files flat, 8 ranks (independent model)")
    for race in ("count", "mover", "opponent"):
        for ep, aware, label in ((False, False, "ep off"), (True, False, "ep on, textbook passer"),
                                 (True, True, "ep on, ep-aware passer")):
            m = Model(ep, aware, race)
            g = canon(m, root)
            m2 = Model(ep, aware, race)
            outs = {n: direct_outcome(m2, root, n) for n in range(4)}
            print(f"{race:8s} {label:24s} value={cgt.show(g):28s} mean={cgt.mean(g)} "
                  f"temp={cgt.temperature(g)}  direct: G+0={outs[0]} G+*={outs[1]} G+*2={outs[2]} G+*3={outs[3]}")


if __name__ == "__main__":
    main()
