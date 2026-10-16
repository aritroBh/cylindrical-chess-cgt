"""Adversarial (REFUTE-lens) independent check of claim C3 (Dawson ring rule).

Written from scratch for this verification. Imports nothing from dawson/, cylcgt/
or crosscheck/. Stdlib only.

Pawn rules on a 3 x n board (ranks 1..3), flat or cylinder (files 0 and n-1 adjacent):
  * White pawns start on rank 1, Black pawns on rank 3, rank 2 empty.
  * A pawn pushes one square forward onto an empty square, or captures one square
    diagonally forward (wrapping on the cylinder).
  * Captures are compulsory: if the side to move has any capture, only captures are legal.
  * Normal play: side to move with no legal move loses.  Misere: it wins.
Adversarial instrumentation (each must stay 0 for the claim's model to be the real game):
  * promo_legal  : reachable positions where a promotion (push or capture onto the last
                   rank) is a LEGAL move for the side to move;
  * dbl_geom     : reachable positions where some pawn of the side to move stands on its
                   first rank with the two squares ahead empty (room for a chess double
                   step, which on 3 ranks would also be a promotion);
  * dbl_legal    : same, but at a moment when the side to move has no capture (so a
                   double step would be legal if the rules allowed one).
States are canonicalised under the board's symmetry group (rotations+reflection on the
cylinder, reflection on the flat board); outcomes are invariant under these.
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(1 << 20)

E, W, B = 0, 1, 2


def code(r1, r2, r3):
    return r1 + 3 * r2 + 9 * r3


def sq(c, r):  # piece on rank r (1..3) of a file with code c
    return (c // (3 ** (r - 1))) % 3


def setsq(c, r, v):
    return c - sq(c, r) * 3 ** (r - 1) + v * 3 ** (r - 1)


FULL = code(W, E, B)


class Game:
    def __init__(self, n, cyl):
        self.n, self.cyl = n, cyl
        self.memo = {}
        self.promo_legal = 0
        self.dbl_geom = 0
        self.dbl_legal = 0
        self.flagged = set()

    def nb(self, f):
        out = []
        for d in (-1, 1):
            g = f + d
            if self.cyl:
                g %= self.n
            if 0 <= g < self.n and g != f and g not in out:
                out.append(g)
        return out

    def canon(self, s):
        if self.cyl:
            n = self.n
            best = s
            r = s[::-1]
            for k in range(n):
                a = s[k:] + s[:k]
                b = r[k:] + r[:k]
                if a < best:
                    best = a
                if b < best:
                    best = b
            return best
        r = s[::-1]
        return r if r < s else s

    def moves(self, s, side):
        """Return (legal_children, has_promo_legal, dbl_geom)."""
        n = self.n
        me = W if side == 0 else B
        opp = B if side == 0 else W
        step = 1 if side == 0 else -1
        first = 1 if side == 0 else 3
        last = 3 if side == 0 else 1
        caps, pushes = [], []
        promo_caps = promo_push = False
        dbl = False
        for f in range(n):
            c = s[f]
            for r in (1, 2, 3):
                if sq(c, r) != me:
                    continue
                t = r + step
                if t < 1 or t > 3:
                    continue  # pawn on its last rank (should never exist)
                # captures
                for g in self.nb(f):
                    if sq(s[g], t) == opp:
                        ns = list(s)
                        ns[f] = setsq(ns[f], r, E)
                        ns[g] = setsq(ns[g], t, me)
                        caps.append(tuple(ns))
                        if t == last:
                            promo_caps = True
                # push
                if sq(c, t) == E:
                    nc = setsq(setsq(c, r, E), t, me)
                    ns = list(s)
                    ns[f] = nc
                    pushes.append(tuple(ns))
                    if t == last:
                        promo_push = True
                    if r == first and sq(c, t + step) == E:
                        dbl = True
        if caps:
            return caps, promo_caps, dbl, True
        return pushes, promo_push, dbl, False

    def solve(self, s, side):
        key = (self.canon(s), side)
        m = self.memo.get(key)
        if m is not None:
            return m
        kids, promo, dbl, hascap = self.moves(s, side)
        if promo:
            self.promo_legal += 1
        if dbl:
            self.dbl_geom += 1
            if not hascap:
                self.dbl_legal += 1
        if not kids:
            res = (False, True)
        else:
            nwin = mwin = False
            for k in kids:
                cn, cm = self.solve(k, 1 - side)
                if not cn:
                    nwin = True
                if not cm:
                    mwin = True
                if nwin and mwin:
                    break
            res = (nwin, mwin)
        self.memo[key] = res
        return res


def macro_from_start(n, side, all_files=True):
    """All quiet positions reached by a first push from the full ring plus forced captures.
    all_files=False: only the push on file 0 (exact by rotation symmetry of the full ring).
    Returns set of (state, side_to_move, plies)."""
    G = Game(n, True)
    start = tuple([FULL] * n)
    out = set()
    bad_promo = 0

    def follow(s, mover, plies):
        nonlocal bad_promo
        kids, promo, dbl, hascap = G.moves(s, mover)
        if promo:
            bad_promo += 1
        if hascap:
            for k in kids:
                follow(k, 1 - mover, plies + 1)
        else:
            out.add((s, mover, plies))

    kids, promo, dbl, hascap = G.moves(start, side)
    assert not hascap
    if not all_files:
        kids = [k for k in kids if k[0] != FULL]
        assert len(kids) == 1
    for k in kids:
        follow(k, 1 - side, 1)
    return out, bad_promo, len(kids)


def check_shape(n, s, mover, plies, first_side):
    """Expect: exactly one blocked file b, files b-1,b+1 empty, rest untouched,
    mover = opponent of first_side, plies odd."""
    blocked_code = code(E, W, B) if first_side == 0 else code(W, B, E)
    blocked = [f for f in range(n) if s[f] == blocked_code]
    if len(blocked) != 1:
        return False
    b = blocked[0]
    empt = {(b - 1) % n, (b + 1) % n}
    for f in range(n):
        if f == b:
            continue
        want = E if f in empt else FULL
        if f in empt and s[f] != code(E, E, E):
            return False
        if f not in empt and s[f] != FULL:
            return False
    return mover == 1 - first_side and plies % 2 == 1


# ---------- independent octal 0.137 Grundy values (no import of worker code) ----------
def octal_0137(N):
    g = [0] * (N + 1)
    for n in range(1, N + 1):
        opts = set()
        if n == 1:
            opts.add(0)  # digit 1: remove 1 token, leaving nothing
        if n >= 2:
            opts.add(g[n - 2])  # digit 3: remove 2, leave 0 or 1 heap
        if n >= 3:  # digit 7: remove 3, leave 0, 1 or 2 heaps
            for a in range(0, n - 2):
                b = n - 3 - a
                if a > b:
                    break
                opts.add(g[a] ^ g[b])
        m = 0
        while m in opts:
            m += 1
        g[n] = m
    return g


# ---------- independent misere solver for sums of 0.137 heaps (small totals) ----------
@lru_cache(maxsize=None)
def misere_P(heaps):
    """heaps: sorted tuple of positive ints. True iff player to move LOSES misere."""
    if not heaps:
        return False  # no move: mover wins in misere -> N-position
    hs = list(heaps)
    for i, h in enumerate(hs):
        rest = hs[:i] + hs[i + 1:]
        opts = []
        if h == 1:
            opts.append(())
        if h >= 2:
            opts.append((h - 2,))
        if h >= 3:
            for a in range(0, h - 2):
                b = h - 3 - a
                if a > b:
                    break
                opts.append((a, b))
        for o in opts:
            nh = tuple(sorted([x for x in rest + list(o) if x > 0]))
            if misere_P(nh):
                return False
    return True


def main():
    nmax_full = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    nmax_macro = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    g = octal_0137(2000)

    print("== Part A: first-move lemma, forced lines from the full ring, both colours ==")
    lemma_ok = True
    for n in range(3, nmax_macro + 1):
        for side in (0, 1):
            res, bad, nfirst = macro_from_start(n, side, all_files=(n <= 80))
            ok = bad == 0 and all(check_shape(n, s, m, p, side) for (s, m, p) in res)
            plies = sorted({p for (_, _, p) in res})
            if not ok or plies != [5]:
                lemma_ok = False
                print("  LEMMA FAIL n=%d side=%d plies=%s bad_promo=%d" % (n, side, plies, bad))
            if n <= 6 or n % 50 == 0:
                print("  n=%3d side=%s first moves=%d distinct quiet results=%d plies=%s shape_ok=%s"
                      % (n, "WB"[side], nfirst, len(res), plies, ok))
    print("  lemma holds for all 3<=n<=%d, both colours (every first move for n<=80, the file-0 push"
          " for n>80 by rotation symmetry): %s" % (nmax_macro, lemma_ok))

    print("== Part B: full pawn-level minimax (normal + misere), cylinder n vs flat strip n-3 ==")
    flat = {}
    allok = True
    for m in range(0, nmax_full - 2):
        if m == 0:
            flat[m] = (False, True)  # empty board: mover has no move
            continue
        F = Game(m, False)
        flat[m] = F.solve(tuple([FULL] * m), 0)
        Fb = F.solve(tuple([FULL] * m), 1)
        assert Fb == flat[m]
        if F.promo_legal or F.dbl_legal:
            print("  FLAT FLAG m=%d promo=%d dbl_legal=%d" % (m, F.promo_legal, F.dbl_legal))
    for n in range(3, nmax_full + 1):
        C = Game(n, True)
        rw = C.solve(tuple([FULL] * n), 0)
        rb = C.solve(tuple([FULL] * n), 1)
        fl = flat[n - 3]
        pred_norm = (g[n - 3] == 0)
        pred_mis_heap = misere_P(tuple([n - 3]) if n > 3 else ())
        ok = (rw == rb and rw[0] == (not fl[0]) and rw[1] == (not fl[1])
              and rw[0] == pred_norm and rw[1] == pred_mis_heap
              and fl[0] == (g[n - 3] != 0)
              and C.promo_legal == 0 and C.dbl_legal == 0)
        allok &= ok
        print("  cyl n=%2d states=%7d normal 1st=%s misere 1st=%s | flat(n-3): normal=%s misere=%s"
              " | g(n-3)=%d heapMisP=%s | promo_legal=%d dbl_geom=%d dbl_legal=%d ok=%s"
              % (n, len(C.memo), "win" if rw[0] else "loss", "win" if rw[1] else "loss",
                 "N" if fl[0] else "P", "N" if fl[1] else "P", g[n - 3], pred_mis_heap,
                 C.promo_legal, C.dbl_geom, C.dbl_legal, ok))
    print("  all full-game checks ok: %s" % allok)

    print("== Part C: octal 0.137 values, ring outcomes and periodicity ==")
    print("  g(0..33):", " ".join(map(str, g[:34])))
    exc = [n for n in range(0, 2000 - 34 + 1) if g[n] != g[n + 34]]
    print("  n with g(n)!=g(n+34), n<=1966:", exc)
    print("  max g up to 2000:", max(g))
    R = {n: (1 if g[n - 3] == 0 else 0) for n in range(3, 2001)}
    wins = [n for n in range(3, 201) if R[n] == 1]
    print("  ring first-player wins n<=200:", wins)
    rexc = [n for n in range(3, 2001 - 34) if R[n] != R[n + 34]]
    print("  n with R(n)!=R(n+34) (n<=1966):", rexc)
    # least period on n >= 38 (check on window 38..1966)
    lp = None
    for p in range(1, 200):
        if all(R[n] == R[n + p] for n in range(38, 2001 - p)):
            lp = p
            break
    print("  least p with R(n+p)=R(n) for all 38<=n<=2000-p:", lp)
    # is there any smaller eventual period at all (from any start <= 1000)?
    small = []
    for p in range(1, 34):
        last = max([n for n in range(3, 2001 - p) if R[n] != R[n + p]], default=None)
        small.append((p, last))
    print("  for p<34, last n with R(n)!=R(n+p):", small)
    claimed = [3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57, 61, 65, 75, 79]
    print("  claimed prefix matches:", wins[:len(claimed)] == claimed)
    # misere ring wins vs strip misere P (heap model), small n
    mis = [n for n in range(3, 40) if misere_P(tuple([n - 3]) if n > 3 else ())]
    print("  misere ring first-player wins (heap model, n<40):", mis)


if __name__ == "__main__":
    main()
